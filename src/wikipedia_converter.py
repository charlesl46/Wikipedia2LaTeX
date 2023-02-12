import requests
from unidecode import unidecode
import pypandoc
import wikipedia
import urllib
from tqdm import tqdm

class WikipediaArticle:  
    accents = {'à' : '#A1#','â' : '#A2#','ä' : '#A3#','é' : '#E1#','è': '#E2#','ê' : '#E3#','ë' : '#E4#','ï': '#I1#','î': '#I2#','ô': '#O1#','ö': '#O2#','ù': '#U1#','û': '#U2#','ü': '#U3#','ÿ': '#Y1#','ç': '#C1#'}

    def __init__(self) -> None:
        """Method to initialize the class"""
        print('<!> Initializing...\n')
        wikipedia.set_lang("fr")

        print('enter the title of the article you want to convert')
        ok = False
        while not ok:
            try:
                title = input()
                page = wikipedia.page(title)
                self.title = page.title
                self.abstract = decode_french_accents(unidecode(encode_french_accents(wikipedia.summary(self.title,sentences = 1),accents = self.accents)),self.accents)
                ok = True
            except wikipedia.exceptions.DisambiguationError as e:
                print('enter a page in these pages, there is a ambiguation')
                print (e.options)
        pass

    def fetch_content(self):
        """Method to fetch content of the article from Wikipedia's API"""
        print('<!> Fetching content...\n')
        api_url = f'https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={self.title}&explaintext=1'
        response = requests.get(api_url)
        data = response.json()
        self.content = next(iter(data['query']['pages'].values()))['extract']
        pass

    def convert_to_latex(self):
        self.latex_content = pypandoc.convert_text(self.content, 'latex', format='mediawiki').split('.')[1:]

    def preprocess(self):
        self.latex_content = decode_french_accents(unidecode(encode_french_accents(('.'.join(self.latex_content)),self.accents)),self.accents)
        
    def produce_pdf(self):
        output_filename = f'{self.title}.pdf'
        pypandoc.convert_text(self.latex_content, 'pdf', format='latex', outputfile=f"../pdf/{output_filename}", extra_args=['-V', 'geometry:margin=3cm','-V',f'title:{self.title}', '-V',f'abstract:{self.abstract}','-V','lang:fr-FR','-V', 'toc','-V', 'pagestyle:headings'])

def encode_french_accents(text : str, accents : dict):    
    for accent in tqdm(accents.keys()):
        if text.__contains__(accent):
            text = text.replace(accent,accents[accent])
    return text

def decode_french_accents(text : str,accents : dict):
    return encode_french_accents(text,{v: k for k, v in accents.items()})



def main():
    article = WikipediaArticle()
    article.fetch_content()
    article.convert_to_latex()
    article.preprocess()
    article.produce_pdf()

main()
