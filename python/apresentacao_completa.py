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
LOG_FILE = "logs/apresentacao_completa_log.csv"

# Configurações das apresentações
RAINBOW_X, RAINBOW_Y, RAINBOW_Z = 445, 72, -419
ESTRELA_X, ESTRELA_Y, ESTRELA_Z = 445, 72, -419
ENCENACAO_X, ENCENACAO_Y, ENCENACAO_Z = 445, 72, -419

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

# Função para limpar área entre apresentações
def limpar_area(mc, x, y, z, raio=50):
    """Limpa uma área circular para nova apresentação"""
    try:
        mc.setBlocks(x - raio, y - 30, z - raio, x + raio, y + 80, z + raio, block.AIR.id)
        mc.postToChat(f"🧹 Área limpa em x={x}, y={y}, z={z}")
        registrar_log("CLEAR", f"Área limpa em x={x}, y={y}, z={z}")
    except Exception as e:
        registrar_log("ERROR", f"Erro ao limpar área: {e}")

# Função para apresentação do arco-íris
def apresentacao_rainbow(mc):
    """Executa a apresentação do sistema de arco-íris"""
    try:
        mc.postToChat("=" * 60)
        mc.postToChat("🌈 APRESENTAÇÃO 1: SISTEMA DE ARCO-ÍRIS 🌈")
        mc.postToChat("=" * 60)
        mc.postToChat("📖 Este sistema cria um arco-íris roxo, azul e rosa...")
        mc.postToChat("✨ Com 12 estrelas de vidro brilhantes ao redor!")
        time.sleep(4)
        
        # Constrói arco-íris
        mc.postToChat("🎨 Construindo arco-íris com múltiplas camadas...")
        construir_arco_iris_apresentacao(mc)
        time.sleep(3)
        
        # Adiciona estrelas de vidro
        mc.postToChat("⭐ Adicionando estrelas de vidro brilhantes...")
        adicionar_estrelas_vidro_apresentacao(mc, RAINBOW_X, RAINBOW_Y, RAINBOW_Z)
        time.sleep(3)
        
        mc.postToChat("🎉 Apresentação do arco-íris concluída!")
        mc.postToChat("⏳ Aguarde 5 segundos para a próxima apresentação...")
        time.sleep(5)
        
        registrar_log("RAINBOW_SHOW", "Apresentação do arco-íris concluída")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro na apresentação do arco-íris: {e}")
        print(f"[ERROR] Falha na apresentação do arco-íris: {e}")

# Função para construir arco-íris na apresentação
def construir_arco_iris_apresentacao(mc):
    """Constrói arco-íris para apresentação"""
    try:
        height = 50
        colors = [10, 11, 6]  # Roxo, Azul, Rosa
        
        # Constrói o arco-íris com múltiplas camadas
        for x in range(0, 160):
            for colourindex in range(0, len(colors)):
                for camada in range(3):  # 3 camadas de espessura
                    y = sin((x / 160.0) * pi) * height + colourindex + RAINBOW_Y
                    z_offset = camada - 1
                    mc.setBlock(x - 80 + RAINBOW_X, y, RAINBOW_Z + z_offset, block.WOOL.id, colors[len(colors) - 1 - colourindex])
            time.sleep(0.01)
        
        registrar_log("RAINBOW_BUILD", "Arco-íris construído")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao construir arco-íris: {e}")

# Função para adicionar estrelas de vidro na apresentação
def adicionar_estrelas_vidro_apresentacao(mc, center_x, center_y, center_z):
    """Adiciona estrelas de vidro para apresentação"""
    try:
        cores_vidro = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        raio_estrelas = 25
        num_estrelas = 12
        
        for i in range(num_estrelas):
            angulo = (i * 360 / num_estrelas) * pi / 180
            x_estrela = center_x + int(raio_estrelas * cos(angulo))
            y_estrela = center_y + 20 + (i % 3) * 5
            z_estrela = center_z + (i % 3) * 2 - 2
            
            criar_estrela_vidro_apresentacao(mc, x_estrela, y_estrela, z_estrela, cores_vidro[i % len(cores_vidro)])
        
        registrar_log("GLASS_STARS", f"{num_estrelas} estrelas de vidro criadas")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao criar estrelas de vidro: {e}")

