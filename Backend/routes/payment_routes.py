# routes/payments.py
from fastapi import APIRouter, HTTPException
from models.PAYMENT.CardPaymentMethod import CardPaymentMethod
from models.PAYMENT.PaypalPaymentMethod import PaypalPaymentMethod
from services.payment_service import PaymentService

from pydantic import BaseModel
class CardPaymentRequest(BaseModel):
    amount: float
    card_holder: str
    card_number: str
    expiry_date: str

class PaypalPaymentRequest(BaseModel):
    amount: float
    email: str




router = APIRouter()

@router.post("/payments/card")
def pay_by_card(payload: CardPaymentRequest):
    try:
        service = PaymentService(CardPaymentMethod())
        service.process_payment(payload.model_dump())
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/payments/paypal")
def pay_by_paypal(payload: PaypalPaymentRequest):
    try:
        service = PaymentService(PaypalPaymentMethod())
        service.process_payment(payload.model_dump())
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
