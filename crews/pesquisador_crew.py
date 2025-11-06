import os
import yaml
from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables (apenas se não existir)
if not os.getenv('OPENAI_API_KEY'):
    load_dotenv(override=False)

# Função para obter o modelo OpenAI apenas quando necessário
def get_openai_model():
    """Retorna o modelo OpenAI, inicializando apenas quando necessário"""
    # Garantir que a variável de ambiente está carregada
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente!")
    
    # Limpar apenas quebras de linha
    api_key = str(api_key).strip().replace('\n', '').replace('\r', '')
    
    # Validação rigorosa da chave
    if not api_key.startswith('sk-'):
        raise ValueError(f"OPENAI_API_KEY inválida! Deve começar com 'sk-'. Recebido: {api_key[:15]}...")
    
    if len(api_key) < 50:
        raise ValueError(f"OPENAI_API_KEY muito curta! Chaves OpenAI têm 100+ caracteres. Recebido: {len(api_key)} caracteres")
    
    # Inicializar ChatOpenAI explicitamente com a API key
    return ChatOpenAI(
        model_name="gpt-4o-mini",  # Mudado para gpt-4o-mini para consistência
        temperature=0.7,
        api_key=api_key
    )

# SOLICITAÇÕES
solicitacoes = """
1 - OBJETIVOS - Identificação dos Objetivos: Realize uma análise cuidadosa do conteúdo do trabalho para extrair os objetivos principais. Resuma esses objetivos em um parágrafo claro e conciso, capturando a essência das metas e intenções do estudo.
2 - GAP - Identificação do GAP: Analise o conteúdo do trabalho para identificar o GAP científico que ele aborda, mesmo que não esteja explicitamente mencionado. Formule um parágrafo conciso, focando em destacar a questão central que o estudo procura resolver ou elucidar.
3 - METODOLOGIA - Extração Detalhada da Metodologia do Trabalho: Identificação e Descrição da Metodologia: Proceda com uma análise minuciosa do trabalho para identificar a metodologia utilizada. Detalhe cada aspecto da metodologia, sempre incluindo o número de participantes quando descrito no estudo, incluindo o desenho do estudo, as técnicas e ferramentas empregadas, os procedimentos de coleta e análise de dados, os passos do método e quaisquer metodologias específicas ou inovadoras adotadas. Formule uma descrição compreensiva em texto corrido, limitando-se a um máximo de 250 palavras para manter a concisão sem sacrificar detalhes importantes.
4 - DATASET - Identifique os datasets usados no trabalho. Descreva-os brevemente em texto corrido, limitando-se a 40 palavras. Quero somente o nome dos dataset na mesma linha e separados por virgula. Se o dataset foi criado pelos autores escreve "OWN DATASET"
5 - RESULTADOS - Escreva em um parágrafo os resultados obitidos estudo dando enfase a dados quantitativos, quero dados numéricos explicitamente. Nesse paragrafo também dê enfase a comparação ao melhor trabalho anterior em relação ao trabalho proposto. Não use superlativos. Deixe o tom neutro e científico.
6 - LIMITAÇÕES - Produza um texto parafraseado das limitações do trabalho.
7 - CONCLUSÃO - Resuma as conclusões dos autores em relação ao trabalho.
8 - FUTURO - Extraia as Recomendações para Pesquisa Futura: Aponte recomendações para futuras investigações baseadas nas conclusões do artigo.
9 - AVALIAÇÃO - Faça uma avaliação crítica ao trabalho. Não seja generalista faça uma crítica aprofundada.
"""

# CONTROLES
controles = """
NÍVEIS DE CONTROLE:
1. Entonação: Formal Científico.
2. Foco de Tópico: Você deve responder sempre com alto foco no texto do artigo científico.
3. Língua: Responda sempre em Português do Brasil como os Brasileiros costumam escrever textos científicos aderindo aos padrões de redação científica do país, a não ser o que será especificado para não traduzir.
4. Controle de Sentimento: Neutro e científico. Evite superlativos como: inovador, revolucionário e etc.
5. Nível Originalidade: 10, onde 1 é pouco original e 10 é muito original. Em hipótese alguma copie frases do texto original.
6. Nível de Abstração: 1, onde 1 é muito concreto e real e 10 é muito abstrato e irreal.
7. Tempo Verbal: Escreva no passado.
"""

