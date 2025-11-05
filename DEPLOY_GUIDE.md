# 🚀 Guia de Deploy - Agentic Platform no Streamlit Cloud

## 📋 Visão Geral

Este guia explica como fazer o deploy da Agentic Platform no **Streamlit Community Cloud** (gratuito) para compartilhar com terceiros.

## 🎯 O que é necessário?

### 1. **Conta no GitHub**
- Todos os arquivos do projeto devem estar em um repositório GitHub público
- O repositório pode ser privado, mas você precisará conectar sua conta Streamlit

### 2. **Variáveis de Ambiente**
- `OPENAI_API_KEY` - Chave da API OpenAI
- `SERPER_API_KEY` - Chave da API Serper (para busca web)
- Outras chaves de API que você possa usar

### 3. **Arquivos do Projeto**
- Código organizado e funcionando localmente
- Dependências listadas no `pyproject.toml` ou `requirements.txt`
- Arquivo principal (`app.py`) na raiz do projeto

---

## 📝 PASSO A PASSO DETALHADO

### **ETAPA 1: Preparar o Repositório GitHub**

#### 1.1. Verificar se o projeto está no GitHub
```bash
# Verificar se já é um repositório Git
git status

# Se não for, inicializar:
git init
git add .
git commit -m "Preparando para deploy no Streamlit Cloud"
```

