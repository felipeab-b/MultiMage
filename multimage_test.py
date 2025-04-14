from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import StringVar

janela = tk.Tk()
janela.geometry("400x400")

#Abre a imagem base
imagem = Image.open("fundo_para_testes.jpg")

#Cria um objeto de desenho, "pincel"
desenho = ImageDraw.Draw(imagem)

#Define a fonte e o tamanho
fonte = ImageFont.truetype("arial.ttf", size = 200)

#texto = input('') //teste para entrada de dados 
#texto = '001' //teste de adiconar texto
texto = StringVar()
tk.Entry(
    janela,
    textvariable = texto,
    width = 50,
    bd = 2
    ).pack(pady = 10)

posicao = (300,200)

def fechar():
    janela.destroy()
    desenho.text(posicao, texto.get(), font = fonte, fill = "black")
    imagem.save("imagem_editada.jpg")
    print("Imagem gerada com sucesso !!")

tk.Button(
    janela,
    text = 'Gerar Imagem',
    command = fechar
).pack(pady = 20)

janela.mainloop()

#Escreve o texto na imagem e salva
