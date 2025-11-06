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
    # Temperatura reduzida para melhor precisão na extração de dados
    return ChatOpenAI(
        model_name="gpt-4o-mini",  # Mudado para gpt-4o-mini para consistência
        temperature=0.3,  # Reduzido de 0.7 para 0.3 para melhor precisão
        api_key=api_key
    )

# SOLICITAÇÕES
solicitacoes = """
IMPORTANTE: Use APENAS informações que estão explicitamente no PDF fornecido. NUNCA invente, infira ou adicione informações de outros estudos.

1 - OBJETIVOS - Identificação dos Objetivos: Extraia do PDF os objetivos principais do estudo. Se os objetivos não estiverem claramente definidos no PDF, escreva "Objetivos não explicitamente definidos no documento" ou similar. Resuma em um parágrafo claro e conciso, capturando APENAS o que está no PDF.

2 - GAP - Identificação do GAP: Analise o PDF para identificar o GAP científico mencionado. Se o GAP não estiver explicitamente mencionado no PDF, escreva "GAP não explicitamente mencionado no documento". Formule um parágrafo conciso baseado APENAS no conteúdo do PDF.

3 - METODOLOGIA - Extração Detalhada da Metodologia: Extraia do PDF a metodologia utilizada. Inclua o número de participantes APENAS se estiver mencionado no PDF. Detalhe cada aspecto da metodologia que está no documento. Se alguma informação metodológica não estiver no PDF, não invente. Formule uma descrição em texto corrido, limitando-se a um máximo de 250 palavras, usando APENAS informações do PDF.

4 - DATASET - Identifique os datasets mencionados no PDF. Se não houver menção a datasets, escreva "Nenhum dataset mencionado no documento" ou "OWN DATASET" se o documento indicar que os autores criaram seus próprios dados. Limite-se a 40 palavras. Apenas nomes dos datasets na mesma linha, separados por vírgula.

5 - RESULTADOS - Escreva em um parágrafo os resultados mencionados no PDF, dando ênfase a dados quantitativos que estão explicitamente no documento. Use APENAS números e dados que estão no PDF. Se houver comparação com trabalhos anteriores no PDF, mencione. Se não houver, não invente comparações. Não use superlativos. Tom neutro e científico.

6 - LIMITAÇÕES - Extraia do PDF as limitações mencionadas pelos autores. Se não houver seção de limitações, escreva "Limitações não explicitamente mencionadas no documento". Produza um texto parafraseado baseado APENAS no que está no PDF.

7 - CONCLUSÃO - Resuma as conclusões que estão no PDF. Use APENAS as conclusões mencionadas pelos autores no documento. Se não houver seção de conclusão clara, indique isso.

8 - FUTURO - Extraia do PDF as recomendações para pesquisa futura mencionadas. Se não houver recomendações explícitas, escreva "Recomendações para pesquisa futura não explicitamente mencionadas no documento".

9 - AVALIAÇÃO - Faça uma avaliação crítica baseada APENAS no conteúdo do PDF fornecido. Não compare com outros estudos que não estão mencionados no PDF. Seja específico e baseie-se apenas no que está no documento.
"""

# CONTROLES
controles = """
NÍVEIS DE CONTROLE:
1. Entonação: Formal Científico.
2. Foco de Tópico: Você deve responder sempre com alto foco no texto do artigo científico FORNECIDO. Use APENAS informações deste PDF específico.
3. Língua: Responda sempre em Português do Brasil como os Brasileiros costumam escrever textos científicos aderindo aos padrões de redação científica do país, a não ser o que será especificado para não traduzir.
4. Controle de Sentimento: Neutro e científico. Evite superlativos como: inovador, revolucionário e etc.
5. Nível Originalidade: 10, onde 1 é pouco original e 10 é muito original. Em hipótese alguma copie frases do texto original. MAS: NUNCA invente informações que não estão no PDF.
6. Nível de Abstração: 1, onde 1 é muito concreto e real e 10 é muito abstrato e irreal. Baseie-se APENAS em dados concretos do PDF.
7. Tempo Verbal: Escreva no passado.
8. PRECISÃO CRÍTICA: Se uma informação não estiver no PDF, você DEVE escrever "Informação não disponível no documento" ou similar. NUNCA invente ou infira dados.
"""

# Restrições
restrições = """
RESTRIÇÕES CRÍTICAS:
1. Use APENAS informações do PDF fornecido. NUNCA adicione informações de outros estudos ou conhecimento prévio.
2. Se uma informação não estiver no PDF, escreva "Informação não disponível no documento" ou similar.
3. NUNCA invente números, resultados, conclusões ou dados.
4. NUNCA faça inferências além do que está explicitamente no PDF.

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
ARTIGO:
  - TÍTULO: "[Extrair o título real do PDF]"
  - ARQUIVO: "[Nome real do arquivo PDF]"
  - OBJETIVOS: "[Extrair objetivos reais do PDF]"
  - GAP: "[Extrair gap real do PDF ou indicar se não encontrado]"
  - METODOLOGIA: "[Extrair metodologia real do PDF]"
  - DATASET: "[Extrair datasets reais do PDF ou indicar se não encontrado]"
  - RESULTADOS: "[Extrair resultados reais do PDF]"
  - LIMITAÇÕES: "[Extrair limitações reais do PDF ou indicar se não encontrado]"
  - CONCLUSÃO: "[Extrair conclusões reais do PDF]"
  - FUTURO: "[Extrair recomendações futuras reais do PDF ou indicar se não encontrado]"
  - AVALIAÇÃO: "[Fazer avaliação crítica baseada no PDF]"
"""

