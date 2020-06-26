from flask import Flask, request, jsonify
import json
from flask_json import FlaskJSON, JsonError, json_response, as_json
import requests
app = Flask(__name__)

dataJson = '{    "ocorrencias":[        {            "id_ocorrencia":1,            "id_dispositivo":1,            "vl_temperatura":26.5,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"10:57:24"        },        {            "id_ocorrencia":2,            "id_dispositivo":1,            "vl_temperatura":25.2,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"10:58:24"        },        {            "id_ocorrencia":3,            "id_dispositivo":1,            "vl_temperatura":26.6,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"10:59:24"        },        {            "id_ocorrencia":4,            "id_dispositivo":1,            "vl_temperatura":25.3,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"11:00:24"        },        {            "id_ocorrencia":5,            "id_dispositivo":1,            "vl_temperatura":27.7,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"11:01:24"        },        {            "id_ocorrencia":6,            "id_dispositivo":1,            "vl_temperatura":28.4,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"11:02:24"        },        {            "id_ocorrencia":7,            "id_dispositivo":1,            "vl_temperatura":25.8,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"11:03:24"        },        {            "id_ocorrencia":8,            "id_dispositivo":2,            "vl_temperatura":26.5,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"11:04:24"        },        {            "id_ocorrencia":9,            "id_dispositivo":1,            "vl_temperatura":25.2,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"11:05:24"        },        {            "id_ocorrencia":10,            "id_dispositivo":1,            "vl_temperatura":26.1,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"11:06:24"        },        {            "id_ocorrencia":11,            "id_dispositivo":2,            "vl_temperatura":24.8,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"11:07:24"        },        {            "id_ocorrencia":12,            "id_dispositivo":1,            "vl_temperatura":26.5,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"11:08:24"        },        {            "id_ocorrencia":13,            "id_dispositivo":2,            "vl_temperatura":24.3,            "vl_luminosidade":400,            "dt_ocorrencia":"2020-06-22",            "hr_ocorrencia":"11:09:24"        }    ],    "ultimoRegDips1":{        "id_ocorrencia":12,        "id_dispositivo":1,        "vl_temperatura":26.5,        "vl_luminosidade":400,        "dt_ocorrencia":"2020-06-22",        "hr_ocorrencia":"11:08:24"    },    "ultimoRegDips2":{        "id_ocorrencia":13,        "id_dispositivo":2,        "vl_temperatura":24.3,        "vl_luminosidade":400,        "dt_ocorrencia":"2020-06-22",        "hr_ocorrencia":"11:09:24"    }}'
dataJson = json.loads(dataJson)

JSONdifTemp = '{    "diferencaTemperatura":2.2,    "diferencaMin":1}'
JSONdifTemp = json.loads(JSONdifTemp)

JSONdevices = '{    "dispositivos":[        {            "idDispositivo":1,            "localDispositivo":"120.0.0.1",            "nomeDispositivo":"IBTI",            "statusLuminosidade":"1"        },        {            "idDispositivo":2,            "localDispositivo":"120.0.0.2",            "nomeDispositivo":"IBTI",            "statusLuminosidade":"1"        }    ]}'
JSONdevices = json.loads(JSONdevices)

JSONfreq = '{    "frequenciaDoDispositivo":5.0}'
JSONfreq = json.loads(JSONfreq)

JSONlastTemp = '{    "ultimaTemperatura":26.5}'
JSONlastTemp = json.loads(JSONlastTemp)



def answerTo(appServer, http_code, json_return):
    print("In Function", type(appServer))
    responseServer = appServer.response_class(
        response=json.dumps(json_return),
        status=http_code,
        mimetype='application/json'
    )
    return responseServer
'''
    Rotas default 
'''
@app.route("/") 
def home_view(): 
        return "<h1>Welcome to FINALMENTE EU CONSEGUI</h1>"

@app.route("/upwifi")
def upwifi():
    
    ip_address = request.remote_addr
    print(f"ip wifi =  {ip_address}")
    lux =  int(request.args.get('lux'))
    temp = int(request.args.get('temp'))
    
    #print(type(lux), "lux ", type(temp))
    print(f"Rota preestabelecida WiFi - temp = {temp} e lux = {lux} ")
    # pegar a frequencia wifi 
    # lembrar de depois de passar o novo valor zerar variavel donde veio
    DATA_GLOBAL = 65
    dataFreq = {
        'freq': DATA_GLOBAL
    }
    return answerTo(app,200,dataFreq)

@app.route("/hello")
def hello2():
    print("Rota preestabelecida "" - hello world")
    return "Hello World!"

@app.route("/answer")
def answer():
    print("Rota preestabelecida ANSWER ")
    print(type(app))
    return answerTo(app, 200,JSONlastTemp)

