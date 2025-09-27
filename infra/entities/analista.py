from infra.configs.base import Base
from sqlalchemy import Column, Integer, String


class Analista(Base):
    __tablename__ = "analistas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    cargo = Column(String)