# Função para criar estrela de vidro na apresentação
def criar_estrela_vidro_apresentacao(mc, x, y, z, cor):
    """Cria estrela de vidro com glowstone para apresentação"""
    try:
        # Estrutura da estrela de vidro (8 pontas)
        offsets = [
            (0, 0, 0),  # centro
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1),
            (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
            (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
            (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1)
        ]
        for dx, dy, dz in offsets:
            mc.setBlock(x + dx, y + dy, z + dz, block.GLASS.id, cor)

        # Glowstone central e nas pontas principais
        glow_offsets = [
            (0, 0, 0),
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]
        for dx, dy, dz in glow_offsets:
            mc.setBlock(x + dx, y + dy, z + dz, block.GLOWSTONE.id)

        # Comentário: agora a estrela é mais simétrica e iluminada
    except Exception as e:
        print(f"[ERROR] Falha ao criar estrela de vidro: {e}")

# Função para apresentação da estrela
def apresentacao_estrela(mc):
    """Executa a apresentação do sistema de estrela"""
    try:
        mc.postToChat("=" * 60)
        mc.postToChat("⭐ APRESENTAÇÃO 2: SISTEMA DE ESTRELA ⭐")
        mc.postToChat("=" * 60)
        mc.postToChat("📖 Este sistema cria uma estrela roxa, azul e rosa...")
        mc.postToChat("✨ Com estrelas de vidro brilhantes ao redor!")
        time.sleep(4)
        
        # Constrói estrela
        mc.postToChat("🎨 Construindo estrela de 5 pontas...")
        construir_estrela_apresentacao(mc)
        time.sleep(3)
        
        # Adiciona estrelas de vidro
        mc.postToChat("⭐ Adicionando estrelas de vidro brilhantes...")
        adicionar_estrelas_vidro_apresentacao(mc, ESTRELA_X, ESTRELA_Y, ESTRELA_Z)
        time.sleep(3)
        
        mc.postToChat("🎉 Apresentação da estrela concluída!")
        mc.postToChat("⏳ Aguarde 5 segundos para a próxima apresentação...")
        time.sleep(5)
        
        registrar_log("STAR_SHOW", "Apresentação da estrela concluída")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro na apresentação da estrela: {e}")
        print(f"[ERROR] Falha na apresentação da estrela: {e}")

# Função para construir estrela na apresentação
def construir_estrela_apresentacao(mc):
    """Constrói estrela para apresentação"""
    try:
        raio_externo = 15
        raio_interno = 6
        colors = [10, 11, 6]  # Roxo, Azul, Rosa
        
        # Desenha as 5 pontas da estrela
        for i in range(5):
            angulo = (i * 72) * pi / 180
            
            # Ponta externa
            x_ext = ESTRELA_X + int(raio_externo * cos(angulo))
            y_ext = ESTRELA_Y + int(raio_externo * sin(angulo))
            
            # Ponta interna
            angulo_interno = angulo + 36 * pi / 180
            x_int = ESTRELA_X + int(raio_interno * cos(angulo_interno))
            y_int = ESTRELA_Y + int(raio_interno * sin(angulo_interno))
            
            # Próxima ponta externa
            angulo_proximo = ((i + 1) * 72) * pi / 180
            x_prox = ESTRELA_X + int(raio_externo * cos(angulo_proximo))
            y_prox = ESTRELA_Y + int(raio_externo * sin(angulo_proximo))
            
            # Desenha as linhas
            desenhar_linha_apresentacao(mc, ESTRELA_X, ESTRELA_Y, ESTRELA_Z, x_ext, y_ext, ESTRELA_Z, colors[i % len(colors)])
            desenhar_linha_apresentacao(mc, x_ext, y_ext, ESTRELA_Z, x_int, y_int, ESTRELA_Z, colors[i % len(colors)])
            desenhar_linha_apresentacao(mc, x_int, y_int, ESTRELA_Z, x_prox, y_prox, ESTRELA_Z, colors[i % len(colors)])
            
            time.sleep(0.1)
        
        # Preenche o centro
        for x in range(ESTRELA_X - 3, ESTRELA_X + 4):
            for y in range(ESTRELA_Y - 3, ESTRELA_Y + 4):
                mc.setBlock(x, y, ESTRELA_Z, block.WOOL.id, colors[0])
        
        registrar_log("STAR_BUILD", "Estrela construída")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao construir estrela: {e}")

# Função para desenhar linhas na apresentação
def desenhar_linha_apresentacao(mc, x1, y1, z1, x2, y2, z2, cor):
    """Desenha linha para apresentação"""
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    steps = max(abs(dx), abs(dy), abs(dz))
    
    if steps > 0:
        for step in range(steps + 1):
            x = x1 + (dx * step) // steps
            y = y1 + (dy * step) // steps
            z = z1 + (dz * step) // steps
            mc.setBlock(x, y, z, block.WOOL.id, cor)

# Função para apresentação da encenação
def apresentacao_encenacao(mc):
    """Executa a apresentação do sistema de encenação"""
    try:
        mc.postToChat("=" * 60)
        mc.postToChat("🎭 APRESENTAÇÃO 3: SISTEMA DE ENCENAÇÃO 🎭")
        mc.postToChat("=" * 60)
        mc.postToChat("📖 Este sistema cria uma apresentação dramática...")
        mc.postToChat("✨ Com porta, arco-íris e estrela em sequência!")
        time.sleep(4)
        
        # Executa encenação
        mc.postToChat("🎬 Iniciando encenação dramática...")
        encenacao_completa_apresentacao(mc)
        
        mc.postToChat("🎉 Apresentação da encenação concluída!")
        registrar_log("ENCENACAO_SHOW", "Apresentação da encenação concluída")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro na apresentação da encenação: {e}")
        print(f"[ERROR] Falha na apresentação da encenação: {e}")

# Função para encenação completa na apresentação
def encenacao_completa_apresentacao(mc):
    """Executa encenação completa para apresentação"""
    try:
        mc.postToChat("🎭 INICIANDO ENCENAÇÃO MÁGICA! 🎭")
        mc.postToChat("📖 Esta encenação terá 5 passos mágicos...")
        time.sleep(3)
        
        # Passo 1: Criar porta
        mc.postToChat("🚪 Passo 1: Criando porta mágica...")
        criar_porta_apresentacao(mc)
        time.sleep(3)
        
        # Passo 2: Abrir porta
        mc.postToChat("🔓 Passo 2: Abrindo porta...")
        abrir_porta_apresentacao(mc)
        time.sleep(4)
        
        # Passo 3: Criar arco-íris
        mc.postToChat("🌈 Passo 3: Criando arco-íris...")
        criar_arco_iris_encenacao_apresentacao(mc)
        time.sleep(3)
        
        # Passo 4: Criar estrela
        mc.postToChat("⭐ Passo 4: Criando estrela...")
        criar_estrela_encenacao_apresentacao(mc)
        time.sleep(3)
        
        # Passo 5: Fechar porta
        mc.postToChat("🔒 Passo 5: Fechando porta...")
        fechar_porta_apresentacao(mc)
        time.sleep(3)
        
        mc.postToChat("🎉 ENCENAÇÃO CONCLUÍDA! 🎉")
        registrar_log("ENCENACAO_COMPLETE", "Encenação completa executada")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro na encenação: {e}")

# Funções auxiliares para encenação
def criar_porta_apresentacao(mc):
    """Cria porta para apresentação"""
    for y in range(3):
        for x in range(2):
            mc.setBlock(ENCENACAO_X + x, ENCENACAO_Y + y, ENCENACAO_Z, block.IRON_BLOCK.id)
    mc.setBlock(ENCENACAO_X, ENCENACAO_Y + 1, ENCENACAO_Z, block.GOLD_BLOCK.id)
    mc.setBlock(ENCENACAO_X + 1, ENCENACAO_Y + 1, ENCENACAO_Z, block.GOLD_BLOCK.id)

def abrir_porta_apresentacao(mc):
    """Abre porta para apresentação"""
    for y in range(3):
        for x in range(2):
            mc.setBlock(ENCENACAO_X + x, ENCENACAO_Y + y, ENCENACAO_Z, block.AIR.id)

def criar_arco_iris_encenacao_apresentacao(mc):
    """Cria arco-íris para encenação na apresentação"""
    height = 30
    colors = [10, 11, 6]
    
    for x in range(0, 80):
        for colourindex in range(0, len(colors)):
            y = sin((x / 80.0) * pi) * height + colourindex + ENCENACAO_Y
            mc.setBlock(x - 40 + ENCENACAO_X, y, ENCENACAO_Z, block.WOOL.id, colors[len(colors) - 1 - colourindex])
        time.sleep(0.05)

def criar_estrela_encenacao_apresentacao(mc):
    """Cria estrela para encenação na apresentação"""
    raio = 8
    for i in range(5):
        angulo = (i * 72) * pi / 180
        x = ENCENACAO_X + int(raio * cos(angulo))
        y = ENCENACAO_Y + int(raio * sin(angulo))
        mc.setBlock(x, y, ENCENACAO_Z, block.WOOL.id, 4)

def fechar_porta_apresentacao(mc):
    """Fecha porta para apresentação"""
    for y in range(3):
        for x in range(2):
            mc.setBlock(ENCENACAO_X + x, ENCENACAO_Y + y, ENCENACAO_Z, block.IRON_BLOCK.id)
    mc.setBlock(ENCENACAO_X, ENCENACAO_Y + 1, ENCENACAO_Z, block.GOLD_BLOCK.id)
    mc.setBlock(ENCENACAO_X + 1, ENCENACAO_Y + 1, ENCENACAO_Z, block.GOLD_BLOCK.id)

# Função principal da apresentação
def apresentacao_completa(mc):
    """Executa apresentação completa dos 3 sistemas"""
    try:
        mc.postToChat("🎓 APRESENTAÇÃO COMPLETA DO TRABALHO 🎓")
        mc.postToChat("=" * 60)
        mc.postToChat("📚 Sistema NFC Minecraft - Projeto Acadêmico")
        mc.postToChat("👥 Equipe: Matheus Gustavo, Davi Moreno")
        mc.postToChat("🔬 Demonstração dos 3 sistemas desenvolvidos")
        time.sleep(5)
        
        # Apresentação 1: Arco-íris
        apresentacao_rainbow(mc)
        
        # Apresentação 2: Estrela
        apresentacao_estrela(mc)
        
        # Apresentação 3: Encenação
        apresentacao_encenacao(mc)
        
        # Conclusão
        mc.postToChat("=" * 60)
        mc.postToChat("🎉 APRESENTAÇÃO COMPLETA FINALIZADA! 🎉")
        mc.postToChat("👏 Obrigado por assistir à demonstração!")
        mc.postToChat("✨ Sistema NFC Minecraft - v3.0")
        mc.postToChat("🔒 Controle de acesso com Arduino + Minecraft")
        time.sleep(5)
        
        registrar_log("PRESENTATION_COMPLETE", "Apresentação completa finalizada")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro na apresentação completa: {e}")
        print(f"[ERROR] Falha na apresentação completa: {e}")

# Conexão com Minecraft e Arduino
inicializar_log()
try:
    print("[INFO] Tentando conectar ao servidor Minecraft em {}:{}".format(MINECRAFT_HOST, MINECRAFT_PORT))
    mc = minecraft.Minecraft.create(MINECRAFT_HOST, MINECRAFT_PORT)
    print("[INFO] Conectado ao servidor Minecraft")
    registrar_log("START", "Conexão estabelecida com Minecraft")
    mc.postToChat("🎓 Sistema de Apresentação NFC iniciado!")
    mc.postToChat("📚 Pronto para demonstração completa do trabalho!")
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
                    mc.postToChat("✅ Acesso autorizado! Iniciando apresentação completa...")
                    # Limpa a área uma única vez antes de todas as apresentações
                    limpar_area(mc, RAINBOW_X, RAINBOW_Y, RAINBOW_Z)
                    time.sleep(2)
                    apresentacao_completa(mc)
                elif status == "NEGADO":
                    mc.postToChat("🚫 Acesso negado! Limpando área...")
                    limpar_area(mc, RAINBOW_X, RAINBOW_Y, RAINBOW_Z)
                elif status == "READY":
                    mc.postToChat("🟡 Sistema pronto para apresentação.")
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