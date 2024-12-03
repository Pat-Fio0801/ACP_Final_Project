daily_sales = {}
weekly_sales = []
weekly_product_summary = {}
weekly_cost = 0
inventory = {}

def add_item(inventory):
    fruit_name = input("Enter fruit name: ").strip().title()
    quantity = float(input(f"Enter quantity for {fruit_name} (in kilos): "))
    base_price = float(input(f"Enter base price per kilo for {fruit_name} (in pesos): "))
    sell_price = base_price + 20
    if fruit_name in inventory:
        inventory[fruit_name]["quantity"] += quantity
        inventory[fruit_name]["base_price"] = base_price
        inventory[fruit_name]["sell_price"] = sell_price
    else:
        inventory[fruit_name] = {"quantity": quantity, "base_price": base_price, "sell_price": sell_price}

    print(f"Added {quantity} kg of {fruit_name} at ₱{sell_price:.2f} per kilo.")
    return quantity * base_price

def view_inventory(inventory):
    if not inventory:
        print("No inventory available.")
    else:
        print("\nCurrent Fruit Inventory:")
        print(f"{'Fruit Name':<15} {'Quantity (kg)':<15} {'Price per Kilo (₱)':<20}")
        print("-" * 50)  # Separator line for neatness

        for fruit, details in inventory.items():
            print(f"{fruit:<15} {details['quantity']:<15} {details['sell_price']:<20.2f}")

def record_sale(inventory, day):
    global weekly_product_summary
    fruit_name = input("Enter fruit name sold: ").strip().title()
    if fruit_name in inventory:
        kilos_sold = float(input("Enter quantity sold in kilos: "))
        if kilos_sold <= inventory[fruit_name]["quantity"]:
            total_sale = kilos_sold * inventory[fruit_name]["sell_price"]
            profit = kilos_sold * (inventory[fruit_name]["sell_price"] - inventory[fruit_name]["base_price"])
            inventory[fruit_name]["quantity"] -= kilos_sold

            daily_sales[day].append({"item": fruit_name, "kilos": kilos_sold, "total": total_sale, "profit": profit, "refund": False})

            if fruit_name in weekly_product_summary:
                weekly_product_summary[fruit_name] += kilos_sold
            else:
                weekly_product_summary[fruit_name] = kilos_sold

            print(f"Sale recorded: {kilos_sold} kg of {fruit_name} sold for ₱{total_sale:.2f}. Profit: ₱{profit:.2f}.")
            if inventory[fruit_name]["quantity"] == 0:
                print(f"Fruit '{fruit_name}' is now out of stock.")
        else:
            print(f"Not enough stock for '{fruit_name}'. Available: {inventory[fruit_name]['quantity']} kg")
    else:
        print(f"Fruit '{fruit_name}' not found in inventory.")

def view_daily_sales(day):
    if not daily_sales[day]:
        print(f"No sales recorded for {day}.")
    else:
        print(f"\nSales for {day}:")
        total_sales = 0
        total_profit = 0
        total_refunds = 0
        profit_lost_from_returns = 0

        for sale in daily_sales[day]:
            if sale["refund"]:
                print(f"{sale['kilos']} kg of {sale['item']} returned for ₱{sale['total']:.2f} (Refund)")
                total_refunds += sale["total"]
                profit_lost_from_returns += sale["kilos"] * 20  # Subtract the profit lost
            else:
                print(f"{sale['kilos']} kg of {sale['item']} sold for ₱{sale['total']:.2f} (Profit: ₱{sale['profit']:.2f})")
                total_sales += sale['total']
                total_profit += sale['profit']

        total_profit -= profit_lost_from_returns

        print(f"Total Sales for {day}: ₱{total_sales:.2f}")
        print(f"Total Refunds for {day}: ₱{total_refunds:.2f}")
        print(f"Net Total for {day}: ₱{total_sales - total_refunds:.2f}")
        print(f"Total Profit for {day}: ₱{total_profit:.2f}")


def end_day(day):
    total_sales = sum(sale["total"] for sale in daily_sales[day] if not sale["refund"])
    weekly_sales.append({"day": day, "total": total_sales})
    print(f"End of {day}: Total sales: ₱{total_sales:.2f}")

