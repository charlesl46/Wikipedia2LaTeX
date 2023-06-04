import requests
from unidecode import unidecode
import pypandoc
import wikipedia
import urllib
from tqdm import tqdm
import nltk
import re

class WikipediaArticle: 
    """A class to manage a wikipedia article and its convertion to LaTeX""" 
    accents = {'à' : '#A1#','â' : '#A2#','ä' : '#A3#','á' : '#A4#','é' : '#E1#','è': '#E2#','ê' : '#E3#','ë' : '#E4#','ï': '#I1#','î': '#I2#',"í" : "#I3#",'ô': '#O1#','ö': '#O2#','ó' : '#O3#','ù': '#U1#','û': '#U2#','ü': '#U3#',"ú" : "#U4#","ñ" : "#N1#",'ÿ': '#Y1#','ç': '#C1#'}
    available_lang = ["fr","es","en","de","it"]

    def first_sentence(self,text : str):
        return ''.join(nltk.sent_tokenize(text)[:1])

    def all_sentences_but_first(self,text : str):
        return ''.join(nltk.sent_tokenize(text)[1:])

    def remove_references(self,text : str):
        return re.sub(r'\[\d+\]', '',text)

    

    def __init__(self,title_input : str = None) -> None:
        """Method to initialize the class"""
        print('<!> Initializing...\n')
        nltk.download('punkt')
        pypandoc.download_pandoc()
        print("Select a language :\n")
        print(self.available_lang)
        self.language = None
        while not self.language in self.available_lang:
            self.language = input()
            if self.language not in self.available_lang:
                print("<!> Make sure you entered a valid language")
        wikipedia.set_lang(self.language)

        if title_input == None:
            print('enter the title of the article you want to convert')
        ok = False
        while not ok:
            try:
                if title_input == None:
                    title = input()
                else:
                    title = title_input
                page = wikipedia.page(title)
                self.title = page.title
                ok = True
            except wikipedia.exceptions.PageError as e:
                print('Here are matching possibilities\n')
                possibilities = wikipedia.search(title,results = 5)
                for i,poss in enumerate(possibilities):
                    print(f'- #{i+1} {poss}\n')
                print('Please choose \n')
                choice = int(input())
                choice_page = ''.join(possibilities[choice-1])
                self.title = choice_page
                ok = True
            except wikipedia.exceptions.DisambiguationError as e:
                print('enter a page in these pages, there is a ambiguation')
                print (e.options)
        pass

    def fetch_content(self):
        """Method to fetch content of the article from Wikipedia's API"""
        print('<!> Fetching content...\n')
        api_url = f'https://{self.language}.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={self.title}&explaintext=1'
        response = requests.get(api_url)
        data = response.json()
        self.content = next(iter(data['query']['pages'].values()))['extract']
        pass

    def convert_to_latex(self):
        """Method to convert the mediawiki content to latex content
        """

        self.latex_content = pypandoc.convert_text(self.content, 'latex', format='mediawiki')
        

    def preprocess(self):
        """Method to process the french accents and non compatible chars
        """
        self.latex_content = self.remove_references(self.decode_accents(unidecode(self.encode_accents(self.latex_content))))
        self.abstract = self.first_sentence(self.latex_content)
        self.latex_content = self.all_sentences_but_first(self.latex_content)

        
    def produce_pdf(self):
        """Method to produce the final pdf"""
        output_filename = f'{self.title}.pdf'
        BCP_47_languages = {"fr" : "fr-FR","de" : "en-US","en" : "en-GB","it" : "en-US","es" : "en-US"}
        pypandoc.convert_text(self.latex_content, 'pdf', format='latex', outputfile=f"../pdf/{output_filename}", extra_args=['-V', 'geometry:margin=3cm','-V',f'title:{self.title}', '-V',f'abstract:{self.abstract}','-V',f'lang:{BCP_47_languages[self.language]}','-V', 'toc','-V', 'pagestyle:headings'])
        print(f'<!> Successfully converted to {output_filename} in pdf folder \n')
        self.output_filename = f"../pdf/{output_filename}"


    def encode_accents(self,text : str,accents_inv = None) -> str:  
        """Function to encode the accents

        Args:
            text (str): the text to encode

        Returns:
            str: the encoded text
        """
        if accents_inv == None:
            for accent in self.accents.keys():
                if text.__contains__(accent):
                    text = text.replace(accent,self.accents[accent])
        else:
            for accent in accents_inv.keys():
                if text.__contains__(accent):
                    text = text.replace(accent,accents_inv[accent])            
        return text

    def decode_accents(self,text : str) -> str:
        """Exact inverse of encode_accents

        Args:
            text (str): the text to decode
            accents (dict): the accents dict

        Returns:
            str: the decoded text
        """
        return self.encode_accents(text,{v: k for k, v in self.accents.items()})

    def show_result(self):
        import os
        os.system(f"open {self.output_filename}")
        
import sys       
def convert_wikipedia_to_latex(title_input = None):
    article = WikipediaArticle(title_input)
    article.fetch_content()
    article.convert_to_latex()
    article.preprocess()
    article.produce_pdf()
    print("Want to see the result ?")
    ans = input()
    if ans == 'yes':
        article.show_result()




if __name__ == "__main__":
    convert_wikipedia_to_latex()
    


    
