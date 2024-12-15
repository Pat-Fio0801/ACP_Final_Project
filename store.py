import csv
from datetime import datetime

daily_sales = {}
weekly_sales = []
weekly_product_summary = {}
weekly_cost = 0
inventory = {}
weekly_sales_total = 0
weekly_profit_total = 0
current_week = datetime.now().strftime("%U")

def load_inventory_from_csv(file_name):
    inventory = {}
    try:
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            print("CSV Header Names:", reader.fieldnames)  # Print header names for debugging

            for row in reader:
                try:
                    fruit_name = row["Fruit Name"]
                    quantity = float(row["Quantity"])
                    base_price = float(row["Base Price"])
                    sell_price = float(row["Sell Price"])
                    inventory[fruit_name] = {"quantity": quantity, "base_price": base_price, "sell_price": sell_price}
                except KeyError as e:
                    print(f"Missing column in CSV: {e}")
    except FileNotFoundError:
        print("CSV file not found. Creating a new inventory.")
    return inventory

# Save inventory to CSV
def save_inventory_to_csv(file_name, inventory):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["Fruit Name", "Quantity", "Base Price", "Sell Price"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for fruit_name, details in inventory.items():
            writer.writerow({
                "Fruit Name": fruit_name,
                "Quantity": details["quantity"],
                "Base Price": details["base_price"],
                "Sell Price": details["sell_price"]
            })

# Function to add item to inventory
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

# Function to view inventory
def view_inventory(inventory):
    if not inventory:
        print("No inventory available.")
    else:
        print("\nCurrent Fruit Inventory:")
        print(f"{'Fruit Name':<15} {'Quantity (kg)':<15} {'Price per Kilo (₱)':<20}")
        print("-" * 50)  # Separator line for neatness
        for fruit, details in inventory.items():
            print(f"{fruit:<15} {details['quantity']:<15} {details['sell_price']:<20.2f}")

# Function to record a sale
def record_sale(inventory, day):
    global weekly_product_summary
    fruit_name = input("Enter fruit name sold: ").strip().title()
    if fruit_name in inventory:
        kilos_sold = float(input("Enter quantity sold in kilos: "))
        if kilos_sold <= inventory[fruit_name]["quantity"]:
            total_sale = kilos_sold * inventory[fruit_name]["sell_price"]
            profit = kilos_sold * (inventory[fruit_name]["sell_price"] - inventory[fruit_name]["base_price"])
            inventory[fruit_name]["quantity"] -= kilos_sold

            if day not in daily_sales:
                daily_sales[day] = []  # Initialize the list for the day if not already initialized

            # Record the sale with 'refund' set to False
            daily_sales[day].append({"item": fruit_name, "kilos": kilos_sold, "total": total_sale, "profit": profit, "refund": False})

            # Update weekly summary data
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

# Function to view daily sales
def view_daily_sales(day):
    if day not in daily_sales or not daily_sales[day]:
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

def process_return(inventory, day):
    fruit_name = input("Enter fruit name being returned: ").strip().title()
    if fruit_name in inventory:
        kilos_returned = float(input(f"Enter quantity returned for {fruit_name} (in kilos): "))
        if kilos_returned <= inventory[fruit_name]["quantity"]:
            total_refund = kilos_returned * inventory[fruit_name]["sell_price"]
            refund_profit_loss = kilos_returned * 20  # Lost profit from return

            # Update daily sales with refund
            daily_sales[day].append({"item": fruit_name, "kilos": kilos_returned, "total": total_refund, "profit": -refund_profit_loss, "refund": True})

            # Update weekly summary data
            if fruit_name in weekly_product_summary:
                weekly_product_summary[fruit_name] -= kilos_returned
            else:
                weekly_product_summary[fruit_name] = -kilos_returned  # Return will show as negative sold quantity

            print(f"Return processed: {kilos_returned} kg of {fruit_name} returned for ₱{total_refund:.2f}. Lost profit: ₱{refund_profit_loss:.2f}.")
        else:
            print(f"Not enough stock for '{fruit_name}'. Available: {inventory[fruit_name]['quantity']} kg")
    else:
        print(f"Fruit '{fruit_name}' not found in inventory.")


def end_day(day):
    # Calculate and print total sales and profit for the day
    total_day_sales = 0
    total_day_profit = 0
    
    # Loop through the daily sales to calculate the total sales and total profit
    for sale in daily_sales[day]:
        total_day_sales += sale["total"]
        total_day_profit += sale["profit"]  # Adding the profit from each sale
    
    print(f"\n--- {day} Ended ---")
    print(f"Total Sales for {day}: ₱{total_day_sales:.2f}")
    print(f"Total Profit for {day}: ₱{total_day_profit:.2f}")
    
    # Prepare the data to be saved in the CSV file
    day_data = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Day": day,
        "Total Sales": total_day_sales,
        "Profit": total_day_profit
    }
    
    # Define the CSV file name (end_day.csv will store all days' data)
    file_name = "end_day.csv"

    # Check if the file exists. If it doesn't, create it and write the header.
    file_exists = False
    try:
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ["Date", "Day", "Total Sales", "Profit"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # If the file does not exist, write the header
        if not file_exists:
            writer.writeheader()
        
        # Write the current day's sales data to the file
        writer.writerow(day_data)
    
    print(f"Sales and profit data for {day} has been saved in '{file_name}'.")
    
# At the end of each day's operations, you can add a summary for the day:
def update_weekly_sales(day):
    total_day_sales = sum(sale["total"] for sale in daily_sales[day])
    weekly_sales.append({"day": day, "total": total_day_sales})

    
def calculate_weekly_summary(inventory, week_number, daily_sales):
    global weekly_sales_total, weekly_profit_total
    
    print(f"\n--- Weekly Summary for Week {week_number} ---")
    
    total_sales_before_refund = 0
    total_sales_after_refund = 0
    total_cost_before_refund = 0
    total_cost_after_refund = 0
    total_refunds = 0
    product_summary = {fruit: 0 for fruit in inventory}

    # Process each day's sales to generate the weekly summary
    for day, sales in daily_sales.items():
        for sale in sales:
            fruit_name = sale["item"]
            quantity_sold = sale["kilos"]
            
            if not sale["refund"]:
                # Normal sale
                total_sales_before_refund += sale["total"]
                total_sales_after_refund += sale["total"]
                total_cost_before_refund += inventory[fruit_name]["base_price"] * quantity_sold
                total_cost_after_refund += inventory[fruit_name]["base_price"] * quantity_sold
                product_summary[fruit_name] += quantity_sold
            else:
                # Refund
                total_refunds += sale["total"]
                total_sales_after_refund -= sale["total"]
                total_cost_after_refund -= inventory[fruit_name]["base_price"] * quantity_sold

    # Calculate profit after refunds
    profit = total_sales_after_refund - total_cost_after_refund - total_refunds

    # Check if product_summary is not empty before finding the most purchased fruit
    if product_summary:
        max_sold_quantity = max(product_summary.values())
        most_purchased_fruits = [
            f"{fruit} ({quantity:.2f} kg)" for fruit, quantity in product_summary.items() if quantity == max_sold_quantity
        ]
    else:
        most_purchased_fruits = ["No sales recorded"]

    # Display the weekly summary
    print(f"\nTotal Weekly Sales Before Refund: ₱{total_sales_before_refund:.2f}")
    print(f"Total Weekly Sales After Refund: ₱{total_sales_after_refund:.2f}")
    print(f"Total Weekly Cost Before Refund: ₱{total_cost_before_refund:.2f}")
    print(f"Total Weekly Cost After Refund: ₱{total_cost_after_refund:.2f}")
    print(f"Total Refunds: ₱{total_refunds:.2f}")
    print(f"Total Weekly Profit (After Refunds): ₱{profit:.2f}")
    print(f"Most Purchased Fruit(s): {', '.join(most_purchased_fruits)}")

    # Save the weekly summary to CSV
    with open("weekly_summary.csv", mode='a', newline='', encoding='utf-8') as file:
        fieldnames = [
            "Week Number",
            "Total Weekly Sales Before Refund",
            "Total Weekly Sales After Refund",
            "Total Weekly Cost Before Refund",
            "Total Weekly Cost After Refund",
            "Total Refunds",
            "Total Weekly Profit",
            "Most Purchased Fruits"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if the file is empty
        file_exists = file.tell() > 0
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "Week Number": f"Week {week_number}",
            "Total Weekly Sales Before Refund": total_sales_before_refund,
            "Total Weekly Sales After Refund": total_sales_after_refund,
            "Total Weekly Cost Before Refund": total_cost_before_refund,
            "Total Weekly Cost After Refund": total_cost_after_refund,
            "Total Refunds": total_refunds,
            "Total Weekly Profit": profit,
            "Most Purchased Fruits": ", ".join(most_purchased_fruits),
        })

    print(f"Weekly summary saved to 'weekly_summary.csv'.")
    
