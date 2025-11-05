import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função para obter o modelo OpenAI apenas quando necessário
def get_openai_model():
    """Retorna o modelo OpenAI, inicializando apenas quando necessário"""
    # Garantir que a variável de ambiente está carregada
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente!")
    
    # Inicializar ChatOpenAI explicitamente com a API key
    return ChatOpenAI(
        model_name="gpt-4o-mini", 
        temperature=0.7,
        api_key=api_key
    )


class CrewPDFResumo:

    def __init__(self, pdf_path):
        self.pdf_tool = PDFSearchTool(pdf_path)  # Tool nativa do CrewAI para leitura de PDF
        self.llm = get_openai_model()  # Configuração do modelo LLM
        self.crew = self._criar_crew()

    def _criar_crew(self):
        # Definindo o agente resumidor
        resumidor = Agent(
            role='''Resumidor''',
            goal='''Criar um resumo do conteúdo de um PDF.''',
            verbose=True,
            memory=True,
            backstory='''Você é um especialista em sintetizar informações de documentos extensos. 
                        Seu objetivo é identificar os pontos principais e entregar um resumo conciso e útil.''',
            tools=[self.pdf_tool],  # Associando a tool de leitura de PDF ao agente
            llm=self.llm
        )

        # Tarefa de resumo
        resumo_tarefa = Task(
            description='''Leia o conteúdo do PDF fornecido usando a tool integrada. 
                          Produza um resumo objetivo, destacando os principais pontos e ideias essenciais.''',
            expected_output='''Um resumo claro e objetivo do conteúdo do PDF.''',
            agent=resumidor
        )
        # Criando o Crew
        return Crew(
            agents=[resumidor],
            tasks=[resumo_tarefa],
            process=Process.sequential
        )
    def kickoff(self):
        # Executa o Crew com o caminho do PDF como entrada
        resposta = self.crew.kickoff()
        return resposta.raw
