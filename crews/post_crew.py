from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

from core.openai_client import get_openai_chat_model


class CrewPostagem:
    def __init__(self):
        self.search_tool = SerperDevTool()
        self.llm = get_openai_chat_model(model_name="gpt-4o-mini", temperature=0.7)
        self.crew = self._criar_crew()

    def _criar_crew(self):
        pesquisador = Agent(
            role="Pesquisador",
            goal="Encontrar informacoes relevantes sobre {topic}",
            verbose=True,
            memory=False,
            backstory=(
                "Voce e um pesquisador especializado em descobrir informacoes "
                "uteis e relevantes para escrever sobre {topic}."
            ),
            tools=[self.search_tool],
            llm=self.llm,
        )

        escritor = Agent(
            role="Escritor",
            goal="Criar uma postagem convincente sobre {topic}",
            verbose=True,
            memory=False,
            backstory=(
                "Voce e um redator experiente que transforma informacoes em "
                "conteudos interessantes e informativos."
            ),
            llm=self.llm,
        )

        revisor = Agent(
            role="Revisor",
            goal="Revisar e melhorar a postagem sobre {topic}",
            verbose=True,
            memory=False,
            backstory=(
                "Voce e um revisor detalhista, especializado em ajustar o tom, "
                "a clareza e a gramatica de textos."
            ),
            llm=self.llm,
        )

        pesquisa_tarefa = Task(
            description=(
                "Pesquise informacoes detalhadas sobre {topic}. "
                "Foque em identificar pontos importantes e um resumo geral."
            ),
            expected_output="Um resumo detalhado sobre {topic}.",
            tools=[self.search_tool],
            agent=pesquisador,
        )

        escrita_tarefa = Task(
            description=(
                "Escreva uma postagem com base no conteudo pesquisado. "
                "A postagem deve ser clara, interessante e envolvente."
            ),
            expected_output="Uma postagem completa sobre {topic} com 3 paragrafos.",
            agent=escritor,
            context=[pesquisa_tarefa],
        )

        revisao_tarefa = Task(
            description=(
                "Revise a postagem criada, ajustando a clareza e corrigindo possiveis erros."
            ),
            expected_output="Uma postagem revisada e otimizada.",
            agent=revisor,
            context=[escrita_tarefa],
        )

        return Crew(
            agents=[pesquisador, escritor, revisor],
            tasks=[pesquisa_tarefa, escrita_tarefa, revisao_tarefa],
            process=Process.sequential,
        )

    def kickoff(self, inputs):
        resposta = self.crew.kickoff(inputs=inputs)
        return resposta.raw
