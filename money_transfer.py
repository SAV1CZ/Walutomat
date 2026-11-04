from database import SessionLocal
import models
from decimal import Decimal, ROUND_FLOOR

def exchange(base, quote, amount_of_base, From, To):

    db = SessionLocal()
    margin = Decimal(0.997)
    amount = Decimal(amount_of_base)
    source_wallet = db.query(models.Wallet).filter_by(id=From, currency=base).first()
    if not source_wallet:
        raise Exception(f"{base} Wallet not found")
    if source_wallet.balance < amount:
        raise Exception(f"Not enought money to complete operation")
    destination_wallet = db.query(models.Wallet).filter_by(id=To,currency=quote).first()
    if not destination_wallet:
        raise Exception(f"{quote} Wallet not found")
    source_wallet.balance -= amount
    
    try:

        pair = db.query(models.CrossRate).filter_by(Base_currency=base, Quote_currency=quote).first()
        ratio = pair.Exchange_rate
        clients_part = amount * ratio * margin
        client_recive = clients_part.quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
        real = amount * ratio
        profit = real - client_recive
        destination_wallet.balance += client_recive

        walutomat = db.query(models.AvaiableCurrencies).filter_by(Code=quote).first()
        walutomat.Walutomat_balance += profit
        transaction = models.Transaction(Source = From, Destination = To, Amount = amount, Transaction_Currency = base)

        db.add(transaction)
        db.commit()
        db.close()

    
    except Exception as e:
        source_wallet.balance += amount
        db.commit()
        db.close()
        print (e)









exchange("SEK", "EUR",5000, 1, 2)