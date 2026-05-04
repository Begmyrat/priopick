import uuid
from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vendor import Vendor


class VendorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        style: Optional[str] = None,
        min_capacity: Optional[int] = None,
    ) -> Tuple[List[Vendor], int]:
        """
        Get paginated and filtered list of vendors.
        Returns (list of vendors, total count)

        Tuple means this function returns TWO things:
            → the vendors list
            → the total count
        """
        # Start with base query
        query = select(Vendor).where(Vendor.is_active == True)

        # Add filters ONLY if they were provided
        # This is called "dynamic query building"
        if category:
            query = query.where(Vendor.category == category)

        if max_price is not None:
            # Vendor is affordable if their MIN price is within budget
            query = query.where(Vendor.min_price <= max_price)

        if min_price is not None:
            query = query.where(Vendor.max_price >= min_price)

        if min_capacity is not None:
            query = query.where(Vendor.max_capacity >= min_capacity)

        if style:
            # style_tags is stored as "luxury,modern,traditional"
            # ilike = case-insensitive search
            query = query.where(Vendor.style_tags.ilike(f"%{style}%"))

        # Count total matching vendors BEFORE pagination
        # We need this to calculate total pages
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)

        # Apply pagination
        # offset = how many records to skip
        # Example: page=2, page_size=10 → skip first 10
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # Order by rating — best vendors first
        query = query.order_by(Vendor.rating.desc())

        result = await self.db.execute(query)
        vendors = result.scalars().all()

        return vendors, total

    async def get_by_id(self, vendor_id: uuid.UUID) -> Optional[Vendor]:
        """Get a single vendor by ID."""
        result = await self.db.execute(
            select(Vendor).where(Vendor.id == vendor_id)
        )
        return result.scalar_one_or_none()

    async def search(self, query_str: str, limit: int = 10) -> List[Vendor]:
        """
        Search vendors by name.
        ilike = case-insensitive LIKE search
        % means "anything before/after"
        Example: search("grand") matches "Grand Ballroom", "The Grand Hotel"
        """
        result = await self.db.execute(
            select(Vendor)
            .where(Vendor.name.ilike(f"%{query_str}%"))
            .where(Vendor.is_active == True)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, **kwargs) -> Vendor:
        """Create a new vendor."""
        vendor = Vendor(**kwargs)
        self.db.add(vendor)
        await self.db.flush()
        await self.db.refresh(vendor)
        return vendor

    async def update(self, vendor: Vendor, **kwargs) -> Vendor:
        """Update only the fields that were provided."""
        for key, value in kwargs.items():
            if value is not None:
                setattr(vendor, key, value)
        await self.db.flush()
        await self.db.refresh(vendor)
        return vendor

    async def delete(self, vendor: Vendor) -> None:
        """
        Soft delete — we never actually delete data.
        We just mark it as inactive.
        Real data is never lost.
        """
        vendor.is_active = False
        await self.db.flush()