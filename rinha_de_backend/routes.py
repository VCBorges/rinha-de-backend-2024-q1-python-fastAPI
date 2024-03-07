from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from . import schemas, services
from .database import get_db_session

router = APIRouter(prefix='/clientes', tags=['clientes'])


@router.get('/{id}/extrato')
async def get_extrato(
    id: int,
    session: AsyncSession = Depends(get_db_session),
) -> schemas.ExtratoOutput:
    extrato = await services.get_extrato(cliente_id=id, session=session)
    return extrato


@router.post('/{id}/transacoes')
async def transacionar(
    id: int,
    transacao_input: schemas.TransacaoInput,
    session: AsyncSession = Depends(get_db_session),
) -> schemas.TransacaoOutput:
    cliente = await services.create_transacao(
        cliente_id=id,
        transacao_input=transacao_input,
        session=session,
    )
    return schemas.TransacaoOutput(
        limite=cliente.limite,
        saldo=cliente.saldo,
    )
