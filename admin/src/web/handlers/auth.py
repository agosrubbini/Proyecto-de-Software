from src.core.auth import find_user_by_email

def is_authenticated(session):
    return session.get("user") is not None

def get_user_info(session):

    user = find_user_by_email(session.get("user"))

    if user:
        return {"email": user.email, "alias": user.alias} 

    return None