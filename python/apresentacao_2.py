import csv
from datetime import datetime
import mcpi.minecraft as minecraft
import mcpi.block as block
from math import *
import serial
import time
import os
import sys
import io

# Força codificação UTF-8 no console do Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configurações
MINECRAFT_HOST = "26.127.43.27"  # IP do servidor via Radmin VPN
MINECRAFT_PORT = 4711  # Porta do RaspberryJuice
ARDUINO_PORT = "COM5"  # Ajuste para sua porta (ex: '/dev/ttyUSB0' no Linux)
ARDUINO_BAUDRATE = 9600
LOG_FILE = "logs/encenacao_nfc_log.csv"

# Configurações da encenação (TODOS NA MESMA COORDENADA BASE PARA SOBREPOSIÇÃO)
BASE_X, BASE_Y, BASE_Z = 445, 72, -419
PORTA_X, PORTA_Y, PORTA_Z = BASE_X, BASE_Y, BASE_Z  # Posição da porta
ARCO_X, ARCO_Y, ARCO_Z = BASE_X, BASE_Y, BASE_Z    # Posição do arco-íris
ESTRELA_X, ESTRELA_Y, ESTRELA_Z = BASE_X, BASE_Y, BASE_Z  # Posição da estrela

# Dimensões da porta (2 blocos de largura por 3 blocos de altura)
PORTA_LARGURA = 2
PORTA_ALTURA = 3
PORTA_MATERIAL = block.IRON_BLOCK.id
MOLDURA_MATERIAL = block.STONE_BRICK.id

# Inicializa o CSV de logs
def inicializar_log():
    if not os.path.exists(LOG_FILE):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Timestamp", "Status", "Detalhes"])
    print(f"[INFO] Arquivo de log inicializado em {LOG_FILE}")

# Função para registrar log
def registrar_log(status, detalhes):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, status, detalhes])
        print(f"[{timestamp}] {status}: {detalhes}")
    except Exception as e:
        print(f"[ERROR] Falha ao registrar log: {e}")

# Função para criar a porta de encenação (MELHORADA COM MOLDURA)
def criar_porta_encenacao(mc):
    """Cria uma porta de ferro 2x3 com uma moldura de tijolos de pedra para destaque."""
    try:
        # 1. Cria a moldura (Frame) ao redor da porta (3x4)
        for y in range(-1, PORTA_ALTURA + 1):
            # Lados (x de -1 a 2)
            mc.setBlock(PORTA_X - 1, PORTA_Y + y, PORTA_Z, MOLDURA_MATERIAL)
            mc.setBlock(PORTA_X + PORTA_LARGURA, PORTA_Y + y, PORTA_Z, MOLDURA_MATERIAL)
        
        # Topo e Base
        for x in range(PORTA_LARGURA):
            mc.setBlock(PORTA_X + x, PORTA_Y - 1, PORTA_Z, MOLDURA_MATERIAL)
            mc.setBlock(PORTA_X + x, PORTA_Y + PORTA_ALTURA, PORTA_Z, MOLDURA_MATERIAL)

        # 2. Cria a porta principal (Iron Blocks)
        for y in range(PORTA_ALTURA):
            for x in range(PORTA_LARGURA):
                mc.setBlock(PORTA_X + x, PORTA_Y + y, PORTA_Z, PORTA_MATERIAL)
        
        # 3. Adiciona maçanetas (blocos de ouro)
        mc.setBlock(PORTA_X, PORTA_Y + 1, PORTA_Z, block.GOLD_BLOCK.id)
        mc.setBlock(PORTA_X + 1, PORTA_Y + 1, PORTA_Z, block.GOLD_BLOCK.id)
        
        # 4. Adiciona uma placa (Sign)
        # O bloco de sinalização deve ser colocado em uma posição onde haja um bloco sólido atrás (a moldura)
        mc.setBlock(PORTA_X + PORTA_LARGURA, PORTA_Y + 1, PORTA_Z - 1, block.SIGN.id, 0)
        
        registrar_log("DOOR", "Porta de encenação criada com moldura")
        print(f"[INFO] Porta de encenação criada em x={PORTA_X}, y={PORTA_Y}, z={PORTA_Z}")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao criar porta: {e}")
        print(f"[ERROR] Falha ao criar porta: {e}")

# Função para abrir a porta dramaticamente
def abrir_porta_dramatica(mc):
    """Abre a porta removendo o material principal, mantendo a moldura."""
    try:
        mc.postToChat("🚪 A porta está se abrindo...")
        
        # Efeito de partículas na porta
        for i in range(8):
            mc.postToChat(f"✨ Efeito mágico {i+1}/8...")
            time.sleep(0.5)  # Tempo entre cada efeito
        
        # Remove a porta (abre)
        for y in range(PORTA_ALTURA):
            for x in range(PORTA_LARGURA):
                mc.setBlock(PORTA_X + x, PORTA_Y + y, PORTA_Z, block.AIR.id) # Remove Iron Blocks
        
        mc.postToChat("🌟 A porta se abriu! O caminho está livre!")
        registrar_log("DOOR_OPEN", "Porta aberta dramaticamente")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao abrir porta: {e}")
        print(f"[ERROR] Falha ao abrir porta: {e}")

