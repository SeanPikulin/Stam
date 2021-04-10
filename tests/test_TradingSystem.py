import pytest
from Backend.Service.trading_system import TradingSystem

# TODO: parallel testing
# TODO: get admin permissions
system = TradingSystem.getInstance()
username_number = 0
store_number = 0
product_number = 0

def _initialize_info(
    username: str, password: str, store_name: str = None
) -> tuple[str, str, str, str]:
    cookie = system.enter_system()
    system.register(cookie, username, password)
    system.login(cookie, username, password)
    if store_name:
        system.create_store(cookie, store_name)
    return cookie, username, password, store_name


def _generate_username() -> str:
    global username_number
    username_number += 1
    return str(username_number)


def _generate_store_name() -> str:
    global store_number
    store_number += 1
    return str(store_number)


def _generate_product_name() -> str:
    global product_number
    product_number += 1
    return str(product_number)


# 2.3 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#23-Registration
def test_register_success():
    new_username = _generate_username()
    password = "aaa"
    cookie = system.enter_system()
    assert system.register(cookie, new_username, password).succeeded()


def test_register_used_username_fail():
    existing_username = _generate_username()
    password = "aaa"
    cookie = system.enter_system()
    system.register(cookie, existing_username, password)
    assert not system.register(cookie, existing_username, password).succeeded()


# 2.4 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#24-Login
def test_login_success():
    new_username = _generate_username()
    password = "aaa"
    cookie = system.enter_system()
    system.register(cookie, new_username, password)
    assert system.login(cookie, new_username, password).succeeded()


def test_login_wrong_username_fail():
    new_username = _generate_username()
    password = "aaa"
    wrong_username = "doorbelman"
    cookie = system.enter_system()
    system.register(cookie, new_username, password)
    assert not system.login(cookie, wrong_username, password).succeeded()


def test_login_wrong_password_fail():
    new_username = _generate_username()
    password = "aaa"
    wrong_password = "aa"
    cookie = system.enter_system()
    system.register(cookie, new_username, password)
    assert not system.login(cookie, new_username, wrong_password).succeeded()


# 3.2 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#32-#Open-a-store
def test_open_store_success():
    cookie, username, password, _ = _initialize_info(_generate_username(), "aaa")
    store_name = _generate_store_name()
    assert system.create_store(cookie, store_name).succeeded()


def test_open_store_unsupported_character_fail():
    cookie, username, password, _ = _initialize_info(_generate_username(), "aaa")
    store_name = "stαrbucks"
    assert not system.create_store(cookie, store_name).succeeded()


# 2.5 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#25-Getting-store-information
def test_get_store_information_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    response = system.get_stores_details()
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].name == store_name
    )


def test_get_store_information_no_stores_fail():
    cookie, username, password, _ = _initialize_info(_generate_username(), "aaa")
    assert not system.get_stores_details().succeeded()  # an empty list evaluates to false


# 4.1 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#41-Add-new-product
def test_add_new_product_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    assert system.create_product(cookie, store_name, product_name, price, quantity).succeeded()


def test_add_new_product_negative_quantity_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = -10
    assert not system.create_product(cookie, store_name, product_name, price, quantity).succeeded()


def test_add_new_product_negative_price_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = -5.50
    quantity = 10
    assert not system.create_product(cookie, store_name, product_name, price, quantity).succeeded()


def test_remove_product_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert system.remove_product_from_store(cookie, store_name, product_name).succeeded()


def test_remove_product_wrong_product_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    wrong_product = "cofee"
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert not system.remove_product_from_store(cookie, store_name, wrong_product).succeeded()


def test_change_product_quantity_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    new_quantity = 15
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert system.change_product_quantity_in_store(
        cookie, store_name, product_name, new_quantity
    ).succeeded()


def test_change_product_quantity_negative_quantity_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    new_quantity = -15
    cookie = system.enter_system()
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert not system.change_product_quantity_in_store(
        cookie, store_name, product_name, new_quantity
    ).succeeded()


def test_change_product_quantity_wrong_product_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    wrong_product = "cofee"
    price = 5.50
    quantity = 10
    new_quantity = 15
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert not system.change_product_quantity_in_store(
        cookie, store_name, wrong_product, new_quantity
    ).succeeded()


def test_edit_product_details_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    new_name = "cofee"
    new_price = 6.0
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert system.edit_product_details(
        cookie, store_name, product_name, new_name, new_price
    ).succeeded()


def test_edit_product_details_wrong_product_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    wrong_product = "coffe"
    price = 5.50
    quantity = 10
    new_name = "cofee"
    new_price = 6.0
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert not system.edit_product_details(
        cookie, store_name, wrong_product, new_name, new_price
    ).succeeded()


