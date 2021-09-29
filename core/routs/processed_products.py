from typing import List

from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session

from core.db.dependecy import get_db
from core.crud.processed_product import CRUDProcessed
from core.models.processed_product import ProcessedProduct

router = APIRouter()
crud = CRUDProcessed(model=ProcessedProduct())


@router.get('/processed_products', response_model=List[ProcessedProduct])
def get_processed_products(session: Session = Depends(get_db)):
    return crud.get_all(session=session)


@router.get('/processed_product/{product_id}', response_model=ProcessedProduct)
def get_processed_product(product_id: int, session: Session = Depends(get_db)):
    return crud.get(session=session, obj_id=product_id)


@router.post('/processed_product_xlsx/{shop_id}')
async def processed_product_xlsx(
        shop_id: int,
        file: UploadFile = File(
            'test.xlsx',
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ),
        session: Session = Depends(get_db)
):
    file = await file.read()
    crud.add_processed_products(file=file, shop_id=shop_id, session=session)

