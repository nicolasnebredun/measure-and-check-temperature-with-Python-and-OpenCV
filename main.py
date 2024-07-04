import shutil
import schedule
import time
import pyscreenshot as ImageGrab
import os
from datetime import datetime
import pytesseract
import argparse
import cv2
import http.client
import json
def call_api1():

    conn = http.client.HTTPConnection("")
    payload = json.dumps({
        "args": {
        "to": "Number", 
        "content": "ATENÇÃO: Algo De errado na Maquina de Vigilancia, Verificar a Maquina!"
        }
        })
    headers = {
        'Content-Type': 'application/json'
        }
    conn.request("POST", "URL", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print('Mensagem Enviada')
    #print(data.decode("utf-8"))
def call_api():

    conn = http.client.HTTPConnection("10.1.1.26", 8182)
    payload = json.dumps({
        "args": {
        "to": "5569992692250@c.us", 
        "content": "ATENÇÃO: Servidor com temperatura acima do normal!"
        }
        })
    headers = {
        'Content-Type': 'application/json'
        }
    conn.request("POST", "/eagle-session/sendText", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print('Mensagem Enviada')
    #print(data.decode("utf-8"))
def delete(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
def print_temperatura():
    print("------Pegando Temperatura------")

    # Definando Nome do Arquivo
    image_name = f"temperatura.png"

    # Lugar do Print
    # Definindo as coordenadas do retângulo (box)
    x = 300  # posição inicial x do canto superior esquerdo
    y = 300  # posição inicial y do canto superior esquerdo
    width = 40  # largura do retângulo
    height = 40  # altura do retângulo

# Criando o box com as coordenadas especificadas
    box = (x, y, x + width, y + height)

    screenshot = ImageGrab.grab(bbox=box)

    # Verificando Diretório

    directory = "./print"

    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, image_name)
    screenshot.save(filepath)

    print("Print feito com sucesso!")

    return filepath

def check_temperatura():
    #Carregando a Imagem
    image = cv2.imread('./print/temperatura.png')
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    options = ''

    #Chechando se o Tesseract consegue identificar
    if True:
        options = '--psm 10'

    # OCR verificando e convertendo a imagem
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
    text = pytesseract.image_to_string(rgb, config=options)
    
    
    # Colocando o Valor em String
    temperatura = (''.join(filter(str.isdigit, text)))

    print(temperatura)
    if temperatura >= '26':
            print("Temperatura muito alta!")
            timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            with open(os.path.join(".\log", f"temperatura_{timestamp}.txt"), 'w') as f:
                f.write(f"{timestamp}: Temperatura muito alta!\n")
                call_api()
                delete(directory="./print")
    elif not temperatura.isdigit() or temperatura == '':
        call_api1()
    else:
        print("Temperatura normal!")
        print(temperatura)
        # Execute the delete function
        delete(directory="./print")

def main():
    # Objeto fora do loop
    sched = schedule.Scheduler()

    # tasks
    
    sched.every(28).seconds.do(print_temperatura)
    
    sched.every(32).seconds.do(check_temperatura)
    

    # Laço
    while True:
        sched.run_pending()
        time.sleep(1)
        calor = 10
        if calor == 30:
            break
            
        
if __name__ == '__main__':
    main()
