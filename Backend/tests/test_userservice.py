from services.user_service import UserService
from unittest.mock import MagicMock, patch
from models.user import Customer
from db.models import User

def test_verify_correct_password():
    password = "securepassword123"
    hashed = UserService.hash_password(password)
    assert UserService.verify_password(hashed, password) == True

def test_verify_correct_password():
    password = "securepassword123"
    hashed = UserService.hash_password(password)
    assert UserService.verify_password(hashed, "wrongpassword") == False


@patch("services.user_service.getpass.getpass", return_value="plainpass")
@patch("services.user_service.input", return_value="Leo")
@patch("services.user_service.get_session")
@patch("services.user_service.get_user_by_username")
def test_login_customer_success(
    mock_get_user_by_username,
    mock_get_session,
    mock_input,
    mock_getpass
):
    
    fake_user = User(
        user_id=1,
        username="Leo",
        password=UserService.hash_password("plainpass"),
        role="customer",
        email="leo@outlook.com"
    )

    mock_get_user_by_username.return_value = fake_user

    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db
    mock_get_session.return_value.__exit__.return_value = None

    result = UserService.login()

    assert isinstance(result, Customer)
    assert result.username == "Leo"
    

@patch("services.user_service.getpass.getpass", return_value="wrongpass")
@patch("services.user_service.input", return_value="leo")
@patch("services.user_service.get_session")
@patch("services.user_service.get_user_by_username")
def test_login_wrong_password(
    mock_get_user_by_username,
    mock_get_session,
    mock_input,
    mock_getpass
):
    fake_user = MagicMock()
    fake_user.password = UserService.hash_password("correctpass")
    fake_user.role = "customer"

    mock_get_user_by_username.return_value = fake_user

    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db

    result = UserService.login()

    assert result is None