class CrewPDFResumo:
    def __init__(self, pdf_path):
        # Verificar se o arquivo existe
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")
        
        # Verificar se é um arquivo PDF
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError(f"Arquivo deve ser um PDF: {pdf_path}")
        
        self.pdf_path = pdf_path
        self.pdf_tool = PDFSearchTool(pdf_path)  # Tool nativa do CrewAI para leitura de PDF
        self.llm = get_openai_model()  # Inicializar o modelo uma vez
        self.crew = self._criar_crew()

    def _criar_crew(self):
        # Agente Leitor
        agent_leitor = Agent(
            role='PDF Reader',
            goal="Ler o PDF fornecido usando a ferramenta PDFSearchTool e extrair informações reais do documento. "
                 "Gerar um YAML completo com informações extraídas do PDF conforme <template>. "
                 "Use a ferramenta para buscar e ler o conteúdo do PDF antes de responder. {solicitacoes} {template}.",
            backstory="Você é um especialista em leitura e análise de artigos científicos. "
                      "Sua missão é usar a ferramenta PDFSearchTool para ler o PDF fornecido e extrair informações reais do documento. "
                      "PASSO 1: Use a ferramenta PDFSearchTool para ler o PDF completamente. "
                      "PASSO 2: Busque informações específicas no PDF usando termos relevantes. "
                      "PASSO 3: Extraia as informações encontradas e organize em YAML. "
                      "CRÍTICO: Você DEVE usar a ferramenta PDFSearchTool para ler o PDF. Não responda sem usar a ferramenta. "
                      "Se uma informação não estiver no PDF após buscar cuidadosamente, escreva 'Informação não disponível no documento'. "
                      "NUNCA invente dados, números, resultados ou conclusões. "
                      "Use APENAS informações que você encontrou no PDF através da ferramenta. "
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
            goal="Revisar o YAML produzido pelo Agente Leitor garantindo que: "
                 "1) Todas as informações vieram APENAS do PDF fornecido, "
                 "2) Nenhuma informação foi inventada ou inferida, "
                 "3) O formato está de acordo com o template proposto em <template>, "
                 "4) Todos os campos solicitados em <solicitacoes> foram preenchidos. "
                 "Se encontrar informações que parecem inventadas, remova-as ou marque como 'Informação não disponível'. {solicitacoes} {template}",
            backstory="Você é um especialista na revisão de informações em YAML "
                      "especialmente de resumos de artigos científicos. "
                      "Sua função é garantir que os dados extraídos reflitam "
                      "com precisão APENAS o conteúdo do PDF fornecido, sem adicionar informações de outros estudos. "
                      "CRÍTICO: Se você identificar informações que não estão no PDF original, você DEVE removê-las ou substituí-las por 'Informação não disponível no documento'. "
                      "Sua atenção aos detalhes assegura que os resultados finais "
                      "sejam precisos, baseados exclusivamente no PDF fornecido e formatados conforme o template proposto em <template>. {solicitacoes} {template}",
            verbose=True,
            memory=False,
            llm=self.llm,
        )

        # Tarefa do Leitor
        task_leitor = Task(
            description=f"""
PRIMEIRO: Use a ferramenta PDFSearchTool para ler o conteúdo completo do PDF localizado em: {self.pdf_path}

INSTRUÇÕES DE LEITURA:
1. Use a ferramenta PDFSearchTool com a query vazia ou "*" para ler todo o PDF primeiro
2. Depois, faça buscas específicas no PDF usando termos como: 'title', 'objetivo', 'objective', 'metodologia', 'methodology', 'resultados', 'results', 'conclusão', 'conclusion', 'limitações', 'limitations', etc.
3. Leia cuidadosamente todo o conteúdo do PDF antes de responder
4. Para o TÍTULO: Busque por "title", "título", ou leia a primeira página do PDF
5. Para o ARQUIVO: Use o nome do arquivo: {os.path.basename(self.pdf_path)}

DEPOIS: Extraia as informações solicitadas em <solicitacoes> e organize em YAML conforme <template>.
Para cada campo solicitado, busque no PDF usando a ferramenta.
Se encontrar a informação no PDF, extraia e parafraseie.
Se NÃO encontrar após buscar cuidadosamente, escreva 'Informação não disponível no documento'.

CRÍTICO: Você DEVE usar a ferramenta PDFSearchTool para ler o PDF. Não responda sem ler o PDF primeiro.
NUNCA invente dados, números, resultados ou conclusões.
Use APENAS informações que você encontrou no PDF através da ferramenta.

{solicitacoes}
{template}
{restrições}
{controles}
""",
            expected_output="YAML completo com TODOS os campos preenchidos conforme <template>. "
                           "Cada campo deve conter informações extraídas do PDF (usando a ferramenta) ou 'Informação não disponível no documento' se não encontrado. "
                           "O YAML deve ter o título real do artigo, nome do arquivo real, e informações reais extraídas do PDF.",
            agent=agent_leitor,
            tools=[self.pdf_tool]
        )

        # Tarefa do Revisor
        task_revisor = Task(
            description="Revise o YAML produzido pelo agente leitor garantindo que: "
                        "1) Todas as informações vieram APENAS do PDF (sem informações inventadas), "
                        "2) O formato está de acordo com o template definido em <template>, "
                        "3) Contém todas as informações solicitadas em <solicitacoes> (ou indica 'Informação não disponível' quando apropriado). "
                        "Se identificar informações que parecem inventadas ou de outros estudos, remova-as ou substitua por 'Informação não disponível no documento'. {solicitacoes} {template}",
            expected_output="YAML revisado e validado que esteja de acordo com o template definido em <template>, "
                            "contenha todas as informações solicitadas em <solicitacoes> (ou indique quando não disponível), "
                            "e contenha APENAS informações extraídas do PDF fornecido, sem alucinações ou informações inventadas. {solicitacoes} {template}",
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
