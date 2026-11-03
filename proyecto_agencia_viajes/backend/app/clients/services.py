from app.clients.exceptions import ClientNotFound
from app.clients.models import ClientModel, CompanionModel
from app.clients.ports import ClientRepository


def register_client(repository: ClientRepository, client: ClientModel) -> ClientModel:
    return repository.add(client)


def update_client(repository: ClientRepository, client: ClientModel) -> ClientModel:
    if repository.get(client.id or 0) is None:
        raise ClientNotFound("Cliente no encontrado")
    return repository.update(client)


def search_clients(repository: ClientRepository, query: str | None = None) -> list[ClientModel]:
    return repository.list(query)


def add_companion(repository: ClientRepository, client_id: int, companion: CompanionModel) -> CompanionModel:
    if repository.get(client_id) is None:
        raise ClientNotFound("Cliente no encontrado")
    return repository.add_companion(client_id, companion)

def delete_client(repository: ClientRepository, client_id: int) -> None:
    if repository.get(client_id) is None:
        raise ClientNotFound("Cliente no encontrado")
    repository.delete(client_id)
    