def test_edit_product_details_negative_price_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    new_name = "cofee"
    new_price = -6.0
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert not system.edit_product_details(
        cookie, store_name, product_name, new_name, new_price
    ).succeeded()


# 2.6 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#26-Filter-search-results
def test_product_search_no_args_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.search_products(product_name)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].name == product_name
    )


def test_product_search_args_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    min_price = 5.0
    max_price = 6.0
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.search_products(product_name, min_price=min_price, max_price=max_price)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].name == product_name
    )


def test_product_search_wrong_product_no_args_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    wrong_product = "cofee"
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.search_products(wrong_product)
    assert not response.succeeded()


def test_product_search_wrong_product_args_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    wrong_product = "cofee"
    price = 5.50
    quantity = 10
    min_price = 5.0
    max_price = 6.0
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.search_products(wrong_product, min_price=min_price, max_price=max_price)
    assert not response.succeeded()


def test_product_search_wrong_args_min_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    min_price = 6.0
    max_price = 7.0
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.search_products(product_name, min_price=min_price, max_price=max_price)
    assert not response.succeeded()


def test_product_search_wrong_args_max_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    min_price = 4.0
    max_price = 5.0
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.search_products(product_name, min_price=min_price, max_price=max_price)
    assert not response.succeeded()


def test_products_by_store_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.get_products_by_store(store_name)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].name == product_name
    )


def test_products_by_store_wrong_store():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    wrong_store = "starbux"
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.get_products_by_store(wrong_store)
    assert response.succeeded()


# 2.7 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#27-Save-products-in-shopping-bag
def test_add_to_cart_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert system.save_product_in_cart(cookie, store_name, product_name, 1).succeeded()


def test_add_to_cart_wrong_product_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    wrong_product = "cofee"
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert not system.save_product_in_cart(cookie, store_name, wrong_product, 1).succeeded()


def test_add_to_cart_wrong_store_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    wrong_store = "starbux"
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert not system.save_product_in_cart(cookie, wrong_store, product_name, 1).succeeded()


def test_add_to_cart_quantity_too_high_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    assert not system.save_product_in_cart(cookie, store_name, product_name, 11).succeeded()


# 2.8 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#28-Visit-cart
def test_visit_cart_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    response = system.get_cart_details(cookie)
    assert (
        response.succeeded()
        and len(response.object.bags) == 1
        and response.object.bags[0].store_name == store_name
        and len(response.object.bags[0].products) == 1
        and response.object.bags[0].products[0].name == product_name
    )


def test_visit_cart_no_items_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    assert not system.get_cart_details(cookie).succeeded()


def test_change_amount_in_cart_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    assert (
        system.change_product_quantity_in_cart(cookie, store_name, product_name, 2).succeeded()
        and system.get_cart_details(cookie).object.bags[0].products[0].quantity == 2
    )


def test_change_amount_in_cart_wrong_product_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    wrong_product = "cofee"
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    assert not system.change_product_quantity_in_cart(
        cookie, store_name, wrong_product, 2
    ).succeeded()


def test_change_amount_in_cart_wrong_store_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    wrong_store = "starbux"
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    assert not system.change_product_quantity_in_cart(
        cookie, wrong_store, product_name, 2
    ).succeeded()


def test_change_amount_in_cart_negative_quantity_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    assert not system.change_product_quantity_in_cart(
        cookie, store_name, product_name, -1
    ).succeeded()


def test_change_amount_in_cart_quantity_too_high_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    assert not system.change_product_quantity_in_cart(
        cookie, store_name, product_name, 11
    ).succeeded()


def test_remove_product_from_cart_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    assert (
        system.remove_product_from_cart(cookie, store_name, product_name).succeeded()
        and not system.get_cart_details(cookie).succeeded()
    )


def test_remove_product_from_cart_wrong_product_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    wrong_product = "cofee"
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    assert not system.remove_product_from_cart(cookie, store_name, wrong_product).succeeded()


def test_remove_product_from_cart_wrong_store_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    wrong_store = "starbux"
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    assert not system.remove_product_from_cart(cookie, wrong_store, product_name).succeeded()


# 2.9 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#29-Purchase-products
def test_purchase_cart_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    response = system.purchase_cart(cookie)
    assert (
        response.succeeded()
        and system.get_products_by_store(store_name).products[0].quantity == 9
        and system.get_cart_details(cookie).succeeded()
        and response.object.value == price
    )


def test_purchase_cart_no_items_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    assert not system.purchase_cart(cookie).succeeded()


