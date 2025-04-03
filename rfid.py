
import RPi.GPIO as GPIO
import requests
from time import sleep
from mfrc522 import SimpleMFRC522

GPIO.setmode(GPIO.BOARD)

chave = 'senha'

def send_post_request_user(tag):
        print("Valide sua chave antes de criar um usuário: ")
        chave_digitada = input("Digite sua chave: ")
        if chave_digitada == chave:
            data = {'nome': input("Nome do usuário: "),
                    'tag': tag,
                    'permissao': int(input("Permissao para acessar? 0 - Não / 1 - Sim: "))}
            try:
                response = requests.post('http://localhost:5000/user', json=data)
                if response.status_code == 201:
                    print("Mensagem enviada com sucesso!")
                    print(response.json().get('message'))
                else:
                    print(f"Erro ao enviar mensagem: {response.status_code}")
            except Exception as e:
                print(f"Erro na conexão: {e}")
        else:
            print("Chave não encontrada")

def send_delete_request_user():
    print("Valide sua chave antes de criar um usuário: ")
    chave_digitada = input("Digite sua chave: ")
    if chave_digitada == chave:
        data = {'id':input("Digite o ID do usuário a ser deletado: ")}
        try:
            response = requests.delete('http://localhost:5000/user',json=data)
            if response.status_code == 201:
                print(response.json().get('message'))
        except Exception as e:
            print(f"Erro na conexão: {e}")
    else:
        print("Chave não encontrada")

def send_post_request_acesso(tag):
    data = {'tag':tag}
    try:
        response = requests.post('http://localhost:5000/acesso',json=data)
        if response.status_code == 201:
            print("Mensagem enviada com sucesso!")
            print(response.json().get('message'))
        else:
            print(f"Erro ao enviar mensagem: {response.status_code}")
    except Exception as e:
        print(f"Erro na conexão: {e}")

def send_get_request_users():
    try:
        response = requests.get('http://localhost:5000/user')
        if response.status_code == 201:
            print(response.json())

    except Exception as e:
                print(f"Erro na conexão: {e}")

def send_get_request_acesso():
    try:
        response = requests.get('http://localhost:5000/acesso')
        if response.status_code == 201:
            print(response.json())

    except Exception as e:
                print(f"Erro na conexão: {e}")

def send_update_request_user():
    print("Valide sua chave antes de criar um usuário: ")
    chave_digitada = input("Digite sua chave: ")
    if chave_digitada == chave:
        data = {'id':input("Digite o ID do usuário: "),
                'permissao': int(input("1 - Acesso Permitido / 0 - Acesso Negado: "))}
        try:
            response = requests.put('http://localhost:5000/user',json=data)
            if response.status_code == 201:
                print(response.json().get('message'))
        except Exception as e:
            print(f"Erro na conexão: {e}")
    else:
        print("Chave não encontrada")

while True:
    result = int(input("1-Criar usuário\n2-Tentativa de Acesso\n3-Listar Usuários\n4-Logs de acesso\n5-Alterar Permissao do Usuario\n6-Deletar Usuário\n0-Sair da aplicação: "))
    
    if result == 1:
        GPIO.cleanup()
        leitorRfid = SimpleMFRC522()
        try:
            print ("Aguardando leitura da tag")
            tag, text = leitorRfid.read()
            print (f"ID do cartao: {tag}")
            send_post_request_user(tag)
        finally:
            GPIO.cleanup()
    elif result == 2:
        GPIO.cleanup()
        leitorRfid = SimpleMFRC522()
        try:
            print ("Aguardando leitura da tag")
            tag, text = leitorRfid.read()
            print (f"ID do cartao: {tag}")
            send_post_request_acesso(tag)
        finally:
            GPIO.cleanup()
    elif result == 3:
        send_get_request_users()
    elif result == 4:
        send_get_request_acesso()
    elif result == 5:
        send_update_request_user()
    elif result == 6:
        send_delete_request_user()
    elif result == 0:
         break