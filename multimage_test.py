from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import StringVar, messagebox, IntVar, filedialog, ttk
import os

def verificar_erros():
    if not texto.get():
        messagebox.showinfo('Erro', "Por favor, insira um texto válido")
        return False

    try:
        inicio = numero_inicial.get()
        final = numero_final.get()
    except tk.TclError:
        messagebox.showerror('Erro', "Valores numéricos inválidos")
        return False
    
    if inicio > final:
        messagebox.showerror('Erro', "Número inicial maior que o final")
        return False
    
    return True 

def selecionar_pasta():
    pasta = filedialog.askdirectory(title = "Selecione onde salvar as imagens")
    if pasta:
        gerar_imagem.pasta_destino = pasta
        messagebox.showinfo("Pasta selecionada", f"Imagens serão salvas em: {pasta}")

def mostrar_preview():
    if not verificar_erros():
        return
    
    valorX = eixoX.get()
    valorY = eixoY.get()
    posicao = (valorX,valorY)

    try:
        fonte_preview = ImageFont.truetype(fonte_escolhida.get(), size = tamanho_fonte.get())
    except:
        fonte_preview = fonte

    image_temp = imagem.copy()
    desenho_temp = ImageDraw.Draw(image_temp)

    texto_preview = f"{texto.get()} 001"
    desenho_temp.text(posicao,texto_preview, font = fonte_preview, fill = cor_texto.get())

    image_temp.thumbnail((350,350))
    imagem_tk = ImageTk.PhotoImage(image_temp)

    preview.config(image = imagem_tk)
    preview.image = imagem_tk

def progress_bar(total):
    janela_progresso = tk.Toplevel(janela)
    janela_progresso.title("Gerando imagens...")
    janela_progresso.geometry("300x120")

    progresso = ttk.Progressbar(janela_progresso, orient="horizontal",length=200,mode="determinate",maximum=total)
    progresso.pack(pady = 20)

    status = tk.Label(janela_progresso, text="0/%d concluído" % total)
    status.pack()

    return janela_progresso, progresso, status

def gerar_imagem():
    if not verificar_erros():
        return
    
    inicio = numero_inicial.get()
    final = numero_final.get()
    valorX = eixoX.get()
    valorY = eixoY.get()
    posicao = (valorX,valorY)
    total_de_imagens = final - inicio + 1

    janela_progresso, progresso, status = progress_bar(total_de_imagens)

    try:
        fonte_atual = ImageFont.truetype('arial.ttf', size = tamanho_fonte.get())
    except:
        fonte_atual = fonte

    try:
        cor_texto_atual = cor_texto.get()
    except:
        cor_texto_atual = 'black'

    try:
        for i, num in enumerate(range(inicio,final + 1)):
            progresso['value'] = i + 1
            status.config(text=f"{i+1}/{total_de_imagens} concluído")
            janela_progresso.update()

            numero_formatado = str(num).zfill(3)
            texto_final = f"{texto.get()} {numero_formatado}"

            imagem_temp = imagem.copy()
            desenho_temp = ImageDraw.Draw(imagem_temp)
            desenho_temp.text(posicao, texto_final, font = fonte_atual, fill = cor_texto_atual)

            caminho = os.path.join(gerar_imagem.pasta_destino, f"imagem_{numero_formatado}.jpg")
            imagem_temp.save(caminho)
        
    except PermissionError:
        messagebox.showerror('Erro', "Sem permissão para salvar nessa pasta") 
    except Exception as e:
        messagebox.showerror('Erro', f"Falha ao gerar imagens: {str(e)}")
    finally:
        janela_progresso.destroy()
        if 'e' not in locals() or isinstance(e, (PermissionError, Exception)):
            messagebox.showinfo('Sucesso', f"{total_de_imagens} imagens geradas com sucesso!")
        janela.destroy()

janela = tk.Tk()
janela.title("MultiMage")
janela.geometry("1025x350")

try:
    imagem = Image.open("fundo_para_testes.jpg")
    desenho = ImageDraw.Draw(imagem)
    fonte = ImageFont.truetype("arial.ttf", size = 200)
except Exception as e:
    messagebox.showerror('Erro', f"Falha ao carregar recursos: {str(e)}")
    janela.destroy()
    exit()

texto = StringVar()
numero_inicial = IntVar(value = 1)
numero_final = IntVar(value = 10)
eixoX = IntVar(value = 100)
eixoY = IntVar(value = 100)
cor_texto = StringVar(value = 'black')
tamanho_fonte = IntVar(value = 100)
fontes_disponiveis = ["arial.ttf", "cour.ttf", "time.ttf"]
fonte_escolhida = StringVar(value = fontes_disponiveis[0])

config_div = tk.LabelFrame(janela, text = 'Configurações', padx = 10, pady = 10)
config_div.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = 'n')

preview_div = tk.LabelFrame(janela, text = 'Preview', padx = 10, pady = 10)
preview_div.grid(row = 0, column = 1, padx = 20, pady = 10)

btn_div = tk.Frame(janela)
btn_div.grid(row = 1, column= 0, columnspan=2, pady = 20)

tk.Label(config_div,text = "Texto base:").grid(row = 0, column=0,sticky='w')
tk.Entry(config_div,textvariable = texto,width = 50,bd = 2).grid(row = 0, column=1)

tk.Label(config_div, text = "Escolha a cor do texto:").grid(row=1, column=0, sticky="w")
tk.Entry(config_div, textvariable = cor_texto,).grid(row=1, column=1)

tk.Label(config_div, text = "Escolha o tamanho da fonte:").grid(row=2, column=0, sticky="w")
tk.Entry(config_div, textvariable = tamanho_fonte,).grid(row=2, column=1)

tk.Label(config_div, text = "Escolha a fonte:").grid(row=3, column=0, sticky="w")
ttk.Combobox(config_div, textvariable = fonte_escolhida, values = fontes_disponiveis, state = 'readonly').grid(row=3, column=1)

tk.Label(config_div, text = "Número inicial:").grid(row=4, column=0, sticky="w")
tk.Entry(config_div, textvariable = numero_inicial).grid(row=4, column=1)

tk.Label(config_div, text = "Número Final:").grid(row=5, column=0, sticky="w")
tk.Entry(config_div, textvariable = numero_final).grid(row=5, column=1)

tk.Label(config_div, text = "Posição horizontal (px):").grid(row=6, column=0, sticky="w")
tk.Entry(config_div, textvariable = eixoX).grid(row=6, column=1)

tk.Label(config_div, text = "Posição vertical (px):").grid(row=7, column=0, sticky="w")
tk.Entry(config_div, textvariable = eixoY).grid(row=7, column=1)

preview = tk.Label(preview_div)
preview.pack()

tk.Button(btn_div,text = 'Selecionar Pasta',command = selecionar_pasta).grid(row=0, column=0, padx=10)
tk.Button(btn_div,text = 'Visualizar Preview', command = mostrar_preview).grid(row=0, column=1, padx=10)
tk.Button(btn_div,text = 'Gerar Imagem',command = gerar_imagem).grid(row=0, column=2, padx=10)


janela.mainloop()
