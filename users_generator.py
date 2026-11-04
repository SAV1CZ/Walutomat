import random
from faker import Faker
from database import SessionLocal
from models import Person, Wallet 

fake = Faker()


COUNTRIES_CURRENCIES = {
    "Poland":"PLN", "Germany":"EUR", "UK":"GBP", "USA":"USD", "Canada":"USD", "France":"EUR",
    "Spain":"EUR", "Italy":"EUR", "Japan":"JPY", "Switzerland":"CHF", "Brazil":"BRL", "Mexico":"USD",
    "Sweden":"SEK", "Hongkong":"HKD", "Austria":"EUR", "Croatia":"EUR", "Turkey":"EUR",
    "Czech Republic":"EUR","Denmark":"DKK", "Portugal":"EUR"
}

COUNTRIES_WEIGHTS = [25, 5, 7, 10, 3, 4, 4, 2, 1, 1, 6, 2, 7, 7, 2, 1, 3, 2, 6, 2]

ALLOWED_CURRENCIES = {"PLN":8, "USD":30, "EUR":20, "GBP":6, "CHF":9,"BRL":4, "HKD":13, "JPY":7, "DKK":2,"SEK":1 }

ANOTHER_CURRENCY = ["Y","N"]
ANOTHER_CURRENCY_WEIGHTS = [15,85]

BANNED = []

def generate_test_users(db_session, num_users=5000):
    print(f"Rozpoczynam generowanie {num_users} sztucznych kont z restrykcjami...")
    
    for _ in range(num_users):
    
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 999)}@test.com"
        while email in BANNED:
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1000, 9999)}@test.com"
        BANNED.append(email)




        country = random.choices(list(COUNTRIES_CURRENCIES.keys()), weights=COUNTRIES_WEIGHTS, k=1)[0]

        db_user = Person(email=email, first_name=first_name, last_name=last_name, location=country)
        db_session.add(db_user)
        db_session.flush()  

        
        asigned_currency = COUNTRIES_CURRENCIES[country]
        currency_weight = ALLOWED_CURRENCIES.get(asigned_currency)
        user_currencies = [asigned_currency]
        user_currencies_weights = [currency_weight]

        
        initial_balance = round(random.uniform(50.0, 30000.0), 2) 
        db_wallet = Wallet(owner=db_user.id, currency=asigned_currency, balance=initial_balance)
        db_session.add(db_wallet)




        available_for_second = [c for c in ALLOWED_CURRENCIES if c not in user_currencies]
        avaiable_currency_weight =[w for w in ALLOWED_CURRENCIES.values() if w not in user_currencies_weights]
        second_currency = random.choices(available_for_second, weights=avaiable_currency_weight, k=1)[0]
        second_currency_weight = ALLOWED_CURRENCIES.get(second_currency)

        user_currencies.append(second_currency)
        user_currencies_weights.append(second_currency_weight)

        second_wallet = Wallet(owner=db_user.id, currency=second_currency, balance=0)
        db_session.add(second_wallet)




        another_currency = random.choices(ANOTHER_CURRENCY, weights=ANOTHER_CURRENCY_WEIGHTS, k=1)[0]
        if another_currency == "Y":
            available_for_third = [c for c in ALLOWED_CURRENCIES if c not in user_currencies]
            avaiable_currency_weight_for_third = [w for w in ALLOWED_CURRENCIES.values() if w not in user_currencies_weights]
            if available_for_third:
                third_currency = random.choices(available_for_third, weights=avaiable_currency_weight_for_third, k=1)[0]
                third_wallet = Wallet(owner=db_user.id, currency=third_currency, balance=0)
                db_session.add(third_wallet)

    
    db_session.commit()
    print("Generator zakończył pracę! Baza danych została zasilona.")


session = SessionLocal()
generate_test_users(session)