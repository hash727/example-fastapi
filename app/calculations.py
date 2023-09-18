
def add(num1, num2):
    return num1 + num2


class Bankaccount():
    def __init__(self, starting_balance = 0):
        self.balance = starting_balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficiant Funds")
        self.balance -= amount
    
    def interest(self):
        self.balance *= 1.1
        