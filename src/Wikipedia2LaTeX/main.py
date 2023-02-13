from wikipedia_converter import WikipediaArticle
if __name__ == "__main__":
    article = WikipediaArticle()
    article.fetch_content()
    article.convert_to_latex()
    article.preprocess()
    article.produce_pdf()
