import sys
import requests
import os
import json
from newspaper import Article
import xml.etree.ElementTree as etree 
from textblob import TextBlob

json_data=open("secrets.json").read()
 
calais_url = 'https://api.thomsonreuters.com/permid/calais'
calais_token = 'nAYWp4WGV6Thlsqj6BO626qXyUAL8Q8O'
prnewswire = 'http://www.prnewswire.com/rss/english-releases-news.rss'
headline_url = 'http://globalnews.xignite.com/xGlobalNews.json/GetTopReleasesBySecurity?IdentifierType=Symbol&Identifier=GOOG&Count=10&_Token=DF4A9CD07413493F8EDD92F13C3AA34D'
headers = {'X-AG-Access-Token' : calais_token, 'Content-Type' : 'text/raw', 'outputformat' : 'application/json'}
 
def main():
    try:
        headlines = requests.get(headline_url)
        
        headlines = json.loads(headlines.text)
        for headline in headlines['Headlines']:
            print("Processing Article %s" % headline['Url'])
            article = Article(headline['Url'])
            article.download()
            article.parse()
            
            
            response = requests.post(calais_url, files={'file': article.text}, headers=headers, timeout=80)
            rdf = json.loads(response.text)
            
            for x in rdf:
                if '_type' in rdf[x] and 'name' in rdf[x]:
                    print("Output for %s %s" % (rdf[x]['_type'], rdf[x]['name']))
                    for instance in rdf[x]['instances']:
                        text = instance['prefix'] + instance['suffix']
                        blob = TextBlob(text)
                        for sentence in blob.sentences:
                            print(sentence)
                            print(sentence.sentiment.polarity)
            print('--------------------')
            
            #print(rdf)
    except Exception as e:
        print ('Error in connect ' , e)

 
if __name__ == "__main__":
   main()
