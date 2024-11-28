#instale as bibliotecas abaixo↴
#pip install pyautogui pillow numpy

#caso precise atualizar a biblioteca ↴
#python -m ensurepip --upgrade       ↵
import pyautogui
import time
from PIL import Image, ImageFilter
import numpy as np

def image_to_contour_lines(image_path, threshold=128, scale=0.5):
    """
    Converte uma imagem em uma lista de linhas contínuas para desenhar contornos.
    """
    image = Image.open(image_path).convert("L")  # Converter para escala de cinza
    image = image.resize((int(image.width * scale), int(image.height * scale)))
    image = image.filter(ImageFilter.FIND_EDGES)  # Detectar bordas

    img_array = np.array(image)

    lines = []
    for y, row in enumerate(img_array):
        line = []
        for x, pixel in enumerate(row):
            if pixel < threshold:
                line.append((x, y))
            elif line:
                lines.append(line)
                line = []
        if line:
            lines.append(line)
    
    return lines

def draw_contour_lines(lines, start_x, start_y, step=2):
    """
    Desenha contornos agrupando pixels em linhas contínuas.
    """
    if not lines:
        print("Nenhuma linha gerada para desenhar!")
        return

    print("Iniciando o desenho de contornos...")

    pyautogui.PAUSE = 0.01  # Pequena pausa automática entre movimentos
    
    for line in lines:
        pyautogui.moveTo(start_x + line[0][0] * step, start_y + line[0][1] * step, duration=0.005)
        pyautogui.mouseDown()

        for x, y in line:
            pyautogui.moveTo(start_x + x * step, start_y + y * step, duration=0.005)
        
        pyautogui.mouseUp()
        time.sleep(0.01)  # Pausa curta entre linhas
    
    print("Desenho finalizado!")

# Configurações
image_path = r"C:\Users\SeuUsuario\Downloads\sua-imagem.png"
threshold = 128
scale = 0.5
step = 2

# Gerar as linhas de contorno
lines = image_to_contour_lines(image_path, threshold, scale)

print("Total de linhas geradas:", len(lines))
if lines:
    print("Primeira linha:", lines[0])

if not lines:
    print("Nenhuma linha válida gerada.")
else:
    print("Posicione o mouse no ponto inicial do desenho.")
    time.sleep(1)
    start_x, start_y = pyautogui.position()

    draw_contour_lines(lines, start_x, start_y, step)
    print("Desenho completo!")