import os
import requests
from crewai import LLM
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar API do Google para o CrewAI
import os
if os.getenv("GOOGLE_API_KEY"):
    os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")


class LLMagentes():
    
    # Classe interna com constantes para autocomplete
    class Models:
        # OpenAI
        GPT4O_MINI = "gpt4o_mini"
        GPT4O_MINI_2024_07_18 = "gpt4o_mini_2024_07_18"
        GPT4O_2024_08_06 = "gpt4o_2024_08_06"
        GPT4O = "gpt4o"
        GPT_O1 = "gpt_o1"
        GPT_O1_MINI = "gpt_o1_mini"
        
        # Google Gemini
        GEMINI = "gemini"
        GEMINI25 = "gemini25"
        GEMINI_PRO = "gemini_pro"
        
        # DeepSeek
        DEEPSEEK_MODEL = "deepseek_model"
        DEEPSEEK_REASONER = "deepseek_reasoner"
        DEEPSEEK_CHAT = "deepseek_chat"
        
        # Anthropic Claude
        CLAUDE_HAIKU = "claude_haiku"
        CLAUDE_SONNET = "claude_sonnet"
        CLAUDE_OPUS = "claude_opus"
        CLAUDE_35_OPUS = "claude_35_opus"
        
        # Mistral AI
        MISTRAL_TINY = "mistral_tiny"
        MISTRAL_SMALL = "mistral_small"
        MISTRAL_MEDIUM = "mistral_medium"
        
        # Cohere
        COHERE_COMMAND = "cohere_command"
        COHERE_COMMAND_LIGHT = "cohere_command_light"
        
        # Perplexity
        PERPLEXITY_SONAR_SMALL = "perplexity_sonar_small"
        PERPLEXITY_SONAR_MEDIUM = "perplexity_sonar_medium"
        PERPLEXITY_SONAR_LARGE = "perplexity_sonar_large"
        PERPLEXITY_CODELLAMA = "perplexity_codellama"
        
        # Groq
        GROQ_LLAMA3_8B = "groq_llama3_8b"
        GROQ_LLAMA3_70B = "groq_llama3_70b"
        GROQ_LLAMA3_14B = "groq_llama3_14b"
        GROQ_LLAMA3_70B_128K = "groq_llama3_70b_128k"
        GROQ_LLAMA3_70B_8K = "groq_llama3_70b_8k"
        QWEN = "qwen"
        GROQ_DEEPSEEK_14B = "groq_deepseek_14b"
        GROQ_DEEPSEEK_70B = "groq_deepseek_70b"
        GROQ_GEMMA2_7B = "groq_gemma2_7b"
        GROQ_GEMMA2_9B = "groq_gemma2_9b"
        WHISPER = "whisper"
        
    # Modelos OpenAI
    gpt4o_mini = LLM(model="gpt-4o-mini", temperature=0.2)  # Rápido, tarefas simples
    gpt4o_mini_2024_07_18 = LLM(model="gpt-4o-mini-2024-07-18", temperature=0.2)
    gpt4o_2024_08_06 = LLM(model="gpt-4o-2024-08-06", temperature=0.2)
    gpt4o = LLM(model="gpt-4o", temperature=0.2)  # Balanceado, uso geral
    gpt_o1 = LLM(model="o1-preview", temperature=0.2)  # RACIOCÍNIO AVANÇADO, pesquisa complexa
    gpt_o1_mini = LLM(model="o1-mini", temperature=0.2, stop=None)  # Raciocínio eficiente
    
    
    # Modelos Google Gemini
    gemini = LLM(model="gemini/gemini-1.5-flash", temperature=0.2)  # Rápido, multimodal
    gemini25 = LLM(model="gemini/gemini-2.5-flash-preview-04-17", temperature=0.2)  # Mais recente, melhor
    gemini_pro = LLM(model="gemini/gemini-1.5-pro", temperature=0.2)
  

    # Modelo DeepSeek
    deepseek_model = LLM(model="deepseek/deepseek-reasoner", temperature=0.2)
    deepseek_reasoner = LLM(model="deepseek/deepseek-reasoner", temperature=0.2)  # Alias RACIOCÍNIO PROFUNDO
    deepseek_chat = LLM(model="deepseek/deepseek-chat", temperature=0.2)

  
    # Modelos Anthropic Claude
    claude_haiku = LLM(model="anthropic/claude-3-5-haiku-20241022", temperature=0.2)  # Rápido, tarefas simples
    claude_sonnet = LLM(model="anthropic/claude-3-5-sonnet-20240620", temperature=0.2)  # Balanceado, uso geral
    claude_opus = LLM(model="anthropic/claude-3-opus-20240229", temperature=0.2)  # Análises complexas
    claude_35_opus = LLM(model="anthropic/claude-3-5-opus-20241022", temperature=0.2)  # MAIS PODEROSO, pesquisa avançada
    
    # Modelos Mistral AI
    mistral_tiny = LLM(model="mistral/mistral-tiny", temperature=0.2)  # Rápido, tarefas simples
    mistral_small = LLM(model="mistral/mistral-small", temperature=0.2)  # Balanceado, uso geral
    mistral_medium = LLM(model="mistral/mistral-medium", temperature=0.2)  # Análises complexas
    
    # Modelos Cohere
    cohere_command = LLM(model="cohere/command", temperature=0.2)  # Geração estruturada, relatórios
    cohere_command_light = LLM(model="cohere/command-light", temperature=0.2)  # Versão rápida
    
    # Modelos Perplexity
    perplexity_sonar_small = LLM(model="perplexity/sonar-small-chat", temperature=0.2)  # Rápido, com busca web
    perplexity_sonar_medium = LLM(model="perplexity/sonar-medium-chat", temperature=0.2)  # Balanceado, com busca web
    perplexity_sonar_large = LLM(model="perplexity/sonar-large-chat", temperature=0.2)  # Poderoso, com busca web
    perplexity_codellama = LLM(model="perplexity/codellama-70b-instruct", temperature=0.2)  # Especializado em código
    
    # Modelos Groq (Cloud)
    groq_llama3_8b = LLM(model="groq/llama3-8b-8192", temperature=0.2)  # 8K contexto, tarefas rápidas
    groq_llama3_70b = LLM(model="groq/llama3-70b-8192", temperature=0.2)  # 8K contexto, análises complexas
    groq_llama3_14b = LLM(model="groq/llama3-3.3-14b-versatile", temperature=0.2)  # Versátil, uso geral
    groq_llama3_70b_128k = LLM(model="groq/llama3-3.3-70b-versatile", temperature=0.2)  # 128K! DOCUMENTOS GRANDES
    groq_llama3_70b_8k = LLM(model="groq/llama-3.3-70b-instruct", temperature=0.2)  # Instruções precisas
    qwen = LLM(model="groq/qwen-qwq-32b", temperature=0.2)  # RACIOCÍNIO MATEMÁTICO, problemas complexos
    groq_deepseek_14b = LLM(model="groq/deepseek-r1-distill-llama-14b", temperature=0.2)  # Código e lógica
    groq_deepseek_70b = LLM(model="groq/deepseek-r1-distill-llama-70b", temperature=0.2)  # CÓDIGO AVANÇADO
    groq_gemma2_7b = LLM(model="groq/gemma2-7b-it", temperature=0.2)  # 8K contexto, eficiente
    groq_gemma2_9b = LLM(model="groq/gemma2-9b-it", temperature=0.2)  # 8K contexto, mais capaz
    whisper = LLM(model="groq/distil-whisper-large-v3-en", temperature=0.2)  # Transcrição de áudio

    @classmethod
    def list_available_models(cls):
        """Lista todos os modelos disponíveis na classe."""
        models = []
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, (LLM)) and not attr_name.startswith('_'):
                models.append(attr_name)
        return models
    
    @classmethod
    def get_model(cls, model_name):
        """Retorna um modelo específico pelo nome."""
        if hasattr(cls, model_name):
            return getattr(cls, model_name)
        else:
            raise ValueError(f"Modelo '{model_name}' não encontrado. Modelos disponíveis: {cls.list_available_models()}")
    
    @classmethod
    def get_model_info(cls, model_name):
        """Retorna informações sobre um modelo específico."""
        if hasattr(cls, model_name):
            model = getattr(cls, model_name)
            return {
                "attribute_name": model_name,
                "model_path": model.model,
                "temperature": model.temperature
            }
        else:
            raise ValueError(f"Modelo '{model_name}' não encontrado.")
    
    @classmethod
    def list_all_models_detailed(cls):
        """Lista todos os modelos com suas informações detalhadas."""
        models_info = {}
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, (LLM)) and not attr_name.startswith('_'):
                models_info[attr_name] = {
                    "model_path": attr.model,
                    "temperature": attr.temperature,
                    "provider": attr.model.split('/')[0] if '/' in attr.model else "openai"
                }
        return models_info

