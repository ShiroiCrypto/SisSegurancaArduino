# 🚧 Projeto Minecraft Interativo com NFC 🚀

Este projeto integra o jogo Minecraft (utilizando a API Raspberry Juice) com um sistema de Leitura NFC (usando Arduino e comunicação serial) para criar construções e encenações dinâmicas no mundo do jogo, ativadas pela aproximação de cartões NFC.

## 🌟 Funcionalidades Principais

  * **Ativação por NFC:** Cartões autorizados disparam apresentações ou construções no Minecraft.
  * **Encenação Sequencial:** Execução de uma sequência de passos (porta, arco-íris, estrela) na mesma coordenada.
  * **Construções Não Apagáveis:** As construções são mantidas e sobrepostas, a menos que uma limpeza manual ou um cartão "NEGADO" seja ativado.
  * **Registro de Logs:** Todas as ações e leituras NFC são registradas em arquivos CSV.

## ⚙️ Pré-requisitos

Para rodar este projeto, você precisará de:

### Hardware

  * Computador (Windows, Linux ou macOS).
  * Placa Arduino (ex: Uno, Nano) configurada para ler um módulo NFC (ex: PN532 ou RC522).
  * Módulo NFC.
  * Cabos e cartões/tags NFC para leitura.

### Software

  * **Minecraft:** Uma versão compatível com a API (geralmente a versão clássica do Minecraft Pi Edition ou um servidor com o plugin Raspberry Juice).
  * **Raspberry Juice Plugin/Servidor:** Para permitir que os scripts Python se conectem ao Minecraft.
  * **Python 3:** Com as seguintes bibliotecas:
      * `mcpi` (para comunicação com o Minecraft).
      * `pyserial` (para comunicação serial com o Arduino).

<!-- end list -->

```bash
pip install mcpi pyserial
```

## 🛠️ Configuração

Antes de executar os scripts, ajuste as configurações de conexão em todos os arquivos (`.py`):

1.  **Conexão Minecraft:**

      * `MINECRAFT_HOST`: IP do servidor Minecraft (Ex: `"26.127.43.27"` para Radmin VPN ou `"localhost"`).
      * `MINECRAFT_PORT`: Porta do servidor Raspberry Juice (`4711`).

2.  **Conexão Arduino:**

      * `ARDUINO_PORT`: A porta serial onde o Arduino está conectado (Ex: `"COM5"` no Windows ou `"/dev/ttyUSB0"` no Linux).
      * `ARDUINO_BAUDRATE`: A taxa de transmissão configurada no seu código Arduino (`9600`).

3.  **Coordenadas de Construção:**

      * `BASE_X`, `BASE_Y`, `BASE_Z`: Defina as coordenadas base no seu mundo Minecraft. Nos scripts modificados, todas as construções (porta, arco-íris, estrela) serão sobrepostas nesta coordenada.

## 🚀 Uso dos Scripts

### 1\. `apresentacao_completa.py` (Modo Loop Automático)

Este é o script principal para demonstração, que executa todas as construções sequencialmente e sobrepostas na mesma coordenada.

  * Se o Arduino não estiver conectado, ele entra em um loop infinito, limpando a área e reconstruindo a cada 35 segundos.
  * Se o Arduino estiver conectado, ele aguarda a leitura de um cartão NFC "AUTORIZADO" para iniciar a apresentação.

**Como executar:**

```bash
python apresentacao_completa.py
```

### 2\. `encenacao_nfc.py` (Modo Encenação)

Este script executa uma encenação passo a passo (Porta -\> Abre -\> Arco-Íris -\> Estrela -\> Fecha Porta) na mesma coordenada, sendo ideal para demonstrações ativadas por NFC.

  * **Cartão AUTORIZADO:** Inicia a `encenacao_completa`, limpando a área antes de começar e deixando as construções sobrepostas ao final, com a porta fechada.
  * **Cartão NEGADO:** Limpa a área de encenação imediatamente.

**Como executar:**

```bash
python encenacao_nfc.py
```

### 3\. Scripts Individuais (`estrela_nfc.py`, `rainbow_nfc.py`)

Estes scripts funcionam como unidades modulares, ativando ou desativando uma construção específica baseada na leitura NFC:

  * **Cartão AUTORIZADO:** Constrói a Estrela ou o Arco-Íris.
  * **Cartão NEGADO:** Destrói a construção.

## 📂 Estrutura do Projeto

| Arquivo | Função |
| :--- | :--- |
| `apresentacao_completa.py` | Apresentação sequencial de Arco-Íris, Estrela e Encenação, todos sobrepostos em uma única coordenada. |
| `encenacao_nfc.py` | Executa uma encenação mágica completa (porta, efeitos, construções), ativada por NFC, mantendo as construções sobrepostas. |
| `estrela_nfc.py` | Sistema de ativação por NFC para construir/destruir uma estrela. |
| `rainbow_nfc.py` | Sistema de ativação por NFC para construir/destruir um arco-íris. |
| `logs/` | Diretório onde os arquivos CSV de log são armazenados. |

## 👥 Créditos

- Matheus Gustavo (ShiroiCrypto)
- Davi Moreno (Retr0DedSec0)
- Davi Franklin (dvfrnkln)

## 🤝 Contribuindo

Veja o arquivo `CONTRIBUTING.md` para guia de estilo de código, convenções e como abrir PRs.
