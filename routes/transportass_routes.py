from fastapi import APIRouter

router = APIRouter(prefix="/transport-assignments",tags=["Transport Assignments"])

@router.post("")
def create_transport_assignment():
    pass

@router.get("/{assignment_id}")
def get_transport_assignment(assignment_id: str):
    pass