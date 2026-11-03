from app.interactions.models import InteractionModel
from app.interactions.ports import InteractionRepository


def record_interaction(repository: InteractionRepository, interaction: InteractionModel) -> InteractionModel:
    return repository.add(interaction)


def list_interactions(repository: InteractionRepository, client_id: int) -> list[InteractionModel]:
    return repository.list(client_id)
