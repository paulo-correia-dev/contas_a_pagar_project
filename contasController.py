import http
from fastapi import FastAPI, Response
import mysql.connector
from contas import Contas
from retornos import Retornos

app = FastAPI()
retorno_api = Retornos()


@app.post("/cadastrarContas", status_code=http.HTTPStatus.CREATED)
def cadastro_contas(contas: Contas, response: Response):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()

    if contas.baixado:
        contas.baixado = 'T'
    elif not contas.baixado:
        contas.baixado = 'F'

    sql = f"insert into a_pagar (descricao_conta, data_vencimento, valor, baixado) " \
          f"values ('{contas.descricao}', '{contas.data_vencimento}', {contas.valor}, '{contas.baixado}') "
    cursor.execute(sql)
    conexao.commit()
    response.status_code = http.HTTPStatus.CREATED
    retorno_api.status_code = response.status_code
    retorno_api.desc_status_code = "CREATED"
    retorno_api.mensagem = "Conta cadastrada com sucesso"
    return retorno_api


@app.get("/consultarContas", status_code=http.HTTPStatus.OK)
def consulta_contas(response: Response):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()
    sql = 'select * from a_pagar'
    cursor.execute(sql)
    retorno = cursor.fetchall()

    if len(retorno) == 0:
        response.status_code = http.HTTPStatus.BAD_REQUEST
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD-REQUEST"
        retorno_api.mensagem = "Não existem contas cadastradas"
        return retorno_api

    obj_list = []

    for cada_conta in retorno:
        conta = Contas()
        conta.id = cada_conta[0]
        conta.descricao = cada_conta[1]
        conta.data_vencimento = cada_conta[2]
        conta.valor = cada_conta[3]
        if cada_conta[4].upper() == "T":
            conta.baixado = True
        elif cada_conta[4].upper() == "F":
            conta.baixado = False

        obj_list.append(conta)

    response.status_code = http.HTTPStatus.OK
    retorno_api.status_code = response.status_code
    retorno_api.desc_status_code = "OK"
    retorno_api.mensagem = "Lista obtida com sucesso!"

    return retorno_api, obj_list


@app.put("/atualizarContas", status_code=http.HTTPStatus.CREATED)
def atualiza_contas(contas: Contas, response: Response):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()
    cursor.execute('select * from a_pagar')
    retorno = cursor.fetchall()

    if contas.baixado:
        contas.baixado = 'T'
    elif not contas.baixado:
        contas.baixado = 'F'

    for cont in retorno:
        if contas.id == cont[0]:
            response.status_code = http.HTTPStatus.CREATED
            sql = f"update a_pagar set descricao_conta = '{contas.descricao}', data_vencimento = " \
                  f"'{contas.data_vencimento}', valor = {contas.valor}, baixado = '{contas.baixado}' " \
                  f"where id = {contas.id};"
            cursor.execute(sql)
            conexao.commit()
            break
        else:
            response.status_code = http.HTTPStatus.BAD_REQUEST

    if response.status_code == http.HTTPStatus.CREATED:
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "CREATED"
        retorno_api.mensagem = "Conta atualizada com sucesso!"
        return retorno_api
    else:
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD_REQUEST"
        retorno_api.mensagem = "Não existe conta com esse id para ser atualizada."
        return retorno_api


@app.delete("/excluirContas/{id_conta}", status_code=http.HTTPStatus.OK)
def deleta_contas(id_conta, response: Response):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()

    if str(id_conta).isdecimal():
        id_conta = int(id_conta)
    else:
        response.status_code = http.HTTPStatus.BAD_REQUEST
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD_REQUEST"
        retorno_api.mensagem = "O valor de id deve ser numérico."
        return retorno_api

    cursor.execute(f"select * from a_pagar")
    retorno = cursor.fetchall()

    for cont in retorno:
        if cont[0] == id_conta:
            response.status_code = http.HTTPStatus.OK
            cursor.execute(f"delete from a_pagar where id= {id_conta};")
            conexao.commit()
            break
        else:
            response.status_code = http.HTTPStatus.BAD_REQUEST

    if response.status_code == http.HTTPStatus.OK:
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "OK"
        retorno_api.mensagem = "Conta excluída com sucesso!"
        return retorno_api
    else:
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD_REQUEST"
        retorno_api.mensagem = "Não existe conta com esse id para ser excluída."
        return retorno_api


@app.put("/baixarContas/{id_conta}", status_code=http.HTTPStatus.OK)
def baixa_contas(id_conta, response: Response):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()

    if str(id_conta).isdecimal():
        id_conta = int(id_conta)
    else:
        response.status_code = http.HTTPStatus.BAD_REQUEST
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD_REQUEST"
        retorno_api.mensagem = "O valor de id deve ser numérico."
        return retorno_api

    cursor.execute(f'select * from a_pagar')
    retorno = cursor.fetchall()

    nao_existe_conta = False

    for cont in retorno:
        if cont[0] == int(id_conta):
            if cont[4] == 'F':
                cursor.execute(f"update a_pagar set baixado = 'T' where id= {int(id_conta)}")
                conexao.commit()
                response.status_code = http.HTTPStatus.OK
                retorno_api.status_code = response.status_code
                retorno_api.desc_status_code = "OK"
                retorno_api.mensagem = "Conta baixada com sucesso!"
                return retorno_api
            elif cont[4] == 'T':
                response.status_code = http.HTTPStatus.BAD_REQUEST
                retorno_api.status_code = response.status_code
                retorno_api.desc_status_code = "BAD_REQUEST"
                retorno_api.mensagem = "Essa conta já foi baixada!"
                return retorno_api
        else:
            nao_existe_conta = True

    if nao_existe_conta:
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD_REQUEST"
        retorno_api.mensagem = "Não existe conta cadastrada com esse id."
        return retorno_api


