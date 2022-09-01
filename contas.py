import datetime
from pydantic import BaseModel


class Contas(BaseModel):
    id = 0
    descricao = ''
    data_vencimento = datetime.date(year=1, month=1, day=1)
    valor = 0
    baixado = True
