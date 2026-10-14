from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "secret123ll"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)


def test_create_access_token():    
    token = create_access_token(1)

    assert isinstance(token, str)
    assert len(token) > 0                 