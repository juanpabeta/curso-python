from fastapi import APIRouter, Depends,status
from app.auth.dependencies import get_current_user
from app.clients.models import ClientModel, CompanionModel
from app.clients.schemas import ClientCreate, ClientResponse, ClientUpdate, CompanionCreate, CompanionResponse
from app.container import (
    get_add_companion_service,
    get_client_service,
    get_delete_client_service,
    get_register_client_service,
    get_search_clients_service,
    get_update_client_service,
)

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(get_current_user)],
)


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create(request: ClientCreate, service=Depends(get_register_client_service)):
    return service(ClientModel(name=request.name, phone=request.phone, email=str(request.email) if request.email else None))


@router.get("", response_model=list[ClientResponse],status_code=status.HTTP_200_OK)
def list_all(query: str | None = None, service=Depends(get_search_clients_service)):
    return service(query)


@router.get("/{client_id}", response_model=ClientResponse)
def get(client_id: int, service=Depends(get_client_service)):
    return service(client_id)


@router.patch("/{client_id}", response_model=ClientResponse)
def update(client_id: int, request: ClientUpdate, service=Depends(get_update_client_service)):
    return service(ClientModel(id=client_id, name=request.name or "", phone=request.phone or "", email=str(request.email) if request.email else None))


@router.post("/{client_id}/companions", response_model=CompanionResponse)
def companion(client_id: int, request: CompanionCreate, service=Depends(get_add_companion_service)):
    return service(client_id, CompanionModel(name=request.name, phone=request.phone, client_id=client_id))
