daily_sales = {}  # Dictionary to store daily sales
weekly_sales = []  # List to store sales of each day
weekly_cost = 14300  # Starting capital of 14,300 pesos
weekly_product_summary = {}  # Tracks fruit sales across the week

# Main program
def main():
    global weekly_cost
    print("Welcome to the Fruit Store Management System (in Pesos)")

    # Pre-populate inventory with 10 kilos of each specified fruit
    inventory = {
        "Apple": {"quantity": 10, "price": 60},
        "Orange": {"quantity": 10, "price": 60},
        "Banana": {"quantity": 10, "price": 30},
        "Grapes": {"quantity": 10, "price": 120},
        "Chikoo": {"quantity": 10, "price": 100},
        "Dragon Fruit": {"quantity": 10, "price": 150},
        "Avocado": {"quantity": 10, "price": 130},
        "Guava": {"quantity": 10, "price": 80},
        "Mango": {"quantity": 10, "price": 160},
        "Lemon": {"quantity": 10, "price": 140},
        "Mangosteen": {"quantity": 10, "price": 180},
        "Star Apple": {"quantity": 10, "price": 120},
        "Rambutan": {"quantity": 10, "price": 100}
    }

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for day in days:
        print(f"\n--- {day} ---")
        daily_sales[day] = []
        while True:
            print("\n1. Add Fruit\n2. View Inventory\n3. Delete Fruit")
            print("4. Record Sale\n5. View Daily Sales\n6. End Day")
            choice = input("Enter your choice: ")

            if choice == "1":
                weekly_cost += add_item(inventory)
            elif choice == "2":
                view_inventory(inventory)
            elif choice == "3":
                delete_item(inventory)
            elif choice == "4":
                record_sale(inventory, day)
            elif choice == "5":
                view_daily_sales(day)
            elif choice == "6":
                end_day(day)
                break
            else:
                print("Invalid choice. Try again.")

    calculate_weekly_summary()

# Function 1: Add fruit
def add_item(inventory):
    while True:
        item_name = input("Enter fruit name (e.g., Apple, Banana): ").strip().title()
        if item_name.isalpha():
            break
        else:
            print("Invalid input. Please enter only fruit names.")

    quantity = float(input("Enter quantity in kilos (e.g., 1.5 for 1.5 kg): "))
    price = float(input("Enter price per kilo in pesos: ₱"))
    cost = quantity * price  # Cost of items added
    inventory[item_name] = {"quantity": quantity, "price": price}
    print(f"Fruit '{item_name}' added successfully.")
    return cost

# Function 2: View inventory
def view_inventory(inventory):
    if not inventory:
        print("The fruit inventory is empty.")
    else:
        print("\nCurrent Fruit Inventory:")
        for fruit, details in inventory.items():
            print(f"{fruit}: Quantity: {details['quantity']} kg, Price per kilo: ₱{details['price']:.2f}")

# Function 3: Delete fruit
def delete_item(inventory):
    fruit_name = input("Enter the fruit name to delete: ").strip().title()
    if fruit_name in inventory:
        del inventory[fruit_name]
        print(f"Fruit '{fruit_name}' deleted successfully.")
    else:
        print(f"Fruit '{fruit_name}' not found.")

# Function 4: Record fruit sale
def record_sale(inventory, day):
    global weekly_product_summary
    fruit_name = input("Enter fruit name sold: ").strip().title()
    if fruit_name in inventory:
        kilos_sold = float(input("Enter quantity sold in kilos (e.g., 2.5 for 2.5 kg): "))
        if kilos_sold <= inventory[fruit_name]["quantity"]:
            total_sale = kilos_sold * inventory[fruit_name]["price"]
            inventory[fruit_name]["quantity"] -= kilos_sold
            daily_sales[day].append({"item": fruit_name, "kilos": kilos_sold, "total": total_sale})

            # Update weekly product summary
            if fruit_name in weekly_product_summary:
                weekly_product_summary[fruit_name] += kilos_sold
            else:
                weekly_product_summary[fruit_name] = kilos_sold

            print(f"Sale recorded: {kilos_sold} kg of {fruit_name} sold for ₱{total_sale:.2f}.")
            if inventory[fruit_name]["quantity"] == 0:
                print(f"Fruit '{fruit_name}' is now out of stock.")
        else:
            print(f"Not enough stock for '{fruit_name}'. Available: {inventory[fruit_name]['quantity']} kg")
    else:
        print(f"Fruit '{fruit_name}' not found in inventory.")

# Function 5: View daily sales
def view_daily_sales(day):
    if not daily_sales[day]:
        print(f"No sales recorded for {day}.")
    else:
        print(f"\nSales for {day}:")
        for sale in daily_sales[day]:
            print(f"{sale['kilos']} kg of {sale['item']} sold for ₱{sale['total']:.2f}")
        daily_total = sum(sale['total'] for sale in daily_sales[day])
        print(f"Total Sales for {day}: ₱{daily_total:.2f}")

# Function 6: End day
def end_day(day):
    daily_total = sum(sale['total'] for sale in daily_sales[day])
    weekly_sales.append({"day": day, "total": daily_total})
    print(f"End of {day}. Total sales: ₱{daily_total:.2f}")

# Weekly summary
def calculate_weekly_summary():
    print("\n--- Weekly Summary ---")
    total_sales = 0
    for day in weekly_sales:
        print(f"{day['day']}: ₱{day['total']:.2f}")
        total_sales += day['total']

    profit = total_sales - weekly_cost
    print(f"\nTotal Weekly Sales: ₱{total_sales:.2f}")
    print(f"Total Weekly Cost: ₱{weekly_cost:.2f}")
    print(f"Total Weekly Profit: ₱{profit:.2f}")

    # Display weekly product summary
    print("\n--- Weekly Product Summary ---")
    for fruit, kilos in weekly_product_summary.items():
        print(f"{fruit}: {kilos} kg sold")

    # Find most purchased product
    if weekly_product_summary:
        most_purchased = max(weekly_product_summary, key=weekly_product_summary.get)
        print(f"\nMost Purchased Fruit: {most_purchased} ({weekly_product_summary[most_purchased]} kg sold)")




if __name__ == "__main__":
    main()
