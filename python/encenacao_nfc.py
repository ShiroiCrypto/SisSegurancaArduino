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

# Configurações da encenação
PORTA_X, PORTA_Y, PORTA_Z = 445, 72, -419  # Posição da porta
ARCO_X, ARCO_Y, ARCO_Z = 445, 72, -419     # Posição do arco-íris
ESTRELA_X, ESTRELA_Y, ESTRELA_Z = 445, 72, -419  # Posição da estrela

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

# Função para criar a porta de encenação
def criar_porta_encenacao(mc):
    """Cria uma porta de ferro para a encenação"""
    try:
        # Cria uma porta de ferro 2x3
        for y in range(3):
            for x in range(2):
                mc.setBlock(PORTA_X + x, PORTA_Y + y, PORTA_Z, block.IRON_BLOCK.id)
        
        # Adiciona maçanetas (blocos de ouro)
        mc.setBlock(PORTA_X, PORTA_Y + 1, PORTA_Z, block.GOLD_BLOCK.id)
        mc.setBlock(PORTA_X + 1, PORTA_Y + 1, PORTA_Z, block.GOLD_BLOCK.id)
        
        # Adiciona uma placa com texto
        mc.setBlock(PORTA_X + 1, PORTA_Y + 3, PORTA_Z, block.SIGN.id)
        
        registrar_log("DOOR", "Porta de encenação criada")
        print(f"[INFO] Porta de encenação criada em x={PORTA_X}, y={PORTA_Y}, z={PORTA_Z}")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao criar porta: {e}")
        print(f"[ERROR] Falha ao criar porta: {e}")

# Função para abrir a porta dramaticamente
def abrir_porta_dramatica(mc):
    """Abre a porta com efeitos dramáticos"""
    try:
        mc.postToChat("🚪 A porta está se abrindo...")
        
        # Efeito de partículas na porta
        for i in range(8):
            mc.postToChat(f"✨ Efeito mágico {i+1}/8...")
            time.sleep(1.0)  # Mais tempo entre cada efeito
        
        # Remove a porta (abre)
        for y in range(3):
            for x in range(2):
                mc.setBlock(PORTA_X + x, PORTA_Y + y, PORTA_Z, block.AIR.id)
        
        mc.postToChat("🌟 A porta se abriu! O caminho está livre!")
        registrar_log("DOOR_OPEN", "Porta aberta dramaticamente")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao abrir porta: {e}")
        print(f"[ERROR] Falha ao abrir porta: {e}")

# Função para fechar a porta dramaticamente
def fechar_porta_dramatica(mc):
    """Fecha a porta com efeitos dramáticos"""
    try:
        mc.postToChat("🚪 A porta está se fechando...")
        
        # Efeito de partículas
        for i in range(5):
            mc.postToChat(f"💫 Efeito de fechamento {i+1}/5...")
            time.sleep(0.8)  # Mais tempo entre cada efeito
        
        # Recria a porta
        for y in range(3):
            for x in range(2):
                mc.setBlock(PORTA_X + x, PORTA_Y + y, PORTA_Z, block.IRON_BLOCK.id)
        
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
    """Cria um arco-íris para a encenação"""
    try:
        height = 30
        colors = [10, 11, 6]  # Roxo, Azul, Rosa
        
        mc.postToChat("🌈 Criando arco-íris mágico...")
        
        # Constrói o arco-íris
        for x in range(0, 80):
            for colourindex in range(0, len(colors)):
                y = sin((x / 80.0) * pi) * height + colourindex + ARCO_Y
                mc.setBlock(x - 40 + ARCO_X, y, ARCO_Z, block.WOOL.id, colors[len(colors) - 1 - colourindex])
            
            # Mensagens de progresso
            if x % 20 == 0:  # A cada 20 blocos
                progresso = (x / 80) * 100
                mc.postToChat(f"🎨 Progresso do arco-íris: {progresso:.0f}%")
            
            time.sleep(0.1)  # Mais tempo para ver a construção
        
        mc.postToChat("✨ Arco-íris mágico criado!")
        registrar_log("RAINBOW", "Arco-íris de encenação criado")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao criar arco-íris: {e}")
        print(f"[ERROR] Falha ao criar arco-íris: {e}")

