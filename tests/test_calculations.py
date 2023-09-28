import pytest
from app.calculations import add, Bankaccount

@pytest.fixture
def zero_deposit_account():
    print("Commit this first")
    return Bankaccount()

@pytest.fixture
def initial_deposit_account():
    return Bankaccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (5, 3, 8),
    (6, 3, 9),
    (2, 5, 7)
])

def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_bank_account_starting_balance(zero_deposit_account):
    #bank_account = Bankaccount()
    print("initialized access")
    assert zero_deposit_account.balance == 0

def test_bank_initial_amount(initial_deposit_account):
    #bank_account = Bankaccount(50)
    assert initial_deposit_account.balance == 50

def test_deposits(initial_deposit_account):
    #bank_account = Bankaccount(50)
    initial_deposit_account.deposit(30)
    assert initial_deposit_account.balance == 80
    
def test_withdraw(initial_deposit_account):
    #bank_account = Bankaccount(50)
    initial_deposit_account.withdraw(20)
    assert initial_deposit_account.balance == 30

def test_interest(initial_deposit_account):
    #bank_account = Bankaccount(50)
    initial_deposit_account.interest()
    assert round(initial_deposit_account.balance,5) == 55

def test_transaction(zero_deposit_account):
    zero_deposit_account.deposit(200)
    zero_deposit_account.withdraw(100)
    assert zero_deposit_account.balance == 100
    
@pytest.mark.parametrize("deposited, withdrew, expected",[
    (200, 100, 100),
    (80, 20, 60),
    (1500, 300, 1200)
])
def test_trans_para(zero_deposit_account, deposited, withdrew, expected):
    zero_deposit_account.deposit(deposited)
    zero_deposit_account.withdraw(withdrew)
    assert zero_deposit_account.balance == expected
    
def test_funds_exception(initial_deposit_account):
    with pytest.raises(Exception):
        initial_deposit_account.withdraw(200)
    