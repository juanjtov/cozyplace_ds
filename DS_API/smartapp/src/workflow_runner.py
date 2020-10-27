from models import City, Activities
import requests
from bs4 import BeautifulSoup
import pandas as pd


#This file for the input URL get the main cities and for each city the list of activities

def get_cities(country_url, url_scraping): #Input the country
#url_attractions = 'https://www.tripadvisor.com/Attractions'
    country = requests.get(country_url)
    s_country = BeautifulSoup(country.text, 'html.parser')
    top_cities = s_country.find_all('div', attrs={'class':'_3IKpjWD9'})    
    links_top_cities = []
    for city in top_cities:
        if city.find('a'):
            links_top_cities.append(url_scraping+city.find('a').get('href'))
        
    return links_top_cities #returning the list of cities


def get_city_activities_link(url_city, url_scraping): #input link for each city
    r_url_city = requests.get(url_city)
    if r_url_city.status_code == 200:
        s_city =  BeautifulSoup(r_url_city.text, 'html.parser')
        #print(s_city)
        final_links =[]
        activities_city_explore = s_city.find_all('div', attrs={'class':'_1sXmOkVY'})
        #print(activities_class)
        if len(activities_city_explore) != 0:
            links_activities_explore = [(url_scraping+activity.find('a').get('href')) for activity in activities_city_explore]
                            #.replace('https','http') for activity in activities_class]
            final_links.extend(links_activities_explore)
        else:
            activities_city_explore = s_city.find_all('div', attrs={'class':'_999WBlyA'})
            if activities_city_explore:
                for activity in activities_city_explore:
                    links_activities_explore = activity.find('a').get('href')
                    if links_activities_explore:
                        final_links.append(url_scraping + links_activities_explore)
                    else:
                        final_links.append(None)
            
    return final_links #return activities links for each city

def get_content_per_activity(activities_list): #Input activities list
    activities_overview = []
    for activity in activities_list:
        if activity is not None:
            r_activity = requests.get(activity)
            if r_activity.status_code == 200:
                r_activity_soup = BeautifulSoup(r_activity.text,'html.parser')
                activity_content =  r_activity_soup.find('div', attrs={'class':'AvpaRatK'})
                if activity_content:
                    activities_overview.append(activity_content.find('span').text)
                else:
                    activities_overview.append('Activity N/A')
        else:
            activities_overview.append('Activity N/A')
            
    
    return activities_overview #return overview per activity


def content_information(soup, activities_list_urls): #Input the Soup of the city and the list of links for each activity
    #for link in links_top_attractions:
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
            dir_results['images'] = [img_fin.replace('https','http') for img_fin in images]
        else:
            images_media = soup.find_all('a', attrs={'class':'_1o7ZDa9J'})
            if images_media:
                images = [img.img.get('data-url') for img in images_media]
                dir_results['images'] = [img_fin.replace('https','http') for img_fin in images]
            
            else:
                dir_results['images'] = None
        
        #Extracting Content
        
        
        content_overview = get_content_per_activity(activities_list_urls)
        if content_overview:
            dir_results['overviews'] = content_overview
        else:
            dir_results['overviews'] = None
        
            
        
        #print(dir_results)
      
        return dir_results #return a dictionary with all the information for each city
                                         
          
    except Exception as e:
        print('Error')
        print(e)
        print('\n')


def dic_asignment_activities(result): #Input is a Dictionary List
    dir_per_activity = {}
    results_dic_list = []
    activities_list = result['activities']
    overviews_list = result['overviews']
    images_list = result['images']
    dir_per_activity['Location']= result['title']

    for i in range(0, len(activities_list)):
        if activities_list[i]:
            dir_per_activity['activity_title'] = activities_list[i]
        else:
            dir_per_activity['activity_title'] = None
                
        if overviews_list:    
            dir_per_activity['description'] = overviews_list[i]
        else:
            dir_per_activity['description'] = None
            
        if images_list:    
            dir_per_activity['images'] = images_list[i]
        else:
            dir_per_activity['images'] = None

        print(dir_per_activity) #output is a dict list with json for activity

    
def extract_information(results): #Input the results from the content as a list of dicts
    show_results_per_city = []
    for result in results: #each result belongs to a dictionary of a place: Cartagena, Bogota,etc
        final_results = dic_asignment_activities(result)
        if final_results:
            show_results_per_city.append(final_results)
    
    #return show_results_per_city #return organized results
        
#We gotta try async def....
def run(config, url_scraping):
    activities_per_city_links = []
    results_per_city = []
    url_country = config.get_url()
    top_places = get_cities(url_country, url_scraping)
    for link in top_places: #Top places refers to the place: Bucaramanga, Cartagena, etc.
        content_places = requests.get(link)
        if content_places.status_code == 200:
            s_content_places = BeautifulSoup(content_places.text,'html.parser')
        
            activities_per_city_links = get_city_activities_link(link, url_scraping)
            #  activities_per_city_ links = get_links_activities_final(link)
            #print(activities_per_city_links)
            results_per_city.append(content_information(s_content_places, activities_per_city_links))
            #results_per_activity = get_activity_info(activities_content_links)
            #extract_information(results_per_city)
    
    return results_per_city