# apresentacao_completa.py
import subprocess
import time

def executar_script(nome_script, mensagem_inicio, mensagem_fim, delay=2):
    print(f"\n🔹 {mensagem_inicio}")
    time.sleep(delay)
    subprocess.run(["python", f"python/{nome_script}"])
    print(f"✅ {mensagem_fim}\n")
    time.sleep(delay)

def main():
    print("🚀 Iniciando apresentação completa do Sistema NFC + Minecraft...\n")
    time.sleep(2)

    executar_script("rainbow_nfc.py", "Iniciando arco-íris...", "Arco-íris concluído!")
    executar_script("estrela_nfc.py", "Iniciando construção das estrelas...", "Estrelas concluídas!")
    executar_script("encenacao_nfc.py", "Iniciando encenação final...", "Encenação finalizada!")

    print("🎉 Apresentação completa finalizada com sucesso!")

if __name__ == "__main__":
    main()
