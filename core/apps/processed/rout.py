from typing import List
import io

from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session
from starlette.responses import StreamingResponse

from core.db.dependecy import get_db
from core.apps.processed.crud import CRUDProcessed
from core.apps.processed.models import ProcessedProduct
from core.apps.processed.manager import AnaliseProducts

router = APIRouter()
crud = CRUDProcessed(model=ProcessedProduct())


@router.get('/processed_products', response_model=List[ProcessedProduct])
def get_processed_products(session: Session = Depends(get_db)):
    return crud.get_all(session=session)


@router.get('/processed_product/{product_id}', response_model=ProcessedProduct)
def get_processed_product(product_id: int, session: Session = Depends(get_db)):
    return crud.get(session=session, obj_id=product_id)


@router.post('/processed_product_xlsx/{shop_id}', response_class=StreamingResponse)
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
    df = AnaliseProducts().price_difference()
    to_write = io.BytesIO()
    df.to_excel(to_write, index=False)
    to_write.seek(0)
    return StreamingResponse(to_write, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')




