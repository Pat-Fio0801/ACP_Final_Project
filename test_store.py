import pytest
from store import (
    load_inventory_from_csv,
    save_inventory_to_csv,
)

TEST_INVENTORY_FILE = "test_inventory.csv"

@pytest.fixture
def sample_inventory():
    return {
        "Apple": {"quantity": 10, "base_price": 50, "sell_price": 75},
        "Banana": {"quantity": 20, "base_price": 30, "sell_price": 45},
    }

def test_load_inventory_from_csv(sample_inventory):
    save_inventory_to_csv(TEST_INVENTORY_FILE, sample_inventory)
    loaded_inventory = load_inventory_from_csv(TEST_INVENTORY_FILE)
    assert loaded_inventory == sample_inventory

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

