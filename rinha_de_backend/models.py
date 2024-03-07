from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, Relationship, String

from . import schemas


class Cliente(schemas.BaseCliente, table=True):
    __tablename__ = 'clientes'
    id: int = Field(primary_key=True, index=True)
    transacoes: list['Transacao'] = Relationship(back_populates='cliente')

    def get_min_saldo(self) -> int:
        return self.limite * -1


class Transacao(schemas.BaseTransacao, table=True):
    __tablename__ = 'transacoes'
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: schemas.TipoTransacao = Field(sa_column=Column(String(1)))
    realizada_em: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True)),
    )
    cliente_id: int = Field(
        foreign_key='clientes.id',
        index=True,
    )
    cliente: Cliente = Relationship(back_populates='transacoes')
