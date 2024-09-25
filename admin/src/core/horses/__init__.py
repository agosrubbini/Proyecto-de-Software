from src.core.database import db
from src.core.horses.models.horse import Horse


def create_horse(**kwargs):
    horse = Horse(**kwargs)
    db.session.add(horse)
    db.session.commit()

    return horse