#### 1.2. Criar/Atualizar repositório no GitHub
1. Acesse: https://github.com
2. Crie um novo repositório (ou use o existente)
3. Sincronize seu código:
```bash
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

#### 1.3. Verificar arquivos importantes na raiz
Certifique-se de que estes arquivos estão na raiz do projeto:
- ✅ `app.py` (arquivo principal)
- ✅ `pyproject.toml` ou `requirements.txt` (dependências)
- ✅ `README.md` (opcional, mas recomendado)

---

### **ETAPA 2: Criar arquivo de configuração do Streamlit**

#### 2.1. Criar arquivo `.streamlit/config.toml` (opcional)
Crie a pasta `.streamlit` na raiz do projeto e adicione:

```
.streamlit/
└── config.toml
```

**Conteúdo do `config.toml`:**
```toml
[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false
```

#### 2.2. Criar arquivo `requirements.txt` (se usar pip)
Se você usa `pyproject.toml` com UV, o Streamlit Cloud pode ter problemas. Crie um `requirements.txt` também:

```txt
streamlit>=1.40.0
streamlit-option-menu>=0.4.0
crewai>=0.95.0
crewai-tools>=0.25.8
beautifulsoup4>=4.12.0
requests>=2.32.0
python-dotenv>=1.0.0
langchain-openai>=0.2.0
openai>=1.0.0
```

---

### **ETAPA 3: Preparar o código para produção**

#### 3.1. Verificar caminhos de arquivos
Certifique-se de que os caminhos de imagens estão corretos:
- Verifique `images/_my_images.py`
- Os caminhos devem ser relativos ou funcionar em qualquer ambiente

#### 3.2. Remover arquivos sensíveis do Git
Crie/atualize o `.gitignore`:
```
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
.env.local
*.log
db/
temp/
```

#### 3.3. Verificar que não há dados sensíveis no código
- Nunca commite arquivos `.env`
- Não coloque chaves de API diretamente no código
- Use apenas variáveis de ambiente

---

### **ETAPA 4: Fazer Deploy no Streamlit Cloud**

#### 4.1. Acessar Streamlit Cloud
1. Acesse: https://share.streamlit.io/
2. Faça login com sua conta GitHub
3. Clique em **"New app"**

#### 4.2. Configurar o App
Preencha os campos:

- **Repository**: Selecione seu repositório GitHub
- **Branch**: `main` (ou a branch que você usa)
- **Main file path**: `app.py`
- **App URL**: Escolha um nome único (ex: `agentic-platform-remederi`)

#### 4.3. Configurar Variáveis de Ambiente
1. Clique em **"Advanced settings"**
2. Clique em **"Secrets"**
3. Adicione suas variáveis de ambiente:

```
OPENAI_API_KEY=sk-sua-chave-openai-aqui
SERPER_API_KEY=sua-chave-serper-aqui
```

**Formato no Streamlit Secrets:**
```toml
[secrets]
OPENAI_API_KEY = "sk-sua-chave-openai-aqui"
SERPER_API_KEY = "sua-chave-serper-aqui"
```

#### 4.4. Deploy
1. Clique em **"Deploy!"**
2. Aguarde o build (pode levar 2-5 minutos na primeira vez)
3. Seu app estará disponível em: `https://seu-app.streamlit.app`

---

### **ETAPA 5: Atualizar código para usar Secrets do Streamlit**

#### 5.1. Modificar código para ler secrets
No início do `app.py` ou nos arquivos que usam `.env`, adicione:

```python
import os
import streamlit as st

# Tentar carregar do .env (local) ou do Streamlit Secrets (produção)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Se estiver no Streamlit Cloud, usar secrets
if hasattr(st, 'secrets'):
    os.environ['OPENAI_API_KEY'] = st.secrets.get('OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
    os.environ['SERPER_API_KEY'] = st.secrets.get('SERPER_API_KEY', os.getenv('SERPER_API_KEY'))
```

#### 5.2. Atualizar crews para usar variáveis de ambiente
Os crews já usam `load_dotenv()`, então funcionarão automaticamente se as variáveis estiverem configuradas.

---

### **ETAPA 6: Testar e Compartilhar**

#### 6.1. Testar o App Deployado
1. Acesse a URL do seu app
2. Teste todas as funcionalidades:
   - ✅ Menu funcionando
   - ✅ Post Agent
   - ✅ Summary PDF
   - ✅ Pesquisador PDF
   - ✅ PubMed Agent

#### 6.2. Compartilhar com Terceiros
1. Compartilhe a URL: `https://seu-app.streamlit.app`
2. Qualquer pessoa pode acessar sem precisar de login (se o repositório for público)
3. Para repositório privado, os usuários precisarão ter acesso ao GitHub

---

## 🔧 TROUBLESHOOTING

### Problema: App não inicia
**Solução:**
- Verifique se `app.py` está na raiz
- Verifique se todas as dependências estão no `requirements.txt`
- Veja os logs de erro no Streamlit Cloud

### Problema: Erro de API Key
**Solução:**
- Verifique se as chaves estão configuradas em "Secrets"
- Verifique se o nome das variáveis está correto
- Certifique-se de que não há espaços extras

### Problema: Imagens não aparecem
**Solução:**
- Verifique os caminhos das imagens
- Certifique-se de que as imagens estão commitadas no GitHub
- Use caminhos relativos

### Problema: Dependências não instalam
**Solução:**
- Crie um `requirements.txt` mesmo usando `pyproject.toml`
- Verifique se todas as versões são compatíveis
- Veja os logs de build no Streamlit Cloud

---

## 📊 CUSTOS

### Streamlit Community Cloud (GRATUITO)
- ✅ Deploy gratuito
- ✅ Sem limite de apps públicos
- ✅ Até 1 app privado
- ✅ Sem custo de infraestrutura

### APIs Externas (CUSTOS)
- **OpenAI API**: Pago por uso (verifique preços)
- **Serper API**: Pago por uso (verifique preços)
- **Outras APIs**: Dependem do provedor

---

## 🔒 SEGURANÇA

### Boas Práticas:
1. ✅ Nunca commite arquivos `.env`
2. ✅ Use sempre variáveis de ambiente
3. ✅ Mantenha suas chaves de API seguras
4. ✅ Revise quem tem acesso ao repositório
5. ✅ Use repositório privado se necessário

---

## 📚 RECURSOS ADICIONAIS

- Documentação Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit Secrets: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management

---

## ✅ CHECKLIST PRÉ-DEPLOY

Antes de fazer deploy, verifique:

- [ ] Código está no GitHub
- [ ] `app.py` está na raiz do projeto
- [ ] `requirements.txt` ou `pyproject.toml` está atualizado
- [ ] `.gitignore` está configurado corretamente
- [ ] Nenhum arquivo `.env` está commitado
- [ ] Caminhos de imagens estão corretos
- [ ] Todas as dependências estão listadas
- [ ] Variáveis de ambiente identificadas
- [ ] Código testado localmente

---

## 🎉 Pronto!

Após seguir estes passos, sua Agentic Platform estará disponível online e pronta para compartilhar!

**URL do seu app:** `https://seu-app.streamlit.app`

