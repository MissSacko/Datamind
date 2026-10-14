from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user

def register_user(
    db: Session,
    name: str,
    first_name: str,
    email: str,
    password: str,
    profession: str | None = None,
) -> User:

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user is not None:
        raise ValueError("Email already registered")

    hashed_password = hash_password(password)

    user = User(
        name=name,
        first_name=first_name,
        email=email,
        profession=profession,
        password_hash=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user