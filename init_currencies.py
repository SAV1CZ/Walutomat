from database import SessionLocal
import requests
import models


CURRENCIES = ["PLN","USD","EUR","GBP","CHF","BRL","JPY","HKD","DKK","SEK"]


db = SessionLocal()
for x in CURRENCIES:
    check=db.query(models.AvaiableCurrencies).filter_by(Code=x).first()
    if not check:
        currency = models.AvaiableCurrencies(Code=x)
        db.add(currency)
db.commit()
db.close()

db = SessionLocal()
for x in CURRENCIES:
    base_currency = x
    for y in CURRENCIES:
        if y == x:
            continue
        target_currency = y
        url = f"https://api.frankfurter.app/latest?from={base_currency}&to={target_currency}"
        response = requests.get(url)
        if response.status_code == 200:

            
            data = response.json()
            exchange_rate = data["rates"][target_currency]
            check = db.query(models.CrossRate).filter_by(Base_currency=base_currency, Quote_currency=target_currency).first()
            if not check:
                pair = models.CrossRate(Base_currency=base_currency, Quote_currency=target_currency,Exchange_rate=exchange_rate)
                db.add(pair)


        else:
            print("Błąd pobierania danych z API.")
db.commit()
db.close()