def test_purchase_cart_twice_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    system.purchase_cart(cookie)
    assert not system.purchase_cart(cookie).succeeded()


def test_send_payment_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    system.purchase_cart(cookie)
    assert (
        system.send_payment(cookie, card_number, card_expire, card_cvv).succeeded()
        and system.get_products_by_store(store_name).products[0].quantity == 9
        and not system.get_cart_details(cookie).succeeded()
    )


def test_send_payment_before_purchase_cart_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    assert (
        not system.send_payment(cookie, card_number, card_expire, card_cvv).succeeded()
        and system.get_products_by_store(store_name).products[0].quantity == 9
        and system.get_cart_details(cookie).succeeded()
    )


# 3.7 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#37-Get-personal-purchase-history
def test_get_purchase_history_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    system.purchase_cart(cookie)
    system.send_payment(cookie, card_number, card_expire, card_cvv)
    response = system.get_purchase_history(cookie)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].name == product_name
    )


def test_get_purchase_history_no_purchases_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.get_purchase_history(cookie)
    assert not response.succeeded()


def test_get_purchase_history_no_purchases_saved_to_cart_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    response = system.get_purchase_history(cookie)
    assert not response.succeeded()


def test_get_purchase_history_no_payment_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    system.purchase_cart(cookie)
    response = system.get_purchase_history(cookie)
    assert not response.succeeded()


# 4.3 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#43-Appoint-new-store-owner
def test_appoint_store_owner_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    assert system.appoint_owner(cookie, store_name, new_owner_username).succeeded()


def test_appoint_store_owner_chain_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    last_owner_cookie, last_owner_username, last_owner_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_owner(cookie, store_name, new_owner_username)
    assert system.appoint_owner(new_owner_cookie, store_name, last_owner_username).succeeded()


def test_appoint_store_owner_wrong_name_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    wrong_name = "Ravit Ron"
    assert not system.appoint_owner(cookie, store_name, wrong_name).succeeded()


def test_appoint_store_owner_wrong_store_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    wrong_store = "starbux"
    assert not system.appoint_owner(cookie, wrong_store, new_owner_username).succeeded()


def test_appoint_store_owner_direct_circular_appointment_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    last_owner_cookie, last_owner_username, last_owner_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_owner(cookie, store_name, new_owner_username)
    assert not system.appoint_owner(new_owner_cookie, store_name, username).succeeded()


def test_appoint_store_owner_circular_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    last_owner_cookie, last_owner_username, last_owner_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_owner(cookie, store_name, new_owner_username)
    system.appoint_owner(new_owner_cookie, store_name, last_owner_username)
    assert not system.appoint_owner(last_owner_cookie, store_name, username).succeeded()


# 4.5 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#45-Appoint-new-store-manager
def test_appoint_store_manager_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    assert system.appoint_manager(cookie, store_name, new_manager_username).succeeded()


def test_appoint_store_manager_manager_chain_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    last_manager_cookie, last_manager_username, last_manager_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_manager(cookie, store_name, new_manager_username)
    assert system.appoint_manager(new_manager_cookie, store_name, last_manager_username).succeeded()


def test_appoint_store_owner_manager_chain_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    last_manager_cookie, last_manager_username, last_manager_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_owner(cookie, store_name, new_owner_username)
    assert system.appoint_manager(new_owner_cookie, store_name, last_manager_username).succeeded()


def test_appoint_store_manager_wrong_name_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    wrong_name = "Ravit Ron"
    assert not system.appoint_manager(cookie, store_name, wrong_name).succeeded()


def test_appoint_store_manager_wrong_store_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    wrong_store = "starbux"
    assert not system.appoint_manager(cookie, wrong_store, new_manager_username).succeeded()


def test_appoint_store_manager_direct_circular_appointment_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_name, new_manager_username)
    assert not system.appoint_manager(new_manager_cookie, store_name, username).succeeded()


def test_appoint_store_manager_circular_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    last_manager_cookie, last_manager_username, last_manager_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_manager(cookie, store_name, new_manager_username)
    system.appoint_manager(new_manager_cookie, store_name, last_manager_username)
    assert not system.appoint_manager(last_manager_cookie, store_name, username).succeeded()


def test_appoint_store_manager_owner_chain_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    last_owner_cookie, last_owner_username, last_owner_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_manager(cookie, store_name, new_manager_username)
    assert not system.appoint_owner(new_manager_cookie, store_name, last_owner_username).succeeded()


# 4.6 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#46-Edit-manager%E2%80%99s-responsibilities
def test_add_responsibility_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    new_responsibility = "remove_manager"
    system.appoint_manager(cookie, store_name, new_manager_username)
    assert system.add_manager_permission(
        cookie, store_name, new_manager_username, new_responsibility
    ).succeeded()