def get_working_llm():
    """Encontrar todas as LLMs que funcionam"""
    print("🔍 PROCURANDO LLMs FUNCIONAIS...")
    
    # Lista de modelos para testar na ordem de preferência
    models_to_test = [
        ('groq_llama3_8b', 'GROQ_API_KEY', 'Groq Llama3-8B'),
        ('claude_haiku', 'ANTHROPIC_API_KEY', 'Claude Haiku'),
        ('gpt4o_mini', 'OPENAI_API_KEY', 'GPT-4o Mini'),
        ('gemini', 'GEMINI_API_KEY', 'Google Gemini'),
        ('deepseek_reasoner', 'DEEPSEEK_API_KEY', 'DeepSeek Reasoner'),
        ('mistral_tiny', 'MISTRAL_API_KEY', 'Mistral Tiny'),
        ('cohere_command_light', 'COHERE_API_KEY', 'Cohere Command Light'),
        ('perplexity_sonar_small', 'PERPLEXITY_API_KEY', 'Perplexity Sonar Small'),
    ]
    
    working_models = []
    
    for model_name, api_key_name, description in models_to_test:
        # Verificar se API está configurada
        api_key = os.getenv(api_key_name)
        if not api_key or len(api_key) < 10:
            print(f"⚠️ {description}: {api_key_name} não configurada")
            continue
        
        try:
            print(f"🧪 Testando {description}...")
            
            # Obter modelo
            model = LLMagentes.get_model(model_name)
            
            # Teste simples
            test_messages = [{"role": "user", "content": "Responda apenas: OK"}]
            result = model.call(test_messages)
            
            if result and len(result.strip()) > 0:
                print(f"✅ {description} FUNCIONANDO!")
                working_models.append((model, description))
            else:
                print(f"❌ {description}: Resposta vazia")
                
        except Exception as e:
            print(f"❌ {description}: {str(e)[:50]}...")
            continue
    
    if working_models:
        print(f"\n📊 TOTAL: {len(working_models)} LLMs funcionando")
        return working_models
    else:
        raise Exception("❌ Nenhuma LLM funcionando! Configure pelo menos uma API válida.")

