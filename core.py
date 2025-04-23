from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk,StringVar,IntVar,BooleanVar,Entry,Label,Checkbutton
import os
from pathlib import Path

imagem_base = None
posicao_inicial_arraste = None
imagem_tk = None

texto = None
numero_de_copias = None
eixoX = None
eixoY = None
cor_texto = None
tamanho_fonte = None
fontes_disponiveis = None
fonte_escolhida = None
preview = None
janela = None
hub = None
mostrar_numeraçao = None

class BlocoTexto:
    def __init__(self,texto,x,y,cor,tamanho,fonte,numerado):
        self.texto = texto
        self.x = x
        self.y = y
        self.cor = cor
        self.tamanho = tamanho
        self.fonte = fonte
        self.numerado = numerado

bloco_de_texto = []

def botao_texto():
    botao_texto = tk.Toplevel(janela)
    botao_texto.title("Adicionar texto")
    botao_texto.geometry("350x350")
    botao_texto.resizable(width=False, height=False)

    texto_var = StringVar()
    x_var = IntVar(value=100)
    y_var = IntVar(value=100)
    cor_var = StringVar(value="black")
    tamanho_var = IntVar(value=100)
    fontes = ["arial.ttf", "cour.ttf", "times.ttf"]
    fonte_var = StringVar(value=fontes[0])
    numerado_var = BooleanVar(value=False)

    Label(botao_texto, text="Texto:").pack()
    Entry(botao_texto, textvariable=texto_var).pack()

    Label(botao_texto, text="Posição X:").pack()
    Entry(botao_texto, textvariable=x_var).pack()

    Label(botao_texto, text="Posição Y:").pack()
    Entry(botao_texto, textvariable=y_var).pack()

    Label(botao_texto, text="Cor do texto:").pack()
    Entry(botao_texto, textvariable=cor_var).pack()

    Label(botao_texto, text="Tamanho da fonte:").pack()
    Entry(botao_texto, textvariable=tamanho_var).pack()

    Label(botao_texto, text="Fonte:").pack()
    ttk.Combobox(botao_texto, textvariable=fonte_var, values=fontes, state="readonly").pack()

    Checkbutton(botao_texto, text="Incluir numeração", variable=numerado_var).pack(pady=10)

    def adicionar_bloco():
        bloco = BlocoTexto(
            texto=texto_var.get(),
            x=x_var.get(),
            y=y_var.get(),
            cor=cor_var.get(),
            tamanho=tamanho_var.get(),
            fonte=fonte_var.get(),
            numerado=numerado_var.get()
        )
        bloco_de_texto.append(bloco)
        botao_texto.destroy()

    tk.Button(botao_texto, text="Adicionar Bloco", command=adicionar_bloco).pack(pady=20)

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
        new_size = max(10, min(500, new_size))

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
            copias = numero_de_copias.get()
        except tk.TclError:
            messagebox.showerror('Erro', "Valores numéricos inválidos")
            return False
    
    return True 

def selecionar_pasta():
    pasta = filedialog.askdirectory(title = "Selecione onde salvar as imagens")
    if pasta:
        gerar_imagem.pasta_destino = pasta
        messagebox.showinfo("Pasta selecionada", f"Imagens serão salvas em: {pasta}")

def mostrar_preview(event = None):
    global imagem_tk

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

    if mostrar_numeraçao.get():
        texto_preview = f"{texto.get()} 001"
    else:
        texto_preview = f"{texto.get()}"
    desenho_temp.text(posicao,texto_preview, font = fonte_preview, fill = cor_texto.get())

    image_temp.thumbnail((350,350))
    imagem_tk = ImageTk.PhotoImage(image_temp)

    preview.config(image = imagem_tk)
    preview.image = imagem_tk

    return image_temp

def selecionar_imagem():
    global imagem_base

    caminho = filedialog.askopenfilename(title="Selecione a imagem base", filetypes=[("Imagens", "*.jpg;*.png;*.jpeg;*.bmp")])
    
    if caminho:
        try:
            imagem_base = Image.open(caminho)
            image_temp = mostrar_preview()

            largura, altura = image_temp.size
            new_largura = largura + 700
            new_altura = altura + 150
            janela.geometry(f"{new_largura}x{new_altura}")
            janela.resizable(width=False, height=False)   
             
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
    
    copias = numero_de_copias.get()
    valorX = eixoX.get()
    valorY = eixoY.get()
    posicao = (valorX,valorY)
    total_de_imagens = copias

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
        for i, num in enumerate(range(copias)):
            progresso['value'] = i + 1
            status.config(text=f"{i+1}/{total_de_imagens} concluído")
            janela_progresso.update()

            numero_formatado = str(num).zfill(3)
            if mostrar_numeraçao.get():
                texto_final = f"{texto.get()} {numero_formatado}"
            else:
                texto_final = f"{texto.get()}"

            if imagem_base is None:
                messagebox.showwarning('Aviso',"Nenhuma imagem foi selecionada ainda.")
                return

            imagem_temp = imagem_base.copy()
            desenho_temp = ImageDraw.Draw(imagem_temp)
            desenho_temp.text(posicao, texto_final, font = fonte_atual, fill = cor_texto_atual)

            if imagem_temp.mode == 'RGBA':
                imagem_temp = imagem_temp.convert('RGB')

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

def load_and_place_image(image_name,size,pos,bg_color="#864cbc"):
        image_path = Path("assets") / image_name
        img = Image.open(image_path)
        img = img.resize(size, Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        
        label = tk.Label(hub, image=tk_img, bg=bg_color)
        label.image = tk_img  # Mantém referência
        label.place(x=pos[0], y=pos[1])
        return label

def animacao_mensagem(label, texto, delay=50):
    def escrever(i=0):
        if i < len(texto):
            label.config(text=label.cget("text") + texto[i])
            label.after(delay, escrever, i + 1)
    label.config(text="")
    escrever()

def fechar_hub():
    hub.destroy()
