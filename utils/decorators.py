from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from utils.logger import logging


def handle_db_exceptions(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        db = kwargs.get("db")
        if not db:
            db = args[-1]
        try:
            return func(*args, **kwargs)

        except IntegrityError as e:
            db.rollback()
            logging.error(
                f"Integrity error: {str(e)}"
            )

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Database integrity error"
            )
        
        except HTTPException:

            raise

        except Exception as e:
            db.rollback()
            logging.error(
                f"Unexpected error: {str(e)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    return wrapper


def transactional(func):

    @wraps(func)

    def wrapper(*args, **kwargs):

        db = kwargs.get("db")

        if db is None:

            for arg in args:

                if hasattr(arg, "commit"):

                    db = arg
                    break

        try:

            result = func(*args, **kwargs)

            db.commit()

            return result

        except Exception:

            db.rollback()

            raise

    return wrapper