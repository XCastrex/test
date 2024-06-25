import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Configurações iniciais do jogo
jogadorIn = True
dealerIn = True
baralho = [2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10,
           'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A']
maoJogador = []
maoDealer = []

# Dicionário para mapear cartas a imagens
imagens_cartas = {}

# Carregar imagens das cartas
def carregar_imagens():
    naipes = ['hearts', 'diamonds', 'clubs', 'spades']
    valores = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    for naipe in naipes:
        for valor in valores:
            nome_arquivo = f'images/{valor}_of_{naipe}.png'  # Ajuste o caminho conforme necessário
            if os.path.exists(nome_arquivo):
                imagem = Image.open(nome_arquivo)
                imagem = imagem.resize((100, 150), Image.LANCZOS)  # Redimensiona a imagem
                imagens_cartas[f'{valor}{naipe[0].upper()}'] = ImageTk.PhotoImage(imagem)
            else:
                print(f"Arquivo de imagem não encontrado: {nome_arquivo}")

# Função para distribuir uma carta a um turno (jogador ou dealer)
def distribuirCarta(turno):
    carta = random.choice(baralho)  # Seleciona uma carta aleatória do baralho
    turno.append(carta)  # Adiciona a carta ao turno (mão do jogador ou dealer)
    baralho.remove(carta)  # Remove a carta do baralho

# Função para calcular o total da mão de um turno
def total(turno):
    total = 0
    ases = 0
    for carta in turno:
        if isinstance(carta, int):  # Se a carta for um número entre 2 e 10
            total += carta
        elif carta in ['J', 'K', 'Q']:  # Se a carta for uma das figuras
            total += 10
        else:  # Se a carta for um Ás
            total += 11
            ases += 1
    while ases and total > 21:  # Ajusta o valor do Ás de 11 para 1 se necessário
        total -= 10
        ases -= 1
    return total

# Função para revelar a mão do dealer
def revelarMaoDealer():
    if len(maoDealer) == 2:
        return [maoDealer[0], 'X']  # Mostra uma carta oculta se o dealer tiver duas cartas
    elif len(maoDealer) > 2:
        return maoDealer[:2]  # Mostra as duas primeiras cartas se o dealer tiver mais de duas

# Função para iniciar um novo jogo
def Novo_jogo():
    global jogadorIn, dealerIn, baralho, maoJogador, maoDealer
    jogadorIn = True
    dealerIn = True
    baralho = [2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10,
               'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A']  # Reinicia o baralho
    maoJogador = []
    maoDealer = []
    for i in range(2):  # Distribui duas cartas para o jogador e duas para o dealer
        distribuirCarta(maoDealer)
        distribuirCarta(maoJogador)
    atualizar_interface()

# Função para atualizar a interface gráfica
def atualizar_interface():
    dealer_frame.destroy()
    jogador_frame.destroy()
    
    criar_frames_cartas()
    
    # Adiciona cartas do dealer (esconde a segunda carta)
    for i, carta in enumerate(maoDealer):
        if i == 1 and dealerIn:
            adicionar_carta(dealer_frame, 'X')
        else:
            adicionar_carta(dealer_frame, carta)
    
    # Adiciona cartas do jogador
    for carta in maoJogador:
        adicionar_carta(jogador_frame, carta)

    dealer_cartas.set(f'Dealer: {revelarMaoDealer()}')  # Atualiza a exibição das cartas do dealer
    jogador_cartas.set(f'Tu tens: {maoJogador} para um total de {total(maoJogador)}')  # Atualiza a exibição das cartas do jogador

