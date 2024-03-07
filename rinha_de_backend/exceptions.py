from fastapi import HTTPException, status


class ClienteNaoEncontrado(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Cliente não encontrado',
        )


class SaldoInsuficiente(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Saldo insuficiente',
        )
