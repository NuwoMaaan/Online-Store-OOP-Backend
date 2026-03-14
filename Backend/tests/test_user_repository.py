from db.repositories.user_repository import create_user, get_user_by_username
from db.models import User


def test_create_user(db_session):
    user_data = {
        "username": "leo",
        "password": "hashed_pw",
        "role": "customer",
        "email": "leo@test.com"
    }
    user_id = create_user(user_data, db_session)

    assert user_id is not None
    assert isinstance(user_id, int)

    user = db_session.query(User).filter(User.user_id == user_id).first()
    assert user is not None
    assert user.username == "leo"
    assert user.email == "leo@test.com"
    assert user.role == "customer"


def test_get_user_by_username_found(db_session):
    user = User(
        username="leo",
        password="hashed_pw",
        role="customer",
        email="leo@test.com"
    )
    db_session.add(user)
    db_session.commit()

    result = get_user_by_username("leo", db_session)

    assert result is not None
    assert result.username == "leo"
    assert result.email == "leo@test.com"


def test_get_user_by_username_not_found(db_session):
    result = get_user_by_username("missing_user", db_session)

    assert result is None