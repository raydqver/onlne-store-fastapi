from typing import Annotated

from fastapi import APIRouter, Query, Depends

from core import SessionDep, settings
from products.database.repositories.product import ProductRepository
from products.dependencies.queries import get_filtering_options
from products.schemas.catalog import FilterQuerySchema
from products.services.categories import get_categories_and_subcategories
from products.services.products import (
    get_products,
    get_product_by_id,
    get_sales_products,
    get_catalog,
)

router = APIRouter()


@router.get("/product/{product_id}")
async def get_product(product_id: int, session: SessionDep):
    return await get_product_by_id(session=session, product_id=product_id)


@router.get("/products/popular")
async def popular_product(session: SessionDep):
    return await get_products(session=session, is_popular=True)


@router.get("/products/limited")
async def limited_product(session: SessionDep):
    return await get_products(session=session, is_limited=True)


@router.get("/banners")
async def get_banners(session: SessionDep):
    return await get_products(session=session, is_banner=True)


@router.get("/sales")
async def get_discounted_items(
    session: SessionDep,
    current_page: Annotated[int, Query(alias="currentPage")] = 1,
):
    return await get_sales_products(session=session, current_page=current_page)


@router.get("/catalog")
async def get_catalog_of_products(
    session: SessionDep,
    filtering_data: Annotated[
        FilterQuerySchema, Depends(get_filtering_options)
    ],
):
    return await get_catalog(session=session, filtering_data=filtering_data)


@router.get("/categories")
async def get_categories(
    session: SessionDep,
):
    result = await get_categories_and_subcategories(session)
    return result
