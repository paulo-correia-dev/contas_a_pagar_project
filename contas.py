from pydantic import BaseModel


class Contas(BaseModel):
    descricao = ''
    data_vencimento = ' '
    valor = ' '
    baixado = True
