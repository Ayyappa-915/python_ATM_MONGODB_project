import pymongo
server=pymongo.MongoClient("mongodb://localhost:27017")
mydb=server["atm_database"]
mycoll=mydb["accounts"]
mycoll1=mydb["Transactions"]
def registration():
    print()
    balance=0
    a=input("Enter account holder name:")
    account_holder_name=a.upper()
    try:
        account_number=int(input("Enter account number:"))
        x=str(account_number)
        if len(x) == 10:
            q1=mycoll.find_one({'Account-number':{'$eq':account_number}})
            if q1:
                print("... Account number must be unique.Please use another account number ...")
            else:
                choice=mycoll.find_one({'Account-Holder-name':account_holder_name , 'Account-number': account_number ,'money':balance})
                if choice:
                    print("... '{0}' user already registered in the ATM...".format(account_holder_name))
                else:
                    mycoll.insert_one({'Account-Holder-name':account_holder_name , 'Account-number':account_number , 'money':balance })
                    print("....Account was successfully registered....")
        else:
            print("....Account number must contain 10 digits....")
    except:
        print("...Account number must contain only digits...")
    enquiry()
def generate_pin():
    import pwinput as p
    print()
    a=input("Enter account holder name:")
    account_holder_name=a.upper()
    account_number=int(input("Enter account number:"))
    try:
        x=str(account_number)
        if len(x) == 10:
            z=mycoll.find_one({'$and':[{'Account-Holder-name':{'$eq':account_holder_name}},{'Account-number':{'$eq':account_number}}]})
            if z:
                q1='pin'
                document=mycoll.find_one({'Account-number':account_number})
                if q1 in document:
                    print("... Pin number was already generated for your account ...")
                else:
                    choice=mycoll.find_one({'$and':[{'Account-Holder-name':{'$eq':account_holder_name}},{'Account-number':{'$eq':account_number}}] })
                    if choice:
                        try:
                            pin_number1=int(p.pwinput("Please enter the four digit pin number :" ,'*' ))
                            if pin_number1==0000:
                                print("...pin number not be zero...")
                            x1=str(pin_number1)
                            if len(x1) == 4:
                                pin_number2=int(p.pwinput("Re-enter the four digit pin number :" ,'*' ))
                                if pin_number1 == pin_number2:
                                    pin_number=pin_number1
                                    mycoll.update_one({'Account-Holder-name':account_holder_name , 'Account-number':account_number},{'$set':{'pin':pin_number}})
                                    mycoll1.update_one({'Account-number':account_number},{'$set':{'pin':pin_number}})
                                    print("... Pin was successfully generated for your account ...")
                                else:
                                    print(" ...pin number should be matched. please Try again ...")
                            else:
                                print("... Pin number must contain 4 digits ...")
                        except:
                            print("...Pin number must contain only digits...")
                    else:
                        print("...Please enter valid Account and Pin number details...")
            else:
                print("...Account user must be Registered in the ATM...")
        else:
            print("...Account number must contain 10 digits...")
    except:
        print("...Account number must contain only digits...")
    enquiry()
def deposit():
    import pwinput as p
    print()
    try:
        account_number=int(input("Enter account number:"))
        x=str(account_number)
        if len(x) == 10:
            doc1=mycoll.find_one({'Account-number':{'$eq':account_number}})
            if doc1:
                try:
                    p1=int(p.pwinput("Please enter the four digit pin number :" ,'*' ))
                    if p1 == 0000:
                        print("...Pin number must not be zero...")
                    s=str(p1)
                    if len(s) == 4:
                        q1='pin'
                        document=mycoll.find_one({'Account-number':account_number})
                        if q1 in document:
                            query1=mycoll.find_one({'$and':[{'Account-number':{'$eq':account_number}},{'pin':{'$eq':p1}}]})
                            if query1:
                                amount=int(input("Enter how much money do you want to deposit:"))
                                mycoll.update_one({'Account-number':account_number},{'$inc':{'money':amount}})
                                print(f" ...Your money 'Rs:{amount}' was successfully deposited into your account ...")
                                create_transac_his(account_number,"deposit",amount,p1)
                            else:
                                print(" ...Please Enter valid Account number or Pin number...")
                        else:
                            print(" ...User must be generate Pin number for the Account ...")
                    else:
                        print("...Pin number must contain 4 digits...")
                except:
                    print("...Pin number must contain only digits...")
            else:
                print(" ...User must be register in the ATM system ...")
        else:
            print("...Account number must contain 10 digits...")
    except:
        print("...Account number must contain only digits...")
    enquiry()
def create_transac_his(accno,trans_type,amount,pwd):
    from datetime import datetime
    account_number=accno
    transaction_type=trans_type
    amt=amount
    time=datetime.now()
    pin=pwd
    t=time.strftime("%Y:%D:%H:%M:%S")
    mycoll1.insert_one({'Account-number':account_number , 'Transaction-Type':transaction_type , 'Amount':amt , 'Time':t , 'pin':pwd})
