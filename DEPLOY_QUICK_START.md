# ⚡ Guia Rápido - Deploy Streamlit Cloud

## 🎯 Resumo em 5 Passos

### 1️⃣ **Preparar GitHub**
```bash
# Se ainda não estiver no GitHub:
git init
git add .
git commit -m "Preparando para deploy"
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git push -u origin main
```

### 2️⃣ **Criar App no Streamlit Cloud**
1. Acesse: https://share.streamlit.io/
2. Login com GitHub
3. Clique em "New app"
4. Selecione repositório e branch
5. Main file: `app.py`

### 3️⃣ **Configurar Secrets (Variáveis de Ambiente)**
No Streamlit Cloud, vá em "Secrets" e adicione:
```toml
OPENAI_API_KEY = "sua-chave-aqui"
SERPER_API_KEY = "sua-chave-aqui"
```

### 4️⃣ **Deploy**
- Clique em "Deploy!"
- Aguarde 2-5 minutos
- Seu app estará em: `https://seu-app.streamlit.app`

### 5️⃣ **Compartilhar**
- Compartilhe a URL com terceiros
- Qualquer pessoa pode acessar (se repositório público)

---

## 📋 Checklist Rápido

- [ ] Código no GitHub
- [ ] `requirements.txt` criado
- [ ] `.gitignore` configurado
- [ ] Secrets configurados no Streamlit Cloud
- [ ] Deploy realizado
- [ ] Testado funcionando

---

## 🔗 Links Úteis

- **Streamlit Cloud**: https://share.streamlit.io/
- **Documentação**: https://docs.streamlit.io/streamlit-community-cloud
- **Secrets**: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management

---

## ⚠️ Importante

1. **Nunca** commite arquivos `.env` (ele fica só na sua máquina; o Cloud usa **Secrets**)
2. Antes de `git add` / `git push`, confira que o `.env` **não** vai no commit:
   - `git check-ignore -v .env` → deve mostrar que `.gitignore` ignora `.env`
   - `git ls-files .env` → deve **não** listar nada (se listar, rode `git rm --cached .env` e commit a remoção do rastreamento)
3. **Sempre** use Secrets do Streamlit para chaves de API
4. Verifique se `requirements.txt` está atualizado
5. Teste localmente antes de fazer deploy

---

## 🆘 Problemas Comuns

**Erro: "Module not found"**
→ Adicione a dependência no `requirements.txt`

**Erro: "API Key not found"**
→ Verifique se configurou corretamente no Secrets

**Erro: "App não inicia"**
→ Verifique se `app.py` está na raiz do projeto