def test_all_apis():
    """Testar todas as APIs configuradas"""
    print("🧪 TESTANDO TODAS AS APIS")
    print("="*40)
    
    api_tests = [
        ('ANTHROPIC_API_KEY', 'Claude'),
        ('GROQ_API_KEY', 'Groq'),
        ('OPENAI_API_KEY', 'OpenAI'),
        ('GOOGLE_API_KEY', 'Google Gemini'),
        ('DEEPSEEK_API_KEY', 'DeepSeek'),
        ('MARITACA_API_KEY', 'Maritaca'),
        ('MISTRAL_API_KEY', 'Mistral'),
        ('COHERE_API_KEY', 'Cohere'),
        ('PERPLEXITY_API_KEY', 'Perplexity'),
    ]
    
    working_apis = []
    
    for api_name, description in api_tests:
        api_key = os.getenv(api_name)
        if api_key and len(api_key) > 10:
            print(f"✅ {description}: {api_key[:15]}...")
            working_apis.append(description)
        else:
            print(f"❌ {description}: Não configurada")
    
    print(f"\n📊 RESULTADO: {len(working_apis)} APIs configuradas")
    return working_apis

# Exemplo de uso
if __name__ == "__main__":
    print("🤖 SISTEMA DE LLMs - VERSÃO CORRIGIDA")
    print("="*50)
    
    # Testar APIs
    working_apis = test_all_apis()
    
    if working_apis:
        try:
            # Encontrar LLMs funcionais
            working_llms = get_working_llm()
            print(f"\n🎯 LLMs FUNCIONAIS:")
            for _, name in working_llms:
                print(f"  ✅ {name}")
            print("\n✅ Sistema pronto para uso!")
            
        except Exception as e:
            print(f"\n❌ {e}")
            print("\n💡 CONFIGURE TODAS AS API:")
            print("• Groq (GRATUITO): https://console.groq.com/")
            print("• Claude: https://console.anthropic.com/")
            print("• OpenAI: https://platform.openai.com/")
            print("• DeepSeek: https://platform.deepseek.com/")
            print("• Gemini: https://makersuite.google.com/")
            print("• Perplexity: https://docs.perplexity.ai/")
            print("• Mistral: https://console.mistral.ai/")
            print("• Cohere: https://dashboard.cohere.com/")
    else:
        print("\n❌ Nenhuma API configurada!")
        print("Configure pelo menos uma chave no arquivo .env")

    


    """
    Classe que disponibiliza vários modelos de LLM para uso com CrewAI.
    
    RECOMENDAÇÕES DE USO POR CATEGORIA:
    
    🚀 TAREFAS SIMPLES E RÁPIDAS:
    - sabiazinho_3, gpt4o_mini, claude_haiku, mistral_tiny
    - groq_llama3_8b, groq_gemma2_7b, qwen3_4b
    
    📊 USO GERAL E BALANCEADO:
    - sabia_3, gpt4o, claude_sonnet, mistral_small
    - groq_llama3_14b, gemini, deepseek_8b
    
    🧠 ANÁLISES COMPLEXAS E TÉCNICAS:
    - gpt_o1_mini, claude_opus, mistral_medium
    - groq_llama3_70b, deepseek_14b, phi4_14b
    
    🔬 PESQUISA AVANÇADA E DEBATES INTELIGENTES:
    - gpt_o1, claude_35_opus, groq_llama3_70b_128k
    - qwen (32b), groq_deepseek_70b, gemma3_27b
    
    💡 CASOS ESPECÍFICOS:
    - Código: deepcoder_14b, deepseek_model
    - Visão: llama3_vision
    - Áudio: whisper
    - Português BR: sabiazinho_3, sabia_3
    """




    
