import requests
from bs4 import BeautifulSoup

def get_sections(url):
    tripadv = requests.get(url)
    s_trip = BeautifulSoup(tripadv.text, 'html.parser')
    sections = s_trip.find_all('div', attrs={'class':'_2R--RBNa _39kFrNls _2PEEtTWK _3_rLKjCx _3wprI9Ge _1_nbwDp3'})

    links_sections = []
    for section in sections:
        if section.find('a'):
            links_sections.append('http://www.tripadvisor.com'+section.find('a').get('href'))

    return links_sections


def get_top_destinations(url_attractions):
    attractions = requests.get(url_attractions)
    s_attract = BeautifulSoup(attractions.text, 'html.parser')
    top_destinations = s_attract.find('div', attrs={'data-track-label':'popular_destinations'}).find_all('div', attrs={'class':'poi ui_shelf_item_container ui_geo_shelf_item'})
    links_top_attractions = []
    for destination in top_destinations:
        if destination.find('a'):
            links_top_attractions.append('http://www.tripadvisor.com'+destination.find('a').get('href'))
    
    return links_top_attractions


def get_content(activities_list):
    activities_overview = []
    for activity in activities_list:
        r_activity = requests.get(activity)
        if r_activity.status_code == 200:
            r_activity_soup = BeautifulSoup(r_activity.text,'html.parser')
            activity_content =  r_activity_soup.find('div', attrs={'class':'AvpaRatK'})
            if activity_content:
                activities_overview.append(activity_content.find('span').text)
            else:
                activities_overview.append('Activity N/A')
            
    
    return activities_overview


def get_links_activities(url_city, url_basic):
    r_url_city = requests.get(url_city)
    if r_url_city.status_code == 200:
        s_city =  BeautifulSoup(r_url_city.text, 'html.parser')
        activities_class = s_city.find_all('div', attrs={'class':'_1sXmOkVY'})
        links_activities = [(url_basic+activity.find('a').get('href')) for activity in activities_class]
                            #.replace('https','http') for activity in activities_class]
    
    return links_activities


def content_info(soup, activities_list_urls):
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
        
        activities = soup.find_all('span', attrs = {'class':'_2e_OvRJN'})
                
        #if activities is not None:
        if len(activities) != 0:
            activities_list = [activitie.h3.text for activitie in activities]
            dir_results['activities'] = activities_list
        else:  
          
            activities = soup.find_all('div', attrs = {'class':'_1lY2qyk3'})
            
            if activities is not None:
                activities_list = [activitie.h3.text for activitie in activities]
                dir_results['activities'] = activities_list
            else:
                dir_results['activities'] = None

        
        #Extracting Images
        
        images_media = soup.find_all('a', attrs={'class':'_1zqXepI-'})
        
        if len(images_media) != 0:
            images = [img.find('img').get('data-url') for img in images_media]
            dir_results['images'] = images
        else:
            images_media = soup.find_all('a', attrs={'class':'_1o7ZDa9J'})
            if images_media:
                images = [img.img.get('data-url') for img in images_media]
                dir_results['images'] = images
            
            else:
                dir_results['images'] = None
        
         #Extracting Content
        
        content_overview = get_content(activities_list_urls)
        if content_overview:
            dir_results['overviews'] = content_overview
        else:
            dir_results['overviews'] = None

        
        
        return dir_results
        
    except Exception as e:
        print('Error')
        print(e)
        print('\n')
        

        

