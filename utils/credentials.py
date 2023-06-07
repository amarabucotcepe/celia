from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import sys
import requests

def setup():      
    api_id = str(input('digite o api_id:'))
    environment = str(input('digite o ambiente(desenvolvimento, homologacao ou producao):'))
    registration_access_token = str(input('digite o registration_access_token:'))
    return get_credentials(api_id, environment, registration_access_token)

def get_credentials(api_id, environment, registration_access_token):
    answer = get_client_id(api_id, environment, registration_access_token)
    if answer != False:
       answer2 = get_client_secret(api_id, environment, answer['registration_access_token'], answer['client_id'])
       return answer2
    else:
        return False

def get_client_id(api_id, environment, registration_access_token):
    
    headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {registration_access_token}',
            }
        
    if (environment == 'desenvolvimento'):
        url = f"https://oauth.desenv.bb.com.br/oauth/clients/{api_id}/installations"
    elif (environment == 'homologacao'):
        url = f"https://oauth.hm.bb.com.br/oauth/clients/{api_id}/installations"
    elif (environment == 'producao'):
        url = f"https://oauth.bb.com.br/oauth/clients/{api_id}/installations"
    else:
        print('ambiente não encontrado. tente novamente.')   
        return False
    
    r = requests.post(url, headers=headers)
    if r.ok:
        print('anote os dados abaixo, pois somente são gerados uma vez:')
        print(r.json())
        return r.json()
    else:
        print('erro:')
        print(r.json())
        return False
    
def get_client_secret(api_id, environment, registration_access_token, client_id):
    headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {registration_access_token}',
            }
    
    if environment == 'desenvolvimento':
        url = f"https://oauth.desenv.bb.com.br/oauth/clients/{api_id}/installations/{client_id}/credentials"
    elif environment == 'homologacao':
        url = f"https://oauth.hm.bb.com.br/oauth/clients/{api_id}/installations/{client_id}/credentials"
    elif environment == 'producao':
        url = f"https://oauth.bb.com.br/oauth/clients/{api_id}/installations/{client_id}/credentials"
    else:
        print('ambiente não encontrado. tente novamente.')   
        return False
    
    r = requests.post(url, headers=headers)
    if r.ok:
        print('anote os dados abaixo, pois somente são gerados uma vez:')
        print(r.json())
        return r.json()
    else:
        print('erro:')
        print(r.json())
        return False
        
def get_token(client_id, client_secret, scope, environment):
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client) 
    oauth = OAuth2Session(client=client, scope=scope)
    if environment == 'desenvolvimento':
        token = oauth.fetch_token(token_url='https://oauth.desenv.bb.com.br/oauth/token', auth=auth)
    if environment == 'homologacao':
        token = oauth.fetch_token(token_url='https://oauth.hm.bb.com.br/oauth/token', auth=auth)
    if environment == 'producao':
        token = oauth.fetch_token(token_url='https://oauth.bb.com.br/oauth/token', auth=auth)
    return token    

if __name__ == "__main__":
    setup()
    # txt = sys.argv[1]
    # print(txt)
    # if txt == 'client_id':
    #     get_client_id()
    # if txt == 'client_secret':
    #     get_client_secret()
    # if txt == 'access_token':
    #     environment = str(input('digite o ambiente(desenvolvimento, homologacao ou producao): '))
    #     client_id = str(input('digite o client_id: '))
    #     client_secret = str(input('digite o client_secret: '))
    #     scope = str(input('digite o scope: '))
    #     token = get_access_token(client_id, client_secret, scope, environment)
    #     print(token)
        
