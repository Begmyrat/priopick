import uuid
from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi_filter import FilterDepends

from app.api.v1.deps import get_vendor_service
from app.filters.vendor import VendorFilter
from app.schemas.vendor import (
    VendorCreate,
    VendorListResponse,
    VendorResponse,
    VendorUpdate,
)
from app.services.vendor import VendorService

router = APIRouter(prefix="/api/v1/vendors", tags=["Vendors"])


@router.get("/")
async def get_vendors(
    filters: VendorFilter = Depends(),
    page: int = 1,
    page_size: int = 10,
    vendor_service: VendorService = Depends(get_vendor_service),
):
    return await vendor_service.get_all(filters, page, page_size)


@router.get("/search", response_model=List[VendorResponse])
async def search_vendors(
    q: str = Query(description="Search query"),
    vendor_service: VendorService = Depends(get_vendor_service),
):
    """Search vendors by name."""
    return await vendor_service.search(q)


@router.get("/{vendor_id}", response_model=VendorResponse)
async def get_vendor(
    vendor_id: uuid.UUID,
    vendor_service: VendorService = Depends(get_vendor_service),
):
    """Get a single vendor by ID."""
    return await vendor_service.get_by_id(vendor_id)


@router.post("/", response_model=VendorResponse, status_code=201)
async def create_vendor(
    data: VendorCreate,
    vendor_service: VendorService = Depends(get_vendor_service),
):
    """Create a new vendor."""
    return await vendor_service.create(data)


@router.patch("/{vendor_id}", response_model=VendorResponse)
async def update_vendor(
    vendor_id: uuid.UUID,
    data: VendorUpdate,
    vendor_service: VendorService = Depends(get_vendor_service),
):
    """Update a vendor — only send fields you want to change."""
    return await vendor_service.update(vendor_id, data)


@router.delete("/{vendor_id}")
async def delete_vendor(
    vendor_id: uuid.UUID,
    vendor_service: VendorService = Depends(get_vendor_service),
):
    """Soft delete a vendor."""
    return await vendor_service.delete(vendor_id)


@router.get("/health")
async def health():
    return {"status": "healthy", "service": "vendor"}