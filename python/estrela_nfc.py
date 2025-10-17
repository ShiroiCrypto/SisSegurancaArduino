"""
Sistema NFC Minecraft – Estrela colorida com estrelas de vidro

Autores:
- Matheus Gustavo (ShiroiCrypto)
- Davi Moreno (Retr0DedSec0)

Descrição:
  Constrói uma estrela de 5 pontas usando geometria polar e adiciona
  estrelas de vidro iluminadas ao redor. Integra com Arduino via Serial e
  Minecraft via RaspberryJuice.
"""

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
LOG_FILE = "logs/estrela_nfc_log.csv"

# Cores da estrela (dados de lã): roxa (10), azul (11), rosa (6)
colors = [10, 11, 6]  # Roxa, Azul, Rosa

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

# Função para construir a estrela melhorada
def construir_estrela(mc):
    try:
        center_x, center_y, center_z = 445, 72, -419  # Centro em /tp 445 72 -419
        raio_externo = 15
        raio_interno = 6
        
        # Limpa a área (ar para evitar sobreposição)
        mc.setBlocks(center_x - 20, center_y - 20, center_z - 5, center_x + 20, center_y + 20, center_z + 5, block.AIR.id)
        registrar_log("CLEAR", f"Área limpa para a estrela ({center_x-20},{center_y-20},{center_z-5} a {center_x+20},{center_y+20},{center_z+5})")
        mc.postToChat("⭐ Construindo uma estrela roxa, azul e rosa em x=445, y=72, z=-419!")

        # Constrói a estrela de 5 pontas usando coordenadas polares
        for i in range(5):  # 5 pontas da estrela
            # Ângulo da ponta externa
            angulo_externo = (i * 72) * pi / 180  # 72 graus entre cada ponta
            
            # Ponta externa
            x_ext = center_x + int(raio_externo * cos(angulo_externo))
            y_ext = center_y + int(raio_externo * sin(angulo_externo))
            
            # Ângulo da ponta interna (entre as pontas externas)
            angulo_interno = angulo_externo + 36 * pi / 180  # 36 graus para a ponta interna
            
            # Ponta interna
            x_int = center_x + int(raio_interno * cos(angulo_interno))
            y_int = center_y + int(raio_interno * sin(angulo_interno))
            
            # Próxima ponta externa (para fechar a estrela)
            angulo_proximo = ((i + 1) * 72) * pi / 180
            x_prox = center_x + int(raio_externo * cos(angulo_proximo))
            y_prox = center_y + int(raio_externo * sin(angulo_proximo))
            
            # Desenha as linhas da estrela
            desenhar_linha_estrela(mc, center_x, center_y, center_z, x_ext, y_ext, center_z, colors[i % len(colors)])
            desenhar_linha_estrela(mc, x_ext, y_ext, center_z, x_int, y_int, center_z, colors[i % len(colors)])
            desenhar_linha_estrela(mc, x_int, y_int, center_z, x_prox, y_prox, center_z, colors[i % len(colors)])
            
            time.sleep(0.05)  # Pequena pausa para visualização
        
        # Preenche o centro da estrela
        for x in range(center_x - 3, center_x + 4):
            for y in range(center_y - 3, center_y + 4):
                mc.setBlock(x, y, center_z, block.WOOL.id, colors[0])  # Roxa no centro
        
        # Adiciona estrelas de vidro coloridas ao redor
        adicionar_estrelas_vidro_estrela(mc, center_x, center_y, center_z)
        
        mc.postToChat("🎉 Estrela roxa, azul e rosa com estrelas de vidro concluída!")
        registrar_log("SUCCESS", "Estrela construída com sucesso")
        print(f"[INFO] Estrela construída em x={center_x-20} a {center_x+20}, y={center_y-20} a {center_y+20}, z={center_z}")
    except Exception as e:
        mc.postToChat("❌ Erro ao construir a estrela!")
        registrar_log("ERROR", f"Erro ao construir estrela: {e}")
        print(f"[ERROR] Falha ao construir estrela: {e}")

# Função para desenhar linhas da estrela
def desenhar_linha_estrela(mc, x1, y1, z1, x2, y2, z2, cor):
    """Desenha uma linha de blocos entre dois pontos"""
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

