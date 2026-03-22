import os
from datetime import datetime
from textwrap import dedent

from crewai import Agent, Task, Crew, Process
from crewai_tools.tools.scrape_website_tool.scrape_website_tool import ScrapeWebsiteTool

from core.env import bootstrap_environment
from my_llm import LLMagentes


bootstrap_environment()


def build_instagram_crew() -> Crew:
    cannabise_saude = ScrapeWebsiteTool(website_url="https://www.cannabisesaude.com.br/")
    dr_cannabis = ScrapeWebsiteTool(website_url="https://www.drcannabis.com.br/")

    planejador = Agent(
        role="Planejador de postagem",
        goal="Planejar conteudo envolvente para Instagram sobre {topic}",
        backstory=(
            "Voce planeja {n} posts para Instagram e prepara a base da pesquisa."
        ),
        verbose=True,
        llm=LLMagentes.get_model(LLMagentes.Models.DEEPSEEK_MODEL),
        allow_delegation=False,
    )

    pesquisador = Agent(
        role="Pesquisador",
        goal="Pesquisar tendencias e fatos relevantes sobre {topic}",
        backstory="Voce busca tendencias recentes e referencias confiaveis.",
        verbose=True,
        llm=LLMagentes.get_model(LLMagentes.Models.DEEPSEEK_MODEL),
        tools=[cannabise_saude, dr_cannabis],
        allow_delegation=False,
    )

    escritor = Agent(
        role="Escritor",
        goal=(
            "Escrever {n} posts cativantes em portugues para Instagram "
            "sobre {topic}, com 250 a 350 palavras por post."
        ),
        backstory="Voce transforma dados em texto claro e atraente.",
        llm=LLMagentes.get_model(LLMagentes.Models.DEEPSEEK_MODEL),
        verbose=True,
        allow_delegation=False,
    )

    fotografo = Agent(
        role="Fotografo",
        goal="Gerar prompts de imagem para {n} posts sobre {topic}",
        backstory="Voce cria prompts visuais claros e fortes para Instagram.",
        verbose=True,
        llm=LLMagentes.get_model(LLMagentes.Models.DEEPSEEK_MODEL),
        max_rpm=3,
        allow_delegation=False,
    )

    gerente = Agent(
        role="Gerente de postagens",
        goal="Revisar, corrigir e aprovar os {n} posts sobre {topic}",
        backstory="Voce garante padrao editorial e coerencia final.",
        verbose=True,
        llm=LLMagentes.get_model(LLMagentes.Models.DEEPSEEK_MODEL),
    )

    plano_task = Task(
        description=(
            "Defina publico-alvo, principais dores, palavras-chave e plano de conteudo "
            "para {n} posts sobre {topic}."
        ),
        expected_output="Plano de conteudo estruturado para {n} posts.",
        agent=planejador,
        allow_delegation=False,
        verbose=True,
    )

    pesquisa_task = Task(
        description="Pesquise tendencias recentes e referencias sobre {topic}.",
        expected_output="Relatorio de pesquisa com tendencias e fontes.",
        agent=pesquisador,
        allow_delegation=False,
        verbose=True,
    )

    escrita_task = Task(
        description=dedent(
            """
            Escreva {n} posts em portugues com base na pesquisa de {topic}.
            Cada post deve seguir o formato:

            POST:
            texto

            PROMPT:
            prompt da imagem
            """
        ),
        expected_output="{n} posts completos no formato POST/PROMPT.",
        agent=escritor,
        allow_delegation=False,
        verbose=True,
    )

    criacao_imagem_task = Task(
        description="Crie {n} prompts de imagem para Instagram sobre {topic}.",
        expected_output="{n} prompts de imagem de alta qualidade.",
        agent=fotografo,
        allow_delegation=False,
        verbose=True,
    )

    revisao_task = Task(
        description=(
            "Revise os {n} posts e prompts, corrija erros e garanta consistencia "
            "editorial em portugues do Brasil sobre {topic}."
        ),
        expected_output="{n} posts revisados e prontos para publicacao.",
        agent=gerente,
        verbose=True,
    )

    return Crew(
        agents=[planejador, pesquisador, escritor, fotografo, gerente],
        tasks=[plano_task, pesquisa_task, escrita_task, criacao_imagem_task, revisao_task],
        process=Process.sequential,
        verbose=True,
        memory=True,
    )


def run_instagram_crew(topic: str, n: int = 1):
    crew = build_instagram_crew()
    return crew.kickoff(inputs={"topic": topic, "n": n})


if __name__ == "__main__":
    result = run_instagram_crew(
        topic="Cannabis medicinal e melhora da coordenacao motora de autistas",
        n=1,
    )

    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"posts-{current_date}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(result))

    print(f"Resultado salvo em {os.path.abspath(filename)}")
