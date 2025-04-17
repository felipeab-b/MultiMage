from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import StringVar, messagebox, IntVar, filedialog, ttk
import os

imagem_base = None
posicao_inicial_arraste = None
imagem_tk = None

def iniciar_arraste(event):
    global posicao_inicial_arraste
    posicao_inicial_arraste = (eixoX.get(), eixoY.get(), event.x, event.y)

def mover_texto(event):
    global posicao_inicial_arraste
    
    if posicao_inicial_arraste:
        orig_x, orig_y, start_x, start_y = posicao_inicial_arraste
        delta_x = event.x - start_x
        delta_y = event.y - start_y
        
        eixoX.set(orig_x + delta_x)
        eixoY.set(orig_y + delta_y)

        mostrar_preview()

def finalizar_arraste(event=None):
    global posicao_inicial_arraste
    posicao_inicial_arraste = None
    mostrar_preview()

def configurar_scroll(event):
    preview.bind("<MouseWheel>", alterar_tamanho_fonte)

def alterar_tamanho_fonte(event):
        if not event.state & 0x0004:
            return
        
        scroll_direction = event.delta

        change = 1 if scroll_direction > 0 else -1

        current_size = tamanho_fonte.get()
        new_size = current_size + (5 * change)
        new_size = max(10, min(200, new_size))

        tamanho_fonte.set(new_size)

        mostrar_preview()

try:
    fonte = ImageFont.truetype("arial.ttf", size=100)
except:
    fonte = ImageFont.load_default()

def verificar_erros(ignorar_erro=None):
    if ignorar_erro != 'texto_vazio':
        if not texto.get():
            messagebox.showinfo('Erro', "Por favor, insira um texto válido")
            return False

    if ignorar_erro != 'valores_numericos':
        try:
            inicio = numero_inicial.get()
            final = numero_final.get()
        except tk.TclError:
            messagebox.showerror('Erro', "Valores numéricos inválidos")
            return False
    
    if ignorar_erro != 'intervalo_invalido':
        if inicio > final:
            messagebox.showerror('Erro', "Número inicial maior que o final")
            return False
    
    return True 

def selecionar_pasta():
    pasta = filedialog.askdirectory(title = "Selecione onde salvar as imagens")
    if pasta:
        gerar_imagem.pasta_destino = pasta
        messagebox.showinfo("Pasta selecionada", f"Imagens serão salvas em: {pasta}")

def mostrar_preview(event = None):
    if not verificar_erros('texto_vazio'):
        return
    
    valorX = eixoX.get()
    valorY = eixoY.get()
    posicao = (valorX,valorY)

    try:
        fonte_preview = ImageFont.truetype(fonte_escolhida.get(), size = tamanho_fonte.get())
    except:
        fonte_preview = fonte

    if imagem_base is None:
        messagebox.showwarning("Aviso", "Nenhuma imagem foi selecionada ainda.")
        return

    image_temp = imagem_base.copy()
    desenho_temp = ImageDraw.Draw(image_temp)

    texto_preview = f"{texto.get()} 001"
    desenho_temp.text(posicao,texto_preview, font = fonte_preview, fill = cor_texto.get())

    image_temp.thumbnail((350,350))
    global imagem_tk
    imagem_tk = ImageTk.PhotoImage(image_temp)

    preview.config(image = imagem_tk)
    preview.image = imagem_tk

def selecionar_imagem():
    global imagem_base
    caminho = filedialog.askopenfilename(title="Selecione a imagem base", filetypes=[("Imagens", "*.jpg;*.png;*.jpeg;*.bmp")])
    if caminho:
        try:
            imagem_base = Image.open(caminho)
            mostrar_preview()
            messagebox.showinfo('Imagem selecionada', "Imagem carregada com sucesso!")
        except Exception as e:
            messagebox.showerror('Erro', f"Erro ao abrir imagem: {str(e)}")

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

            if imagem_base is None:
                messagebox.showwarning('Aviso',"Nenhuma imagem foi selecionada ainda.")
                return

            imagem_temp = imagem_base.copy()
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

tk.Button(btn_div,text = 'Selecionar Imagem', command = selecionar_imagem).grid(row=0, column=0, padx=10)
tk.Button(btn_div,text = 'Visualizar Preview', command = mostrar_preview).grid(row=0, column=1, padx=10)
tk.Button(btn_div,text = 'Selecionar Pasta',command = selecionar_pasta).grid(row=0, column=2, padx=10)
tk.Button(btn_div,text = 'Gerar Imagem',command = gerar_imagem).grid(row=0, column=3, padx=10)

preview.bind("<Button-1>", iniciar_arraste)
preview.bind("<B1-Motion>",mover_texto)
preview.bind("<ButtonRelease-1>",finalizar_arraste)
preview.bind("<Enter>", configurar_scroll)

janela.mainloop()
