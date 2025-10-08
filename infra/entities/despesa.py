from infra.configs.base import Base
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship


class Despesa(Base):
    __tablename__ = 'despesas'
    id = Column(Integer, primary_key=True)
    salvado_id = Column(Integer, ForeignKey('salvados.id'))
    fornecedor = Column(String)
    data = Column(Date)
    ocorrencia = Column(String)
    valor = Column(Float)
    observacao = Column(String)
    salvado = relationship("Salvado", back_populates="despesas")
