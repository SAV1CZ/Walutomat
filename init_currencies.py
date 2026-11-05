import requests
from database import SessionLocal
import models

CURRENCIES = ["PLN", "USD", "EUR", "GBP", "CHF", "BRL", "JPY", "HKD", "DKK", "SEK"]

db = SessionLocal()

try:
    
    existing_currencies = {c.Code for c in db.query(models.AvaiableCurrencies.Code).all()}
    
    new_currencies_objects = [models.AvaiableCurrencies(Code=code)
    for code in CURRENCIES if code not in existing_currencies]

    
    if new_currencies_objects:
        db.add_all(new_currencies_objects)
        db.commit()

    
    all_pairs_to_add = []
    
    for base_currency in CURRENCIES:
        url = f"https://api.frankfurter.app/latest?from={base_currency}"
        response = requests.get(url)
        
        if response.status_code == 200:
            rates = response.json().get("rates", {})
            for target_currency, exchange_rate in rates.items():
                if target_currency in CURRENCIES:
                    all_pairs_to_add.append({
                        "Base_currency": base_currency,
                        "Quote_currency": target_currency,
                        "Exchange_rate": exchange_rate
                    })
        else:
            raise Exception(f"Błąd pobierania danych dla bazy: {base_currency}")


    existing_pairs = {(p.Base_currency, p.Quote_currency) for p in db.query(models.CrossRate).all()}
    
    new_pairs_objects = [
        models.CrossRate(
            Base_currency=pair["Base_currency"],
            Quote_currency=pair["Quote_currency"],
            Exchange_rate=pair["Exchange_rate"]
        )
        for pair in all_pairs_to_add
        if (pair["Base_currency"], pair["Quote_currency"]) not in existing_pairs
    ]

    if new_pairs_objects:
        db.add_all(new_pairs_objects)
        db.commit()
    else:
        print("Wszystkie kursy są już aktualne.")

except Exception as e:
    db.rollback()
    print(f"Wystąpił błąd podczas inicjalizacji: {e}")
finally:
    db.close()