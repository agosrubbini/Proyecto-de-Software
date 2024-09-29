def is_authenticated(session):
    return session.get("user") is not None