def view_transac_his():
    print()
    import pwinput as p
    try:
        accno=int(input("Enter Account number:"))
    except:
        print("...Account number must contain only digits...")
    x=str(accno)
    if len(x) == 10:
        z='pin'
        document=mycoll.find_one({'Account-number':{'$eq':accno}})
        if z in document:
            try:
                p1=int(p.pwinput("Please enter the four digit pin number :" ,'*' ))
            except:
                print("...PIN number must contain only digits...")
            y=str(p1)
            if len(y) == 4:
                q1=mycoll.find_one({'$and':[{'Account-number':{'$eq':accno}},{'pin':{'$eq':p1}}]})
                if q1:
                    q2=mycoll1.find({'Account-number':{'$eq':accno}},{'Amount':1,'Time':1,'Transaction-Type':1,'_id':0})
                    for a in q2:
                        print(a)
                else:
                    print("...Enter valid Account and PIN details...")
            else:
                print("...PIN number contain only 4 digits...")
        else:
            print("...User must generate PIN for the Account...")
    else:
        print("...Account number must contain 10 digits...")
    enquiry()
def withdraw():
    import pwinput as p
    print()
    try:
        account_number=int(input("Enter account number:"))
        x=str(account_number)
        if len(x) == 10:
            doc1=mycoll.find_one({'Account-number':{'$eq':account_number}})
            if doc1:
                try:
                    p1=int(p.pwinput("Please enter the four digit pin number :" ,'*' ))
                    if p1 == 0000:
                        print("...Pin number must not be zero...")
                    s=str(p1)
                    if len(s) == 4:
                        q1='pin'
                        document=mycoll.find_one({'Account-number':account_number})
                        if q1 in document:
                            query1=mycoll.find_one({'$and':[{'Account-number':{'$eq':account_number}},{'pin':{'$eq':p1}}]})
                            if query1:
                                amount=int(input("Enter how much money do you want to withdraw:"))
                                z=mycoll.find_one({'$and':[{'Account-number':{'$eq':account_number}} , {'money':{'$gt':amount}}]})
                                if z:
                                    mycoll.update_one({'Account-number':account_number},{'$inc':{'money':-amount}})
                                    print(f" ...Your money 'Rs:{amount}' was successfully  withdrawn from your account ...")
                                    create_transac_his(account_number,"withdraw",amount,p1)
                                else:
                                    print("...Insufficient funds are available in your account...")
                            else:
                                print(" ...Please Enter valid Account number or Pin number...")
                        else:
                            print(" ...User must be generate Pin number for the Account ...")
                    else:
                        print("...Pin number must contain 4 digits...")  
                except:
                    print("...Pin number must contain only digits...")
            else:
                print(" ...User must be register in the ATM system ...")
        else:
            print("...Account number must contain 10 digits...")
    except:
        print("...Account number must contain only digits...")
    enquiry()
def money_transfer():
    print()
    import pwinput as p
    try:
        receiver_account_number=int(input("Enter RECEIVER'S account number:"))
    except:
        print("...Account number must contain only digits...")
    x=str(receiver_account_number)
    if len(x) == 10:
        doc1=mycoll.find_one({'Account-number':{'$eq':receiver_account_number}})
        if doc1:
            try:
                sender_account_number=int(input("Enter SENDER'S account number:"))
            except:
                print("...Account number must contain only digits...")
            y=str(sender_account_number)
            if len(y) == 10:
                doc2=mycoll.find_one({'Account-number':{'$eq':sender_account_number}})
                if doc2:
                    try:
                        p1=int(p.pwinput("Enter four digit Pin number:" , '*'))
                    except:
                        print("...PIN number must contain only digits...")
                    if p1 == 0000:
                        print("...Pin number must not be zero...")
                    else:
                        z=str(p1)
                        if len(z) == 4:
                            q1='pin'
                            document=mycoll.find_one({'Account-number':sender_account_number})
                            if q1 in document:
                                query1=mycoll.find_one({'$and':[{'Account-number':{'$eq':sender_account_number}},{'pin':{'$eq':p1}}]})
                                if query1:
                                    amount=int(input("Enter how much money do you want to transfer :"))
                                    z=mycoll.find_one({'$and':[{'Account-number':{'$eq':sender_account_number}} , {'money':{'$gt':amount}}]})
                                    if z:
                                        mycoll.update_one({'Account-number':receiver_account_number},{'$inc':{'money':amount}})
                                        create_transac_his(receiver_account_number,"money transfer deposit",amount,p1)
                                        mycoll.update_one({'Account-number':sender_account_number},{'$inc':{'money': -amount}})
                                        create_transac_his(sender_account_number,"money transfer withdrawl",amount,p1)
                                        print(f"...your money was RS:{amount} was successfully transfered from your ")
                                    else:
                                        print("...Insufficient funds are available in SENDER'S account...")
                                else:
                                    print(" ...Please enter valid Account number or Pin number ...")
                            else:
                                print("...SENDER must generate PIN number number for the account...")
                        else:
                            print("...PIN number must contain 4 digits")
                else:
                    print("...SENDER must register in the ATM system")
            else:
                print("...Account number must contain 10 digits...")
        else:
            print("...RECEIVER must register in the ATM system...")
    else:
        print("...Account number must contain 10 digits...")
    enquiry()
