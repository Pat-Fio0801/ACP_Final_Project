import pytest
import os
from store import (
    load_inventory_from_csv,
    save_inventory_to_csv,
    add_item,
    record_sale,
)

# Pansamantalang inventory file para sa testing
TEST_INVENTORY_FILE = "test_inventory.csv"

# Sample inventory para sa testing
@pytest.fixture
def sample_inventory():
    return {
        "Apple": {"quantity": 10, "base_price": 50, "sell_price": 75},
        "Banana": {"quantity": 20, "base_price": 30, "sell_price": 45},
    }

# Test para sa load_inventory_from_csv at save_inventory_to_csv
def test_load_and_save_inventory(sample_inventory):
    save_inventory_to_csv(TEST_INVENTORY_FILE, sample_inventory)
    loaded_inventory = load_inventory_from_csv(TEST_INVENTORY_FILE)
    assert loaded_inventory == sample_inventory
    os.remove(TEST_INVENTORY_FILE)  # Tanggalin ang test file pagkatapos gamitin

# Test para sa add_item
def add_item(inventory, fruit_name, quantity, base_price):
    """
    Adds a new fruit to the inventory with a calculated selling price.
    """
    sell_price = base_price * 1.5  # Calculate the selling price
    inventory[fruit_name] = {
        "quantity": quantity,
        "base_price": base_price,
        "sell_price": sell_price,
    }
    return inventory


# Test para sa record_sale
def record_sale(inventory, fruit_name, kilos_sold, day):
    """
    Records a sale, updates inventory, and logs daily sales.
    """
    if fruit_name not in inventory:
        raise ValueError(f"{fruit_name} not found in inventory.")
    if inventory[fruit_name]["quantity"] < kilos_sold:
        raise ValueError("Insufficient stock.")

    inventory[fruit_name]["quantity"] -= kilos_sold
    sell_price = inventory[fruit_name]["sell_price"]
    total_sale = kilos_sold * sell_price

    # Initialize daily sales dictionary
    daily_sales = {}
    if day not in daily_sales:
        daily_sales[day] = []
    daily_sales[day].append({"item": fruit_name, "quantity": kilos_sold, "total": total_sale})

    return inventory, daily_sales, total_sale


# Test para sa error handling kapag walang sapat na stock
def test_record_sale_insufficient_stock(sample_inventory):
    fruit_name = "Banana"
    kilos_sold = 25  # Higit sa available na 20
    day = "2024-12-15"

    with pytest.raises(ValueError, match="Insufficient stock."):
        record_sale(sample_inventory, fruit_name, kilos_sold, day)

# Test para sa error handling kapag wala ang fruit sa inventory
def test_record_sale_fruit_not_found(sample_inventory):
    fruit_name = "Pineapple"  # Wala sa inventory
    kilos_sold = 5
    day = "2024-12-15"

    with pytest.raises(ValueError, match=f"{fruit_name} not found in inventory."):
        record_sale(sample_inventory, fruit_name, kilos_sold, day)
