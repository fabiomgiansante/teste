from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool

from core.openai_client import get_openai_chat_model


class CrewPDFResumo:
    def __init__(self, pdf_path):
        self.pdf_tool = PDFSearchTool(pdf_path)
        self.llm = get_openai_chat_model(model_name="gpt-4o-mini", temperature=0.7)
        self.crew = self._criar_crew()

    def _criar_crew(self):
        resumidor = Agent(
            role="Resumidor",
            goal="Criar um resumo do conteudo de um PDF.",
            verbose=True,
            memory=False,
            backstory=(
                "Voce e um especialista em sintetizar informacoes de documentos extensos. "
                "Seu objetivo e identificar os pontos principais e entregar um resumo conciso e util."
            ),
            tools=[self.pdf_tool],
            llm=self.llm,
        )

        resumo_tarefa = Task(
            description=(
                "Leia o conteudo do PDF fornecido usando a tool integrada. "
                "Produza um resumo objetivo, destacando os principais pontos e ideias essenciais."
            ),
            expected_output="Um resumo claro e objetivo do conteudo do PDF.",
            agent=resumidor,
        )

        return Crew(
            agents=[resumidor],
            tasks=[resumo_tarefa],
            process=Process.sequential,
        )

    def kickoff(self):
        resposta = self.crew.kickoff()
        return resposta.raw
