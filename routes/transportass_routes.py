<<<<<<< HEAD
from fastapi import APIRouter

router = APIRouter(prefix="/transport-assignments",tags=["Transport Assignments"])

@router.post("")
def create_transport_assignment():
    pass

@router.get("/{assignment_id}")
def get_transport_assignment(assignment_id: str):
    pass
=======
from fastapi import APIRouter, HTTPException

from schemas.transportassi_schema import TransportAssignmentSchema
from services.transportass_service import (
    create_transport_assignment,
    get_transport_assignment
)


router = APIRouter(
    prefix="/transport-assignments",
    tags=["Transport Assignments"]
)


@router.post("")
def create_transport_assignment_route(
    data: TransportAssignmentSchema
):
    return create_transport_assignment(
        data.vehicle_id,
        data.driver_id,
        data.departure_id
    )


@router.get("/{assignment_id}")
def get_transport_assignment_route(
    assignment_id: str
):
    try:
        return get_transport_assignment(assignment_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
>>>>>>> origin/anil
