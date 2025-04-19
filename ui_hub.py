import tkinter as tk
import core
from core import load_and_place_image, animacao_mensagem
from ui_1 import criar_janela

def criar_hub():
    hub = tk.Tk()
    hub.title("MultiMage - Início")
    hub.geometry("600x500")
    hub.resizable(width=False, height=False)
    hub.config(bg="#6050DC")

    core.hub = hub

    load_and_place_image("arte-corpo-inteiro.png", (430, 430), (170, 106)).config(bg = '#6050DC')

    texto = tk.Label(hub, text="", font=("Arial", 14), fg="white", bg="#6050DC", wraplength=500, justify="center")
    texto.pack(pady=10)

    mensagem = "Olá, jovem feiticeiro! Sou o MultiMage, seu assistente mágico para criar imagens encantadas em série. Vamos começar?"

    def mostrar_botoes():
        btn_iniciar = tk.Button(hub, text="Criar Imagens Numeradas", font=("Arial", 12, "bold"),bg="white", fg="#6050DC", command=criar_janela)
        btn_iniciar.pack(pady=10)

        btn_sair = tk.Button(hub, text="Sair", font=("Arial", 12),bg="white", fg="#6050DC", command=hub.destroy)
        btn_sair.pack(pady=5)

    animacao_mensagem(texto, mensagem, delay = 30)
    texto.after(len(mensagem) * 40 + 500, mostrar_botoes)

    hub.mainloop()