# Função para criar estrela de encenação
def criar_estrela_encenacao(mc):
    """Cria uma estrela para a encenação"""
    try:
        mc.postToChat("⭐ Criando estrela mágica...")
        
        # Cria uma estrela simples
        raio = 8
        for i in range(5):
            angulo = (i * 72) * pi / 180
            x = ESTRELA_X + int(raio * cos(angulo))
            y = ESTRELA_Y + int(raio * sin(angulo))
            mc.setBlock(x, y, ESTRELA_Z, block.WOOL.id, 4)  # Amarelo
        
        mc.postToChat("🌟 Estrela mágica criada!")
        registrar_log("STAR", "Estrela de encenação criada")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao criar estrela: {e}")
        print(f"[ERROR] Falha ao criar estrela: {e}")

# Função para limpar a área de encenação
def limpar_encenacao(mc):
    """Limpa toda a área de encenação"""
    try:
        mc.postToChat("🧹 Limpando área de encenação...")
        
        # Limpa uma área grande
        mc.setBlocks(ARCO_X - 50, ARCO_Y - 20, ARCO_Z - 10, 
                    ARCO_X + 50, ARCO_Y + 50, ARCO_Z + 10, block.AIR.id)
        
        mc.postToChat("✨ Área limpa! Pronta para nova encenação!")
        registrar_log("CLEAR", "Área de encenação limpa")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao limpar área: {e}")
        print(f"[ERROR] Falha ao limpar área: {e}")

# Função para encenação completa
def encenacao_completa(mc):
    """Executa uma encenação completa"""
    try:
        mc.postToChat("🎭 INICIANDO ENCENAÇÃO MÁGICA! 🎭")
        mc.postToChat("=" * 50)
        mc.postToChat("📖 Esta encenação terá 5 passos mágicos...")
        mc.postToChat("⏰ Cada passo levará alguns segundos para completar...")
        time.sleep(3)  # Tempo para ler as instruções
        
        # Passo 1: Criar porta
        mc.postToChat("🚪 Passo 1: Criando porta mágica...")
        mc.postToChat("⏳ Aguarde enquanto a porta se materializa...")
        criar_porta_encenacao(mc)
        time.sleep(5)  # Mais tempo para ler
        
        # Passo 2: Abrir porta
        mc.postToChat("🔓 Passo 2: Abrindo porta...")
        mc.postToChat("✨ A magia está se intensificando...")
        abrir_porta_dramatica(mc)
        time.sleep(6)  # Mais tempo para apreciar a abertura
        
        # Passo 3: Criar arco-íris
        mc.postToChat("🌈 Passo 3: Criando arco-íris...")
        mc.postToChat("🎨 As cores estão se formando no céu...")
        criar_arco_iris_encenacao(mc)
        time.sleep(5)  # Mais tempo para ver o arco-íris
        
        # Passo 4: Criar estrela
        mc.postToChat("⭐ Passo 4: Criando estrela...")
        mc.postToChat("🌟 A estrela está brilhando intensamente...")
        criar_estrela_encenacao(mc)
        time.sleep(4)  # Mais tempo para ver a estrela
        
        # Passo 5: Fechar porta
        mc.postToChat("🔒 Passo 5: Fechando porta...")
        mc.postToChat("🌙 O espetáculo está chegando ao fim...")
        fechar_porta_dramatica(mc)
        time.sleep(3)  # Tempo final para apreciar
        
        mc.postToChat("🎉 ENCENAÇÃO CONCLUÍDA! 🎉")
        mc.postToChat("👏 Obrigado por assistir ao espetáculo mágico!")
        mc.postToChat("✨ A magia do NFC e Minecraft em ação!")
        time.sleep(4)  # Tempo final para ler as mensagens de conclusão
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