# Função para adicionar estrelas de vidro coloridas ao redor da estrela principal
def adicionar_estrelas_vidro_estrela(mc, center_x, center_y, center_z):
    try:
        # Cores de vidro para as estrelas
        cores_vidro = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # Todas as cores de vidro
        
        # Posições das estrelas de vidro (em círculo ao redor)
        raio_estrelas = 25
        num_estrelas = 8
        
        for i in range(num_estrelas):
            angulo = (i * 360 / num_estrelas) * pi / 180
            x_estrela = center_x + int(raio_estrelas * cos(angulo))
            y_estrela = center_y + int(raio_estrelas * sin(angulo))
            z_estrela = center_z + (i % 3) * 2 - 2  # Varia a profundidade das estrelas
            
            # Cria uma pequena estrela de vidro
            criar_estrela_vidro_pequena(mc, x_estrela, y_estrela, z_estrela, cores_vidro[i % len(cores_vidro)])
        
        registrar_log("GLASS_STARS", f"{num_estrelas} estrelas de vidro coloridas criadas")
        print(f"[INFO] {num_estrelas} estrelas de vidro coloridas criadas ao redor")
        
    except Exception as e:
        registrar_log("ERROR", f"Erro ao criar estrelas de vidro: {e}")
        print(f"[ERROR] Falha ao criar estrelas de vidro: {e}")

# Função para criar uma pequena estrela de vidro
def criar_estrela_vidro_pequena(mc, x, y, z, cor):
    """Cria uma pequena estrela de vidro colorida com glowstone dentro"""
    try:
        # Cria uma estrela simples de vidro (cruz)
        # Centro
        mc.setBlock(x, y, z, block.GLASS.id, cor)
        
        # Pontas da estrela (cruz simples)
        mc.setBlock(x + 1, y, z, block.GLASS.id, cor)
        mc.setBlock(x - 1, y, z, block.GLASS.id, cor)
        mc.setBlock(x, y + 1, z, block.GLASS.id, cor)
        mc.setBlock(x, y - 1, z, block.GLASS.id, cor)
        
        # Adiciona algumas camadas para dar volume
        mc.setBlock(x, y, z + 1, block.GLASS.id, cor)
        mc.setBlock(x, y, z - 1, block.GLASS.id, cor)
        
        # Adiciona glowstone dentro da estrela para brilhar
        mc.setBlock(x, y, z, block.GLOWSTONE.id)  # Centro brilhante
        mc.setBlock(x, y, z + 1, block.GLOWSTONE.id)  # Camada traseira
        mc.setBlock(x, y, z - 1, block.GLOWSTONE.id)  # Camada frontal
        
    except Exception as e:
        print(f"[ERROR] Falha ao criar estrela de vidro em x={x}, y={y}, z={z}: {e}")

# Função para destruir a estrela e tocar som sinistro
def destruir_estrela(mc):
    try:
        center_x, center_y, center_z = 445, 72, -419
        
        # Destrói uma área maior para garantir que tudo seja removido
        mc.setBlocks(center_x - 30, center_y - 30, center_z - 10, center_x + 30, center_y + 30, center_z + 10, block.AIR.id)
        
        mc.postToChat("💥 Estrela e estrelas de vidro destruídas!")
        registrar_log("DESTROY", f"Estrela destruída ({center_x-30},{center_y-30},{center_z-10} a {center_x+30},{center_y+30},{center_z+10})")
        
        # Toca som sinistro
        try:
            mc.postToChat("/playsound minecraft:entity.ghast.scream master @a")
            registrar_log("SOUND", "Som sinistro tocado: minecraft:entity.ghast.scream")
        except:
            mc.postToChat("🔊 Som sinistro tocado!")
            registrar_log("SOUND", "Som sinistro tocado (método alternativo)")
        
        print(f"[INFO] Estrela destruída e som sinistro tocado")
    except Exception as e:
        mc.postToChat("❌ Erro ao destruir a estrela ou tocar o som!")
        registrar_log("ERROR", f"Erro ao destruir estrela ou tocar som: {e}")
        print(f"[ERROR] Falha ao destruir estrela ou tocar som: {e}")

# Conexão com Minecraft e Arduino
inicializar_log()
try:
    print("[INFO] Tentando conectar ao servidor Minecraft em {}:{}".format(MINECRAFT_HOST, MINECRAFT_PORT))
    mc = minecraft.Minecraft.create(MINECRAFT_HOST, MINECRAFT_PORT)
    print("[INFO] Conectado ao servidor Minecraft")
    registrar_log("START", "Conexão estabelecida com Minecraft")
    mc.postToChat("🔒 Sistema NFC iniciado! Aproxime um cartão para construir ou destruir a estrela.")
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
                    mc.postToChat("✅ Acesso autorizado! Construindo a estrela roxa, azul e rosa...")
                    construir_estrela(mc)
                elif status == "NEGADO":
                    mc.postToChat("🚫 Acesso negado! Destruindo a estrela...")
                    destruir_estrela(mc)
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
