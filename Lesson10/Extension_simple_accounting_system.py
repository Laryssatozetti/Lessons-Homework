class Manager:

    def __init__(self):
        self.balance = 0
        self.warehouse = {}
        self.operations = []
        self.actions = {}

    # -------- DECORATOR --------
    def assign(self, name):
        def decorator(func):
            self.actions[name] = func
            return func
        return decorator

    # -------- RUN --------
    def run(self):

        print("Available commands:")
        for cmd in self.actions:
            print(cmd)
        print("end")

        while True:
            command = input("Enter command: ")

            if command == "end":
                print("Program ended.")
                break

            elif command in self.actions:
                self.actions[command](self)  # passa self corretamente

            else:
                print("Unknown command.")

            print()

    # -------- REGISTER ACTIONS --------
    def register_actions(self):

        # -------- BALANCE --------
        @self.assign("balance")
        def balance_action(self):
            try:
                amount = float(input("Enter amount: "))
                self.balance += amount
                self.operations.append(f"BALANCE: {amount}")
                print("Current balance:", self.balance)
            except ValueError:
                print("Invalid number.")

        # -------- SALE --------
        @self.assign("sale")
        def sale_action(self):
            try:
                name = input("Product name: ")
                price = float(input("Price: "))
                quantity = int(input("Quantity: "))

                if name in self.warehouse and self.warehouse[name]["quantity"] >= quantity:
                    total = price * quantity
                    self.balance += total
                    self.warehouse[name]["quantity"] -= quantity

                    self.operations.append(f"SALE: {name}, qty={quantity}, total={total}")
                    print("Sale completed.")
                else:
                    print("Not enough product.")
            except ValueError:
                print("Invalid input.")

        # -------- PURCHASE --------
        @self.assign("purchase")
        def purchase_action(self):
            try:
                name = input("Product name: ")
                price = float(input("Price: "))
                quantity = int(input("Quantity: "))

                total = price * quantity

                if self.balance >= total:
                    self.balance -= total

                    if name in self.warehouse:
                        old_qty = self.warehouse[name]["quantity"]
                        old_price = self.warehouse[name]["price"]

                        # média ponderada do preço
                        new_price = ((old_price * old_qty) + (price * quantity)) / (old_qty + quantity)

                        self.warehouse[name]["price"] = new_price
                        self.warehouse[name]["quantity"] += quantity
                    else:
                        self.warehouse[name] = {
                            "price": price,
                            "quantity": quantity
                        }

                    self.operations.append(f"PURCHASE: {name}, qty={quantity}, total={total}")
                    print("Purchase completed.")
                else:
                    print("Not enough money.")
            except ValueError:
                print("Invalid input.")

        # -------- ACCOUNT --------
        @self.assign("account")
        def account_action(self):
            print("Current balance:", self.balance)

        # -------- LIST --------
        @self.assign("list")
        def list_action(self):
            if not self.warehouse:
                print("Warehouse empty.")
            else:
                for product in self.warehouse:
                    print(product,
                          "price:", self.warehouse[product]["price"],
                          "quantity:", self.warehouse[product]["quantity"])

        # -------- WAREHOUSE --------
        @self.assign("warehouse")
        def warehouse_action(self):
            name = input("Product name: ")
            if name in self.warehouse:
                print(name,
                      "price:", self.warehouse[name]["price"],
                      "quantity:", self.warehouse[name]["quantity"])
            else:
                print("Product not found.")

        # -------- REVIEW --------
        @self.assign("review")
        def review_action(self):
            start = input("From: ")
            end = input("To: ")

            if start == "" and end == "":
                for op in self.operations:
                    print(op)
            else:
                try:
                    start = int(start)
                    end = int(end)

                    if start < 0 or end >= len(self.operations) or start > end:
                        print("Out of range.")
                    else:
                        for i in range(start, end + 1):
                            print(self.operations[i])
                except ValueError:
                    print("Invalid range.")


# -------- MAIN --------
if __name__ == "__main__":
    manager = Manager()
    manager.register_actions()
    manager.run()