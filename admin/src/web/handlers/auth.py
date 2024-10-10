from src.core.auth import find_user_by_email

def is_authenticated(session):
    return session.get("user") is not None

def get_user_info(session):

    user = find_user_by_email(session.get("user"))

    return {"email": user.email, "alias": user.alias} is not None