# Função para fechar a porta dramaticamente
def fechar_porta_dramatica(mc):
    """Fecha a porta recriando o material principal."""
    try:
        mc.postToChat("🚪 A porta está se fechando...")
        
        # Efeito de partículas
        for i in range(5):
            mc.postToChat(f"💫 Efeito de fechamento {i+1}/5...")
            time.sleep(0.4) 
        
        # Recria a porta (Iron Blocks)
        for y in range(PORTA_ALTURA):
            for x in range(PORTA_LARGURA):
                mc.setBlock(PORTA_X + x, PORTA_Y + y, PORTA_Z, PORTA_MATERIAL)
        
        # Adiciona maçanetas
        mc.setBlock(PORTA_X, PORTA_Y + 1, PORTA_Z, block.GOLD_BLOCK.id)
        mc.setBlock(PORTA_X + 1, PORTA_Y + 1, PORTA_Z, block.GOLD_BLOCK.id)
        
        mc.postToChat("🔒 A porta se fechou! O acesso foi negado!")
        registrar_log("DOOR_CLOSE", "Porta fechada dramaticamente")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao fechar porta: {e}")
        print(f"[ERROR] Falha ao fechar porta: {e}")

# Função para criar arco-íris de encenação
def criar_arco_iris_encenacao(mc):
    """Cria um arco-íris para a encenação na mesma coordenada da porta."""
    try:
        height = 30
        colors = [10, 11, 6]  # Roxo, Azul, Rosa
        
        mc.postToChat("🌈 Criando arco-íris mágico...")
        
        # Constrói o arco-íris (sobreposto à porta aberta)
        for x in range(0, 80):
            for colourindex in range(0, len(colors)):
                y = sin((x / 80.0) * pi) * height + colourindex + ARCO_Y
                # Centraliza em ARCO_X
                mc.setBlock(x - 40 + ARCO_X, y, ARCO_Z, block.WOOL.id, colors[len(colors) - 1 - colourindex])
            
            # Mensagens de progresso
            if x % 20 == 0:
                progresso = (x / 80) * 100
                mc.postToChat(f"🎨 Progresso do arco-íris: {progresso:.0f}%")
            
            time.sleep(0.05) # Construção mais rápida
        
        mc.postToChat("✨ Arco-íris mágico criado!")
        registrar_log("RAINBOW", "Arco-íris de encenação criado")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao criar arco-íris: {e}")
        print(f"[ERROR] Falha ao criar arco-íris: {e}")

# Função para criar estrela de encenação
def criar_estrela_encenacao(mc):
    """Cria uma estrela para a encenação (sobreposta à porta e arco-íris)."""
    try:
        mc.postToChat("⭐ Criando estrela mágica...")
        
        # Cria uma estrela simples (pentagrama)
        raio = 8
        for i in range(5):
            angulo = (i * 72) * pi / 180
            x = ESTRELA_X + int(raio * cos(angulo))
            y = ESTRELA_Y + 15 + int(raio * sin(angulo)) # Um pouco mais alta
            
            # Desenha as pontas
            mc.setBlock(x, y, ESTRELA_Z, block.WOOL.id, 4)  # Amarelo
        
        # Adiciona o centro com um bloco de diamante para destaque
        mc.setBlock(ESTRELA_X, ESTRELA_Y + 15, ESTRELA_Z, block.DIAMOND_BLOCK.id)
        
        mc.postToChat("🌟 Estrela mágica criada!")
        registrar_log("STAR", "Estrela de encenação criada")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao criar estrela: {e}")
        print(f"[ERROR] Falha ao criar estrela: {e}")

# Função para limpar a área de encenação
def limpar_encenacao(mc):
    """Limpa toda a área de encenação (Porta, Arco-Íris, Estrela)"""
    try:
        mc.postToChat("🧹 Limpando área de encenação...")
        
        # Limpa uma área grande o suficiente para todas as construções sobrepostas
        mc.setBlocks(BASE_X - 50, BASE_Y - 20, BASE_Z - 10, 
                     BASE_X + 50, BASE_Y + 50, BASE_Z + 10, block.AIR.id)
        
        mc.postToChat("✨ Área limpa! Pronta para nova encenação!")
        registrar_log("CLEAR", "Área de encenação limpa")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao limpar área: {e}")
        print(f"[ERROR] Falha ao limpar área: {e}")

