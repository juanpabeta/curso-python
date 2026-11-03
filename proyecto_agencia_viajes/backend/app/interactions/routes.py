from fastapi import APIRouter, Depends,status
from app.auth.dependencies import get_current_user

from app.container import get_list_interactions_service, get_record_interaction_service
from app.interactions.models import InteractionModel
from app.interactions.schemas import InteractionRequest

router = APIRouter(
    prefix="/clients/{client_id}/interactions",
    tags=["interactions"],
    dependencies=[Depends(get_current_user)],
)



@router.post("", status_code=status.HTTP_201_CREATED)
def create(client_id: int, request: InteractionRequest, service=Depends(get_record_interaction_service)):
    return service(InteractionModel(client_id=client_id, kind=request.kind, content=request.content))

@router.get("",status_code=status.HTTP_200_OK)
def list_all(client_id: int, service=Depends(get_list_interactions_service)):
    return service(client_id)
