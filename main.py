import json
from os import path
import random
import string
import pathlib


class Bank:
    database = "data.json"
    data = []

    try:
        if path.exists(database):
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("File not found")
    except Exception as err:
        print(f"An exception occurred: {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(cls.data, indent=4))

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*()", k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)

    def Createaccount(self):
        info = {
            "name": input("Enter your name :- "),
            "age": int(input("Enter your age :- ")),
            "email": input("Enter your email :- "),
            "pin": int(input("Enter your pin :- ")),
            "account number": Bank.__accountgenerate(),
            "balance": 0,
        }

        if info["age"] < 18:
            print("You are not eligible for creating an account")
        else:
            print("Your account has been created successfully")
            print("Please note down your account number :-", info["account number"])

            Bank.data.append(info)
            Bank.__update()

    def depositmoney(self):
        accnumber = input("please tell your account number ")
        pin = int(input("please tell your pin aswell "))

        userdata = [
            i for i in Bank.data if i["account number"] == accnumber and i["pin"] == pin
        ]

        if not userdata:
            print("sorry no data found")
        else:
            amount = int(input("how much you want to depoit "))
            if amount > 10000 or amount < 0:
                print(
                    "sorry the amount is too much you can deposit below 10000 and above 0"
                )

            else:
                userdata[0]["balance"] += amount
                Bank.__update()
                print("Amount deposited successfully ")

        amount = int(input("Enter the amount you want to deposit :- "))
        userdata[0]["balance"] += amount
        print(f"Your new balance is {userdata[0]['balance']}")
        Bank.__update()


print("press 1 for creating an account")
print("press 2 for Deposititing the money in the bank ")
print("press 3 for withdrawing the money ")
print("press 4 for details ")
print("press 5 for updating the details")
print("press 6 for deleting your account")

check = int(input("tell your response :- "))

if check == 1:
    user.Createaccount()

if check == 2:
    user.depositmoney()

if check == 3:
    user.withdrawmoney()

if check == 4:
    user.showdetails()

if check == 5:
    user.updatedetails()

if check == 6:
    user.Delete()