# Função para encenação completa
def encenacao_completa(mc):
    """Executa uma encenação completa (Mantém a construção após o Passo 5)."""
    try:
        mc.postToChat("🎭 INICIANDO ENCENAÇÃO MÁGICA! 🎭")
        mc.postToChat("=" * 50)
        mc.postToChat("📖 Esta encenação terá 5 passos mágicos sobrepostos...")
        mc.postToChat("⏰ Cada passo levará alguns segundos para completar...")
        
        # Limpeza Inicial (Garante que a área está vazia antes de começar)
        limpar_encenacao(mc)
        mc.postToChat("🧹 Área limpa para iniciar.")
        time.sleep(2)
        
        # Passo 1: Criar porta
        mc.postToChat("🚪 Passo 1: Criando porta mágica com moldura...")
        mc.postToChat("⏳ Aguarde enquanto a porta se materializa...")
        criar_porta_encenacao(mc)
        time.sleep(3) 
        
        # Passo 2: Abrir porta
        mc.postToChat("🔓 Passo 2: Abrindo porta...")
        mc.postToChat("✨ A magia está se intensificando, abrindo caminho...")
        abrir_porta_dramatica(mc)
        time.sleep(3) 
        
        # Passo 3: Criar arco-íris (Aparece no espaço da porta aberta)
        mc.postToChat("🌈 Passo 3: Criando arco-íris...")
        mc.postToChat("🎨 As cores estão se formando no céu, dentro do portal...")
        criar_arco_iris_encenacao(mc)
        time.sleep(4) 
        
        # Passo 4: Criar estrela (Aparece sobre o arco-íris)
        mc.postToChat("⭐ Passo 4: Criando estrela...")
        mc.postToChat("🌟 A estrela está brilhando intensamente sobre as cores...")
        criar_estrela_encenacao(mc)
        time.sleep(3) 
        
        # Passo 5: Fechar porta (Recria apenas a porta, deixando arco-íris e estrela intactos no fundo)
        mc.postToChat("🔒 Passo 5: Fechando porta...")
        mc.postToChat("🌙 O espetáculo está chegando ao fim, fechando o portal...")
        fechar_porta_dramatica(mc)
        time.sleep(3) 
        
        mc.postToChat("🎉 ENCENAÇÃO CONCLUÍDA! 🎉")
        mc.postToChat("👏 A porta está fechada, mas o Arco-Íris e a Estrela estão mantidos!")
        registrar_log("SHOW", "Encenação completa executada")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro na encenação: {e}")
        print(f"[ERROR] Falha na encenação: {e}")

# Conexão com Minecraft e Arduino
inicializar_log()
try:
    print("[INFO] Tentando conectar ao servidor Minecraft em {}:{}".format(MINECRAFT_HOST, MINECRAFT_PORT))
    mc = minecraft.Minecraft.create(MINECRAFT_HOST, MINECRAFT_PORT)
    print("[INFO] Conectado ao servidor Minecraft")
    registrar_log("START", "Conexão estabelecida com Minecraft")
    mc.postToChat("🎭 Sistema de Encenação NFC iniciado! Aproxime um cartão para a apresentação!")
    # Teleporta o jogador para a área para melhor visualização
    mc.player.setPos(BASE_X, BASE_Y, BASE_Z - 10) 
except Exception as e:
    registrar_log("ERROR", f"Falha ao conectar ao Minecraft em {MINECRAFT_HOST}:{MINECRAFT_PORT}: {e}")
    print(f"[ERROR] Falha ao conectar ao Minecraft: {e}")
    exit(1)

try:
    print(f"[INFO] Tentando conectar ao Arduino na porta {ARDUINO_PORT}")
    arduino = serial.Serial(ARDUINO_PORT, ARDUINO_BAUDRATE, timeout=1)
    time.sleep(2)  # Estabiliza conexão
    print(f"[INFO] Conectado ao Arduino na porta {ARDUINO_PORT}")
    registrar_log("START", "Conexão estabelecida com Arduino")
except Exception as e:
    registrar_log("ERROR", f"Falha ao conectar ao Arduino na porta {ARDUINO_PORT}: {e}")
    print(f"[ERROR] Falha ao conectar ao Arduino: {e}")
    exit(1)

# Loop principal
try:
    while True:
        try:
            # Leitura do Arduino
            if arduino.in_waiting > 0:
                linha = arduino.readline().decode('utf-8', errors='ignore').strip()
                print(f"[INFO] Recebido do Arduino: {linha}")
                if not linha or ":" not in linha:
                    registrar_log("IGNORED", "Linha inválida recebida do Arduino")
                    continue
                status, detalhes = linha.split(":", 1)
                registrar_log(status, detalhes)

                if status == "LENDO":
                    mc.postToChat("📶 Lendo cartão NFC...")
                elif status == "AUTORIZADO":
                    mc.postToChat("✅ Acesso autorizado! Iniciando encenação mágica...")
                    encenacao_completa(mc)
                elif status == "NEGADO":
                    mc.postToChat("🚫 Acesso negado! Limpando área...")
                    limpar_encenacao(mc)
                elif status == "READY":
                    mc.postToChat("🟡 Sistema pronto para nova encenação.")
            time.sleep(0.1)  # Reduz uso de CPU
        except Exception as e:
            registrar_log("ERROR", f"Erro no loop principal: {e}")
            time.sleep(1)
except KeyboardInterrupt:
    print("[INFO] Script interrompido pelo usuário (Ctrl+C)")
    registrar_log("STOP", "Script interrompido pelo usuário")
    arduino.close()
    print("[INFO] Conexão com Arduino fechada")
    exit(0)