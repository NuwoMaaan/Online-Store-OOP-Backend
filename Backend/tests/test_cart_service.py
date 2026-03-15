from unittest.mock import MagicMock, patch
from services.cart_service import CartService


# Test for successful cart loading with items
@patch("services.cart_service.Catalogue")
@patch("services.cart_service.load_cart_db")
@patch("services.cart_service.get_cart_by_user_id")
@patch("services.cart_service.get_session")
def test_load_cart_success(
    mock_get_session,
    mock_get_cart_by_user_id,
    mock_load_cart_db,
    mock_catalogue
):
    # domain cart object passed into service
    cart_instance = MagicMock()
    cart_instance.customer_id = 1
    cart_instance.items = []
    cart_instance.quantity = 0
    # fake db session from context manager
    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db
    # ORM cart returned from repository
    orm_cart = MagicMock()
    orm_cart.cart_id = 10
    orm_cart.user_id = 1
    mock_get_cart_by_user_id.return_value = orm_cart
    # rows returned from load_cart_db
    row1 = MagicMock()
    row1.item_id = 5
    row1.quantity = 2

    row2 = MagicMock()
    row2.item_id = 9
    row2.quantity = 1
    mock_load_cart_db.return_value = [row1, row2]
    # catalogue singleton
    catalogue_instance = MagicMock()
    mock_catalogue.get_instance.return_value = catalogue_instance

    # actual item objects returned by catalogue lookup
    item5 = MagicMock()
    item9 = MagicMock()

    catalogue_instance.get_item_by_id.side_effect = lambda item_id: {
        5: item5,
        9: item9
    }.get(item_id)

    CartService.load_cart(cart_instance)
    assert cart_instance.items == [item5, item5, item9]
    assert cart_instance.quantity == 3

# No cart found for user
@patch("services.cart_service.get_cart_by_user_id", return_value=None)
@patch("services.cart_service.get_session")
def test_load_cart_no_cart(
    mock_get_session,
    _mock_get_cart_by_user_id
):
    # domain cart object passed into service
    cart_instance = MagicMock()
    cart_instance.customer_id = 1
    cart_instance.items = []
    cart_instance.quantity = 0

    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db

    CartService.load_cart(cart_instance)
    assert cart_instance.items == []
    assert cart_instance.quantity == 0


# Cart found but no items in cart
@patch("services.cart_service.load_cart_db", return_value=[])
@patch("services.cart_service.get_cart_by_user_id")
@patch("services.cart_service.get_session")
def test_load_cart_no_items(
    mock_get_session,
    mock_get_cart_by_user_id,
    _mock_load_cart_db
):
    # domain cart object passed into service
    cart_instance = MagicMock()
    cart_instance.customer_id = 1
    cart_instance.items = []
    cart_instance.quantity = 0

    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db

    # ORM cart returned from repository
    orm_cart = MagicMock()
    orm_cart.cart_id = 10
    mock_get_cart_by_user_id.return_value = orm_cart

    CartService.load_cart(cart_instance)
    assert cart_instance.items == []
    assert cart_instance.quantity == 0



# Catalogue misses an item
@patch("services.cart_service.Catalogue")
@patch("services.cart_service.load_cart_db")
@patch("services.cart_service.get_cart_by_user_id")
@patch("services.cart_service.get_session")
def test_load_cart_skips_missing_catalogue_item(
    mock_get_session,
    mock_get_cart_by_user_id,
    mock_load_cart_db,
    mock_catalogue
):
    cart_instance = MagicMock()
    cart_instance.customer_id = 1
    cart_instance.items = []
    cart_instance.quantity = 0

    mock_db = MagicMock()
    mock_get_session.return_value.__enter__.return_value = mock_db

    orm_cart = MagicMock()
    orm_cart.cart_id = 10
    mock_get_cart_by_user_id.return_value = orm_cart

    row1 = MagicMock()
    row1.item_id = 5
    row1.quantity = 2

    row2 = MagicMock()
    row2.item_id = 999
    row2.quantity = 3

    mock_load_cart_db.return_value = [row1, row2]

    catalogue_instance = MagicMock()
    mock_catalogue.get_instance.return_value = catalogue_instance

    item5 = MagicMock()

    catalogue_instance.get_item_by_id.side_effect = lambda item_id: {5: item5}.get(item_id)

    CartService.load_cart(cart_instance)
    assert cart_instance.items == [item5, item5]
    assert cart_instance.quantity == 2