def test_remove_responsibility_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    new_responsibility = "remove_manager"
    system.appoint_manager(cookie, store_name, new_manager_username)
    system.add_manager_permission(cookie, store_name, new_manager_username, new_responsibility)
    assert system.remove_manager_permission(
        cookie, store_name, new_manager_username, new_responsibility
    ).succeeded()


def test_default_permissions_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    default_permission = "get appointments"
    other_permissions = ["remove manager", "manage products", "appoint manager", "get history"]
    system.appoint_manager(cookie, store_name, new_manager_username)
    assert system.remove_manager_permission(
        cookie, store_name, new_manager_username, default_permission
    ).succeeded()
    for responsibility in other_permissions:
        assert system.add_manager_permission(
            cookie, store_name, new_manager_username, responsibility
        ).succeeded()


def test_add_responsibility_twice_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    new_responsibility = "remove_manager"
    system.appoint_manager(cookie, store_name, new_manager_username)
    system.add_manager_permission(cookie, store_name, new_manager_username, new_responsibility)
    assert not system.add_manager_permission(
        cookie, store_name, new_manager_username, new_responsibility
    ).succeeded()


def test_remove_responsibility_twice_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    new_responsibility = "remove_manager"
    system.appoint_manager(cookie, store_name, new_manager_username)
    assert not system.remove_manager_permission(
        cookie, store_name, new_manager_username, new_responsibility
    ).succeeded()


def test_get_appointment_permission_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_name, new_manager_username)
    assert system.get_store_appointments(new_manager_cookie, store_name).succeeded()


def test_get_history_permission_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_name, new_manager_username)
    system.add_manager_permission(cookie, store_name, new_manager_username, "get history")
    assert system.get_store_purchase_history(new_manager_cookie, store_name).succeeded()


def test_appoint_manager_permission_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    last_manager_cookie, last_manager_username, last_manager_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_manager(cookie, store_name, new_manager_username)
    system.add_manager_permission(cookie, store_name, new_manager_username, "appoint manager")
    assert system.appoint_manager(new_manager_cookie, store_name, last_manager_username).succeeded()


def test_remove_manager_permission_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    last_manager_cookie, last_manager_username, last_manager_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_manager(cookie, store_name, new_manager_username)
    system.appoint_manager(cookie, store_name, last_manager_username)
    system.add_manager_permission(cookie, store_name, new_manager_username, "remove manager")
    assert system.remove_appointment(
        new_manager_cookie, store_name, last_manager_username
    ).succeeded()


def test_manage_products_permission_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_name, new_manager_username)
    system.add_manager_permission(cookie, store_name, new_manager_username, "manage products")
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    assert system.create_product(
        new_manager_cookie, store_name, product_name, price, quantity
    ).succeeded()


def test_get_appointment_no_permission_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_name, new_manager_username)
    system.remove_manager_permission(cookie, store_name, new_manager_username, "get appointments")
    assert not system.get_store_appointments(new_manager_cookie, store_name).succeeded()


def test_get_history_no_permission_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_name, new_manager_username)
    assert not system.get_store_purchase_history(new_manager_cookie, store_name).succeeded()


def test_appoint_manager_no_permission_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    last_manager_cookie, last_manager_username, last_manager_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_manager(cookie, store_name, new_manager_username)
    assert not system.appoint_manager(
        new_manager_cookie, store_name, last_manager_username
    ).succeeded()


def test_remove_manager_no_permission_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    last_manager_cookie, last_manager_username, last_manager_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_manager(cookie, store_name, new_manager_username)
    system.appoint_manager(cookie, store_name, last_manager_username)
    assert not system.remove_appointment(
        new_manager_cookie, store_name, last_manager_username
    ).succeeded()


def test_manage_products_no_permission_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_manager(cookie, store_name, new_manager_username)
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    assert not system.create_product(
        new_manager_cookie, store_name, product_name, price, quantity
    ).succeeded()


# 4.7 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#43-Dismiss-an-owner
def test_dismiss_owner_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    last_manager_cookie, last_manager_username, last_manager_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_owner(cookie, store_name, new_owner_username)
    response = system.remove_appointment(cookie, store_name, new_owner_username)
    assert response.succeeded()


def test_dismiss_owner_wrong_name_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    wrong_name = "Ravit Ron"
    system.appoint_owner(cookie, store_name, new_owner_username)
    assert not system.remove_appointment(cookie, store_name, wrong_name).succeeded()


