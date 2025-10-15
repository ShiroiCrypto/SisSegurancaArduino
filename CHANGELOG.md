# 📝 Changelog - Sistema NFC Minecraft

## [2.0.0] - 2025-01-15

### 🚀 Novas Funcionalidades
- **Arquitetura Modular**: Código reorganizado em classes especializadas
- **Configuração Centralizada**: Todas as configurações em `config.json`
- **Sistema de Logs Robusto**: Logs com rotação automática e múltiplos níveis
- **Reconexão Automática**: Recuperação automática de conexões perdidas
- **Seleção Dinâmica de Portas**: Toque em portas no jogo para selecioná-las
- **Cache Inteligente**: Sistema de cache para melhor performance
- **Configuração Interativa**: Setup guiado via `setup_config.py`
- **Validação de Configurações**: Verificação automática de configurações
- **Scripts de Teste**: Sistema de testes automatizados

### 🔧 Melhorias
- **Tratamento de Erros**: Recuperação robusta de falhas
- **Performance**: Otimizações no gerenciamento de portas
- **Usabilidade**: Interface mais amigável para configuração
- **Documentação**: README atualizado com guias detalhados
- **Migração**: Guia de migração da v1.0 para v2.0

### 📁 Novos Arquivos
- `python/nfc_minecraft_system.py` - Sistema principal refatorado
- `python/connection_manager.py` - Gerenciamento de conexões
- `python/door_manager.py` - Gerenciamento de portas
- `python/logger.py` - Sistema de logs robusto
- `config.json` - Configuração centralizada
- `config.example.json` - Exemplo de configuração
- `run_system.py` - Script principal de execução
- `setup_config.py` - Configuração interativa
- `test_system.py` - Script de testes
- `MIGRATION_GUIDE.md` - Guia de migração
- `CHANGELOG.md` - Este arquivo

### 🔄 Mudanças Breaking
- **Execução**: Agora use `python run_system.py` em vez de `python python/acesso_nfc_minecraft.py`
- **Configuração**: Todas as configurações agora estão em `config.json`
- **Logs**: Estrutura de logs completamente reformulada
- **Dependências**: Novas dependências adicionadas ao `requirements.txt`

### 🐛 Correções
- Corrigido problema de codificação UTF-8 no Windows
- Melhorado tratamento de conexões perdidas
- Corrigido problema de spam de logs
- Melhorado sistema de cache de portas

### 📚 Documentação
- README.md completamente atualizado
- Adicionado guia de migração
- Documentação de API das classes
- Exemplos de configuração

---

## [1.0.0] - 2025-01-15 (Legacy)

### Funcionalidades Originais
- Sistema básico de controle de acesso NFC
- Integração com Minecraft via RaspberryJuice
- Logs simples em CSV
- Configuração hardcoded no código Python
- Código monolítico em um único arquivo

### Limitações da v1.0
- Configuração difícil (editar código Python)
- Sem reconexão automática
- Logs limitados
- Sem validação de configurações
- Código difícil de manter
- Sem tratamento robusto de erros
