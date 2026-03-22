from pathlib import Path

from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool

from core.openai_client import get_openai_chat_model


TEMPLATE = """
ARTIGO:
  - TITULO: "[titulo do artigo no PDF]"
  - ARQUIVO: "[nome do arquivo PDF]"
  - OBJETIVOS: "[objetivos encontrados no PDF ou 'Informacao nao disponivel no documento']"
  - GAP: "[gap cientifico encontrado no PDF ou 'Informacao nao disponivel no documento']"
  - METODOLOGIA: "[metodologia encontrada no PDF ou 'Informacao nao disponivel no documento']"
  - DATASET: "[datasets citados ou 'Informacao nao disponivel no documento']"
  - RESULTADOS: "[resultados encontrados no PDF ou 'Informacao nao disponivel no documento']"
  - LIMITACOES: "[limitacoes citadas ou 'Informacao nao disponivel no documento']"
  - CONCLUSAO: "[conclusao no PDF ou 'Informacao nao disponivel no documento']"
  - FUTURO: "[recomendacoes futuras ou 'Informacao nao disponivel no documento']"
  - AVALIACAO: "[avaliacao critica baseada apenas no PDF]"
"""


REGRAS = """
Regras obrigatorias:
1) Use somente informacoes do PDF fornecido.
2) Se nao encontrar um dado no PDF, escreva: Informacao nao disponivel no documento.
3) Nao invente numeros, resultados, conclusoes ou referencias externas.
4) Entregue resposta final em YAML seguindo exatamente o template.
5) Escreva em portugues do Brasil com tom cientifico e neutro.
"""


class CrewPDFResumo:
    def __init__(self, pdf_path):
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF nao encontrado: {pdf_file}")

        if pdf_file.suffix.lower() != ".pdf":
            raise ValueError(f"Arquivo deve ser PDF: {pdf_file}")

        self.pdf_path = pdf_file
        self.pdf_tool = PDFSearchTool(str(pdf_file))
        self.llm = get_openai_chat_model(model_name="gpt-4o-mini", temperature=0.3)
        self.crew = self._criar_crew()

    def _criar_crew(self):
        leitor = Agent(
            role="Leitor Cientifico de PDF",
            goal="Extrair dados reais do PDF e preencher YAML sem alucinacoes.",
            backstory=(
                "Voce e especialista em leitura de artigo cientifico. "
                "Sempre usa a ferramenta PDFSearchTool antes de responder."
            ),
            tools=[self.pdf_tool],
            verbose=True,
            memory=False,
            llm=self.llm,
        )

        revisor = Agent(
            role="Revisor Cientifico",
            goal="Validar se o YAML contem somente dados do PDF e formato correto.",
            backstory=(
                "Voce revisa respostas cientificas para remover inferencias indevidas "
                "e garantir conformidade com o template."
            ),
            verbose=True,
            memory=False,
            llm=self.llm,
        )

        task_leitor = Task(
            description=(
                f"Leia o PDF em: {self.pdf_path}\n"
                "Use a PDFSearchTool para localizar titulo, objetivos, gap, metodologia, "
                "dataset, resultados, limitacoes, conclusao e pesquisa futura.\n"
                "Preencha todos os campos conforme o template.\n"
                f"Template:\n{TEMPLATE}\n"
                f"Regras:\n{REGRAS}"
            ),
            expected_output=(
                "YAML completo com todos os campos do template, "
                "usando somente dados do PDF ou 'Informacao nao disponivel no documento'."
            ),
            agent=leitor,
            tools=[self.pdf_tool],
        )

        task_revisor = Task(
            description=(
                "Revise o YAML do leitor. Verifique consistencia do formato, "
                "retire qualquer inferencia externa e mantenha apenas dados do PDF.\n"
                f"Template:\n{TEMPLATE}\n"
                f"Regras:\n{REGRAS}"
            ),
            expected_output=(
                "YAML final validado, sem alucinacoes e aderente ao template."
            ),
            agent=revisor,
        )

        return Crew(
            agents=[leitor, revisor],
            tasks=[task_leitor, task_revisor],
            process=Process.sequential,
        )

    def kickoff(self):
        resposta = self.crew.kickoff(
            inputs={
                "template": TEMPLATE,
                "regras": REGRAS,
                "arquivo_pdf": self.pdf_path.name,
            }
        )
        return resposta.raw
