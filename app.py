import json
import random
import string
from pathlib import Path

import streamlit as st


class Bank:
    DATABASE = "data.json"

    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        file = Path(self.DATABASE)

        if file.exists():
            try:
                with open(file, "r") as fs:
                    return json.load(fs)
            except json.JSONDecodeError:
                return []

        return []

    def update(self):
        with open(self.DATABASE, "w") as fs:
            json.dump(self.data, fs, indent=4)

    def accountgenerate(self):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*()", k=1)

        account_id = alpha + num + spchar
        random.shuffle(account_id)

        return "".join(account_id)

    def create_account(self, name, age, email, pin):
        account_number = self.accountgenerate()

        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account number": account_number,
            "balance": 0,
        }

        self.data.append(info)
        self.update()

        return account_number

    def find_user(self, account_number, pin):
        account_number = str(account_number).strip()
        pin = int(pin)

        for user in self.data:
            if (str(user["account number"]).strip() == account_number) and (
                user["pin"] == pin
            ):
                return user

        return None

    def deposit_money(self, account_number, pin, amount):
        user = self.find_user(account_number, pin)

        if user is None:
            return False, "Account number or PIN is incorrect."

        if amount <= 0:
            return False, "Amount must be greater than 0."

        if amount > 10000:
            return False, "You can deposit a maximum of 10000."

        user["balance"] += amount
        self.update()

        return True, "Amount deposited successfully."

    def withdraw_money(self, account_number, pin, amount):
        user = self.find_user(account_number, pin)

        if user is None:
            return False, "Account number or PIN is incorrect."

        if amount <= 0:
            return False, "Amount must be greater than 0."

        if user["balance"] < amount:
            return False, "Insufficient balance."

        user["balance"] -= amount
        self.update()

        return True, "Amount withdrawn successfully."

    def get_details(self, account_number, pin):
        return self.find_user(account_number, pin)

    def update_details(self, account_number, pin, name, age, email, new_pin):
        user = self.find_user(account_number, pin)

        if user is None:
            return False, "Account number or PIN is incorrect."

        user["name"] = name
        user["age"] = age
        user["email"] = email

        if new_pin:
            user["pin"] = new_pin

        self.update()

        return True, "Your details have been updated successfully."

    def delete_account(self, account_number, pin):
        user = self.find_user(account_number, pin)

        if user is None:
            return False, "Account number or PIN is incorrect."

        self.data.remove(user)
        self.update()

        return True, "Account deleted successfully."


bank = Bank()


st.set_page_config(
    page_title="Bank Management System", page_icon="🏦", layout="centered"
)


st.title("🏦 Bank Management System")
st.write("Manage your bank account easily.")


menu = st.sidebar.selectbox(
    "Select an option",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Account Details",
        "Update Details",
        "Delete Account",
    ],
)


if menu == "Create Account":

    st.header("Create New Account")

    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=1, max_value=120, step=1)
    email = st.text_input("Enter your email")
    pin = st.number_input("Enter your PIN", min_value=1000, max_value=9999, step=1)

    if st.button("Create Account"):

        if not name:
            st.error("Please enter your name.")

        elif not email:
            st.error("Please enter your email.")

        elif age < 18:
            st.error("You are not eligible for creating an account.")

        else:
            account_number = bank.create_account(name, int(age), email, int(pin))

            st.success("Your account has been created successfully.")

            st.info(f"Your account number is: {account_number}")


elif menu == "Deposit Money":

    st.header("Deposit Money")

    account_number = st.text_input("Account Number")
    pin = st.number_input("PIN", min_value=1000, max_value=9999, step=1)
    amount = st.number_input("Deposit Amount", min_value=0, step=1)

    if st.button("Deposit"):

        success, message = bank.deposit_money(account_number, int(pin), int(amount))

        if success:
            st.success(message)
        else:
            st.error(message)


elif menu == "Withdraw Money":

    st.header("Withdraw Money")

    account_number = st.text_input("Account Number")
    pin = st.number_input("PIN", min_value=1000, max_value=9999, step=1)
    amount = st.number_input("Withdrawal Amount", min_value=0, step=1)

    if st.button("Withdraw"):

        success, message = bank.withdraw_money(account_number, int(pin), int(amount))

        if success:
            st.success(message)
        else:
            st.error(message)


elif menu == "Account Details":

    st.header("Account Details")

    account_number = st.text_input("Account Number")
    pin = st.number_input("PIN", min_value=1000, max_value=9999, step=1)

    if st.button("Show Details"):

        user = bank.get_details(account_number, int(pin))

        if user is None:
            st.error("No account found.")

        else:
            st.write("### Your Details")

            st.write(f"**Name:** {user['name']}")
            st.write(f"**Age:** {user['age']}")
            st.write(f"**Email:** {user['email']}")
            st.write(f"**Account Number:** {user['account number']}")
            st.write(f"**Balance:** {user['balance']}")


elif menu == "Update Details":

    st.header("Update Account Details")

    account_number = st.text_input("Account Number")
    pin = st.number_input("Current PIN", min_value=1000, max_value=9999, step=1)

    name = st.text_input("New Name")
    age = st.number_input("New Age", min_value=18, max_value=120, step=1)
    email = st.text_input("New Email")

    new_pin = st.text_input("New PIN (optional)", type="password")

    if st.button("Update Details"):

        if not name or not email:
            st.error("Name and email cannot be empty.")

        elif new_pin and (not new_pin.isdigit() or len(new_pin) != 4):
            st.error("PIN must contain exactly 4 digits.")

        else:
            success, message = bank.update_details(
                account_number,
                int(pin),
                name,
                int(age),
                email,
                int(new_pin) if new_pin else None,
            )

            if success:
                st.success(message)
            else:
                st.error(message)

elif menu == "Delete Account":

    st.header(" Delete Account")

    account_number = st.text_input("Account Number", placeholder="Example: D1S10!f")

    pin = st.text_input("PIN", type="password", placeholder="Enter your 4-digit PIN")

    confirmation = st.checkbox(
        "I understand that deleting my account cannot be undone."
    )

    if st.button("Delete Account"):

        if not account_number:
            st.warning("Please enter your account number.")

        elif not pin:
            st.warning("Please enter your PIN.")

        elif not pin.isdigit() or len(pin) != 4:
            st.error("PIN must contain exactly 4 digits.")

        elif not confirmation:
            st.warning("Please confirm account deletion.")

        else:
            success, message = bank.delete_account(account_number, int(pin))

            if success:
                st.success(message)
                st.info("Your account has been deleted successfully.")

            else:
                st.error(message)
