import requests
from bs4 import BeautifulSoup

def get_sections(url):
    tripadv = requests.get(url)
    s_trip = BeautifulSoup(tripadv.text, 'lxml')
    sections = s_trip.find_all('div', attrs={'class':'_2R--RBNa _39kFrNls _2PEEtTWK _3_rLKjCx _3wprI9Ge _1_nbwDp3'})

    links_sections = []
    for section in sections:
        if section.find('a'):
            links_sections.append('http://www.tripadvisor.com'+section.find('a').get('href'))

    return links_sections

