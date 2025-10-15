# 🔒 Sistema de Controle de Acesso NFC com Minecraft 🚀

![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=flat&logo=Arduino)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=Python)
![Minecraft](https://img.shields.io/badge/-Minecraft-62B47A?style=flat)

## 📝 Visão Geral
Este projeto combina o mundo físico com o virtual! Usamos um **Arduino Uno** com um leitor **NFC RC522** para detectar cartões e controlar ações no **Minecraft Java Edition**. Um script **Python** faz a ponte entre o Arduino e o Minecraft, via plugin **RaspberryJuice**, permitindo abrir portas, ativar alarmes visuais e sonoros, exibir mensagens no chat e registrar logs. O console do Arduino é estilizado com emojis para uma experiência divertida e visual! 😎

Ideal para demonstrações educacionais, projetos de IoT ou para impressionar seus amigos no Minecraft!

## 🎮 Como Funciona
- **Arduino + RC522**: Lê cartões NFC e envia estados (`LENDO`, `AUTORIZADO`, `NEGADO`, `READY`) via serial.
- **Python**: Interpreta os sinais do Arduino e envia comandos ao Minecraft.
- **Minecraft (Spigot + RaspberryJuice)**: Executa ações como abrir portas, mostrar mensagens e tocar sons.
- **Rede Local (Radmin VPN)**: Conecta o servidor Minecraft (IP `26.127.43.27`) e clientes na mesma rede.

## 🛠 Tecnologias Utilizadas
- **Hardware**:
  - Arduino Uno
  - Módulo NFC RC522
  - LEDs (Verde, Amarelo, Vermelho) + Buzzer
- **Software**:
  - Arduino IDE (C++)
  - Python 3 (bibliotecas `mcpi`, `pyserial`)
  - Minecraft Java Edition + Servidor Spigot/Paper + Plugin RaspberryJuice
- **Comunicação**:
  - Porta Serial (Arduino ↔ Python)
  - Porta 4711 (Python ↔ Minecraft via RaspberryJuice)
  - Rede local via Radmin VPN (IP: `26.127.43.27`)

## 📊 Funcionalidades
- **Leitura NFC**: Detecta cartões e envia estados via serial.
- **Ações no Minecraft**:
  - **Autorizado**: Abre uma porta de ferro por 3 segundos e toca som (`block.iron_door.open/close`).
  - **Negado**: Ativa um alarme visual (bloco vermelho) e sonoro (`entity.ghast.scream`).
  - **Mensagens**: Exibe mensagens no chat do jogo (ex: "✅ Acesso autorizado!").
- **Logs**: Registra eventos com timestamp em `logs/acessos_nfc.csv`.
- **Console Estilizado**: Saída do Arduino com emojis (🔒, 📶, ✅, ❌, 😎) no Serial Monitor.

## ⚙️ Requisitos
- **Minecraft Java Edition** (qualquer versão compatível com Spigot/Paper).
- **Servidor Spigot/Paper** (mesma versão do jogo).
- **Plugin RaspberryJuice**: [Baixar aqui](https://dev.bukkit.org/projects/raspberryjuice).
- **Python 3**: Instale com `pip install -r requirements.txt`.
- **Arduino Uno**: Com módulo RC522 e código em `arduino/nfc_access_control.ino`.
- **Radmin VPN**: Para rede local com IP `26.127.43.27`.

## 🧩 Instalação
### 1. Configurar o Servidor Minecraft
1. Baixe o Spigot/Paper compatível com sua versão do Minecraft ([Spigot](https://getbukkit.org/) ou [Paper](https://papermc.io/)).
2. Coloque o arquivo `RaspberryJuice.jar` na pasta `server/plugins/`.
3. Configure o arquivo `server.properties`:
   ```properties
   server-ip=26.127.43.27
   server-port=25565
   online-mode=false
   ```
4. Inicie o servidor com:
   ```bash
   java -jar spigot.jar
   ```
5. Conecte-se ao servidor no Minecraft com o IP `26.127.43.27:25565`.

### 2. Configurar o Arduino
1. Conecte o módulo RC522:
   - SDA (pino 10), RST (pino 9), MOSI (11), MISO (12), SCK (13).
2. Conecte os LEDs: Verde (5), Amarelo (6), Vermelho (7). Buzzer: Pino 3.
3. Abra `arduino/nfc_access_control.ino` no Arduino IDE e faça upload.
4. Abra o Serial Monitor (9600 baud) para ver a saída com emojis.

### 3. Configurar o Python
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Edite `python/acesso_nfc_minecraft.py`:
   - Confirme `MINECRAFT_HOST = "26.127.43.27"`.
   - Ajuste `ARDUINO_PORT` (ex: `"COM3"` no Windows ou `"/dev/ttyUSB0"` no Linux).
   - Defina `PORTA_X`, `PORTA_Y`, `PORTA_Z` com as coordenadas da porta no seu mundo.
3. Execute o script:
   ```bash
   python python/acesso_nfc_minecraft.py
   ```

### 4. Configurar a Rede (Radmin VPN)
1. Instale o [Radmin VPN](https://www.radmin-vpn.com/) em todas as máquinas (servidor e clientes).
2. Crie ou entre na mesma rede Radmin.
3. Verifique que o servidor usa o IP `26.127.43.27`.
4. Libere as portas no firewall da máquina do servidor:
   ```bash
   netsh advfirewall firewall add rule name="Minecraft" dir=in action=allow protocol=TCP localport=25565
   netsh advfirewall firewall add rule name="RaspberryJuice" dir=in action=allow protocol=TCP localport=4711
   ```
5. Teste a conectividade:
   ```bash
   ping 26.127.43.27
   telnet 26.127.43.27 4711
   ```

## 💥 Como Testar
1. Inicie o servidor Minecraft com o plugin RaspberryJuice.
2. Conecte o Arduino via USB à máquina que executa o Python.
3. Rode o script Python: `python python/acesso_nfc_minecraft.py`.
4. Entre no Minecraft e conecte-se ao servidor (`26.127.43.27:25565`).
5. Aproxime um cartão NFC:
   - **Autorizado** (ex: UID `BA2CFE03`): Porta de ferro abre por 3s, toca som de porta, mensagem no chat: `✅ Acesso autorizado!`.
   - **Negado**: Bloco vermelho aparece por 2s, toca som de alarme, mensagem: `🚫 Acesso negado!`.
   - **Prontidão**: Mensagem `🟡 Sistema pronto para nova leitura.`.
6. Verifique os logs em `logs/acessos_nfc.csv` e o console do Arduino no Serial Monitor.

## 📂 Estrutura do Projeto
```
nfc-minecraft-access-control/
├── arduino/
│   └── nfc_access_control.ino  # Código Arduino com console estilizado
├── python/
│   └── acesso_nfc_minecraft.py  # Script Python para integração com Minecraft
├── logs/
│   └── .gitkeep                # Mantém a pasta no Git (acessos_nfc.csv é gerado)
├── server/
│   ├── spigot.jar              # Servidor Spigot/Paper (baixe separadamente)
│   └── plugins/
│       └── RaspberryJuice.jar  # Plugin RaspberryJuice (baixe separadamente)
├── README.md                   # Documentação do projeto
├── requirements.txt            # Dependências Python
└── .gitignore                  # Ignora arquivos gerados
```

## 🔧 Customizações
- **Adicionar Cartões**: Inclua novos UIDs na lista `autorizados[]` em `nfc_access_control.ino`.
- **Mudar a Porta**: Altere `PORTA_X`, `PORTA_Y`, `PORTA_Z` em `acesso_nfc_minecraft.py`.
- **Sons Personalizados**: Modifique os comandos `/playsound` no Python (ex: use `entity.villager.no` para acessos negados).
- **Efeitos Visuais**: Adicione partículas com:
  ```python
  mc.executeCommand(f"particle flame {PORTA_X} {PORTA_Y} {PORTA_Z} 0.5 0.5 0.5 0.1 10")
  ```

## 📸 Screenshots
(Adicione imagens do Serial Monitor e do Minecraft aqui após capturá-las)
```markdown
![Arduino Serial Monitor](screenshots/serial_monitor.png)
![Minecraft Door](screenshots/minecraft_door.png)
```

## 👥 Créditos
- **Equipe**: Matheus Gustavo, Davi Moreno
- **Ferramentas**: Arduino, Python, Minecraft, RaspberryJuice, Radmin VPN
- **Assistência**: Grok (xAI) para geração e estilização de código

## 📜 Licença
MIT License - Sinta-se à vontade para usar, modificar e compartilhar!

## ❓ Suporte
Encontrou problemas? Abra uma [issue](https://github.com/seu-usuario/nfc-minecraft-access-control/issues) no repositório ou entre em contato com a equipe.