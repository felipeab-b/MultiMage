import tkinter as tk
from tkinter import StringVar, IntVar, ttk
from core import fechar_hub
import core

COLOR_PRIMARY = "#6050DC"
COLOR_SECONDARY = "#A890FE"
COLOR_LIGHT_BG = "#F4F2FF"
COLOR_DARK_TEXT = "#2D2A4A"

def criar_janela():

    fechar_hub()

    janela = tk.Tk()
    janela.title("MultiMage")
    janela.geometry("1025x350")
    janela.config(bg = COLOR_LIGHT_BG)

    core.janela = janela

    core.texto = StringVar()
    core.numero_inicial = IntVar(value = 1)
    core.numero_final = IntVar(value = 10)
    core.eixoX = IntVar(value = 100)
    core.eixoY = IntVar(value = 100)
    core.cor_texto = StringVar(value = 'black')
    core.tamanho_fonte = IntVar(value = 100)
    core.fontes_disponiveis = ["arial.ttf", "cour.ttf", "time.ttf"]
    core.fonte_escolhida = StringVar(value = core.fontes_disponiveis[0])

    config_div = tk.LabelFrame(janela, text = 'Configurações', padx = 10, pady = 10, bg=COLOR_LIGHT_BG, fg=COLOR_PRIMARY)
    config_div.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = 'n')

    preview_div = tk.LabelFrame(janela, text = 'Preview', padx = 10, pady = 10, bg = COLOR_LIGHT_BG, fg = COLOR_PRIMARY)
    preview_div.grid(row = 0, column = 1, padx = 20, pady = 10)

    btn_div = tk.Frame(janela, bg=COLOR_LIGHT_BG)
    btn_div.grid(row = 1, column= 0, columnspan=2, pady = 20)

    tk.Label(config_div,text = "Texto base:", bg=COLOR_LIGHT_BG, fg=COLOR_DARK_TEXT).grid(row = 0, column=0,sticky='w')
    tk.Entry(config_div,textvariable = core.texto,width = 50,bd = 2, bg='white', fg=COLOR_DARK_TEXT).grid(row = 0, column=1)

    tk.Label(config_div, text = "Escolha a cor do texto:", bg=COLOR_LIGHT_BG, fg=COLOR_DARK_TEXT).grid(row=1, column=0, sticky="w")
    tk.Entry(config_div, textvariable = core.cor_texto, bg='white', fg=COLOR_DARK_TEXT).grid(row=1, column=1)

    tk.Label(config_div, text = "Escolha o tamanho da fonte:", bg=COLOR_LIGHT_BG, fg=COLOR_DARK_TEXT).grid(row=2, column=0, sticky="w")
    tk.Entry(config_div, textvariable = core.tamanho_fonte, bg='white', fg=COLOR_DARK_TEXT).grid(row=2, column=1)

    tk.Label(config_div, text = "Escolha a fonte:", bg=COLOR_LIGHT_BG, fg=COLOR_DARK_TEXT).grid(row=3, column=0, sticky="w")
    ttk.Combobox(config_div, textvariable = core.fonte_escolhida, values = core.fontes_disponiveis, state = 'readonly').grid(row=3, column=1)

    tk.Label(config_div, text = "Número inicial:", bg=COLOR_LIGHT_BG, fg=COLOR_DARK_TEXT).grid(row=4, column=0, sticky="w")
    tk.Entry(config_div, textvariable = core.numero_inicial, bg='white', fg=COLOR_DARK_TEXT).grid(row=4, column=1)

    tk.Label(config_div, text = "Número Final:", bg=COLOR_LIGHT_BG, fg=COLOR_DARK_TEXT).grid(row=5, column=0, sticky="w")
    tk.Entry(config_div, textvariable = core.numero_final, bg='white', fg=COLOR_DARK_TEXT).grid(row=5, column=1)

    tk.Label(config_div, text = "Posição horizontal (px):", bg=COLOR_LIGHT_BG, fg=COLOR_DARK_TEXT).grid(row=6, column=0, sticky="w")
    tk.Entry(config_div, textvariable = core.eixoX, bg='white', fg=COLOR_DARK_TEXT).grid(row=6, column=1)

    tk.Label(config_div, text = "Posição vertical (px):", bg=COLOR_LIGHT_BG, fg=COLOR_DARK_TEXT).grid(row=7, column=0, sticky="w")
    tk.Entry(config_div, textvariable = core.eixoY, bg='white', fg=COLOR_DARK_TEXT).grid(row=7, column=1)

    core.preview = tk.Label(preview_div, bg = 'white')
    core.preview.pack()

    tk.Button(btn_div,text = 'Selecionar Imagem', command = core.selecionar_imagem,bg=COLOR_PRIMARY, fg=COLOR_LIGHT_BG, font=('Arial', 10, 'bold'), bd=0
              ).grid(row=0, column=0, padx=10)
    tk.Button(btn_div,text = 'Selecionar Pasta',command = core.selecionar_pasta,bg=COLOR_PRIMARY, fg=COLOR_LIGHT_BG, font=('Arial', 10, 'bold'), bd=0
              ).grid(row=0, column=1, padx=10)
    tk.Button(btn_div,text = 'Gerar Imagem',command = core.gerar_imagem,bg=COLOR_PRIMARY, fg=COLOR_LIGHT_BG, font=('Arial', 10, 'bold'), bd=0
              ).grid(row=0, column=2, padx=10)

    core.preview.bind("<Button-1>", core.iniciar_arraste)
    core.preview.bind("<B1-Motion>", core.mover_texto)
    core.preview.bind("<ButtonRelease-1>", core.finalizar_arraste)
    core.preview.bind("<Enter>", core.configurar_scroll)

    janela.mainloop()