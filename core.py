from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk,StringVar,IntVar,BooleanVar,Entry,Label,Checkbutton, colorchooser
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
bloco_de_texto_select = None

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

def botao_texto(bloco_editar=None):
    botao_texto = tk.Toplevel(janela)
    botao_texto.title("Adicionar texto" if bloco_editar is None else "Editar ")
    botao_texto.geometry("350x450")
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

    label_cor = Label(botao_texto, text="Cor do texto:")
    label_cor.pack()

    btn_select_cor = tk.Button(
        botao_texto,
        text="Escolher Cor",
        command=lambda: abrir_seletor_de_cores(cor_var)
    )
    btn_select_cor.pack()

    preview_cor = Label(botao_texto,textvariable=cor_var, width=10, relief="solid", bd=1)
    preview_cor.pack()

    def atualizar_preview_cores(*args):
        try:
            preview_cor.config(bg=cor_var.get(), fg="white" if cor_var.get() in ["black","navy","maroon"] else "black")
        except tk.TclError:
            preview_cor.config(bg="white",fg="black")
    
    cor_var.trace_add("write", atualizar_preview_cores)
    atualizar_preview_cores()

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
        mostrar_preview()

    tk.Button(botao_texto, text="Adicionar Bloco", command=adicionar_bloco).pack(pady=20)

def iniciar_arraste(event):
    global posicao_clique, bloco_de_texto_select
    selecionar_bloco(event)
    if bloco_de_texto_select:
        posicao_clique = (event.x, event.y)
    else:
        posicao_clique = None

def mover_texto(event):
    global posicao_clique, bloco_de_texto_select
    
    if posicao_clique and bloco_de_texto_select:
        delta_x = int((event.x - posicao_clique[0]) * preview.escala_x)
        delta_y = int((event.y - posicao_clique[1]) * preview.escala_y)

        bloco_de_texto_select.x += delta_x
        bloco_de_texto_select.y += delta_y

        posicao_clique = (event.x, event.y)
        mostrar_preview()

def finalizar_arraste(event=None):
    global posicao_clique
    posicao_clique = None
    mostrar_preview()

def alterar_tamanho_fonte(event):
    #print(
    #    f"[DEBUG SCROLL] state={event.state}, "
    #   f"num={getattr(event, 'num', '-')}, "
    #    f"delta={getattr(event, 'delta', '-')}, "
    #   f"type={event.type}")

    global bloco_de_texto_select

    if not bloco_de_texto_select:
        return

    ctrl = event.state & 0x4

    if ctrl:
        if hasattr(event, "num"):  # Linux
            if event.num == 4:
                bloco_de_texto_select.tamanho += 5
            elif event.num == 5 and bloco_de_texto_select.tamanho > 5:
                bloco_de_texto_select.tamanho -= 5

        elif hasattr(event, "delta"):  # Windows
            if event.delta > 0:
                bloco_de_texto_select.tamanho += 5
            elif event.delta < 0 and bloco_de_texto_select.tamanho > 5:
                bloco_de_texto_select.tamanho -= 5

        mostrar_preview()

    #print(f"[DEBUG TAMANHO] Novo tamanho: {bloco_de_texto_select.tamanho}")

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

def get_font(font_path, size):
    try:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size=size)
        elif os.path.exists(os.path.join("fonts", font_path)):
            return ImageFont.truetype(os.path.join("fonts",font_path),size=size)
        else:
            #messagebox.showerror('Erro', f"A fonte '{font_path}' não foi encontrada. Usando a fonte padrão")
            return ImageFont.load_default(size=size)
    except Exception as e:
        #messagebox.showerror('Erro', f"A fonte '{font_path}':{e}. não foi encontrada. Usando a fonte padrão")
        return ImageFont.load_default(size=size)

