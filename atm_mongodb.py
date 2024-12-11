import pymongo
import pwinput as p
from datetime import datetime

server = pymongo.MongoClient( "mongodb+srv://coderhoney915:coderhoney915@atm-cluster.1vgy1.mongodb.net/?ssl=true&ssl_ca_certs=/path/to/ca.pem&ssl_certfile=/path/to/cert.pem&ssl_keyfile=/path/to/key.pem")
mydb = server["atm_database"]
mycoll = mydb["accounts"]
mycoll1 = mydb["Transactions"]

def valid_account_number(account_number):
    """Helper function to validate account number length."""
    return len(str(account_number)) == 10

def valid_pin(pin):
    """Helper function to validate pin length."""
    return len(str(pin)) == 4

def registration():
    try:
        print()
        balance = 0
        account_holder_name = input("Enter account holder name:").upper()

        account_number = int(input("Enter account number:"))
        if valid_account_number(account_number):
            if mycoll.find_one({'Account-number': account_number}):
                print("...Account number must be unique. Please use another account number...")
            else:
                if mycoll.find_one({'Account-Holder-name': account_holder_name, 'Account-number': account_number, 'money': balance}):
                    print(f"...'{account_holder_name}' user already registered in the ATM...")
                else:
                    mycoll.insert_one({'Account-Holder-name': account_holder_name, 'Account-number': account_number, 'money': balance})
                    print("....Account was successfully registered....")
        else:
            print("....Account number must contain 10 digits....")
    except ValueError:
        print("...Account number must contain only digits...")
    except Exception as e:
        print(f"...Error: {str(e)}...")
    enquiry()

def generate_pin():
    try:
        print()
        account_holder_name = input("Enter account holder name:").upper()
        account_number = int(input("Enter account number:"))

        if valid_account_number(account_number):
            document = mycoll.find_one({'Account-Holder-name': account_holder_name, 'Account-number': account_number})
            if document:
                if 'pin' in document:
                    print("...Pin number was already generated for your account...")
                else:
                    pin_number1 = int(p.pwinput("Please enter the four-digit pin number: ", '*'))
                    if pin_number1 == 0000:
                        print("...Pin number must not be zero...")
                    elif valid_pin(pin_number1):
                        pin_number2 = int(p.pwinput("Re-enter the four-digit pin number: ", '*'))
                        if pin_number1 == pin_number2:
                            mycoll.update_one({'Account-Holder-name': account_holder_name, 'Account-number': account_number}, {'$set': {'pin': pin_number1}})
                            mycoll1.update_one({'Account-number': account_number}, {'$set': {'pin': pin_number1}})
                            print("...Pin was successfully generated for your account...")
                        else:
                            print("...Pin numbers must match. Please try again...")
                    else:
                        print("...Pin number must contain 4 digits...")
            else:
                print("...Account must be registered in the ATM...")
        else:
            print("...Account number must contain 10 digits...")
    except ValueError:
        print("...Account number and pin must contain only digits...")
    except Exception as e:
        print(f"...Error: {str(e)}...")
    enquiry()

def deposit():
    try:
        print()
        account_number = int(input("Enter account number:"))

        if valid_account_number(account_number):
            doc1 = mycoll.find_one({'Account-number': account_number})
            if doc1:
                pin = int(p.pwinput("Please enter the four-digit pin number: ", '*'))
                if valid_pin(pin):
                    if 'pin' in doc1:
                        account_data = mycoll.find_one({'$and': [{'Account-number': account_number}, {'pin': pin}]})
                        if account_data:
                            amount = int(input("Enter how much money do you want to deposit:"))
                            mycoll.update_one({'Account-number': account_number}, {'$inc': {'money': amount}})
                            print(f"...Your money 'Rs:{amount}' was successfully deposited into your account...")
                            create_transac_his(account_number, "deposit", amount, pin)
                        else:
                            print("...Invalid account number or pin. Please try again...")
                    else:
                        print("...Pin must be generated for the account first...")
                else:
                    print("...Pin number must contain 4 digits...")
            else:
                print("...Account not found. Please register first...")
        else:
            print("...Account number must contain 10 digits...")
    except ValueError:
        print("...Pin number must be a valid number...")
    except Exception as e:
        print(f"...Error: {str(e)}...")
    enquiry()

