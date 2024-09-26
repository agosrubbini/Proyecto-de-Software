from src.core.database import db
from src.core.models.payments.payment import Payment
from src.core.models.payments.billing import Billing

def create_payment(**kwargs):
    payment = Payment(**kwargs)
    db.session.add(payment)
    db.session.commit()

    return payment

def create_billing(**kwargs):
    billing = Billing(**kwargs)
    db.session.add(billing)
    db.session.commit()

    return billing