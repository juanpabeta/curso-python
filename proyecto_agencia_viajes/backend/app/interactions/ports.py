from typing import Protocol

from app.interactions.models import InteractionModel


class InteractionRepository(Protocol):
    def add(self, item: InteractionModel) -> InteractionModel: ...
    def list(self, client_id: int) -> list[InteractionModel]: ...
