from infra.configs.base import Base
from sqlalchemy import Column, Integer, String


class Leiloeiro(Base):
    __tablename__ = "leiloeiros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    endereco = Column(String)
    telefone = Column(String)
    responsavel = Column(String)
    email = Column(String)
