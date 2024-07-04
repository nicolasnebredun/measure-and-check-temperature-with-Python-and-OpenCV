import shutil
import schedule
import time
import pyscreenshot as ImageGrab
import os


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

def main():
    # Objeto fora do loop
    sched = schedule.Scheduler()

    # tasks
    
    sched.every(5).seconds.do(print_temperatura)
    
    

    # Laço
    while True:
        sched.run_pending()
        time.sleep(1)
        calor = 10
        if calor == 30:
            break
            
        
if __name__ == '__main__':
    main()