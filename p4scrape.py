from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, wordpunct_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import requests, re

stop = stopwords.words('english')
stop += ['.', ',', '(', ')', "'", '"','one','even','two','like','first','film','movie','much','also']

def listify(doc):
    tokenizer = RegexpTokenizer(r'\w+')
    doc = tokenizer.tokenize(doc.lower())
    words = [w for w in doc if w not in stop]
    return words

def get_roger(url):
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, 'lxml')
    
    title = soup.find("h1", {"itemprop" : "name"}).text
    
    review_text = soup.find("div", {"itemprop" : "reviewBody"}).text
    
    site = "roger"
    
    score = int(float(soup.find("meta", \
		{"itemprop" : "ratingValue"})['content']))
    
    return [title, review_text, site, score]

def get_guar(url):
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, 'lxml')
    
    title = soup.find("h1", {"class" : "content__headline js-score"}).text
    title = re.search(r'(.*) review', title).group(1)
    
    review_text = soup.find("div", { "itemprop" : "reviewBody" }).text
    
    site = "guardian"
    
    raw_score = int(float(soup.find("span", {"itemprop" 
        : "ratingValue"}).text))
    
    score = 4 if raw_score > 4 else raw_score
    
    return [title, review_text, site, score]

def get_ny(url):
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, 'lxml')
    
    title = soup.find("h4", {"class" : "review-heading"}).text
    
    site = "new york"
    
    paragraphs = soup.find_all("p", {"class" : "story-body-text story-content"})
    review_text = " ".join(p.text for p in paragraphs)
    
    new_url = soup.find("div", {"class" : "imbd-details"}).a['href']
    response = requests.get(new_url)
    page = response.text
    soup = BeautifulSoup(page, 'lxml')
    score = int(float(soup.find("div", {"class" : "ratingValue"}).span.text))/2
    
    return [title, review_text, site, score]
