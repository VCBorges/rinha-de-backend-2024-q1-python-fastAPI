from datetime import datetime

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from . import models, schemas
from .exceptions import ClienteNaoEncontrado, SaldoInsuficiente


async def get_cliente_by_id(id: int, session: AsyncSession):
    return await session.get(models.Cliente, id)


async def get_extrato(
    cliente_id: int,
    session: AsyncSession,
) -> dict[str, list[models.Transacao] | models.Cliente]:
    stmt = (
        select(
            models.Cliente,
            models.Transacao,
        )
        .outerjoin(models.Transacao)
        .where(models.Cliente.id == cliente_id)
        .order_by(desc(models.Transacao.realizada_em))
        .limit(10)
    )
    result = await session.exec(stmt)
    data = result.all()
    if not data:
        raise ClienteNaoEncontrado()
    cliente = data[0][0]
    return schemas.ExtratoOutput(
        saldo=schemas.Saldo(
            total=cliente.saldo,
            data_extrato=datetime.now(),
            limite=cliente.limite,
        ),
        ultimas_transacoes=[
            schemas.TransacaoExtrato(
                valor=transacao[1].valor,
                tipo=transacao[1].tipo,
                descricao=transacao[1].descricao,
                realizada_em=transacao[1].realizada_em,
            )
            for transacao in data
            if data[0][1]
        ],
    )


async def create_transacao(
    cliente_id: int,
    transacao_input: schemas.TransacaoInput,
    session: AsyncSession,
) -> models.Cliente:
    cliente = await get_cliente_by_id(cliente_id, session)
    if not cliente:
        raise ClienteNaoEncontrado()
    if transacao_input.tipo == schemas.TipoTransacao.DEBITO:
        cliente.saldo -= transacao_input.valor
        if cliente.saldo < cliente.get_min_saldo():
            raise SaldoInsuficiente()
    else:
        cliente.saldo += transacao_input.valor

    transacao = models.Transacao(
        valor=transacao_input.valor,
        tipo=transacao_input.tipo,
        descricao=transacao_input.descricao,
        cliente_id=cliente.id,
    )

    session.add(cliente)
    session.add(transacao)
    await session.commit()
    await session.refresh(cliente)
    return cliente
