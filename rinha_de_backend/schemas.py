from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import PositiveInt, StringConstraints
from sqlmodel import SQLModel


class TipoTransacao(StrEnum):
    DEBITO = 'd'
    CREDITO = 'c'


class BaseCliente(SQLModel):
    limite: int
    saldo: int
    nome: Annotated[str, StringConstraints(max_length=100)]


class BaseTransacao(SQLModel):
    valor: PositiveInt
    tipo: TipoTransacao
    descricao: Annotated[str, StringConstraints(max_length=10)]


class TransacaoOutput(SQLModel):
    limite: int
    saldo: int


class Saldo(SQLModel):
    total: int
    data_extrato: datetime
    limite: int


class TransacaoExtrato(BaseTransacao):
    realizada_em: datetime


class ExtratoOutput(SQLModel):
    saldo: Saldo
    ultimas_transacoes: list[TransacaoExtrato]


class TransacaoInput(BaseTransacao):
    pass