def test_dismiss_owner_wrong_store_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    wrong_store = "starbux"
    system.appoint_owner(cookie, store_name, new_owner_username)
    assert not system.remove_appointment(cookie, wrong_store, new_owner_username).succeeded()


def test_dismiss_owner_appointing_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    last_manager_cookie, last_manager_username, last_manager_password, _ = _initialize_info(_generate_username(), "ccc")
    system.appoint_owner(cookie, store_name, new_owner_username)
    system.remove_appointment(cookie, store_name, new_owner_username)
    assert not system.appoint_manager(
        new_owner_cookie, store_name, last_manager_username
    ).succeeded()


def test_dismiss_owner_chain_appointing_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    last_owner_cookie, last_owner_username, last_owner_password, _ = _initialize_info(_generate_username(), "ccc")
    final_manager_cookie, final_manager_username, final_manager_password, _ = _initialize_info(_generate_username(), "ddd")
    system.appoint_owner(cookie, store_name, new_owner_username)
    system.appoint_owner(new_owner_cookie, store_name, last_owner_username)
    system.remove_appointment(cookie, store_name, new_owner_username)
    assert not system.appoint_manager(
        last_owner_cookie, store_name, final_manager_username
    ).succeeded()


# 4.9 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#49-Get-store-personnel-information
def test_get_store_personnel_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    response = system.get_store_appointments(cookie, store_name)
    assert (
        response.succeeded()
        and response.object.name == username
        and response.object.position == "founder"
    )


def test_get_store_personnel_owner_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_owner_cookie, new_owner_username, new_owner_password, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_owner(cookie, store_name, new_owner_username)
    response = system.get_store_appointments(cookie, store_name)
    assert (
        response.succeeded()
        and len(response.object.appointments) == 1
        and response.object.appointments[0].name == new_owner_username
        and response.object.appointments[0].position == "owner"
    )


def test_get_store_personnel_manager_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    new_manager_cookie, new_manager_username, new_manager_password, _ = _initialize_info(_generate_username(), "bbb")
    system.appoint_owner(cookie, store_name, new_manager_username)
    response = system.get_store_appointments(cookie, store_name)
    assert (
        response.succeeded()
        and len(response.object.appointments) == 1
        and response.object.appointments[0].name == new_manager_username
        and response.object.appointments[0].position == "manager"
    )


def test_get_store_personnel_wrong_store_name_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    wrong_store = "starbux"
    assert not system.get_store_appointments(cookie, wrong_store).succeeded()


# 4.11 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#411-Get-store-purchase-history
def test_get_store_purchase_history_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    system.purchase_cart(cookie)
    system.send_payment(cookie, card_number, card_expire, card_cvv)
    response = system.get_store_purchase_history(cookie, store_name)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].name == product_name
    )


def test_get_store_purchase_history_no_purchases_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.get_store_purchase_history(cookie, store_name)
    assert not response.succeeded()


def test_get_store_purchase_history_no_purchases_saved_to_cart_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    response = system.get_store_purchase_history(cookie, store_name)
    assert not response.succeeded()


def test_get_store_purchase_history_no_payment_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    system.purchase_cart(cookie)
    response = system.get_store_purchase_history(cookie, store_name)
    assert not response.succeeded()


# 6.4 https://github.com/SeanPikulin/TradingSystem/blob/main/Documentation/Use%20Cases.md#64-Get-store-purchase-history-system-manager
def test_admin_get_store_purchase_history_success():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    card_number = "1234-1234-1234-1234"
    card_expire = "12/34"
    card_cvv = "123"
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    system.purchase_cart(cookie)
    system.send_payment(cookie, card_number, card_expire, card_cvv)
    response = system.get_store_purchase_history(cookie, store_name)
    assert (
        response.succeeded()
        and len(response.object.values) == 1
        and response.object.values[0].name == product_name
    )


def test_admin_get_store_purchase_history_no_purchases_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    response = system.get_store_purchase_history(cookie, store_name)
    assert not response.succeeded()


def test_admin_get_store_purchase_history_no_purchases_saved_to_cart_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    response = system.get_store_purchase_history(cookie, store_name)
    assert not response.succeeded()


def test_admin_get_store_purchase_history_no_payment_fail():
    cookie, username, password, store_name = _initialize_info(_generate_username(), "aaa", _generate_store_name())
    product_name = _generate_product_name()
    price = 5.50
    quantity = 10
    system.create_product(cookie, store_name, product_name, price, quantity)
    system.save_product_in_cart(cookie, store_name, product_name, 1)
    system.purchase_cart(cookie)
    response = system.get_store_purchase_history(cookie, store_name)
    assert not response.succeeded()