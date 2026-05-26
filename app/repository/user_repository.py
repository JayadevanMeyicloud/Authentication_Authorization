from app.models.user_models import User


def get_user_by_email(email, db):

    return db.query(User).filter(
        User.email == email
    ).first()


def get_user_by_id(user_id, db):

    return db.query(User).filter(
        User.id == user_id
    ).first()