@app.put("/estornarContas/{id_conta}", status_code=http.HTTPStatus.OK)
def estorna_contas(id_conta, response: Response):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()

    if str(id_conta).isdecimal():
        id_conta = int(id_conta)
    else:
        response.status_code = http.HTTPStatus.BAD_REQUEST
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD_REQUEST"
        retorno_api.mensagem = "O valor de id deve ser numérico."
        return retorno_api

    cursor.execute(f'select * from a_pagar')
    retorno = cursor.fetchall()

    nao_existe_conta = False

    for cont in retorno:
        if cont[0] == int(id_conta):
            if cont[4] == 'T':
                cursor.execute(f"update a_pagar set baixado = 'F' where id= {int(id_conta)}")
                conexao.commit()
                response.status_code = http.HTTPStatus.OK
                retorno_api.status_code = response.status_code
                retorno_api.desc_status_code = 'OK'
                retorno_api.mensagem = "Conta estornada com sucesso!"

                return retorno_api
            elif cont[4] == 'F':
                response.status_code = http.HTTPStatus.BAD_REQUEST
                retorno_api.status_code = response.status_code
                retorno_api.desc_status_code = "BAD_REQUEST"
                retorno_api.mensagem = "Essa conta não está baixada para que seja estornada!"
                return retorno_api
        else:
            nao_existe_conta = True

    if nao_existe_conta:
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD_REQUEST"
        retorno_api.mensagem = "Não existe conta cadastrada com esse id."
        return retorno_api


@app.get("/consultarContas/{nome_parcial}")
def busca_nome_parcial(nome_parcial, response: Response):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()
    cursor.execute('select * from a_pagar')
    retorno = cursor.fetchall()

    nao_tem = False
    obj_list = []

    for cont in retorno:
        if nome_parcial in cont[1]:
            cursor.execute(f"select * from  a_pagar where descricao_conta like '%{nome_parcial}%'")
            retorno_in = cursor.fetchall()

            for cont1 in retorno_in:
                conta = Contas()
                conta.id = cont1[0]
                conta.descricao = cont1[1]
                conta.data_vencimento = cont1[2]
                conta.valor = cont1[3]
                conta.baixado = cont1[4]
                obj_list.append(conta)

            response.status_code = http.HTTPStatus.OK
            retorno_api.status_code = response.status_code
            retorno_api.desc_status_code = "OK"
            retorno_api.mensagem = "Lista obtida com sucesso."
            return retorno_api, obj_list
        else:
            nao_tem = True

    if nao_tem:
        response.status_code = http.HTTPStatus.BAD_REQUEST
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD_REQUEST"
        retorno_api.mensagem = "Não encontramos nenhuma conta correspondente!"
        return retorno_api


@app.get("/consultarContas/{ano}/{mes}")
def busca_ano_mes(ano, mes, response: Response):
    conexao = mysql.connector.connect(host='localhost', database='contas_a_pagar', user='root', password='root')
    cursor = conexao.cursor()

    if str(ano).isdecimal() and str(mes).isdecimal():
        ano = int(ano)
        mes = int(mes)
    else:
        response.status_code = http.HTTPStatus.BAD_REQUEST
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD_REQUEST"
        retorno_api.mensagem = "O valor de ano e mês devem ser numéricos."
        return retorno_api

    cursor.execute('select * from a_pagar')
    retorno = cursor.fetchall()

    nao_tem = False
    obj_list = []

    for cont in retorno:
        data = str(cont[2])

        if ano == int(data[0:4]) and mes == int(data[5:7]):
            cursor.execute(f"select * from a_pagar where month(data_vencimento) = {mes} "
                           f"and year(data_vencimento) = {ano}")
            retorno_in = cursor.fetchall()

            for cont1 in retorno_in:
                conta = Contas()
                conta.id = cont1[0]
                conta.descricao = cont1[1]
                conta.data_vencimento = cont1[2]
                conta.valor = cont1[3]
                conta.baixado = cont1[4]
                obj_list.append(conta)

            response.status_code = http.HTTPStatus.OK
            retorno_api.status_code = response.status_code
            retorno_api.desc_status_code = "OK"
            retorno_api.mensagem = "Lista obtida com sucesso."
            return retorno_api, obj_list
        else:
            nao_tem = True

    if nao_tem:
        response.status_code = http.HTTPStatus.BAD_REQUEST
        retorno_api.status_code = response.status_code
        retorno_api.desc_status_code = "BAD_REQUEST"
        retorno_api.mensagem = "Não encontramos nenhuma conta correspondente!"

        return retorno_api