# Exemplo de uso da classe LLMagentes com suporte a autocomplete
    """
from my_llm import LLMagentes

# ====================================
# FORMA 1: Acesso direto (RECOMENDADO para código fixo)
# ====================================
# Digite "LLMagentes." e o IDE mostrará todas as opções disponíveis
llm_direto = LLMagentes.gemini_pro  # ✅ IDE mostra todas as opções ao digitar

# ====================================
# FORMA 2: Acesso via get_model() COM AUTOCOMPLETE
# ====================================
# Digite "LLMagentes.Models." e o IDE mostrará todas as constantes
llm_com_autocomplete = LLMagentes.get_model(LLMagentes.Models.GEMINI_PRO)  # ✅ Autocomplete funciona!

# Outros exemplos com autocomplete:
llm_claude = LLMagentes.get_model(LLMagentes.Models.CLAUDE_HAIKU)
llm_gpt = LLMagentes.get_model(LLMagentes.Models.GPT4O_MINI)
llm_deepseek = LLMagentes.get_model(LLMagentes.Models.DEEPSEEK_REASONER)

# ====================================
# FORMA 3: String direta (quando vem de configuração)
# ====================================
# Use apenas quando o nome vem de arquivo de configuração
modelo_do_config = "gemini_pro"  # Pode vir de .env, JSON, etc
llm_config = LLMagentes.get_model(modelo_do_config)

# ====================================
# NO SEU app.py - EXEMPLO PRÁTICO
# ====================================
from crewai import Agent

# OPÇÃO 1: Direto (mais simples)
agent1 = Agent(
    role="Pesquisador",
    goal="Pesquisar dados",
    backstory="Especialista em pesquisa",
    llm=LLMagentes.gemini_pro  # ✅ Autocomplete funciona
)

# OPÇÃO 2: Via get_model com autocomplete
agent2 = Agent(
    role="Escritor",
    goal="Escrever relatórios",
    backstory="Especialista em redação",
    llm=LLMagentes.get_model(LLMagentes.Models.CLAUDE_SONNET)  # ✅ Autocomplete funciona
)

# OPÇÃO 3: Dinâmico (quando precisa flexibilidade)
modelo_escolhido = LLMagentes.Models.DEEPSEEK_REASONER  # Pode mudar facilmente
agent3 = Agent(
    role="Analista",
    goal="Analisar dados",
    backstory="Especialista em análise",
    llm=LLMagentes.get_model(modelo_escolhido)
)

# ====================================
# VERIFICAR INFORMAÇÕES DO MODELO
# ====================================
info = LLMagentes.get_model_info(LLMagentes.Models.GEMINI_PRO)
print(f"Modelo: {info['model_path']}")
print(f"Temperatura: {info['temperature']}")

# ====================================
# LISTAR TODOS OS MODELOS DISPONÍVEIS
# ====================================
print("\n🤖 MODELOS DISPONÍVEIS:")
print("-" * 50)

# Lista simples
modelos = LLMagentes.list_available_models()
for modelo in sorted(modelos):
    print(f"• {modelo}")

# ====================================
# DICA: MODELOS POR CATEGORIA
# ====================================
print("\n💡 SUGESTÕES DE USO:")
print("-" * 50)

# Para tarefas simples e rápidas
tarefas_simples = [
    LLMagentes.Models.GPT4O_MINI,
    LLMagentes.Models.CLAUDE_HAIKU,
    LLMagentes.Models.GROQ_LLAMA3_8B,
    LLMagentes.Models.GEMINI,
]

# Para análises complexas
tarefas_complexas = [
    LLMagentes.Models.GPT_O1,
    LLMagentes.Models.CLAUDE_35_OPUS,
    LLMagentes.Models.GROQ_LLAMA3_70B_128K,
    LLMagentes.Models.GEMINI_PRO,
]

# Com busca web integrada
com_busca_web = [
    LLMagentes.Models.PERPLEXITY_SONAR_SMALL,
    LLMagentes.Models.PERPLEXITY_SONAR_MEDIUM,
    LLMagentes.Models.PERPLEXITY_SONAR_LARGE,
]

print("\n🚀 Tarefas simples:", tarefas_simples)
print("🧠 Tarefas complexas:", tarefas_complexas)
print("🌐 Com busca web:", com_busca_web)

    """