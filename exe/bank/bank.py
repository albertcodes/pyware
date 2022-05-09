import sqlite3, random, time, datetime
from datetime import datetime

now = datetime.now()

conn = sqlite3.connect("clients.sqlite3")
cursor = conn.cursor()

try:
    cursor.execute("create table client(created string, name text, type integer, account integer, balance money)")
except:
    pass
    
class Bank:
    # class variable
    bank_name = "Git Bank"
    
    # initialization
    def __init__(self, created, name, type, account, balance=0):
        self.created = created
        self.name = name # optional
        self.type = type
        self.account = account
        self.balance = balance
    
    def __str__(self):
        return "{}\'s Bank Account".format(self.name.capitalize())
    
    # save client
    def save(self):
        accounts = cursor.execute("select account from client")
        if (self.account,) not in accounts:
            cursor.execute("insert into client(created, name, type, account, balance) values(?, ?, ?, ?, ?)", [self.created, self.name, self.type, self.account, self.balance])
            conn.commit()
            print("\nAccount created and deposit sent to account.")
            
    
    # deposit
    def deposit(self, amount):
        cursor.execute("update client set balance = balance + ? where account = ?", [amount, self.account])
        conn.commit()
        
    # withdraw        
    def withdraw(self, amount):
        if self.balance >= amount:
            cursor.execute("update client set balance = balance - ? where account = ?", [amount, self.account])
        conn.commit()
        print("\nWithdrawal request successful\n")
        
    # view balance     
    def showBalance(self):
        bal = cursor.execute("select balance from client where account = ?",[self.account])
        for i in bal:
            return "\nYour account balance is KES {:,.2f}.".format(i[0])
    
    # transfer    
    def transfer(self, trans_to, amount):
        accounts = cursor.execute("select account from client")
        if self.balance >= amount and (trans_to,) in accounts and trans_to != self.account:
            cursor.execute("update client set balance = balance - ? where account = ?", [amount, self.account])
            cursor.execute("update client set balance = balance + ? where account = ?", [amount, trans_to])
            conn.commit()
        
# create new clients && save
#client = Bank(345608, "Joe", 9000);client.save()
#client2 = Bank(445691, "Jane", 4000);client2.save()

# client deposit
#client.deposit(1000)


# client withdraw
#client.withdraw(3000)

# client view balance
#print(client.showBalance()) # print to view

# client transfer money
#client2.transfer(345608, 2000) # client2 transfering 2000 to client with the account 345608


def launcher():
    print("Welcome To Git Bank\n\nSelect an option to proceed:\n1. Register\n2. Deposit\n3. Withdraw\n4. Transfer Money\n5. Check Balance\nq. Quit\n")
    endTime = time.time() + 600 # 10 minutes time
    while endTime > 0:
        option = input("Enter option: ")
        if option == "1":
            created = now.strftime("%d/%m/%Y")
            name = input("Enter first name: ")
            print("Account options:\n1. Current\n2. Savings\n")
            type = int(input("Choose account type [1/2] : "))
            init = int(input("Initial deposit amount: "))
            account = random.randint(100000, 999999)
            client = Bank(created, name, type, account, init)
            client.save()
            print("\n\tYour account number is {account}.")
            print("\n\tCreated on {created}.\n")

            # CALCULATE INTEREST BASED ON ACCOUNT TYPE:

            # while type == 1:
            #     if created.strftime("%m")-now.strftime("%m")>=1:
            #         intrest = balance*1/100
            #     else:
            #         intrest=0

            # while type == 2:
            #     if created.strftime("%m")-now.strftime("%m")>=1:
            #         intrest = balance * 3/100
            #     else:
            #         intrest=0
        
       
        elif option == "2":
            name = input("Enter first name: ")
            account = int(input("Enter account no.: "))
            amount = int(input("Enter amount: "))
            bal = cursor.execute("select balance from client where account = ?",[account])
            for i in bal:
                client = Bank(name, account, i[0]);client.deposit(amount)
            print("\nYour deposit has been received.\n")
        
        
        elif option == "3":
            name = input("Enter first name: ")
            account = int(input("Enter account no.: "))
            amount = int(input("Enter amount: "))
            bal = cursor.execute("select balance from client where account = ?",[account])
            for i in bal:
                client = Bank(name, account, i[0]);client.withdraw(amount)
            
            
        elif option == "4":
            name = input("Enter first name: ")
            trans_from = int(input("Enter your account no.: "))
            trans_to = int(input("Enter account no. to transfer money to: "))
            amount = int(input("Enter amount: "))
            bal = cursor.execute("select balance from client where account = ?",[trans_from])
            for i in bal:
                client = Bank(name, trans_from, i[0]);client.transfer(trans_to, amount)
            print("\nTransaction successful.\n")
        
        
        elif option == "5":
            name = input("Enter first name: ")
            account = int(input("Enter account no.: "))
            client = Bank(name, account)
            print(client.showBalance())
            
        elif option == "q":
            break
            
        elif option == "_a":
            print("\n\tClients Summary\n")
            data = cursor.execute("select * from client")
            for i in data:
                print("\tName: {}\tAccount No: {}\tBalance: KES {:,.2f}".format(i[0], i[1], i[2]))
            print()
        else:
            print("Invalid option\n")
            
        endTime -= 1
        
launcher()

#cursor.execute("delete from client");conn.commit()