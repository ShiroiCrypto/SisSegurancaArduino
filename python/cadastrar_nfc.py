import csv
import os
import serial
import time

ARQUIVO = 'funcionarios.csv'
PORTA = 'COM5'   # ⚠️ ajuste para a porta correta do Arduino
BAUD = 9600

def inicializar_arquivo():
    """Garante que o arquivo CSV existe e tem cabeçalho."""
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['nome', 'id_funcional', 'funcao', 'acesso_permitido'])

def cadastrar_funcionario(uid):
    """Solicita dados e cadastra um novo funcionário com base no UID do cartão."""
    print(f"\n🆕 Novo cartão detectado! UID: {uid}")
    nome = input("👤 Nome completo: ").strip()
    funcao = input("🏭 Função no setor: ").strip()

    # Define se tem acesso com base na função (pode ajustar à sua regra)
    permissoes = ['supervisor', 'gerente', 'analista', 'seguranca', 'segurança']
    acesso = funcao.lower() in permissoes

    with open(ARQUIVO, 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow([nome, uid, funcao, acesso])

    print("\n✅ Funcionário cadastrado com sucesso!")
    print("📋 Acesso ao setor de segurança:", "PERMITIDO ✅" if acesso else "NEGADO ❌")

def main():
    inicializar_arquivo()
    print("🔌 Conectando ao Arduino...")
    arduino = serial.Serial(PORTA, BAUD, timeout=1)
    time.sleep(2)
    print("✅ Conectado! Passe um cartão NFC para cadastrar.\n")

    cadastrados = set()

    while True:
        try:
            linha = arduino.readline().decode(errors='ignore').strip()
            if linha.startswith("UID:"):
                uid = linha.split(":")[1].strip().upper()

                if uid in cadastrados:
                    continue  # evita duplicação em uma mesma execução
                cadastrados.add(uid)

                # Verifica se já existe no arquivo
                ja_existe = False
                with open(ARQUIVO, 'r', encoding='utf-8') as arquivo:
                    reader = csv.DictReader(arquivo)
                    for linha in reader:
                        if linha['id_funcional'].upper() == uid:
                            ja_existe = True
                            break

                if ja_existe:
                    print(f"⚠️ Cartão {uid} já está cadastrado.")
                else:
                    cadastrar_funcionario(uid)

                print("\n👉 Passe outro cartão ou pressione Ctrl+C para sair.\n")

        except KeyboardInterrupt:
            print("\n🛑 Encerrando cadastro.")
            break
        except Exception as e:
            print(f"⚠️ Erro: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
