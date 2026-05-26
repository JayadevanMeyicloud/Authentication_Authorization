from fastapi import HTTPException, status
from app.utils.logger import logging
from app.utils.decorators import(
    handle_db_exceptions,
    transactional
)
from app.models.user_models import User, UserRole
from app.schemas.user_schemas import (
    UserResponse,
    UserData,
    AllUsersResponse,
    PaginatedUserResponse,
    PaginationMeta
)
from app.core.response import success_response
from app.core.auth import (
    hash_password,
    verify_password,
    create_access_token
)
from app.repository.user_repository import (
    get_user_by_email,
    get_user_by_id
)



@transactional
@handle_db_exceptions
def register_user(user, db):

    existing_user = get_user_by_email(
        user.email,
        db
    )

    if existing_user:

        logging.warning(
            f"Duplicate email registration attempt: {user.email}"
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        email=user.email,
        password=hashed_password,
        role=UserRole.user
    )

    db.add(new_user)

    db.flush()

    db.refresh(new_user)

    logging.info(
        f"User registered successfully: {new_user.email}"
    )

    return UserResponse(
        success=True,
        message="User registered successfully",
        data=UserData(
            id=new_user.id,
            email=new_user.email,
            role=new_user.role
        )
    )


@handle_db_exceptions
def login_user(user, db):

    db_user = get_user_by_email(
        user.email,
        db
    )

    if not db_user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    access_token = create_access_token(
        data={
            "user_id": db_user.id,
            "email": db_user.email,
            "role": db_user.role.value
        }
    )

    return {
        "success": True,
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_profile_service(user_data):

    return success_response(
        message="Profile fetched successfully",
        data=user_data
    )




def admin_service(user_data):

    return success_response(
        message="Welcome Admin",
        data=user_data
    )


@transactional
@handle_db_exceptions
def create_admin_service(user, db):

    existing_user = get_user_by_email(
        user.email,
        db
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    hashed_password = hash_password(
        user.password
    )

    new_admin = User(
        email=user.email,
        password=hashed_password,
        role=UserRole.admin
    )

    db.add(new_admin)

    db.flush()

    db.refresh(new_admin)

    logging.info(
        f"Admin created successfully: {new_admin.email}"
    )

    return success_response(
        message="Admin created successfully",
        data={
            "id": new_admin.id,
            "email": new_admin.email,
            "role": new_admin.role
        }
    )

@transactional
@handle_db_exceptions
def update_user_service(
    user_id,
    user,
    db
):

    db_user = get_user_by_id(
        user_id,
        db
    )

    if not db_user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db_user.email = user.email

    db_user.password = hash_password(
        user.password
    )
    db_user.role = user.role

    db.flush()

    db.refresh(db_user)

    logging.info(
        f"User updated successfully: {db_user.email}"
    )

    return UserResponse(
        success=True,
        message="User updated successfully",
        data=UserData(
            id=db_user.id,
            email=db_user.email,
            role=db_user.role.value
        )
    )

@transactional
@handle_db_exceptions
def patch_user_service(
    user_id,
    user_update,
    db
):

    db_user = get_user_by_id(
        user_id,
        db
    )

    if not db_user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_update.email is not None:

        db_user.email = user_update.email

    if user_update.password is not None:

        db_user.password = hash_password(
            user_update.password
        )

    db.flush()

    db.refresh(db_user)

    logging.info(
        f"User patched successfully: {db_user.email}"
    )

    return UserResponse(
        success=True,
        message="User patched successfully",
        data=UserData(
            id=db_user.id,
            email=db_user.email,
            role=db_user.role
        )
    )

@transactional
@handle_db_exceptions
def delete_user_service(
    user_id,
    db
):

    db_user = get_user_by_id(
        user_id,
        db
    )

    if not db_user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(db_user)

    logging.info(
        f"User deleted successfully: {db_user.email}"
    )

    return success_response(
        message="User deleted successfully"
    )


@handle_db_exceptions
def get_user_service(
    user_id,
    db
):

    db_user = get_user_by_id(
        user_id,
        db
    )

    if not db_user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        success=True,
        message="User fetched successfully",
        data=UserData(
            id=db_user.id,
            email=db_user.email,
            role=db_user.role
        )
    )
@handle_db_exceptions
def get_all_users_service(
    skip,
    limit,
    db
):

    logging.info("Fetching all users")

    users = db.query(
        User.id,
        User.email,
        User.role
    ).offset(skip).limit(limit).all()

    total = db.query(User).count()

    logging.info(
        f"Total users fetched: {total}"
    )

    return PaginatedUserResponse(

        success=True,

        message="Users fetched successfully",

        meta=PaginationMeta(
            skip=skip,
            limit=limit,
            total=total
        ),

        data=[
            UserData(
                id=user.id,
                email=user.email,
                role=user.role
            )
            for user in users
        ]
    )

@transactional
@handle_db_exceptions
def change_password_service(
    passwords,
    user_data,
    db
):

    user_id = user_data.get("user_id")

    db_user = get_user_by_id(
        user_id,
        db
    )

    if not db_user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(
        passwords.old_password,
        db_user.password
    ):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password incorrect"
        )

    db_user.password = hash_password(
        passwords.new_password
    )

    db.flush()

    logging.info(
        f"Password changed successfully: {db_user.email}"
    )

    return success_response(
        message="Password changed successfully"
    )