def create_transac_his(accno, trans_type, amount, pin):
    try:
        time = datetime.now().strftime("%Y:%D:%H:%M:%S")
        mycoll1.insert_one({'Account-number': accno, 'Transaction-Type': trans_type, 'Amount': amount, 'Time': time, 'pin': pin})
    except Exception as e:
        print(f"...Error creating transaction history: {str(e)}...")

def view_transac_his():
    try:
        print()
        account_number = int(input("Enter account number:"))
        if valid_account_number(account_number):
            doc = mycoll.find_one({'Account-number': account_number})
            if doc and 'pin' in doc:
                pin = int(p.pwinput("Enter your pin number: ", '*'))
                if valid_pin(pin):
                    if mycoll.find_one({'$and': [{'Account-number': account_number}, {'pin': pin}]}):
                        transactions = mycoll1.find({'Account-number': account_number}, {'Amount': 1, 'Time': 1, 'Transaction-Type': 1, '_id': 0})
                        for transaction in transactions:
                            print(transaction)
                    else:
                        print("...Invalid pin or account details...")
                else:
                    print("...Pin number must contain 4 digits...")
            else:
                print("...Pin not generated for the account...")
        else:
            print("...Account number must contain 10 digits...")
    except ValueError:
        print("...Account number and pin must be digits...")
    except Exception as e:
        print(f"...Error: {str(e)}...")
    enquiry()

def withdraw():
    try:
        print()
        account_number = int(input("Enter account number:"))
        if valid_account_number(account_number):
            doc1 = mycoll.find_one({'Account-number': account_number})
            if doc1:
                pin = int(p.pwinput("Please enter your pin number: ", '*'))
                if valid_pin(pin):
                    if 'pin' in doc1:
                        account_data = mycoll.find_one({'$and': [{'Account-number': account_number}, {'pin': pin}]})
                        if account_data:
                            amount = int(input("Enter the amount to withdraw:"))
                            if mycoll.find_one({'$and': [{'Account-number': account_number}, {'money': {'$gte': amount}}]}):
                                mycoll.update_one({'Account-number': account_number}, {'$inc': {'money': -amount}})
                                print(f"...Rs {amount} successfully withdrawn from your account...")
                                create_transac_his(account_number, "withdraw", amount, pin)
                            else:
                                print("...Insufficient funds...")
                        else:
                            print("...Invalid pin...")
                    else:
                        print("...Please generate a pin first...")
                else:
                    print("...Pin must contain 4 digits...")
            else:
                print("...Account not found...")
        else:
            print("...Account number must contain 10 digits...")
    except ValueError:
        print("...Invalid input. Please enter numeric values...")
    except Exception as e:
        print(f"...Error: {str(e)}...")
    enquiry()

def money_transfer():
    try:
        print()
        receiver_account_number = int(input("Enter RECEIVER'S account number:"))
        if valid_account_number(receiver_account_number):
            doc_receiver = mycoll.find_one({'Account-number': receiver_account_number})
            if doc_receiver:
                sender_account_number = int(input("Enter SENDER'S account number:"))
                if valid_account_number(sender_account_number):
                    doc_sender = mycoll.find_one({'Account-number': sender_account_number})
                    if doc_sender:
                        pin = int(p.pwinput("Enter your pin number: ", '*'))
                        if valid_pin(pin):
                            if mycoll.find_one({'$and': [{'Account-number': sender_account_number}, {'pin': pin}]}):
                                amount = int(input("Enter the amount to transfer:"))
                                if mycoll.find_one({'$and': [{'Account-number': sender_account_number}, {'money': {'$gte': amount}}]}):
                                    mycoll.update_one({'Account-number': receiver_account_number}, {'$inc': {'money': amount}})
                                    create_transac_his(receiver_account_number, "money transfer deposit", amount, pin)
                                    mycoll.update_one({'Account-number': sender_account_number}, {'$inc': {'money': -amount}})
                                    create_transac_his(sender_account_number, "money transfer withdrawal", amount, pin)
                                    print(f"...Rs {amount} was successfully transferred...")
                                else:
                                    print("...Insufficient funds in sender's account...")
                            else:
                                print("...Invalid pin for sender account...")
                        else:
                            print("...Invalid pin...")
                    else:
                        print("...Sender account not found...")
                else:
                    print("...Sender account must be registered...")
            else:
                print("...Receiver account not found...")
        else:
            print("...Receiver account number must contain 10 digits...")
    except ValueError:
        print("...Invalid input...")
    except Exception as e:
        print(f"...Error: {str(e)}...")
    enquiry()

