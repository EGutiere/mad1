import requests
import json

"""Localidades onde existe uma concentração maior de filiais do Grupo Madero"""
minasGerais     = [-20.0947, -19.6401, -44.3445, -43.7622]
parana          = [-25.6002, -25.2809, -49.5794, -49.0534]
rioGrandedoSul  = [-30.1645, -29.0427, -51.7582, -50.6689]
rioDeJaneiro    = [-23.0532, -22.7635, -43.6410, -43.0889]
saoPaulo        = [-23.8000, -23.1000, -46.9900, -46.1000]

"""API do IPAM para a consulta"""
api = "https://ipam.grupomadero.com.br/api/3000"

def main():
  
    token = getTokenIPAM(api)

    response = requests.get(api + '/tools/locations', headers={'token' : token}).json()

    file = locationsCreation(response)

    writeFile(file)

"""Salva os arquivos no disco local"""
def writeFile(outf): 
    
    """Nome dos arquivos de saída"""
    localidades = ['minasgerais','parana','riograndedosul','riodejaneiro','saopaulo','outraslocalidades']

    """Escrita local dos arquivos"""
    for i in range(len(localidades)):
        with open(".\{}.json".format(localidades[i]), 'w') as json_file:
            json_file.writelines(outf[i])

"""Criação dos texto no formato aceito pelo plugin WorldMap Panel"""
def locationsCreation(response):    

    """Setando variável file que receberá as filiais de acordo com sua localização"""
    file = ['[','[','[','[','[','[']

    """Adição das filiais em seus respectivos arquivos"""
    for i in range(len(response['data'])):
        
        latI = json.loads(response['data'][i]['lat'].replace(',','.'))
        longI = json.loads(response['data'][i]['long'].replace(',','.'))

        if (minasGerais[0] < latI < minasGerais[1] and minasGerais[2] < longI < minasGerais[3]):
            j = 0
            file[j] = file[j] + dataset(response, i)
        
        elif (parana[0] < latI < parana[1] and parana[2] < longI < parana[3]):
            j = 1
            file[j] = file[j] + dataset(response, i)
        
        elif (rioGrandedoSul[0] < latI < rioGrandedoSul[1] and rioGrandedoSul[2] < longI < rioGrandedoSul[3]):
            j = 2
            file[j] = file[j] + dataset(response, i)

        elif (rioDeJaneiro[0] < latI < rioDeJaneiro[1] and rioDeJaneiro[2] < longI < rioDeJaneiro[3]):
            j = 3
            file[j] = file[j] + dataset(response, i)
        
        elif (saoPaulo[0] < latI < saoPaulo[1] and saoPaulo[2] < longI < saoPaulo[3]):
            j = 4
            file[j] = file[j] + dataset(response, i)

        else:
            j = 5
            file[j] = file[j] + dataset(response, i)
       
    """Fechamento dos arquivos .json"""
    for i in range(len(file)):
        file[i] = file[i] +'\n  {'
        file[i] = file[i] +'\n    "key": "adm1",'
        file[i] = file[i] +'\n    "latitude": -25.4378753,'
        file[i] = file[i] +'\n    "longitude": -49.3097658,'
        file[i] = file[i] +'\n    "name": "Prédio Administrativo - Curitiba"'
        file[i] = file[i] +'\n  }' 
        file[i] = file[i] +'\n]' 

    return(file)

"""Dados estruturados no formato que o WorldMap Panel aceita | Response é o Json do IPAM e I é o cod da chave que ele se encontra no momento"""
def dataset(response, i):

    file = '\n  {'
    file = file +'\n    "key": "'+ response['data'][i]['custom_fields']['custom_Cod_Filial']+'",'
    file = file +'\n    "latitude": '+ response['data'][i]['lat'].replace(',','.') +','
    file = file +'\n    "longitude": '+ response['data'][i]['long'].replace(',','.') +','
    file = file +'\n    "name": "'+ response['data'][i]['name'] +'"'
    file = file +'\n  },'

    return file

"""Autenticação do IPAM - retorna o token necessário para a busca dentro da API do IPAM"""
def getTokenIPAM(url):

    username = "grafana"
    password = "SYPy47U!B5"
    response = requests.post(url + '/user/token', auth=(username, password)).json()
    token = response['data']['token']

    return(token)

if __name__ == '__main__':
    main()