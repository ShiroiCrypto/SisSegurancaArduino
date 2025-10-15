# 🔒 Sistema de Controle de Acesso NFC com Minecraft v3.0 🚀

![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=flat&logo=Arduino)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=Python)
![Minecraft](https://img.shields.io/badge/-Minecraft-62B47A?style=flat)

## 📝 Visão Geral
Este projeto combina o mundo físico com o virtual! Usamos um **Arduino Uno** com um leitor **NFC RC522** para detectar cartões e controlar ações no **Minecraft Java Edition**. O sistema foi completamente refatorado com arquitetura modular, configuração centralizada, logs robustos e reconexão automática. Um script **Python** faz a ponte entre o Arduino e o Minecraft, via plugin **RaspberryJuice**, permitindo construir arco-íris coloridos, estrelas de vidro e destruir construções com cartões não autorizados. 😎

**Nova versão v3.0 com funcionalidades incríveis:**
- ✅ **Arco-íris Colorido**: Roxo, azul e rosa com múltiplas camadas
- ✅ **Estrelas de Vidro**: 12 estrelas coloridas ao redor do arco-íris
- ✅ **Sistema de Destruição**: Cartões não autorizados destroem tudo
- ✅ **Arquitetura Modular**: Código organizado e fácil de manter
- ✅ **Logs Detalhados**: Sistema robusto de logging
- ✅ **Reconexão Automática**: Recuperação de conexões perdidas

Ideal para demonstrações educacionais, projetos de IoT ou para impressionar seus amigos no Minecraft!

## 🎮 Como Funciona
- **Arduino + RC522**: Lê cartões NFC e envia estados (`LENDO`, `AUTORIZADO`, `NEGADO`, `READY`) via serial.
- **Python**: Interpreta os sinais do Arduino e envia comandos ao Minecraft.
- **Minecraft (Spigot + RaspberryJuice)**: Constrói arco-íris coloridos, estrelas de vidro e destrói construções.
- **Rede Local (Radmin VPN)**: Conecta o servidor Minecraft (IP `26.127.43.27`) e clientes na mesma rede.

### 🌈 **Funcionalidades Principais**
- **Cartão Autorizado** → Constrói arco-íris roxo, azul e rosa + 12 estrelas de vidro coloridas
- **Cartão Não Autorizado** → Destrói toda a construção existente
- **Logs Detalhados** → Registra todas as ações em arquivo CSV

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
  - **Autorizado**: Constrói arco-íris roxo, azul e rosa com múltiplas camadas + 12 estrelas de vidro coloridas.
  - **Negado**: Destrói toda a construção existente em uma área ampla.
  - **Mensagens**: Exibe mensagens no chat do jogo (ex: "✅ Acesso autorizado!").
- **Logs**: Registra eventos com timestamp em `logs/rainbow_nfc_log.csv`.
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

### 3. Configurar o Sistema Python
1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o sistema de arco-íris:**
   ```bash
   python python/rainbow_nfc.py
   ```
   
3. **Execute o sistema de estrela (alternativo):**
   ```bash
   python python/estrela_nfc.py
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
3. Rode o script Python: `python python/rainbow_nfc.py`.
4. Entre no Minecraft e conecte-se ao servidor (`26.127.43.27:25565`).
5. Aproxime um cartão NFC:
   - **Autorizado** (ex: UID `BA2CFE03`): Constrói arco-íris roxo, azul e rosa + 12 estrelas de vidro coloridas, mensagem no chat: `✅ Acesso autorizado!`.
   - **Negado**: Destrói toda a construção existente, mensagem: `🚫 Acesso negado!`.
   - **Prontidão**: Mensagem `🟡 Sistema pronto para nova leitura.`.
6. Verifique os logs em `logs/rainbow_nfc_log.csv` e o console do Arduino no Serial Monitor.

## 📂 Estrutura do Projeto (v3.0)
```
SisSegurancaArduino/
├── arduino/
│   └── nfc_access_control.ino     # Código Arduino com console estilizado
├── python/
│   ├── rainbow_nfc.py             # Sistema de arco-íris com estrelas de vidro
│   ├── estrela_nfc.py             # Sistema de estrela colorida
│   └── acesso_nfc_minecraft.py   # Script legado (deprecated)
├── logs/
│   ├── rainbow_nfc_log.csv        # Logs do sistema de arco-íris
│   ├── estrela_nfc_log.csv        # Logs do sistema de estrela
│   └── acessos_nfc.csv           # Logs legados
├── requirements.txt              # Dependências Python
├── README.md                     # Documentação do projeto
└── LICENSE                       # Licença MIT
```

## 🔧 Customizações (v3.0)

### Principais Customizações:
- **Cores do Arco-íris**: Edite `colors = [10, 11, 6]` em `rainbow_nfc.py` (Roxa, Azul, Rosa)
- **Cores da Estrela**: Edite `colors = [10, 11, 6]` em `estrela_nfc.py` (Roxa, Azul, Rosa)
- **Coordenadas**: Modifique `center_x, center_y, center_z` nos scripts Python
- **Tamanho do Arco-íris**: Ajuste `height` e `range(0, 160)` em `rainbow_nfc.py`
- **Quantidade de Estrelas**: Modifique `num_estrelas = 12` em ambos os scripts
- **Área de Destruição**: Ajuste os valores em `destruir_construcao()` e `destruir_estrela()`
- **Logs**: Verifique os arquivos em `logs/` para debug

## 📸 Screenshots
(Adicione imagens do Serial Monitor e do Minecraft aqui após capturá-las)
```markdown
![Arduino Serial Monitor](screenshots/serial_monitor.png)
![Minecraft Door](screenshots/minecraft_door.png)
```

## 🆕 Novidades da v3.0

### Funcionalidades Incríveis:
- **Arco-íris Colorido**: Roxo, azul e rosa com múltiplas camadas para volume
- **Estrelas de Vidro**: 12 estrelas coloridas ao redor do arco-íris
- **Sistema de Destruição**: Cartões não autorizados destroem toda a construção
- **Dois Sistemas**: Arco-íris (`rainbow_nfc.py`) e Estrela (`estrela_nfc.py`)
- **Logs Específicos**: Cada sistema tem seu próprio arquivo de log
- **Performance Otimizada**: Construção mais rápida e eficiente

### Melhorias Técnicas:
- **Código Limpo**: Removidas funções desnecessárias
- **Mensagens Atualizadas**: Chat mais informativo
- **Área de Destruição**: Cobertura ampla para garantir remoção completa
- **Estrelas de Vidro**: 16 cores diferentes para variedade visual

## 👥 Créditos
- **Equipe**: Matheus Gustavo, Davi Moreno
- **Ferramentas**: Arduino, Python, Minecraft, RaspberryJuice, Radmin VPN

## 📜 Licença
MIT License - Sinta-se à vontade para usar, modificar e compartilhar!

## ❓ Suporte
Encontrou problemas? 
- Verifique os logs em `logs/` para detalhes de erros
- Execute `python python/rainbow_nfc.py` para o sistema de arco-íris
- Execute `python python/estrela_nfc.py` para o sistema de estrela
- Consulte a documentação acima para configurações avançadas