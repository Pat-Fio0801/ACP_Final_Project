import pytest
from unittest.mock import patch
from project import (
    add_item,
    view_inventory,
    delete_item,
    record_sale,
    process_return,
    calculate_weekly_summary,
    view_daily_sales,
)

# Sample inventory for testing
inventory = {
    "Apple": {"quantity": 10, "base_price": 60, "sell_price": 80},
    "Orange": {"quantity": 10, "base_price": 60, "sell_price": 80},
    "Banana": {"quantity": 10, "base_price": 30, "sell_price": 50},
    "Grapes": {"quantity": 10, "base_price": 120, "sell_price": 140},
    "Chikoo": {"quantity": 10, "base_price": 100, "sell_price": 120},
    "Dragon Fruit": {"quantity": 10, "base_price": 150, "sell_price": 170},
    "Avocado": {"quantity": 10, "base_price": 130, "sell_price": 150},
    "Guava": {"quantity": 10, "base_price": 80, "sell_price": 100},
    "Mango": {"quantity": 10, "base_price": 160, "sell_price": 180},
    "Lemon": {"quantity": 10, "base_price": 140, "sell_price": 160},
    "Mangosteen": {"quantity": 10, "base_price": 180, "sell_price": 200},
    "Star Apple": {"quantity": 10, "base_price": 120, "sell_price": 140},
    "Rambutan": {"quantity": 10, "base_price": 100, "sell_price": 120},
}

# Sample daily sales for testing
daily_sales = {}

# Test add_item function
@patch('builtins.input', side_effect=["Apple", "5", "60"])  # Mock inputs for Apple, 5 kg, 60 pesos per kilo
def test_add_item(mock_input):
    initial_inventory = inventory["Apple"]["quantity"]
    add_item(inventory)
    assert inventory["Apple"]["quantity"] == initial_inventory + 5  # Adding 5 kilos of Apple
    assert inventory["Apple"]["sell_price"] == 72  # Ensure markup price is correct

# Test view_inventory function
def test_view_inventory():
    result = view_inventory(inventory)
    assert result is None  # view_inventory just prints; we check that no errors occur

# Test delete_item function
@patch('builtins.input', side_effect=["Apple"])  # Mock input for deleting Apple
def test_delete_item(mock_input):
    initial_inventory = inventory.copy()
    delete_item(inventory)
    assert "Apple" not in inventory  # Assuming "Apple" is deleted
    assert "Apple" in initial_inventory  # Ensure "Apple" existed before deletion

# Test record_sale function
@patch('builtins.input', side_effect=["Banana", "5"])  # Mock input for selling 5 kg of Banana
def test_record_sale(mock_input):
    initial_quantity = inventory["Banana"]["quantity"]
    # Ensure "Monday" exists before accessing it
    if "Monday" not in daily_sales:
        daily_sales["Monday"] = []
    record_sale(inventory, "Monday")
    assert inventory["Banana"]["quantity"] == initial_quantity - 5  # Assuming 5 kg of Banana sold
    # Check that "Monday" exists in daily_sales and contains the record
    assert "Monday" in daily_sales
    assert any(sale["item"] == "Banana" for sale in daily_sales["Monday"])

# Test process_return function
@patch('builtins.input', side_effect=["Banana", "5"])  # Mock input for returning 5 kg of Banana
def test_process_return(mock_input):
    initial_quantity = inventory["Banana"]["quantity"]
    # Ensure "Monday" exists before accessing it
    if "Monday" not in daily_sales:
        daily_sales["Monday"] = []
    process_return(inventory, "Monday")
    # 5 kg should be added back to inventory
    assert inventory["Banana"]["quantity"] == initial_quantity + 5
    # Check that "Monday" exists in daily_sales after return
    assert "Monday" in daily_sales
    assert any(sale["item"] == "Banana" for sale in daily_sales["Monday"])

# Test refund process logic (a combination of sale and return)
@patch('builtins.input', side_effect=["Banana", "5"])  # Mock input for selling and returning 5 kg of Banana
def test_process_refund(mock_input):
    # Simulate a sale first
    if "Monday" not in daily_sales:
        daily_sales["Monday"] = []
    record_sale(inventory, "Monday")
    # Now simulate a return of the same quantity
    process_return(inventory, "Monday")
    # Inventory should reflect the original quantity after return
    assert inventory["Banana"]["quantity"] == 10  # Should return back to 10 kg
    # Check "Monday" sales record
    assert "Monday" in daily_sales
    assert any(sale["item"] == "Banana" for sale in daily_sales["Monday"])

# Test calculate_weekly_summary function
def test_calculate_weekly_summary():
    result = calculate_weekly_summary(inventory)
    assert result is None  # Just checking for errors during the summary calculation

# Test view_daily_sales function
def test_view_daily_sales():
    # Ensure "Monday" exists before accessing it
    if "Monday" not in daily_sales:
        daily_sales["Monday"] = []
    view_daily_sales("Monday")
    assert True  # If no errors, the test passes