def change_pin():
    try:
        choice = input("Do you want to change your PIN? (YES/NO):").strip().lower()
        if choice == 'yes':
            account_number = int(input("Enter your account number:"))
            if valid_account_number(account_number):
                doc1 = mycoll.find_one({'Account-number': account_number})
                if doc1:
                    old_pin = int(p.pwinput("Enter your old pin: ", '*'))
                    if valid_pin(old_pin):
                        if mycoll.find_one({'$and': [{'Account-number': account_number}, {'pin': old_pin}]}):
                            new_pin1 = int(p.pwinput("Enter your new pin: ", '*'))
                            if new_pin1 != 0000:
                                new_pin2 = int(p.pwinput("Re-enter your new pin: ", '*'))
                                if new_pin1 == new_pin2:
                                    mycoll.update_one({'Account-number': account_number}, {'$set': {'pin': new_pin1}})
                                    print("...Your pin was successfully changed...")
                                else:
                                    print("...Pins do not match. Please try again...")
                            else:
                                print("...Pin cannot be zero...")
                        else:
                            print("...Incorrect old pin...")
                    else:
                        print("...Pin must be 4 digits...")
                else:
                    print("...Account not found...")
            else:
                print("...Account number must be 10 digits...")
        elif choice == 'no':
            print("...Thank you for using ATM System...")
        else:
            print("...Please enter valid option (YES/NO)...")
    except ValueError:
        print("...Invalid input...")
    except Exception as e:
        print(f"...Error: {str(e)}...")
    enquiry()

def check_balance():
    try:
        print()
        account_number = int(input("Enter your account number:"))
        if valid_account_number(account_number):
            doc1 = mycoll.find_one({'Account-number': account_number})
            if doc1:
                pin = int(p.pwinput("Enter your pin number: ", '*'))
                if valid_pin(pin):
                    if mycoll.find_one({'$and': [{'Account-number': account_number}, {'pin': pin}]}):
                        balance = mycoll.find_one({'Account-number': account_number})['money']
                        print(f"Your balance is: Rs {balance}")
                    else:
                        print("...Invalid pin...")
                else:
                    print("...Pin number must contain 4 digits...")
            else:
                print("...Account not found...")
        else:
            print("...Account number must contain 10 digits...")
    except ValueError:
        print("...Account number and pin must contain only digits...")
    except Exception as e:
        print(f"...Error: {str(e)}...")
    enquiry()

def enquiry():
    try:
        print()
        q1 = input("Do you want to continue the process? (YES/NO):").strip().lower()
        if q1 == "yes":
            ATM()
        elif q1 == "no":
            print("*** Thank you for using ATM System ***")
            print("************* BYE ****************")
        else:
            print("...Please enter a valid choice...")
    except Exception as e:
        print(f"...Error: {str(e)}...")

def main():
    print("\n***** Welcome to ATM System *****")

def ATM():
    print()
    print(" (1) REGISTRATION                (2) PIN GENERATION ")
    print(" (3) DEPOSIT                     (4) WITHDRAW ")
    print(" (5) MONEY TRANSFER              (6) CHANGE PIN ")
    print(" (7) BALANCE ENQUIRY             (8) TRANSACTION HISTORY ")
    try:
        choice = int(input("Enter your choice to perform operation:"))
        if choice == 1:
            registration()
        elif choice == 2:
            generate_pin()
        elif choice == 3:
            deposit()
        elif choice == 4:
            withdraw()
        elif choice == 5:
            money_transfer()
        elif choice == 6:
            change_pin()
        elif choice == 7:
            check_balance()
        elif choice == 8:
            view_transac_his()
        else:
            print("...Please enter a valid choice...")
    except ValueError:
        print("...Invalid input. Please enter a valid number choice...")
    except Exception as e:
        print(f"...Error: {str(e)}...")

main()
ATM()
