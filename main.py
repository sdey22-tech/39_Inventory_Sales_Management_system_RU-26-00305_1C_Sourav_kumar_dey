
import pandas as pd
import os

# Create CSV files if they do not exist
if not os.path.exists("inventory.csv"):
    pd.DataFrame(columns=["ID", "Name", "Stock", "Price"]).to_csv(
        "inventory.csv", index=False
    )

if not os.path.exists("sales.csv"):
    pd.DataFrame(columns=["ID", "Quantity", "Amount"]).to_csv(
        "sales.csv", index=False
    )


# 1. ADD ITEM
def add_item():
    inventory = pd.read_csv("inventory.csv")

    print("\n===== ADD ITEM =====")

    name = input("Enter item name: ").strip()

    if not name:
        print("Item name cannot be empty!")
        return

    try:
        stock = int(input("Enter stock quantity: "))
        price = float(input("Enter item price: "))

        if stock <= 0 or price <= 0:
            print("Stock and price must be greater than zero!")
            return

    except ValueError:
        print("Please enter valid numbers!")
        return

    if inventory.empty:
        item_id = 1101
    else:
        item_id = int(inventory["ID"].max()) + 1

    new_item = pd.DataFrame([{
        "ID": item_id,
        "Name": name,
        "Stock": stock,
        "Price": price
    }])

    inventory = pd.concat([inventory, new_item], ignore_index=True)
    inventory.to_csv("inventory.csv", index=False)

    print("Item added.")
    print(f"ID: {item_id} | {name} | Stock: {stock} | Price: {price:g}")


# 2. SELL ITEM
def sell_item():
    inventory = pd.read_csv("inventory.csv")
    sales = pd.read_csv("sales.csv")

    print("\n===== SELL ITEM =====")

    try:
        item_id = int(input("Enter Item ID: "))
        quantity = int(input("Enter Quantity: "))

        if quantity <= 0:
            print("Quantity must be greater than zero!")
            return

    except ValueError:
        print("Please enter valid numbers!")
        return

    item = inventory[inventory["ID"] == item_id]

    # Test Case 3: Item not found
    if item.empty:
        print(f"Item ID {item_id} not found.")
        return

    index = item.index[0]
    available_stock = int(inventory.loc[index, "Stock"])
    price = float(inventory.loc[index, "Price"])

    # Test Case 3: Insufficient stock
    if quantity > available_stock:
        print(f"Not enough stock. Available: {available_stock}")
        return

    # Calculate sale amount
    amount = quantity * price

    # Reduce stock
    remaining_stock = available_stock - quantity
    inventory.loc[index, "Stock"] = remaining_stock

    inventory.to_csv("inventory.csv", index=False)

    # Save sales record
    new_sale = pd.DataFrame([{
        "ID": item_id,
        "Quantity": quantity,
        "Amount": amount
    }])

    sales = pd.concat([sales, new_sale], ignore_index=True)
    sales.to_csv("sales.csv", index=False)

    print("Sale recorded.")
    print(f"Item: {inventory.loc[index, 'Name']}")
    print(f"Quantity Sold: {quantity}")
    print(f"Total Amount: {amount:g}")
    print(f"Remaining Stock: {remaining_stock}")


# 3. UPDATE ITEM
def update_item():
    inventory = pd.read_csv("inventory.csv")

    try:
        item_id = int(input("Enter Item ID to update: "))
    except ValueError:
        print("Invalid Item ID.")
        return

    item = inventory[inventory["ID"] == item_id]

    if item.empty:
        print(f"Item ID {item_id} not found.")
        return

    index = item.index[0]

    name = input("Enter new name: ").strip()

    try:
        stock = int(input("Enter new stock: "))
        price = float(input("Enter new price: "))

        if stock < 0 or price <= 0:
            print("Invalid stock or price.")
            return

    except ValueError:
        print("Please enter valid numbers.")
        return

    if name:
        inventory.loc[index, "Name"] = name

    inventory.loc[index, "Stock"] = stock
    inventory.loc[index, "Price"] = price

    inventory.to_csv("inventory.csv", index=False)

    print("Item updated successfully.")


# 4. DELETE ITEM
def delete_item():
    inventory = pd.read_csv("inventory.csv")

    try:
        item_id = int(input("Enter Item ID to delete: "))
    except ValueError:
        print("Invalid Item ID.")
        return

    if item_id not in inventory["ID"].values:
        print(f"Item ID {item_id} not found.")
        return

    inventory = inventory[inventory["ID"] != item_id]

    inventory.to_csv("inventory.csv", index=False)

    print("Item deleted successfully.")


# 5. SALES REPORT
def sales_report():
    inventory = pd.read_csv("inventory.csv")
    sales = pd.read_csv("sales.csv")

    print("\n===== SALES REPORT =====")

    if sales.empty:
        print("No sales recorded.")
        return

    # Group sales by Item ID
    report = sales.groupby("ID", as_index=False).agg({
        "Quantity": "sum",
        "Amount": "sum"
    })

    # Add item names
    report = pd.merge(
        report,
        inventory[["ID", "Name"]],
        on="ID",
        how="left"
    )

    # Display item-wise sales and revenue
    for _, row in report.iterrows():
        name = row["Name"] if pd.notna(row["Name"]) else "Unknown"
        quantity = int(row["Quantity"])
        revenue = float(row["Amount"])

        print(
            f"{name}: {quantity} units | Revenue: {revenue:g}"
        )

    # Calculate total revenue
    total_revenue = sales["Amount"].sum()

    print(f"Total revenue: {total_revenue:g}")

    # Find best-selling item
    best_seller = report.loc[report["Quantity"].idxmax()]

    best_name = (
        best_seller["Name"]
        if pd.notna(best_seller["Name"])
        else "Unknown"
    )

    best_quantity = int(best_seller["Quantity"])

    print(
        f"Best seller: {best_name} ({best_quantity} units)"
    )


# MAIN MENU
def main_menu():

    while True:
        print("\n===== INVENTORY + SALES MANAGEMENT SYSTEM =====")

        print("1. Add item")
        print("2. Sell")
        print("3. Update")
        print("4. Delete")
        print("5. Sales report")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_item()

        elif choice == "2":
            sell_item()

        elif choice == "3":
            update_item()

        elif choice == "4":
            delete_item()

        elif choice == "5":
            sales_report()

        elif choice == "0":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main_menu()