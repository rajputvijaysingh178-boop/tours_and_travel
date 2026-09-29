from fastapi import APIRouter, HTTPException

from schemas.package_schema import (
    PackageCreateSchema,
    PackageUpdateSchema,
    PackageResponseSchema
)

from services.package_service import (
    create_package,
    get_packages,
    get_package,
    update_package,
    publish_package,
    delete_package
)


router = APIRouter(
    prefix="/packages",
    tags=["Packages"]
)


@router.post("")
def create_package_route(
    data: PackageCreateSchema
):
    try:
        return create_package(data)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("")
def get_packages_route():
    return get_packages()


@router.get("/{package_id}")
def get_package_route(
    package_id: str
):
    try:
        return get_package(package_id)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.put("/{package_id}")
def update_package_route(
    package_id: str,
    data: PackageUpdateSchema
):
    try:
        return update_package(
            package_id,
            data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.patch("/{package_id}/publish")
def publish_package_route(
    package_id: str
):
    try:
        return publish_package(package_id)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/{package_id}")
def delete_package_route(
    package_id: str
):
    try:
        return delete_package(package_id)

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )