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
LOG_FILE = "logs/rainbow_nfc_log.csv"

# Cores do arco-íris (dados de lã) - Roxo, Azul, Rosa
colors = [10, 11, 6]  # Roxo, Azul, Rosa

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

# Função para construir o arco-íris roxo, azul e rosa com estrela amarela
def construir_arco_iris(mc):
    try:
        height = 50
        center_x, base_y, center_z = 445, 72, -419  # Centro em /tp 445 72 -419
        
        # Limpa a área (ar para evitar sobreposição)
        mc.setBlocks(center_x - 80, base_y - 30, center_z - 30, center_x + 80, base_y + height + 30, center_z + 30, block.AIR.id)
        registrar_log("CLEAR", f"Área limpa para o arco-íris ({center_x-80},{base_y-30},{center_z-30} a {center_x+80},{base_y+height+30},{center_z+30})")
        mc.postToChat("🌈 Construindo arco-íris roxo, azul e rosa com estrelas de vidro!")

        # Constrói o arco-íris com múltiplas camadas para ficar mais bonito
        for x in range(0, 160):
            for colourindex in range(0, len(colors)):
                # Cria múltiplas camadas para dar espessura ao arco-íris
                for camada in range(3):  # 3 camadas de espessura
                    y = sin((x / 160.0) * pi) * height + colourindex + base_y
                    # Adiciona variação na espessura
                    z_offset = camada - 1  # -1, 0, 1 para criar espessura
                    mc.setBlock(x - 80 + center_x, y, center_z + z_offset, block.WOOL.id, colors[len(colors) - 1 - colourindex])
            time.sleep(0.005)  # Reduz delay para construção mais rápida
        
        # Adiciona estrelas de vidro coloridas ao redor
        adicionar_estrelas_vidro(mc, center_x, base_y, center_z)
        
        mc.postToChat("🎉 Arco-íris roxo, azul e rosa com estrelas de vidro concluído!")
        registrar_log("SUCCESS", "Arco-íris com estrelas de vidro construído com sucesso")
        print(f"[INFO] Arco-íris construído em x={center_x-80} a {center_x+80}, y={base_y} a {base_y+height+len(colors)}, z={center_z}")
    except Exception as e:
        mc.postToChat("❌ Erro ao construir o arco-íris!")
        registrar_log("ERROR", f"Erro ao construir arco-íris: {e}")
        print(f"[ERROR] Falha ao construir arco-íris: {e}")

# Função para adicionar estrelas de vidro coloridas ao redor
def adicionar_estrelas_vidro(mc, center_x, base_y, center_z):
    try:
        # Cores de vidro para as estrelas
        cores_vidro = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # Todas as cores de vidro
        
        # Posições das estrelas de vidro (em círculo ao redor)
        raio_estrelas = 25
        num_estrelas = 12
        
        for i in range(num_estrelas):
            angulo = (i * 360 / num_estrelas) * pi / 180
            x_estrela = center_x + int(raio_estrelas * cos(angulo))
            z_estrela = center_z + int(raio_estrelas * sin(angulo))
            y_estrela = base_y + 20 + (i % 3) * 5  # Varia a altura das estrelas
            
            # Cria uma pequena estrela de vidro
            criar_estrela_vidro(mc, x_estrela, y_estrela, z_estrela, cores_vidro[i % len(cores_vidro)])
        
        registrar_log("GLASS_STARS", f"{num_estrelas} estrelas de vidro coloridas criadas")
        print(f"[INFO] {num_estrelas} estrelas de vidro coloridas criadas ao redor")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao criar estrelas de vidro: {e}")
        print(f"[ERROR] Falha ao criar estrelas de vidro: {e}")

# Função para criar uma pequena estrela de vidro
def criar_estrela_vidro(mc, x, y, z, cor):
    """Cria uma pequena estrela de vidro colorida com glowstone dentro"""
    try:
        # Cria uma estrela simples de vidro
        # Centro
        mc.setBlock(x, y, z, block.GLASS.id, cor)
        
        # Pontas da estrela (cruz simples)
        mc.setBlock(x + 1, y, z, block.GLASS.id, cor)
        mc.setBlock(x - 1, y, z, block.GLASS.id, cor)
        mc.setBlock(x, y, z + 1, block.GLASS.id, cor)
        mc.setBlock(x, y, z - 1, block.GLASS.id, cor)
        
        # Adiciona algumas camadas para dar volume
        mc.setBlock(x, y + 1, z, block.GLASS.id, cor)
        mc.setBlock(x, y - 1, z, block.GLASS.id, cor)
        
        # Adiciona glowstone dentro da estrela para brilhar
        mc.setBlock(x, y, z, block.GLOWSTONE.id)  # Centro brilhante
        mc.setBlock(x, y + 1, z, block.GLOWSTONE.id)  # Camada superior
        mc.setBlock(x, y - 1, z, block.GLOWSTONE.id)  # Camada inferior
        
    except Exception as e:
        print(f"[ERROR] Falha ao criar estrela de vidro em x={x}, y={y}, z={z}: {e}")

# Função auxiliar para desenhar linhas
def desenhar_linha(mc, x1, z1, x2, z2, y, block_id):
    """Desenha uma linha de blocos entre dois pontos"""
    dx = x2 - x1
    dz = z2 - z1
    steps = max(abs(dx), abs(dz))
    
    if steps > 0:
        for step in range(steps + 1):
            x = x1 + (dx * step) // steps
            z = z1 + (dz * step) // steps
            mc.setBlock(x, y, z, block.WOOL.id, block_id)


# Função para destruir toda a construção
def destruir_construcao(mc):
    try:
        center_x, base_y, center_z = 445, 72, -419
        
        # Destrói uma área muito maior para garantir que tudo seja removido (incluindo estrelas de vidro)
        mc.setBlocks(center_x - 100, base_y - 50, center_z - 50, center_x + 100, base_y + 100, center_z + 50, block.AIR.id)
        
        mc.postToChat("💥 CONSTRUÇÃO DESTRUÍDA! Cartão não autorizado detectado!")
        mc.postToChat("💥 Arco-íris e estrelas de vidro foram destruídas!")
        registrar_log("DESTROY", "Construção completa destruída por cartão não autorizado")
        print(f"[INFO] Construção destruída em x={center_x-100} a {center_x+100}, y={base_y-50} a {base_y+100}, z={center_z-50} a {center_z+50}")
        
    except Exception as e:
        mc.postToChat("❌ Erro ao destruir construção!")
        registrar_log("ERROR", f"Erro ao destruir construção: {e}")
        print(f"[ERROR] Falha ao destruir construção: {e}")

# Conexão com Minecraft e Arduino
inicializar_log()
try:
    print("[INFO] Tentando conectar ao servidor Minecraft em {}:{}".format(MINECRAFT_HOST, MINECRAFT_PORT))
    mc = minecraft.Minecraft.create(MINECRAFT_HOST, MINECRAFT_PORT)
    print("[INFO] Conectado ao servidor Minecraft")
    registrar_log("START", "Conexão estabelecida com Minecraft")
    mc.postToChat("🔒 Sistema NFC iniciado! Aproxime um cartão autorizado para construir arco-íris roxo, azul e rosa com estrelas de vidro!")
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
                    mc.postToChat("✅ Acesso autorizado! Construindo arco-íris roxo, azul e rosa com estrelas de vidro...")
                    construir_arco_iris(mc)
                elif status == "NEGADO":
                    mc.postToChat("🚫 Acesso negado! Cartão não autorizado. DESTRUINDO CONSTRUÇÃO!")
                    mc.postToChat("💥 Destruindo arco-íris e estrelas de vidro...")
                    destruir_construcao(mc)
                    registrar_log("NEGADO", "Cartão não autorizado - construção completa destruída")
                elif status == "READY":
                    mc.postToChat("🟡 Sistema pronto para nova leitura.")
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

    #sla