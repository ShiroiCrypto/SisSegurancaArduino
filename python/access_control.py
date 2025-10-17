import csv
import os
import serial
import time

ARQUIVO = 'funcionarios.csv'
PORTA = 'COM5'   # Ajuste conforme o Arduino
BAUD = 9600

def inicializar_arquivo():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['nome', 'id_funcional', 'funcao', 'acesso_permitido'])

def encontrar_funcionario(uid):
    with open(ARQUIVO, 'r', encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo)
        for linha in reader:
            if linha['id_funcional'].upper() == uid:
                return linha
    return None

def main():
    inicializar_arquivo()
    print("🔌 Conectando ao Arduino...")
    arduino = serial.Serial(PORTA, BAUD, timeout=1)
    time.sleep(2)
    print("✅ Conectado! Monitorando acessos...\n")

    while True:
        linha = arduino.readline().decode(errors='ignore').strip()
        if not linha:
            continue

        if linha.startswith("UID:"):
            uid = linha.split(":")[1].strip().upper()
            print(f"\n💳 Cartão detectado: {uid}")

            funcionario = encontrar_funcionario(uid)
            if funcionario:
                if funcionario['acesso_permitido'] == 'True':
                    print(f"✅ Acesso liberado para {funcionario['nome']} ({funcionario['funcao']})")
                    arduino.write(b'A')
                else:
                    print(f"❌ {funcionario['nome']} não tem permissão de acesso.")
                    arduino.write(b'N')
            else:
                print("⚠️ Cartão não cadastrado no sistema!")
                arduino.write(b'N')

        time.sleep(0.1)

if __name__ == "__main__":
    main()
