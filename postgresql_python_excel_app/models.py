from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Date, Float, text, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    surname = Column(String, index=True, nullable=False)
    tckno = Column(BigInteger, unique=True, nullable=False)
    date_of_birth = Column(String, nullable=False)
    date_created = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    date_updated = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(String, index=True, nullable=False)

    client_infos = relationship("ClientInfo", back_populates="owner")
    insurances = relationship("Insurance", back_populates="owner")


class ClientInfo(Base):
    __tablename__ = "client_info"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("client.id"), index=True)
    contact_phone = Column(String, nullable=False)
    phone_type = Column(String, nullable=False)
    e_mail = Column(String, nullable=False)
    address = Column(String, nullable=False)
    address_province = Column(String, nullable=False)
    address_city = Column(String, nullable=False)
    date_created = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    date_updated = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(String, index=True, nullable=False)

    owner = relationship("Client", back_populates="client_infos")


class Insurance(Base):
    __tablename__ = "insurance"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("client.id"))
    policy_no = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    policy_start_date = Column(String, nullable=False)
    policy_end_date = Column(String, nullable=False)
    insurance_type = Column(String, nullable=False)
    date_created = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    date_updated = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(String, index=True, nullable=False)

    owner = relationship("Client", back_populates="insurances")