def reset_weekly_data():
    global total_sales_before_refund, total_sales_after_refund
    global total_cost_before_refund, total_cost_after_refund, total_refunds
    
    total_sales_before_refund = 0
    total_sales_after_refund = 0
    total_cost_before_refund = 0
    total_cost_after_refund = 0
    total_refunds = 0
    print("\nWeekly data has been reset!")


# Main loop
def main():
    global weekly_cost
    week_number = 1
    print("\nWelcome to the Fruit Store Management System :))")

    inventory = load_inventory_from_csv("inventory.csv")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_count = 0

    while True:
        print("\n--- Starting New Week ---")
        for day in days:
            day_count += 1
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
                print("7. Move to Next Week")
                print("8. Exit")

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
                elif choice == "7":
                    print("\nMoving to the next week...")
                    calculate_weekly_summary(inventory, week_number)
                    week_number += 1
                    reset_weekly_data()
                    print(f"Welcome to Week {week_number}!")
                elif choice == '8':
                    save_inventory_to_csv("inventory.csv", inventory)
                    print("Exiting program. Goodbye!")
                    return
                else:
                    print("Invalid choice. Please try again.")

        calculate_weekly_summary(inventory, week_number, daily_sales)

        weekly_sales.clear()
        weekly_product_summary.clear()
        day_count = 0

if __name__ == "__main__":
    main()