# Função para adicionar uma carta a um frame
def adicionar_carta(frame, carta):
    if carta == 'X':
        imagem = Image.open('images/back_of_card.png')  # Imagem da carta oculta
        imagem = imagem.resize((100, 150), Image.LANCZOS)
        carta_oculta = ImageTk.PhotoImage(imagem)
        label = tk.Label(frame, image=carta_oculta)
        label.image = carta_oculta  # Mantém a referência da imagem
        label.pack(side='left')
    else:
        if isinstance(carta, int):  # Para cartas numéricas
            naipe = random.choice(['H', 'D', 'C', 'S'])  # Escolhe um naipe aleatório
            chave_carta = f'{carta}{naipe}'
            if chave_carta in imagens_cartas:
                label = tk.Label(frame, image=imagens_cartas[chave_carta])
                label.pack(side='left')
        else:  # Para figuras e Ás
            naipe = random.choice(['H', 'D', 'C', 'S'])  # Escolhe um naipe aleatório
            chave_carta = f'{carta}{naipe}'
            if chave_carta in imagens_cartas:
                label = tk.Label(frame, image=imagens_cartas[chave_carta])
                label.pack(side='left')

# Função para o jogador bater (receber uma nova carta)
def bater():
    global jogadorIn
    if jogadorIn:
        distribuirCarta(maoJogador)  # Distribui uma nova carta ao jogador
        if total(maoJogador) >= 21:  # Verifica se o total do jogador é 21 ou mais
            jogadorIn = False
        atualizar_interface()
        verificar_resultado()  # Verifica o resultado do jogo

# Função para o jogador ficar (parar de receber cartas)
def ficar():
    global jogadorIn, dealerIn
    jogadorIn = False
    while total(maoDealer) < 17:  # O dealer continua comprando cartas até o total ser pelo menos 17
        distribuirCarta(maoDealer)
    dealerIn = False
    atualizar_interface()
    verificar_resultado()  # Verifica o resultado do jogo

# Função para verificar o resultado do jogo
def verificar_resultado():
    if total(maoJogador) == 21:
        messagebox.showinfo("Resultado", f'Blackjack! Tu ganhaste!\n{resultado_mensagem()}')
    elif total(maoDealer) == 21:
        messagebox.showinfo("Resultado", f'Blackjack! Dealer ganhou!\n{resultado_mensagem()}')
    elif total(maoJogador) > 21:
        messagebox.showinfo("Resultado", f'Arrebentaste! Dealer ganhou!\n{resultado_mensagem()}')
    elif total(maoDealer) > 21:
        messagebox.showinfo("Resultado", f'Dealer arrebentou! Tu ganhaste!\n{resultado_mensagem()}')
    elif not jogadorIn and not dealerIn:
        if 21 - total(maoDealer) < 21 - total(maoJogador):
            messagebox.showinfo("Resultado", f'Dealer ganhou!\n{resultado_mensagem()}')
        else:
            messagebox.showinfo("Resultado", f'Tu ganhaste!\n{resultado_mensagem()}')

# Função para formatar a mensagem de resultado
def resultado_mensagem():
    return f'Tu tens {maoJogador} para um total de {total(maoJogador)} e o dealer tem {maoDealer} para um total de {total(maoDealer)}'

# Configuração da interface gráfica
root = tk.Tk()
root.title("Jogo de Blackjack")
root.geometry("800x600")  # Aumenta o tamanho da janela

# Variáveis de interface para exibir as cartas do dealer e do jogador
dealer_cartas = tk.StringVar()
jogador_cartas = tk.StringVar()

carregar_imagens()

# Função para criar os frames das cartas
def criar_frames_cartas():
    global dealer_frame, jogador_frame
    dealer_frame = tk.Frame(root)
    dealer_frame.pack(pady=20)
    jogador_frame = tk.Frame(root)
    jogador_frame.pack(pady=20)

# Botões de controle do jogo
btn_novo_jogo = tk.Button(root, text="Novo Jogo", command=Novo_jogo)
btn_novo_jogo.pack(pady=10)

btn_bater = tk.Button(root, text="Bater", command=bater)
btn_bater.pack(pady=10)

btn_ficar = tk.Button(root, text="Ficar", command=ficar)
btn_ficar.pack(pady=10)

# Labels para exibir as cartas
label_dealer_cartas = tk.Label(root, textvariable=dealer_cartas)
label_dealer_cartas.pack(pady=10)

label_jogador_cartas = tk.Label(root, textvariable=jogador_cartas)
label_jogador_cartas.pack(pady=10)

# Cria os frames iniciais das cartas
criar_frames_cartas()

root.mainloop()
