from sqlalchemy.orm import Session
from app.clients.models import ClientModel, CompanionModel


def _client(row: ClientModel) -> Client:
    return Client(row.id, row.name, row.phone, row.email, [Companion(c.id, c.name, c.phone) for c in row.companions])


class SqlClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, client: Client) -> Client:
        row = ClientModel(name=client.name, phone=client.phone, email=client.email)
        self.db.add(row); self.db.commit(); self.db.refresh(row)
        return _client(row)

    def get(self, client_id: int) -> Client | None:
        row = self.db.get(ClientModel, client_id)
        return None if row is None else _client(row)

    def list(self, query: str | None = None) -> list[Client]:
        rows = self.db.query(ClientModel)
        if query:
            rows = rows.filter(ClientModel.name.ilike(f"%{query}%"))
        return [_client(row) for row in rows.all()]

    def update(self, client: Client) -> Client:
        row = self.db.get(ClientModel, client.id)
        row.name, row.phone, row.email = client.name, client.phone, client.email
        self.db.commit(); self.db.refresh(row)
        return _client(row)

    def add_companion(self, client_id: int, companion: Companion) -> Companion:
        row = CompanionModel(client_id=client_id, name=companion.name, phone=companion.phone)
        self.db.add(row); self.db.commit(); self.db.refresh(row)
        return Companion(row.id, row.name, row.phone)

    def delete(self, client_id: int) -> None:
        row = self.db.get(ClientModel, client_id)
        if row is not None:
            self.db.delete(row)
            self.db.commit()