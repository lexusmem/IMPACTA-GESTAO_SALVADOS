from infra.configs.base import Base
from sqlalchemy import Column, Integer, String


class StatusOpcao(Base):
    __tablename__ = "status_opcoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True)
