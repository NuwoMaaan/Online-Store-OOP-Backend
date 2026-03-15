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

# Test for successful login of a customer
@patch("services.user_service.getpass.getpass", return_value="plainpass")
@patch("services.user_service.input", return_value="leo")
@patch("services.user_service.get_session")
@patch("services.user_service.get_user_by_username")
def test_login_customer_success(
    mock_get_user_by_username,
    mock_get_session,
    _mock_input,
    _mock_getpass
):
    
    fake_user = User(
        user_id=1,
        username="leo",
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
    assert result.username == "leo"

# Test for login failure due to incorrect password
@patch("services.user_service.getpass.getpass", return_value="wrongpass")
@patch("services.user_service.input", return_value="leo")
@patch("services.user_service.get_session")
@patch("services.user_service.get_user_by_username")
def test_login_wrong_password(
    mock_get_user_by_username,
    mock_get_session,
    _mock_input,
    _mock_getpass
):
    fake_user = MagicMock()
    fake_user.password = UserService.hash_password("correctpass")
    mock_get_user_by_username.return_value = fake_user

    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db

    result = UserService.login()
    assert result is None

# Test for successful user creation
@patch("services.user_service.create_cart")
@patch("services.user_service.create_user", return_value=10)
@patch("services.user_service.get_user_by_username", return_value=None)
@patch("services.user_service.get_session")
@patch("services.user_service.input")
def test_create_new_user_success(
    mock_input,
    mock_get_session,
    mock_get_user_by_username,
    mock_create_user,
    mock_create_cart
):
    mock_input.side_effect = [
        "leo@test.com",  
        "leo",            
        "secret123",      
        "c"               
    ]

    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db

    result = UserService.create_new_user()
    assert result == 10

    mock_get_user_by_username.assert_called_once_with("leo", mock_db)
    mock_create_user.assert_called_once()
    mock_create_cart.assert_called_once_with(10, mock_db)

# Test for username already exists
@patch("services.user_service.create_cart")
@patch("services.user_service.create_user")
@patch("services.user_service.get_user_by_username")
@patch("services.user_service.get_session")
@patch("services.user_service.input")
def test_create_new_user_username_exists(
    mock_input,
    mock_get_session,
    mock_get_user_by_username,
    mock_create_user,
    mock_create_cart
):
    mock_input.side_effect = [
        "leo@test.com",   
        "leo",            
        "secret123",      
        "c"               
    ]

    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db

    mock_get_user_by_username.return_value = object()  # Non-None value
    result = UserService.create_new_user()
    assert result is None

    mock_create_user.assert_not_called()
    mock_create_cart.assert_not_called()


# Test for invalid email format missing '@'
@patch("services.user_service.get_session")
@patch("services.user_service.input")
def test_create_new_user_invalid_email(
    mock_input,
    mock_get_session
):
    mock_input.side_effect = [
        "leotest.com",    # invalid email
        "leo",
        "secret123",
        "c"
    ]

    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db

    result = UserService.create_new_user()
    assert result is None

# Test for user creation aborted by user
@patch("services.user_service.get_session")
@patch("services.user_service.input")
def test_create_new_user_aborted(
    mock_input,
    mock_get_session
):
    mock_input.side_effect = [
        "leo@test.com",
        "leo",
        "secret123",
        "q"
    ]
    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db

    result = UserService.create_new_user()
    assert result is None