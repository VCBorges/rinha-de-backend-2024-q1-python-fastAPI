from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/")
async def get_clientes():
    return 'clientes'