from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import StringVar, messagebox, IntVar

janela = tk.Tk()
janela.title("MultiMage")
janela.geometry("400x400")

imagem = Image.open("fundo_para_testes.jpg")
desenho = ImageDraw.Draw(imagem)
fonte = ImageFont.truetype("arial.ttf", size = 200)

texto = StringVar()
entrada_texto = tk.Entry(
    janela,
    textvariable = texto,
    width = 50,
    bd = 2
    )
entrada_texto.pack(padx = 10, pady = 10)

numero_inicial = IntVar()
numero_final = IntVar()

tk.Label(janela, text = "Número inicial:").pack()
tk.Entry(janela, textvariable = numero_inicial).pack(pady = 5)

tk.Label(janela, text = "Número Final:").pack()
tk.Entry(janela, textvariable = numero_final).pack(pady = 5)

posicao = (300,200)

def gerar_imagem():
    if not texto.get():
        messagebox.showinfo('Erro', "Por favor, insira um texto válido")
        return
    
    inicio = numero_inicial.get()
    final = numero_final.get()
    for i in range (inicio, final + 1):
        imagem_temp = imagem.copy() #vai criar uma copia independente da imagem original a cada rep
        desenho_temp = ImageDraw.Draw(imagem_temp) #Cria objeto de desenho para a copia
        #Assim nao modifica a imagem original 
        numero_formatado = str(i).zfill(3) #converte int em str para ser escrito e completa com 0 a esquerda
        texto_final = f"{texto.get()} {numero_formatado}"

        desenho_temp.text(posicao, texto_final, font = fonte, fill = "black")
        imagem_temp.save(f"imagem_{numero_formatado}.jpg")
        messagebox.showinfo('Tudo certo!', "Imagem gerada com sucessor!")
        janela.destroy()

tk.Button(
    janela,
    text = 'Gerar Imagem',
    command = gerar_imagem
).pack(pady = 20)

janela.mainloop()