# Restrições
restrições = """
O QUE NÃO DEVE SER TRADUZIDO DO INGLÊS PARA PORTUGUÊS:
1. Termos técnicos em inglês amplamente aceitos e usados nos textos em português.
2. Nome de algoritmos de machine learning.
3. Métricas usadas no trabalho.
4. Nome dos datasets.
5. Não envolva o retorno do YAML com ```yaml.
6. Não coloque ``` nem ´´´ no texto de retorno.
"""

# Template de saída
template = """
<template>
ARTIGO:
  - TÍTULO: "Título do artigo"
  - ARQUIVO: "nome do arquivo.pdf"
  - OBJETIVOS: "Objetivo geral e específicos"
  - GAP: "Gap científico"
  - METODOLOGIA: "Metodologia"
  - DATASET: "Datasets utilizados"
  - RESULTADOS: "Resultados do artigo"
  - LIMITAÇÕES: "Limitações do artigo científico"
  - CONCLUSÃO: "Conclusões"
  - AVALIAÇÃO: "Análise do artigo"
</template>
"""

class CrewPDFResumo:
    def __init__(self, pdf_path):
        self.pdf_tool = PDFSearchTool(pdf_path)  # Tool nativa do CrewAI para leitura de PDF
        self.llm = get_openai_model()  # Inicializar o modelo uma vez
        self.crew = self._criar_crew()

    def _criar_crew(self):
        # Agente Leitor
        agent_leitor = Agent(
            role='PDF Reader',
            goal="Ler PDFs e extrair informações específicas conforme definido nas solicitações em <solicitacoes>."
                 "Gerar um YAML de acordo com o modelo especificado em <template>. {solicitacoes} {template}.",
            backstory="Você é um especialista em leitura e análise de artigos científicos. "
                      "Sua missão é extrair informações cruciais, compreendendo o contexto semântico completo dos artigos."
                      "Sua função é fundamental para avaliar a relevância dos artigos analisados."
                      "Ao responder às solicitações delimitadas por <solicitacoes></solicitacoes>,"
                      "você deve levar em consideração as definições de controles em <controles></controles>"
                      "e as restrições em <restrições></restrições>."
                      "{solicitacoes} {template} {restrições} {controles}",
            tools=[self.pdf_tool],
            verbose=True,
            memory=False,
            llm=self.llm
        )

        # Agente Revisor
        agent_revisor = Agent(
            role="Revisor de leitura",
            goal="Leia os dados extraídos pelo Agente Leitor e verifique se um YAML foi produzido,"
                 "de acordo com o template proposto em <template>,"
                 "com os dados solicitados em <solicitacoes>."
                 "Como resultado do seu trabalho, você deve retornar um YAML"
                 "revisado no mesmo formato do template proposto. {solicitacoes} {template}",
            backstory="Você é um especialista na revisão de informações em YAML"
                      "especialmente de resumos de artigos científicos."
                      "Sua função é garantir que os dados extraídos reflitam"
                      "com precisão as solicitações definidas em <solicitacoes>"
                      "e estejam formatados conforme o template proposto em <template>."
                      "Sua atenção aos detalhes assegura que os resultados finais "
                      "sejam precisos e conformes às expectativas. {solicitacoes} {template}",
            verbose=True,
            memory=False,
            llm=self.llm,
        )

        # Tarefa do Leitor
        task_leitor = Task(
            description="Leia o PDF e responda em YAML às solicitações definidas em <solicitacoes>"
                        "usando o modelo definido em <template>.",
            expected_output="YAML com as respostas às solicitações definidas em <solicitacoes>, usando o modelo definido em <template>",
            agent=agent_leitor
        )

        # Tarefa do Revisor
        task_revisor = Task(
            description="Revise o YAML produzido pelo agente leitor para garantir que ele esteja de acordo com o template definido em <template>"
                        " e contenha todas as informações solicitadas em <solicitacoes>. {solicitacoes} {template}",
            expected_output="YAML revisado que esteja de acordo com o template definido em <template>"
                            " e contenha todas as informações solicitadas em <solicitacoes>. {solicitacoes} {template}",
            agent=agent_revisor
        )

        # Criando o Crew
        return Crew(
            agents=[agent_leitor, agent_revisor],
            tasks=[task_leitor, task_revisor],
            process=Process.sequential,
        )

    def kickoff(self):
        # Passar template como string diretamente (sem yaml.dump que pode causar problemas)
        resposta = self.crew.kickoff(inputs={
            'solicitacoes': solicitacoes,
            'template': template,  # Passar template como string diretamente
            'restrições': restrições,
            'controles': controles,
        })
        return resposta.raw
