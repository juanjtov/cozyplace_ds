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

def get_top_destinations(url_attractions):
    attractions = requests.get(url_attractions)
    s_attract = BeautifulSoup(attractions.text, 'lxml')
    top_destinations = s_attract.find('div', attrs={'data-track-label':'popular_destinations'}).find_all('div', attrs={'class':'poi ui_shelf_item_container ui_geo_shelf_item'})
    links_top_attractions = []
    for destination in top_destinations:
        if destination.find('a'):
            links_top_attractions.append('http://www.tripadvisor.com'+destination.find('a').get('href'))
    
    return links_top_attractions
        