def change_pin():
    import pwinput as p
    r1="yes"
    r2="YES"
    r3="NO"
    r4="no"
    print()
    choice=input("Are you want to change Pin for your account ? (YES/NO):")
    if choice ==r1 or choice ==r2:
        try:
            account_number=int(input("Enter your Account number:"))
            x=str(account_number)
            if len(x) == 10:
                doc1=mycoll.find_one({'Account-number':{'$eq':account_number}})
                if doc1:
                    try:
                        p1=int(p.pwinput("Enter old Pin number :" , '*'))
                        s=str(p1)
                        if len(s) == 4:
                            q1='pin'
                            document=mycoll.find_one({'Account-number':account_number})
                            if q1 in document:
                                query1=mycoll.find_one({'$and':[{'Account-number':{'$eq':account_number}},{'pin':{'$eq':p1}}]})
                                if query1:
                                    try:
                                        pin_number1=int(p.pwinput("Enter a new Pin number :" , '*'))
                                        if pin_number1==0000:
                                            print("...Pin number must not be zero...")
                                        pin_number2=int(p.pwinput("Re-enter a new Pin number :" , '*'))
                                        if pin_number1 == pin_number2:
                                            pin_number=pin_number1
                                            mycoll.update_one({'Account-number':account_number},{'$set':{'pin':pin_number}})
                                            print(" ...Pin was successfully changed for your account ...")
                                        else:
                                            print(" ...pin number should be matched. please Try again ...")
                                    except:
                                        print("...Pin number must contain only digits...")
                                else:
                                    print("...Please enter valid Account number and pin number details...")
                            else:
                                print("...User must be generate Pin number for the account...")
                        else:
                            print("...Pin number must contain 4 digits...")
                    except:
                        print("...Pin number must contain only digits...")
                else:
                    print("...User must be registered in the ATM system...")
            else:
                print("...Account number must contain 10 digits...")
        except:
            print("...Account number must contain only digits...")
    elif choice == r3 or choice == r4:
        print("...Thank you...")
    else:
        print("...Please choose valid option...")
    enquiry()
def check_balance():
    import pwinput as p
    print()
    try:
        account_number=int(input("Enter your account number:"))
        x=str(account_number)
        if len(x) == 10:
            doc1=mycoll.find_one({'Account-number':{'$eq':account_number}})
            if doc1:
                p1=int(p.pwinput("Enter four digit Pin number:" , '*'))
                if p1 ==0000:
                    print("...Pin number must not be zero...")
                s=str(p1)
                if len(s) == 4:
                    q1='pin'
                    document=mycoll.find_one({'Account-number':account_number})
                    if q1 in document:
                        query1=mycoll.find_one({'$and':[{'Account-number':{'$eq':account_number}},{'pin':{'$eq':p1}}]})
                        if query1:
                            query2=mycoll.find({'Account-number':{'$eq':account_number}},{'money':1,'_id':0})
                            print("....Balance amount in your Account is:")
                            for x in query2:
                                print(x)
                        else:
                            print(" ...Please enter valid Account number or Pin number ...")
                    else:
                        print(" ...User must be generate Pin number for the Account ...")
                else:
                    print("...Pin number must contain 4 digits...")
            else:
                print(" ...User must be register in the ATM system ...")
        else:
            print("...Account number must contain 10 digits...")
    except:
        print("...Account number must contain only digits...")
    enquiry()
def enquiry():
    print()
    q1=input("Are you want to continue the process ? (YES/NO) :")
    if q1.lower()=="yes":
        ATM()
    elif q1.lower() == "no":
        print()
        print("*** Thank For Using ATM System ***")
        print("************* BYE ****************")
    else:
        print("...Please enter valid choice...")
def main():
    print()
    print("***** welcome to ATM system *****")
def ATM():
    print()
    print(" (1) REGISTRATION                (2) PIN GENERATION ")
    print(" (3) DEPOSIT                     (4) WITHDRAW ")
    print(" (5) MONEY TRANSFER              (6) CHANGE PIN ")
    print(" (7) BALANCE ENQUIRY             (8) TRANSACTION HISTORY ")
    print()
    try:
        choice=int(input("Enter your choice to perform operation:"))
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
    except:
        print("...Please enter valid choice...")
main()
ATM()