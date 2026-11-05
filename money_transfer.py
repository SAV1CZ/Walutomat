from decimal import Decimal, ROUND_FLOOR
from database import SessionLocal
import models

def exchange(base, quote, amount_of_base, From, To):
    db = SessionLocal()
    margin = Decimal("0.997")
    amount = Decimal(amount_of_base)
    
    try:

        source_wallet = db.query(models.Wallet).filter_by(id=From, currency=base).with_for_update().first()
        if not source_wallet:
            raise ValueError(f"Wallet source ID {From} for {base} not found.")
        if source_wallet.balance < amount:
            raise ValueError("Not enough money to complete operation.")

        
        destination_wallet = db.query(models.Wallet).filter_by(id=To, currency=quote).first()
        if not destination_wallet:
            raise ValueError(f"Wallet destination ID {To} for {quote} not found.")
            
        
        pair = db.query(models.CrossRate).filter_by(Base_currency=base, Quote_currency=quote).first()
        if not pair:
            raise ValueError(f"Exchange rate for {base} -> {quote} not available.")
            
        ratio = pair.Exchange_rate
        clients_part = amount * ratio * margin
        client_receive = clients_part.quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
        real = amount * ratio
        profit = real - client_receive
        
        
        source_wallet.balance -= amount
        destination_wallet.balance += client_receive
        
        walutomat = db.query(models.AvaiableCurrencies).filter_by(Code=quote).first()
        if walutomat:
            walutomat.Walutomat_balance += profit
            transaction = models.Transaction(Source=From, Destination=To, Amount=amount, Transaction_Currency=base)
            db.add(transaction)
            db.commit()
        
    except Exception as e:
        db.rollback()
        raise e
        
    finally:
        db.close()








exchange("SEK", "EUR",5000, 1, 2)