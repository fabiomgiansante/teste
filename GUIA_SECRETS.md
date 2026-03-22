# 🔐 Guia Completo: Como Configurar a API Key da OpenAI no Streamlit Cloud

## 📋 Passo a Passo

### 1️⃣ Acesse o Streamlit Cloud
1. Acesse: https://share.streamlit.io/
2. Faça login na sua conta
3. Clique no seu app (ou crie um novo se necessário)

### 2️⃣ Acesse as Configurações do App
1. No canto inferior direito do app, clique em **"Manage app"** (⚙️)
2. Ou acesse diretamente: https://share.streamlit.io/ → Seu App → Settings

### 3️⃣ Abra a Seção de Secrets
1. No menu lateral esquerdo, clique em **"Secrets"**
2. Você verá um editor de texto com formato TOML

### 4️⃣ Configure a API Key da OpenAI

#### ✅ Formato CORRETO:
```toml
OPENAI_API_KEY = "sk-proj-sua-chave-completa-aqui"
SERPER_API_KEY = "sua-chave-serper-aqui"
```

#### ❌ Formato INCORRETO (NÃO FAÇA):
```toml
# ❌ SEM aspas
OPENAI_API_KEY = sk-proj-sua-chave

# ❌ Com espaços extras
OPENAI_API_KEY = " sk-proj-sua-chave "

# ❌ Com quebras de linha
OPENAI_API_KEY = "sk-proj-sua-chave
continua-aqui"

# ❌ Com comentários inline
OPENAI_API_KEY = "sk-proj-sua-chave" # minha chave
```

### 5️⃣ Obter a Chave da OpenAI

1. Acesse: https://platform.openai.com/account/api-keys
2. Faça login na sua conta OpenAI
3. Clique em **"Create new secret key"**
4. Dê um nome para a chave (ex: "Streamlit App")
5. **COPIE A CHAVE IMEDIATAMENTE** (ela só aparece uma vez!)
6. Cole no Secrets do Streamlit Cloud

### 6️⃣ Exemplo Prático Completo

```toml
# Secrets do Streamlit Cloud
# Formato TOML - IMPORTANTE: Use aspas duplas!

OPENAI_API_KEY = "sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567abc890def123ghi456jkl789"
SERPER_API_KEY = "sua-chave-serper-aqui-123456"
```

### 7️⃣ Verificar se Está Correto

✅ **Correto:**
- Chave completa (normalmente 100+ caracteres)
- Começa com `sk-proj-` ou `sk-`
- Entre aspas duplas `"`
- Sem espaços antes/depois das aspas
- Uma chave por linha

❌ **Incorreto:**
- Chave truncada ou incompleta
- Sem aspas
- Com espaços extras
- Com quebras de linha
- Múltiplas chaves na mesma linha

### 8️⃣ Salvar e Reiniciar

1. Clique em **"Save"** no editor de Secrets
2. Volte para o app
3. Clique em **"Manage app"** → **"Reboot app"** (ou aguarde o redeploy automático)
4. Teste o app novamente

## 🔍 Troubleshooting

### Erro: "Incorrect API key provided"
**Solução:**
1. Verifique se a chave está completa (não foi truncada ao copiar)
2. Verifique se começa com `sk-proj-` ou `sk-`
3. Recopie a chave do OpenAI
4. Certifique-se de que está entre aspas duplas
5. Reinicie o app após salvar

### Erro: "OPENAI_API_KEY não encontrada"
**Solução:**
1. Verifique se o nome está exatamente: `OPENAI_API_KEY` (maiúsculas)
2. Verifique se está no formato TOML correto
3. Salve novamente e reinicie o app

### A chave funciona localmente mas não no Cloud
**Solução:**
1. Verifique se você está usando a mesma chave
2. Verifique se a chave não expirou ou foi revogada
3. Crie uma nova chave e configure novamente

## 📝 Checklist Final

Antes de testar, verifique:
- [ ] Chave copiada completa (100+ caracteres)
- [ ] Formato: `OPENAI_API_KEY = "sk-proj-..."`
- [ ] Aspas duplas `"` ao redor da chave
- [ ] Sem espaços extras
- [ ] Secrets salvos
- [ ] App reiniciado

## 🆘 Precisa de Ajuda?

Se ainda houver problemas:
1. Verifique os logs do app: "Manage app" → "Logs"
2. Verifique se a chave está ativa em: https://platform.openai.com/account/api-keys
3. Tente criar uma nova chave e configurar novamente

---

**Nota Importante:** A chave da API é sensível. Nunca compartilhe ou commite no Git. Use apenas os Secrets do Streamlit Cloud.
























