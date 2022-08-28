from fastapi import FastAPI
import mysql.connector
from contas import Contas

app = FastAPI()


@app.post("/cadastrarContas/{descricao}/{data}/{valor}/{baixado}")
def cadastro_contas(descricao, data, valor, baixado):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()

    if not valor.isnumeric():
        return "O valor da conta deve ser numérico"

    if baixado.upper() == 'T':
        baixado = 'T'
    elif baixado.upper() == 'F':
        baixado = 'F'
    else:
        return "O valor de baixado deve ser T ou F"

    sql = f"insert into a_pagar (descricao_conta, data_vencimento, valor, baixado) " \
          f"values ('{descricao}', '{data}', {float(valor)}, '{baixado}') """
    cursor.execute(sql)
    conexao.commit()
    return "Conta cadastrada com sucesso", descricao, data, valor, baixado


@app.get("/consultarContas")
def consulta_contas():
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()
    sql = 'select * from a_pagar'
    cursor.execute(sql)
    retorno = cursor.fetchall()

    obj_list = []

    for cada_conta in retorno:
        conta = Contas()
        conta.descricao = cada_conta[1]
        conta.data_vencimento = cada_conta[2]
        conta.valor = cada_conta[3]
        if cada_conta[4].upper() == "T":
            conta.baixado = True
        elif cada_conta[4].upper() == "F":
            conta.baixado = False

        obj_list.append(conta)

    return obj_list


@app.put("/atualizarContas/{descricao}/{data}/{valor}/{baixado}/{id_conta}")
def atualiza_contas(descricao, data, valor, baixado, id_conta):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()
    sql = f"update a_pagar set descricao_conta = '{descricao}', data_vencimento = '{data}', valor = {float(valor)}, " \
          f"baixado = '{baixado}' where id = {int(id_conta)};"
    cursor.execute(sql)
    conexao.commit()
    return "Conta atualizada com sucesso!", descricao, valor, data, baixado


@app.delete("/excluirContas/{id_conta}")
def deleta_contas(id_conta):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()
    sql = f"delete from a_pagar where id = {int(id_conta)}"
    cursor.execute(sql)
    conexao.commit()
    return "Conta Apagada com  sucesso!"


@app.put("/baixarContas/{id_conta}")
def baixa_contas(id_conta):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()
    sql = f"update a_pagar set baixado = 'T' where id= {int(id_conta)}"
    cursor.execute(sql)
    conexao.commit()
    return "Conta baixada com sucesso!"


@app.put("/estornarContas/{id_conta}")
def estorna_contas(id_conta):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()
    sql = f"update a_pagar set baixado = 'F' where id= {int(id_conta)}"
    cursor.execute(sql)
    conexao.commit()
    return "Conta estornada com sucesso!"
