import xml.etree.ElementTree as ET
import re

# Chemin vers le fichier XML
fichier_xml = 'kowiktionary-latest-pages-articles.xml'

# Création d'un itérateur sur le fichier XML
context = ET.iterparse(fichier_xml, events=('start', 'end'))
event, root = next(context)

# Extraction du namespace
namespace = ''
if '}' in root.tag:
    namespace = root.tag.split('}')[0] + '}'

print(f'Namespace détecté : {namespace}')


def extract_sections(text):
    sections = {}
    # Séparer le texte en lignes
    lines = text.split('\n')
    
    current_section = None
    for line in lines:
        # Détecter les sections (niveau 2 ou 3)
        match_section = re.match(r'^(==+)\s*(.*?)\s*\1$', line)
        if match_section:
            level = len(match_section.group(1))
            title = match_section.group(2).strip()
            current_section = title
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)
    
    return sections


def clean_text(text):
    # Supprimer les balises wiki pour la mise en forme
    text = re.sub(r"'''?", '', text)
    # Supprimer les liens internes en conservant le texte visible
    text = re.sub(r'\[$$(?:[^|$$]*\|)?([^\]]+)\]\]', r'\1', text)
    # Supprimer les modèles
    text = re.sub(r'\{\{.*?\}\}', '', text)
    text = text.strip()
    return text

import re

def extract_korean_data(sections):
    korean_data = {}
    hanjas = set()
    definitions = []
    examples = []
    synonyms = []
    antonyms = []
    derived_words = []
    related_words = []

    # Vérifier que la section '한국어' existe
    if '한국어' in sections:
        # Nous n'extrayons plus la prononciation
        # Parcourir les sections
        for section_name, content_lines in sections.items():
            if section_name in ['명사', '동사', '형용사', '부사', '어근']:
                # Sections pour les définitions, hanja et exemples
                current_hanja = ''
                for line in content_lines:
                    # **Extraction des hanja depuis le modèle '{{어원|...}}'**
                    match_hanja_template = re.search(r'\{\{어원\|([^|}]+)', line)
                    if match_hanja_template:
                        current_hanja = match_hanja_template.group(1).strip()
                        hanjas.add(current_hanja)
                        continue  # Passer à la prochaine ligne

                    # **Extraction des hanja depuis les lignes commençant par '*어원: 한자 [[...]]'**
                    match_hanja_line = re.match(r'\*어원: 한자 \[\[([^$$]+)\]\]', line)
                    if match_hanja_line:
                        current_hanja = match_hanja_line.group(1).strip()
                        hanjas.add(current_hanja)
                        continue  # Passer à la prochaine ligne

                    # **Extraction des définitions (lignes commençant par '#')**
                    match_def = re.match(r'^#\s*(.*)', line)
                    if match_def:
                        definition = clean_text(match_def.group(1))
                        definitions.append(definition)
                        continue  # Passer à la prochaine ligne

                    # **Extraction des exemples (lignes commençant par ':*' ou '*')**
                    match_ex = re.match(r'^[:*]+\s*(.*)', line)
                    if match_ex and not line.startswith('*어원:'):
                        example = clean_text(match_ex.group(1))
                        examples.append(example)
                        continue  # Passer à la prochaine ligne

                # Réinitialiser la variable current_hanja pour éviter les interférences entre sections
                current_hanja = ''
            
            elif section_name == '유의어':
                # Extraction des synonymes
                print(content_lines)
                synonyms += re.findall(r'\[\[([^$$]+)\]\]', '\n'.join(content_lines))
                print(synonyms)

            elif section_name == '반의어':
                print(content_lines)
                # Extraction des antonymes
                antonyms += re.findall(r'\[\[([^$$]+)\]\]', '\n'.join(content_lines))
                print(antonyms)

            elif section_name == '파생어':
                # Extraction des mots dérivés
                derived_words += re.findall(r'\[\[([^$$]+)\]\]', '\n'.join(content_lines))

            elif section_name == '관련 어휘':
                # Extraction des mots associés
                related_words += re.findall(r'\[\[([^$$]+)\]\]', '\n'.join(content_lines))
                # Extraction depuis les modèles si nécessaire
                # Exemple pour '{{합성어 상자|...}}'
                match_compound = re.search(r'\{\{합성어 상자\|([^}]+)\}\}', '\n'.join(content_lines))
                if match_compound:
                    words = match_compound.group(1).split('|')
                    related_words += [word.strip() for word in words]

        # Assembler les données extraites
        korean_data['hanjas'] = list(hanjas)
        korean_data['definitions'] = definitions
        korean_data['exemples'] = examples
        korean_data['synonymes'] = synonyms
        korean_data['antonymes'] = antonyms
        korean_data['derived_words'] = derived_words
        korean_data['related_words'] = related_words

        # Ajouter le mot lui-même
        korean_data['mot'] = sections.get('mot', '')

        return korean_data if any(korean_data.values()) else None
    else:
        return None

limite_pages = 1  # Vous pouvez changer ce nombre selon vos besoins
compteur_pages = 0

# Parcours du fichier XML
for event, elem in context:
    if event == 'end' and elem.tag == namespace + 'page':
        compteur_pages += 1  # Incrémentation du compteur
        title_elem = elem.find(namespace + 'title')
        if title_elem is not None:
            title = title_elem.text
            # Filtrer les pages non pertinentes
            if not title.startswith(('사용자:', '토론:', '파일:', '미디어위키:', '틀:', '도움말:', '분류:', '포털:', '특수기능:')):
                revision = elem.find(namespace + 'revision')
                if revision is not None:
                    text_elem = revision.find(namespace + 'text')
                    if text_elem is not None:
                        text = text_elem.text
                        if text:
                            # Extraire les sections du texte
                            sections = extract_sections(text)
                            # Extraire les données en coréen
                            korean_data = extract_korean_data(sections)
                            if korean_data:
                                korean_data['mot'] = title
                                # Afficher ou stocker les données extraites
                                print(f"Mot : {korean_data.get('mot')}")
                                print(f"Hanja : {korean_data.get('hanjas')}")
                                print(f"Définitions : {korean_data.get('definitions')}")
                                print(f"Exemples : {korean_data.get('exemples')}")
                                print(f"Synonymes : {korean_data.get('synonymes')}")
                                print(f"Antonymes : {korean_data.get('antonymes')}")
                                print(f"Mots dérivés : {korean_data.get('derived_words')}")
                                print('---')
                                # Vous pouvez maintenant insérer ces données dans votre base de données
        # Nettoyer l'élément pour libérer la mémoire
        elem.clear()
        
        if compteur_pages >= limite_pages:
            print(f"Limite de {limite_pages} pages atteinte. Arrêt du traitement.")
            break

from datapackage import Package
package = Package('https://raw.githubusercontent.com/garfieldnate/kengdic/master/datapackage.json')
resource = package.get_resource('kengdic')
data = resource.read(keyed=True)
print(data[20977])
print(type(data))
print(len(data))