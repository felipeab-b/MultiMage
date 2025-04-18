import tkinter as tk
import core
from core import load_and_place_image, fechar_hub
from ui_1 import criar_janela

def criar_hub():
    hub = tk.Tk()
    hub.title("MultiMage")
    hub.geometry("1025x800")
    hub.config(bg = "#fbf1e2")

    core.hub = hub

    img1 = load_and_place_image("arte-corpo-inteiro.png", (750, 750), (365, 141)).config(bg = '#fbf1e2')
    img2 = load_and_place_image("name.png", (400, 400), (50, 0)).config(bd = 0)

    tk.Button(hub, text = 'Mutiplicar Imagens Numeradas', command = criar_janela, padx=20, pady=20).place(x=150,y=400)
    tk.Button(hub, text = 'Certificados, Diplomas e Documentos', padx=20, pady=20).place(x=130,y=500)
    tk.Button(hub, text = 'Sair', command = fechar_hub, padx=20, pady=20).place(x=210,y=600)

    hub.mainloop()