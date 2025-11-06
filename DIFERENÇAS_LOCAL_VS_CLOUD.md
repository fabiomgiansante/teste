# Por que há problemas no Streamlit Cloud se funcionava localmente?

## 🔍 Principais Diferenças entre Ambiente Local e Streamlit Cloud

### 1. **Dependências Faltando** ⚠️ CRÍTICO
**Problema:** O `PDFSearchTool` do CrewAI precisa de bibliotecas específicas para ler PDFs que não estavam no `requirements.txt`:
- `pypdf` - Para leitura básica de PDFs
- `pdfplumber` - Para extração avançada de texto e tabelas
- `pdfminer.six` - Para parsing de PDFs complexos

**Solução:** Adicionadas ao `requirements.txt`

### 2. **Variáveis de Ambiente** 🔑
**Local:**
- Usa arquivo `.env` diretamente
- `load_dotenv()` funciona imediatamente
- API keys carregadas antes de qualquer import

**Cloud:**
- Usa Streamlit Secrets (TOML)
- Secrets só disponíveis após `st` estar inicializado
- Precisa de lógica especial para carregar antes dos imports

**Solução:** Implementada prioridade: Secrets primeiro, depois `.env`

### 3. **Caminhos de Arquivos** 📁
**Local:**
- Caminhos absolutos funcionam
- Diretório `temp/` persiste entre execuções
- Permissões de escrita garantidas

**Cloud:**
- Apenas caminhos relativos funcionam
- Diretório `temp/` pode ser limpo entre execuções
- Sistema de arquivos efêmero

**Solução:** Usar caminhos relativos e criar diretórios dinamicamente

### 4. **Memória e Recursos** 💾
**Local:**
- Sem limites de memória
- Sem timeout de execução
- Processamento pode demorar o quanto for necessário

**Cloud:**
- Limite de memória (~1GB)
- Timeout de execução (alguns minutos)
- Processamento pode ser interrompido

**Solução:** Desabilitar `memory=True` nos agents (evita Qdrant/ChromaDB)

### 5. **Cache e Estado** 🔄
**Local:**
- Cache do Streamlit funciona normalmente
- Estado persiste entre recarregamentos
- `__pycache__` é criado e mantido

**Cloud:**
- Cache pode ser limpo entre deploys
- Estado pode ser perdido
- `__pycache__` pode causar problemas

**Solução:** Limpar `__pycache__` e usar `st.session_state` adequadamente

### 6. **Versões de Bibliotecas** 📦
**Local:**
- Versões instaladas podem ser diferentes
- Dependências transitivas podem estar presentes
- Ambiente pode ter bibliotecas extras

**Cloud:**
- Instala apenas o que está em `requirements.txt`
- Versões exatas conforme especificado
- Ambiente limpo sem dependências extras

**Solução:** Especificar todas as dependências explicitamente

### 7. **Processamento de PDF** 📄
**Local:**
- PDFSearchTool pode funcionar mesmo sem todas as dependências
- Sistema pode ter bibliotecas instaladas globalmente
- Processamento pode usar recursos do sistema

**Cloud:**
- PDFSearchTool precisa de todas as dependências explícitas
- Ambiente isolado sem bibliotecas extras
- Processamento limitado aos recursos do container

**Solução:** Adicionar todas as dependências de PDF ao `requirements.txt`

## ✅ Correções Aplicadas

1. ✅ Adicionadas dependências de PDF ao `requirements.txt`
2. ✅ Implementado carregamento prioritário de Secrets
3. ✅ Desabilitado `memory=True` nos agents
4. ✅ Validação de arquivos PDF antes de processar
5. ✅ Instruções melhoradas para uso do PDFSearchTool
6. ✅ Temperatura reduzida para melhor precisão

## 🎯 Próximos Passos

1. **Testar localmente** com as mesmas dependências do Cloud
2. **Verificar logs** no Streamlit Cloud para erros específicos
3. **Monitorar uso de recursos** durante processamento
4. **Adicionar tratamento de erros** mais robusto

## 💡 Dica

Para evitar problemas futuros, sempre teste com um ambiente limpo antes de fazer deploy:
```bash
# Criar ambiente virtual limpo
python -m venv venv_test
source venv_test/bin/activate  # Linux/Mac
# ou
venv_test\Scripts\activate  # Windows

# Instalar apenas do requirements.txt
pip install -r requirements.txt

# Testar o app
streamlit run app.py
```