def mostrar_preview(event = None):
    global imagem_tk, bloco_de_texto_select

    if not verificar_erros('texto_vazio'):
        return

    if imagem_base is None:
        messagebox.showwarning("Aviso", "Nenhuma imagem foi selecionada ainda.")
        return

    image_temp = imagem_base.copy()
    desenho_temp = ImageDraw.Draw(image_temp)

    for bloco in bloco_de_texto:

        fonte_bloco = get_font(bloco.fonte, bloco.tamanho)
        #print(f"Tamanho da fonte: {bloco.tamanho}")
        #print(f"fonte: {bloco.fonte}")

        texto_render = bloco.texto
        if bloco.numerado:
            texto_render += "001"

        desenho_temp.text((bloco.x, bloco.y), texto_render, font = fonte_bloco, fill = bloco.cor)

        if bloco == bloco_de_texto_select:
            x1,y1,x2,y2 = desenho_temp.textbbox((bloco.x, bloco.y), texto_render, font=fonte_bloco)
            padding = 5
            desenho_temp.rectangle((x1 - padding, y1- padding, x2 + padding, y2 + padding),outline="red",width=1)

    image_temp.thumbnail((350,350))
    imagem_tk = ImageTk.PhotoImage(image_temp)

    largura_original, altura_original = imagem_base.size
    largura_preview, altura_preview = image_temp.size
    escala_x = largura_original / largura_preview
    escala_y = altura_original / altura_preview
    preview.escala_x = escala_x
    preview.escala_y = escala_y

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
    total_de_imagens = copias

    janela_progresso, progresso, status = progress_bar(total_de_imagens)

    try:
        for i in enumerate(range(copias)):
            progresso['value'] = i + 1
            status.config(text=f"{i+1}/{total_de_imagens} concluído")
            janela_progresso.update()

            if imagem_base is None:
                messagebox.showwarning('Aviso',"Nenhuma imagem foi selecionada ainda.")
                return

            imagem_temp = imagem_base.copy()
            desenho_temp = ImageDraw.Draw(imagem_temp)
            for bloco in bloco_de_texto:
                try:
                    fonte_bloco = ImageFont.truetype(bloco.fonte, bloco.tamanho)
                except:
                    fonte_bloco = get_font(bloco.fonte, bloco.tamanho)

                texto_render = bloco.texto
                if bloco.numerado:
                    texto_render += f" {str(i).zfill(3)}"

                desenho_temp.text((bloco.x, bloco.y), texto_render, font=fonte_bloco, fill=bloco.cor)

            if imagem_temp.mode == 'RGBA':
                imagem_temp = imagem_temp.convert('RGB')

            caminho = os.path.join(gerar_imagem.pasta_destino, f"imagem_{str(i).zfill(3)}.jpg")
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
        label.image = tk_img  
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

def selecionar_bloco(event):
    global bloco_de_texto_select

    click_x = int(event.x * preview.escala_x)
    click_y = int(event.y * preview.escala_y)

    bloco_de_texto_select_now = None

    img_temporaria = Image.new('RGB', imagem_base.size, (255,255,255))
    draw_temporario = ImageDraw.Draw(img_temporaria)

    for bloco in reversed(bloco_de_texto):
        fonte_bloco = get_font(bloco.fonte, bloco.tamanho)

        x1, y1, x2, y2 = draw_temporario.textbbox((bloco.x, bloco.y), bloco.texto, font=fonte_bloco)

        padding = 5
        x1 -= padding
        y1 -= padding
        x2 += padding
        y2 += padding

        if x1 <= click_x <= x2 and y1 <= click_y <= y2:
            bloco_de_texto_select_now = bloco
            break
    
    if bloco_de_texto_select_now != bloco_de_texto_select:
        bloco_de_texto_select = bloco_de_texto_select_now
        mostrar_preview()

def remover_bloco(event=None):
    global bloco_de_texto_select

    if bloco_de_texto_select:
        messagebox.askyesno("Confirmar Remoção", "Tem certeza que deseja remover esse texto?")
        bloco_de_texto.remove(bloco_de_texto_select)
        bloco_de_texto_select = None
        mostrar_preview()
        messagebox.showinfo("Removido", "Texto removido com sucesso!")
    else:
        messagebox.showinfo("Nenhum texto selecionado", "Por favor selecione um bloco de texto para remoção")

def abrir_seletor_de_cores(cor_var_destino):
    cor_codigo = colorchooser.askcolor(title="Selecione a cor do texto")
    if cor_codigo[1]:
        cor_var_destino.set(cor_codigo[1])
