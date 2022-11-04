from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, func
from sqlalchemy.orm import declarative_base, relationship, Session


def max_id(column_max, column_ret):
    max_ = session.query(func.max(column_max)).scalar()
    max_tx = list(set(session.query(column_ret).filter(column_max == max_).all()))
    max_tx = f"/{max_tx[0][0]}" if max_tx else ""
    return max_tx


Base = declarative_base()


class Movements(Base):
    __tablename__ = 'movements'

    id = Column(Integer, primary_key=True)
    status = Column(String(7))
    network = Column(String(4))
    address = Column(String(34))

    transactions = relationship("Transactions", back_populates="movements")


class Transactions (Base):
    __tablename__ = 'transactions'

    txid = Column(String, primary_key=True)
    mov_id = Column(Integer, ForeignKey('movements.id'))
    input_no = Column(Integer, primary_key=True, default=None, nullable=True)
    output_no = Column(Integer, primary_key=True, default=None, nullable=True)
    script_asm = Column(String)
    script_hex = Column(String)
    witness = Column(String)
    value = Column(Numeric(precision=8, scale=5))
    confirmations = Column(Integer)
    time = Column(Integer)

    movements = relationship("Movements", back_populates="transactions")


engine = create_engine('sqlite:///doge.sqlite')
Base.metadata.create_all(engine)
session = Session(engine)
