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

def content_info(soup):
    dir_results = {}
    try:
        
        #Extracting title
        title = soup.find('div', attrs = {'class':'_1l9azAvU'})
        if title is not None:
            dir_results['title'] = title.h1.text
            
        else:
            title = soup.find('div', attrs={'class':'display_center ui_container'})
            if title is not None:
                dir_results['title'] = title.h1.text
            else:
                dir_results['title'] = None
        
        #Extracting Activities
        #fix it for Boston
        activities = soup.find_all('span', attrs = {'class':'_2e_OvRJN'})
                
        if activities is not None:
            activities_list = [activitie.h3.text for activitie in activities]
            dir_results['activities'] = activities_list
        else:  
           
            activities = soup.find_all('div', attrs = {'class':'_1lY2qyk3'})
            
            if activities is not None:
                activities_list = [activitie.h3.text for activitie in activities]
                dir_results['activities'] = activities_list
            else:
                dir_results['activities'] = None
        return dir_results
        
    except Exception as e:
        print('Error')
        print(e)
        print('\n')
        

        

