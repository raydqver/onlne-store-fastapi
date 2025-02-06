from fastapi import APIRouter

from core import SessionDep, UserIdDep
from catalog.services.products import get_products, get_product_by_id

router = APIRouter()


@router.post("/product/{product_id}/review")
async def write_review(product_id: int, user_id: UserIdDep):
    pass


#