@app.route("/dados_graph")
def dados_enviados():
    print("Rota preestabelecida  - enviando dados  ")
    response = app.response_class(
        response=json.dumps(dataJson),
        status=200,
        mimetype='application/json'
    )
    return response


'''
Enviado pelo servidor: 
id_dispositivo = key do dispositivo do qual desejamos obter a frequência de envio atual.
Esperamos receber: 
frequencia_atual = a frequência de envio atualmente configurada para o dispositivo informado

* Aqui esperamos receber do servidor apenas uma mensagem informando se a alteração de frequência
  foi realizada com sucesso ou se houve erro, e no caso deste último,
  também devemos receber a mensagem de erro.
'''
@app.route("/updateFreq", methods = ['GET','POST'])
def updateFreq():
    data = request.get_json()
    # data deve vir em formato com key e frequencia
    # key = data["key"]
    # freq = data["frequencia"]
    try:
        key = int(data['key'])
        frequencia = int(data['frequencia'])
    except (KeyError, TypeError, ValueError):
        #raise JsonError(description='Invalid value.')
        resp = jsonify(success=False)
        # procurar erro correspondente
        resp.status_code = 444
        return resp
    
    print(f"KEY = {key}, frequencia {frequencia}")
    # resposta para caso de sucess
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

'''
    Enviado pela aplicacao: id_dispositivo = key do dispositivo do qual desejamos obter todas as temperaturas registradas nas últimas 24 horas.
    Aplicacao receber: 
    temp = temperatura registrada
    horaRegistrada = hora de registro da temperatura
    dataRegistro = data do registro da temperatura
     *  Os dados deverão vir ordenados dos mais antigos para os mais recentes

''' 
@app.route("/temperatures", methods = ['GET', 'POST'])
def getTempbyId():
    print("metodo get temperature")
    id_disp = request.get_json()
    print(f"ID recebido - {id_disp}")
    try:
        id_ = int(id_disp['keyDevice'])
    except (KeyError, TypeError, ValueError):
        #raise JsonError(description='Invalid value.')
        resp = jsonify(success=False)
        # procurar erro correspondente
        resp.status_code = 444
        return resp
    resp = ""
    # get dados que eles querem
    print(f"ID disp = {id_}")
    resp = jsonify(success=True)
    resp.status_code = 200
    
    return resp


'''
    Aplicacao envia: 
        id_dispositivo = key do dispositivo do qual desejamos obter a frequência de envio atual.
    Servidor responde: 
        frequencia_atual = a frequência de envio atualmente configurada para o dispositivo informado
''' 
@app.route("/frequency", methods = ['GET','POST'])
def getFreqbyId():
    print("metodo get temperature")
    id_disp = request.get_json()
    print(f"ID recebido - {id_disp}")
    try:
        id_ = int(id_disp['keyDevice'])
    except (KeyError, TypeError, ValueError):
        #raise JsonError(description='Invalid value.')
        resp = jsonify(success=False)
        # procurar erro correspondente
        resp.status_code = 444
        return resp
    resp = ""
    # get dados que eles querem
    print(f"ID disp = {id_}")
    print(answerTo(app,200,JSONfreq))
    return answerTo(app,200,JSONfreq)

##########################################
######          METODOS POST        ######
##########################################

'''
Enviado pela aplicacao: N/A.
Aplicacao receber: 
id_dispositivo = key do dispositivo cadastrado;
no_dispositivo = nome do dispositivo cadastrado;
local = nome do local do dispositivo cadastrado;
luz_on_off = se a luz está ligada ou apagada;

''' 
@app.route("/devices")
def devices():
    #
    # get dados que eles querem
    #

    return answerTo(200,JSONdevices)

'''
Enviado pela aplicacao: N/A.
Aplicacao receber: 
ultimaTemp = o valor da última temperatura registrada, independente de qual foi o dispositivo que a registrou.
''' 
@app.route("/lastTemp")
def lastTemperature():
    # get dados que eles querem
    # resp = jsonify(success=True)
    # resp.status_code = 200
    
    return answerTo(app,200,JSONlastTemp)

'''
    Enviado pela aplicacao: N/A.
    Aplicacao receber: 
    difTemp = a diferença de temperatura entre o último registro do dispositivo 1 e o último registro do dispositivo 2.
    difHora = a diferença entre a hora de registro da última temperatura do dispositivo 1 e a hora de registro da última
    temperatura do dispositivo 2.

''' 
@app.route("/difTemp")
def difTemp():
    # get dados que eles querem
    # resp = jsonify(success=True)
    # resp.status_code = 200
    
    return answerTo(app,200,JSONdifTemp)


if __name__ == '__main__':
    # host por padrao usa o endereco loopback
    #host = "0.0.0.0" irá usar o endereco local
    app.run(host="0.0.0.0",debug=True)
    
