Sistema de Controle de Acesso NFC com Minecraft
📝 Visão Geral
Este projeto integra um leitor NFC (Arduino + RC522) ao Minecraft Java Edition usando o plugin RaspberryJuice. O Arduino lê cartões NFC e envia sinais via serial para um script Python, que controla ações no Minecraft, como abrir portas, ativar alarmes visuais e sonoros, e registrar logs.
🛠 Tecnologias

Hardware: Arduino Uno + Módulo RC522 NFC.
Software:
Arduino IDE (C++).
Python 3 (mcpi, pyserial).
Minecraft Java Edition + Servidor Spigot/Paper + RaspberryJuice.


Portas: Serial (Arduino) e 4711 (Minecraft API).

⚙️ Requisitos

Minecraft Java Edition (qualquer versão compatível com Spigot).
Servidor Spigot/Paper (mesma versão do jogo).
Plugin RaspberryJuice: Baixar.
Python 3: Instale dependências com pip install -r requirements.txt.
Arduino: Grave o código em arduino/nfc_access_control.ino.

🧩 Instalação

Servidor Minecraft:
Baixe e configure um servidor Spigot/Paper.
Coloque RaspberryJuice.jar em server/plugins/.
Inicie o servidor e conecte-se via localhost.


Arduino:
Conecte o RC522 aos pinos 9 (RST) e 10 (SS).
LEDs: Verde (5), Amarelo (6), Vermelho (7). Buzzer: Pino 3.
Grave o código nfc_access_control.ino.


Python:
Ajuste ARDUINO_PORT e PORTA_X, PORTA_Y, PORTA_Z em acesso_nfc_minecraft.py.
Instale dependências: pip install -r requirements.txt.
Rode: python python/acesso_nfc_minecraft.py.



📊 Funcionalidades

Leitura NFC: Detecta cartões e envia estados (LENDO, AUTORIZADO, NEGADO).
Minecraft:
Abre/fecha porta (bloco de ferro) para acessos autorizados.
Alarme visual (bloco vermelho) e sonoro para acessos negados.
Mensagens no chat do jogo.


Logs: Registra eventos em logs/acessos_nfc.csv.

💥 Como Testar

Inicie o servidor Minecraft com RaspberryJuice.
Conecte o Arduino via USB.
Rode o script Python.
Aproxime um cartão NFC:
Autorizado (ex: UID BA2CFE03): Porta abre com som.
Negado: Bloco vermelho + som de alarme.


Verifique logs em acessos_nfc.csv.

🔧 Customizações

Adicione mais UIDs em autorizados[] no código Arduino.
Altere coordenadas da porta no script Python.
Modifique sons em /playsound (ex: use outros sons do Minecraft).

👥 Créditos

Equipe: Matheus Gustavo, Davi Moreno.
Ferramentas: Arduino, Python, Minecraft, RaspberryJuice.

📜 Licença
MIT License - Use e modifique livremente!
Ajuda: Abra uma issue no repositório para suporte.