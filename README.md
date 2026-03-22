# Agentic Platform

Base Streamlit para execucao de crews focadas em suporte medico.

## Arquitetura Atual

- `app.py`: shell da aplicacao (menu + renderizacao da pagina selecionada).
- `menu/page_registry.py`: registro central de paginas do menu.
- `services/crew_factory.py`: registro central de crews e criacao dinamica.
- `core/env.py`: bootstrap de secrets/.env e validacao de API key.
- `core/openai_client.py`: fabrica com cache para `ChatOpenAI`.
- `core/execution_guard.py`: lock por sessao para evitar execucoes concorrentes da mesma tarefa.
- `paginas/`: UI de cada fluxo.
- `crews/`: implementacoes concretas.

## Como adicionar uma nova crew (plug-and-play)

1. Criar a classe da crew em `crews/` com metodo `kickoff`.
2. Registrar a crew em `services/crew_factory.py` (funcao `register_default_crews`).
3. Criar ou atualizar a pagina em `paginas/` chamando `create_crew("sua_chave", ...)`.
4. Registrar a pagina no menu em `menu/page_registry.py`.

## Exemplo de uso da factory

```python
from services.crew_factory import create_crew

crew = create_crew("post_agent")
resultado = crew.kickoff(inputs={"topic": "Cannabis medicinal"})
```

## Observacoes de deploy

- Use Secrets do Streamlit para chaves de API.
- Nao salve arquivos de upload com nome fixo; use caminho temporario unico.
- Evite importar crews no topo das paginas para reduzir cold start.
- Use `SessionExecutionGuard` em tarefas longas para bloquear dupla execucao por sessao.
