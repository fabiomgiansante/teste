import requests
from bs4 import BeautifulSoup

def scrape_pubmed_central(theme, pathology):
    # Construct search URL
    query = f"{theme} {pathology}"
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={query.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    print(f"Fetching data from: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erro ao acessar PubMed: Status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    study_cards = soup.find_all('article', class_='full-docsum')
    studies = []

    for card in study_cards:
        try:
            title_tag = card.find('a', class_='docsum-title')
            title = title_tag.text.strip()
            link = "https://pubmed.ncbi.nlm.nih.gov" + title_tag['href']
            authors = card.find('span', class_='docsum-authors').text.strip() if card.find('span', class_='docsum-authors') else "Autores não disponíveis"

            # Navigate to the detailed page for more information
            study_details = scrape_study_details(link, headers)
            studies.append({
                'title': title,
                'authors': authors,
                **study_details,  # Merge detailed page data
                'link': link
            })
        except Exception as e:
            print(f"Erro ao processar um estudo: {e}")
            continue

    return studies

def scrape_study_details(link, headers):
    """
    Fetch detailed study information from the article page.
    """
    response = requests.get(link, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao acessar página detalhada: {link}")
        return {
            'np': "Informação não disponível",
            'criteria': "Informação não disponível",
            'conclusion': "Informação não disponível"
        }

    soup = BeautifulSoup(response.text, "html.parser")

    # Example parsing; adjust based on actual structure
    np = "Informação não disponível"
    criteria = "Informação não disponível"
    conclusion = "Informação não disponível"

    # Try to extract specific sections, adjust selectors if necessary
    try:
        conclusion_section = soup.find('div', class_='abstract-content selected')
        conclusion = conclusion_section.text.strip() if conclusion_section else "Informação não disponível"
    except Exception:
        pass  # Leave as "Informação não disponível" if extraction fails

    return {
        'np': np,
        'criteria': criteria,
        'conclusion': conclusion
    }

# Código para execução direta do script (não executa quando importado)
if __name__ == "__main__":
    # Input from the user
    print("Digite o tema principal do estudo (ex: cannabinoides):")
    theme = input("Tema: ").strip()
    print("Digite a patologia (ex: demência):")
    pathology = input("Patologia: ").strip()
    
    if not theme or not pathology:
        raise ValueError("Ambos o tema e a patologia devem ser fornecidos.")
    
    # Fetch studies
    studies = scrape_pubmed_central(theme, pathology)
    
    # Display results
    if not studies:
        print("\nNenhum estudo foi encontrado para a combinação fornecida.")
    else:
        print(f"\n=== Resultados da Pesquisa para: {theme} e {pathology} ===")
        for idx, estudo in enumerate(studies, start=1):
            print(f"\nEstudo {idx}:")
            print(f"  Título: {estudo.get('title', 'Título não disponível')}")
            print(f"  Autores: {estudo.get('authors', 'Autores não disponíveis')}")
            print(f"  Número de Participantes: {estudo.get('np', 'Informação não disponível')}")
            print(f"  Critérios: {estudo.get('criteria', 'Informação não disponível')}")
            print(f"  Conclusão: {estudo.get('conclusion', 'Informação não disponível')}")
            print(f"  Link: {estudo.get('link', 'Link não disponível')}")
    
    print("\nFim da execução.")