import pytest
from project import add_item, view_inventory, delete_item, record_sale, view_daily_sales, end_day

def test_add_item():
    inventory = {"Apple": {"quantity": 10, "price": 60}}
    cost = add_item(inventory)
    assert cost == 600  # Check if cost is calculated correctly

def test_view_inventory():
    inventory = {"Apple": {"quantity": 10, "price": 60}}
    assert view_inventory(inventory) == "\nCurrent Fruit Inventory:\nApple: Quantity: 10 kg, Price per kilo: ₱60.00"

def test_delete_item():
    inventory = {"Apple": {"quantity": 10, "price": 60}}
    delete_item(inventory)
    assert "Apple" not in inventory  # Check if item was deleted

def test_record_sale():
    inventory = {"Apple": {"quantity": 10, "price": 60}}
    record_sale(inventory, "Monday")
    assert inventory["Apple"]["quantity"] == 9  # Check if quantity decreased correctly

def test_view_daily_sales():
    daily_sales = {"Monday": [{"item": "Apple", "kilos": 1, "total": 60}]}
    assert view_daily_sales("Monday") == "Sales for Monday:\n1 kg of Apple sold for ₱60.00\nTotal Sales for Monday: ₱60.00"


