from PIL import Image, ImageDraw, ImageFont
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
        valorX = eixoX.get()
        valorY = eixoY.get()
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
        for i, num in enumerate(range(inicio,final + 1)):
            progresso['value'] = i + 1
            status.config(text=f"{i+1}/{total_de_imagens} concluído")
            janela_progresso.update()

            numero_formatado = str(num).zfill(3)
            texto_final = f"{texto.get()} {numero_formatado}"

            imagem_temp = imagem.copy()
            desenho_temp = ImageDraw.Draw(imagem_temp)
            desenho_temp.text(posicao, texto_final, font = fonte, fill = 'black')

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
janela.geometry("400x500")

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

tk.Label(janela,text = "Texto base:").pack()
tk.Entry(janela,textvariable = texto,width = 50,bd = 2).pack(padx = 10, pady = 5)

tk.Label(janela, text = "Número inicial:").pack()
tk.Entry(janela, textvariable = numero_inicial).pack(pady = 5)

tk.Label(janela, text = "Número Final:").pack()
tk.Entry(janela, textvariable = numero_final).pack(pady = 5)

tk.Label(janela, text = "Posição horizontal (px):").pack()
tk.Entry(janela, textvariable = eixoX).pack(pady = 5)

tk.Label(janela, text = "Posição vertical (px):").pack()
tk.Entry(janela, textvariable = eixoY).pack(pady = 5)

tk.Button(janela,text = 'Selecionar Pasta',command = selecionar_pasta).pack(pady = 20)
tk.Button(janela,text = 'Gerar Imagem',command = gerar_imagem).pack(pady = 20)

janela.mainloop()
