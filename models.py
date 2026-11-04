from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from database import Base, engine
from zoneinfo import ZoneInfo
import datetime



class Person(Base):

    __tablename__ = "Person"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    location = Column(String, nullable=False)

    Person_rel = relationship("Wallet", back_populates="Wallet_rel")

    def person_full_name():
        return (Person.first_name, Person.last_name)



class Wallet(Base):

    __tablename__ = "Wallet"
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(3), index = True, nullable=False)
    owner = Column(Integer, ForeignKey("Person.id"))
    balance = Column(Numeric(9,2))

    Wallet_rel = relationship("Person", back_populates="Person_rel")

    Wallet_Source_rel = relationship("Transaction",
        foreign_keys="Transaction.Source",
        back_populates="Source_rel")
    
    Wallet_Destination_rel = relationship("Transaction",
        foreign_keys="Transaction.Destination",
        back_populates="Destination_rel")



class AvaiableCurrencies(Base):

    __tablename__ = "AvaiableCurrencies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(3), unique=True, nullable=False)
    Walutomat_balance = Column(Numeric(12,4), default=0)

    AvaiableCurrencies_Base_rel = relationship("CrossRate", 
        foreign_keys="CrossRate.Base_currency", 
        back_populates="Base_rel")
    
    AvaiableCurrencies_Quote_rel = relationship("CrossRate", 
        foreign_keys="CrossRate.Quote_currency", 
        back_populates="Quote_rel")

    AvaiableCurrencies_Transaction_Currency_rel = relationship(
    "Transaction", foreign_keys="Transaction.Transaction_Currency", back_populates="Transaction_Currency_rel")


class CrossRate(Base):

    __tablename__ = "Cross_rate"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Base_currency = Column(String, ForeignKey("AvaiableCurrencies.Code"))
    Quote_currency = Column(String, ForeignKey("AvaiableCurrencies.Code"))
    Exchange_rate = Column(Numeric, nullable=False)
    
    Base_rel = relationship("AvaiableCurrencies",
        foreign_keys=[Base_currency], 
    back_populates="AvaiableCurrencies_Base_rel")
    
    Quote_rel = relationship("AvaiableCurrencies", 
        foreign_keys=[Quote_currency], 
    back_populates="AvaiableCurrencies_Quote_rel")
    



class Transaction(Base):

    __tablename__ = "Transaction"
    id = Column(Integer, primary_key=True, autoincrement=True,)
    Recived = Column(DateTime, default=lambda:datetime.datetime.now(tz=ZoneInfo("Europe/Warsaw")), index=True)
    Source = Column(Integer, ForeignKey("Wallet.id"))
    Destination = Column(Integer, ForeignKey("Wallet.id"))
    Amount = Column(Numeric(9,2), nullable=False)
    Transaction_Currency = Column(String, ForeignKey("AvaiableCurrencies.Code"))


    Source_rel = relationship(
        "Wallet",foreign_keys=[Source],
    back_populates="Wallet_Source_rel")

    Destination_rel = relationship(
        "Wallet",foreign_keys=[Destination],
    back_populates="Wallet_Destination_rel")

    Transaction_Currency_rel = relationship(
        "AvaiableCurrencies",
        foreign_keys= [Transaction_Currency],
        back_populates="AvaiableCurrencies_Transaction_Currency_rel")
         

Base.metadata.create_all(bind=engine)