def calculate_weekly_summary(inventory):
    print("\n--- Weekly Summary ---")
    total_sales_before_refund = 0
    total_sales_after_refund = 0
    total_cost_before_refund = 0
    total_cost_after_refund = 0
    total_profit = 0
    total_refunds = 0
    product_summary = {fruit: 0 for fruit in inventory}

    for day in weekly_sales:
        total_sales_for_day = day["total"]
        total_sales_before_refund += total_sales_for_day

        for sale in daily_sales[day["day"]]:
            fruit_name = sale["item"]
            if not sale["refund"]:
                quantity_sold = sale["kilos"]
                base_price = inventory[fruit_name]["base_price"]
                total_cost_before_refund += base_price * quantity_sold
                total_cost_after_refund += base_price * quantity_sold
                total_profit += 20 * quantity_sold
                total_sales_after_refund += sale["total"]
                product_summary[fruit_name] += quantity_sold
            else:
                quantity_returned = sale["kilos"]
                total_refunds += quantity_returned * inventory[fruit_name]["sell_price"]
                total_profit -= 20 * quantity_returned
                total_cost_after_refund -= quantity_returned * inventory[fruit_name]["base_price"]

        print(f"{day['day']}: ₱{total_sales_for_day:.2f}")

    profit = total_sales_after_refund - total_cost_after_refund - total_refunds
    print(f"\nTotal Weekly Sales Before Refund: ₱{total_sales_before_refund:.2f}")
    print(f"Total Weekly Sales After Refund: ₱{total_sales_before_refund - total_refunds:.2f}")
    print(f"Total Weekly Cost Before Refund: ₱{total_cost_before_refund:.2f}")
    print(f"Total Weekly Cost After Refund: ₱{total_cost_after_refund:.2f}")
    print(f"Total Refunds: ₱{total_refunds:.2f}")
    print(f"Total Weekly Profit (After Refunds): ₱{profit:.2f}")

    print("\n--- Weekly Product Summary ---")
    for fruit, kilos in product_summary.items():
        print(f"{fruit}: {kilos:.2f} kg sold")

    max_sold_quantity = max(product_summary.values())
    most_purchased_fruits = [fruit for fruit, kilos in product_summary.items() if kilos == max_sold_quantity]

    print("\nMost Purchased Fruits: " + ", ".join(most_purchased_fruits) + f" ({max_sold_quantity:.2f} kg sold)")

def process_return(inventory, day):
    fruit_name = input("Enter fruit name to return: ").strip().title()
    if fruit_name in inventory:
        kilos_returned = float(input(f"Enter quantity of {fruit_name} to return (in kilos): "))
        inventory[fruit_name]["quantity"] += kilos_returned
        total_refund = kilos_returned * inventory[fruit_name]["sell_price"]
        profit_loss = kilos_returned * (inventory[fruit_name]["sell_price"] - inventory[fruit_name]["base_price"])
        daily_sales[day].append({"item": fruit_name, "kilos": kilos_returned, "total": total_refund, "profit": -profit_loss, "refund": True})
        print(f"Refund processed: {kilos_returned} kg of {fruit_name} returned. Total Refund: ₱{total_refund:.2f}")
    else:
        print(f"Fruit '{fruit_name}' not found in inventory.")

def main():
    global weekly_cost
    print("\nWelcome to the Fruit Store Management System :))")

    inventory = {
        "Apple":        {"quantity": 10, "base_price": 60,  "sell_price": 80},
        "Orange":       {"quantity": 10, "base_price": 60,  "sell_price": 80},
        "Banana":       {"quantity": 10, "base_price": 30,  "sell_price": 50},
        "Grapes":       {"quantity": 10, "base_price": 120, "sell_price": 140},
        "Chikoo":       {"quantity": 10, "base_price": 100, "sell_price": 120},
        "Dragon Fruit": {"quantity": 10, "base_price": 150, "sell_price": 170},
        "Avocado":      {"quantity": 10, "base_price": 130, "sell_price": 150},
        "Guava":        {"quantity": 10, "base_price": 80,  "sell_price": 100},
        "Mango":        {"quantity": 10, "base_price": 160, "sell_price": 180},
        "Lemon":        {"quantity": 10, "base_price": 140, "sell_price": 160},
        "Mangosteen":   {"quantity": 10, "base_price": 180, "sell_price": 200},
        "Star Apple":   {"quantity": 10, "base_price": 120, "sell_price": 140},
        "Rambutan":     {"quantity": 10, "base_price": 100, "sell_price": 120},
    }

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for day in days:
        print(f"\n--- {day} ---")
        daily_sales[day] = []
        weekly_product_summary.clear()

        # Simulate daily tasks
        while True:
            print("\nWhat would you like to do?")
            print("1. Add Item")
            print("2. View Inventory")
            print("3. Record Sale")
            print("4. Process Return")
            print("5. View Daily Sales")
            print("6. End Day")
            print("7. Exit")

            choice = input("Enter your choice (1-7): ")

            if choice == '1':
                add_item(inventory)
            elif choice == '2':
                view_inventory(inventory)
            elif choice == '3':
                record_sale(inventory, day)
            elif choice == '4':
                process_return(inventory, day)
            elif choice == '5':
                view_daily_sales(day)
            elif choice == '6':
                end_day(day)
                break
            elif choice == '7':
                return
            else:
                print("Invalid choice. Please try again.")

    calculate_weekly_summary(inventory)

if __name__ == "__main__":
    main()
