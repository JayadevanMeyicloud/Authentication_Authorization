from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user_models import User,UserRole
from app.database import get_db
from app.schemas.user_schemas import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    LoginResponse,
    changePasswordRequest,
    AllUsersResponse,
    PaginatedUserResponse,
    PaginationMeta
)

from app.services.user_service import (
    register_user,
    login_user,
    get_profile_service,
    admin_service,
    create_admin_service,
    update_user_service,
    patch_user_service,
    delete_user_service,
    get_user_service,
    get_all_users_service,
    change_password_service
)

from app.core.auth import verify_access_token, require_role

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Authentication API Running"
    }


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(user, db)


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return login_user(user, db)


@router.get("/profile")
def get_profile(
    user_data: dict = Depends(verify_access_token)
):
    return get_profile_service(user_data)


@router.get("/admin")
def admin_route(
    user_data: dict = Depends(require_role("admin"))
):
    return admin_service(user_data)


@router.post("/create-admin")
def create_admin(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_admin_service(user, db)


@router.put(
    "/users/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_role("admin"))
):
    return update_user_service(user_id, user, db)


@router.patch(
    "/users/{user_id}",
    response_model=UserResponse
)
def patch_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_role("admin"))
):
    return patch_user_service(user_id, user_update, db)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_role("admin"))
):
    return delete_user_service(user_id, db)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(require_role("admin"))
):
    return get_user_service(user_id, db)


@router.get(
    "/all_users",
    response_model=PaginatedUserResponse
)
def get_all_users(

    skip: int = 0,
    limit: int = 50,

    db: Session = Depends(get_db),
    _: dict = Depends(require_role("admin"))
):
    return get_all_users_service(skip,limit,db)


@router.patch("/change-password")
def change_password(
    passwords: changePasswordRequest,
    db: Session = Depends(get_db),
    user_data: dict = Depends(verify_access_token)
):
    return change_password_service(
        passwords,
        user_data,
        db
    )

