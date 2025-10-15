import csv
from datetime import datetime
from mcpi.minecraft import Minecraft
import serial
import time
import os

# Configurações
MINECRAFT_HOST = "26.127.43.27"  # IP do servidor Minecraft via Radmin VPN
MINECRAFT_PORT = 4711             # Porta padrão do RaspberryJuice
ARDUINO_PORT = "COM3"             # Ajuste para sua porta (ex: '/dev/ttyUSB0' no Linux)
ARDUINO_BAUDRATE = 9600

# Coordenadas da porta no Minecraft (ajuste conforme seu mundo)
PORTA_X, PORTA_Y, PORTA_Z = 10, 65, 10

# Arquivo de log CSV
LOG_FILE = "logs/acessos_nfc.csv"

# Inicializa o CSV se não existir
if not os.path.exists(LOG_FILE):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Status", "Detalhes"])

# Função para registrar log
def registrar_log(status, detalhes):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, status, detalhes])
    print(f"📝 Log: {status} - {detalhes}")

# Conexão com Minecraft e Arduino
try:
    mc = Minecraft.create(MINECRAFT_HOST, MINECRAFT_PORT)
    arduino = serial.Serial(ARDUINO_PORT, ARDUINO_BAUDRATE, timeout=1)
    time.sleep(2)  # Estabiliza conexão
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    exit(1)

print("✅ Conectado ao Arduino e ao Minecraft!")
mc.postToChat("🔒 Sistema de Acesso NFC iniciado!")

# Loop principal
while True:
    try:
        if arduino.in_waiting > 0:
            linha = arduino.readline().decode().strip()
            if not linha:
                continue
            print(f"Arduino: {linha}")
            status, detalhes = linha.split(":", 1) if ":" in linha else (linha, "")
            registrar_log(status, detalhes)

            # Ações no Minecraft
            if status == "LENDO":
                mc.postToChat("📶 Lendo cartão NFC...")
            elif status == "AUTORIZADO":
                mc.postToChat("✅ Acesso autorizado! Abrindo a porta...")
                mc.setBlock(PORTA_X, PORTA_Y, PORTA_Z, 0)  # Abre a porta (remove bloco)
                mc.executeCommand(f"playsound block.iron_door.open block @a {PORTA_X} {PORTA_Y} {PORTA_Z} 1 1")
                time.sleep(3)
                mc.setBlock(PORTA_X, PORTA_Y, PORTA_Z, 64)  # Fecha a porta (bloco de ferro)
                mc.postToChat("🚪 Porta fechada.")
                mc.executeCommand(f"playsound block.iron_door.close block @a {PORTA_X} {PORTA_Y} {PORTA_Z} 1 1")
            elif status == "NEGADO":
                mc.postToChat("🚫 Acesso negado! Ativando alarme...")
                mc.setBlock(PORTA_X, PORTA_Y, PORTA_Z, 152)  # Bloco vermelho (alarme)
                mc.executeCommand(f"playsound entity.ghast.scream block @a {PORTA_X} {PORTA_Y} {PORTA_Z} 1 1")
                time.sleep(2)
                mc.setBlock(PORTA_X, PORTA_Y, PORTA_Z, 64)  # Volta ao normal
            elif status == "READY":
                mc.postToChat("🟡 Sistema pronto para nova leitura.")
    except Exception as e:
        print(f"⚠️ Erro no loop: {e}")
        time.sleep(1)  # Evita loop infinito