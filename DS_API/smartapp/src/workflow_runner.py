from models import  Activities, Configuration, City
import requests
from bs4 import BeautifulSoup
import pandas as pd


#This file for the input URL get the main cities and for each city the list of activities

def get_cities(config, url_scraping): #Input the country
#url_attractions = 'https://www.tripadvisor.com/Attractions'
    country_url = config.get_url_country()
    country = requests.get(country_url)
    s_country = BeautifulSoup(country.text, 'html.parser')
    dir_cities = {}
    top_cities = s_country.find_all('div', attrs={'class':'_3IKpjWD9'})    
    links_top_cities = []
    for city in top_cities:
        if city.find('a'):
            links_top_cities.append(url_scraping+city.find('a').get('href'))
    
    dir_cities[f'{config.country}'] = links_top_cities
        
    return dir_cities              #returning the list of cities in a JSON format


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
    activities_user = []
    activities_duration = []
    for activity in activities_list:
        if activity is not None:
            r_activity = requests.get(activity)
            if r_activity.status_code == 200:
                r_activity_soup = BeautifulSoup(r_activity.text,'html.parser')
                activity_content =  r_activity_soup.find('div', attrs={'class':'AvpaRatK'})
                activity_user =  r_activity_soup.find('span', attrs={'class':'_3nwb933a'})
                #activity_duration =  r_activity_soup.find('div', attrs={'class':'_3qTEiGfC'})
                activity_duration_list =  r_activity_soup.find_all('li', attrs={'class':'_2PwpULJT'})

                if activity_content:
                    activities_overview.append(activity_content.find('span').text)
                else:
                    activities_overview.append('Activity N/A')

                if activity_user:
                    activities_user.append(activity_user.text)
                else:
                    activities_user.append('Activity N/A')
                
                if activity_duration_list:
                    for duration in activity_duration_list:
                        if duration:
                            duration_analyze = duration.text
                            if duration_analyze.find('Duration') != -1:
                                activities_duration.append(duration_analyze)
                                #break
                
                else:
                    activities_duration.append('Activity N/A')

        else:
            activities_overview.append('Activity N/A')
            activities_user.append('Activivity N/A')
            activities_duration.append('Activiy N/A')
    
    return activities_overview, activities_user, activities_duration #return overview per activity


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
        
        
        content_per_activity = get_content_per_activity(activities_list_urls)
        if content_per_activity:
            dir_results['overviews'] = content_per_activity[0]
            dir_results['users'] = content_per_activity[1]
            dir_results['duration'] = content_per_activity[2]
        else:
            dir_results['overviews'] = None
            dir_results['users'] = None
            dir_results['duration'] = None
        
            
        #Extracting tags
        tags = soup.find_all('span',attrs={'class':'_21qUqkJx'})
        str_x = []
        if len(tags) != 0:
            dir_results['tags'] = [tag.text for tag in tags]
        else:
            [str_x.append('general') for i in range(len( activities_list_urls))]
            dir_results['tags'] = str_x
        
      
        return dir_results #return a dictionary with all the information for each city
                                         
          
    except Exception as e:
        print('Error')
        print(e)
        print('\n')


def extract_information(results): #Input the results from the content as a list of dicts
    show_results_per_city = []
    for result in results: #each result belongs to a dictionary of a place: Cartagena, Bogota,etc
        final_results = dic_asignment_activities(result)
        if final_results:
            show_results_per_city.append(final_results)
    
    #return show_results_per_city #return organized results
def selec_activities(activ, stg2, stg3, stg4, stg5, stg6, stg_title):
    dir_stg = {}

    if activ:
        dir_stg['title'] = activ
    else:
        dir_stg['title'] = None
    
    if stg4:    
        dir_stg['user'] = stg4
    else:
        dir_stg['user'] = None

    if stg5:    
        dir_stg['duration'] = stg5
    else:
        dir_stg['duration'] = None
        
    if stg_title:
        dir_stg['city'] = stg_title
    else:
        dir_stg['city'] = None   
                   
    if stg3:    
        dir_stg['description'] = stg3
    else:
        dir_stg['description'] = None

    if stg6:    
        dir_stg['tags'] = stg6
    else:
        dir_stg['tags'] = None
            
    if stg2:    
        dir_stg['images'] = stg2
    else:
        dir_stg['images'] = None
            
    return dir_stg
    
        
def organize_info(result):
    stg_title = result['title']
    stg1 = result['activities']
    stg2 = result['images']
    stg3 = result['overviews']
    stg4 = result['users']
    stg5 = result['duration']
    stg6 = result['tags']

    if len(stg5) != len(stg1):
        #dif_dur = len(stg5)-len(stg1)
        #for i in range(dif_dur):
        stg5.append('N/A')
    
    if len(stg6) != len(stg1):
        #dif = len(stg6)-len(stg1)
        #for i in range(dif):
        stg6.append('general')

    lis_activ = []
    for j, activ in enumerate(stg1):
        lis_activ.append(selec_activities(activ, stg2[j], stg3[j], stg4[j], stg5[j], stg6[j], stg_title))
    
    return lis_activ
        

        
#We gotta try async def....
def run(config, url_scraping):

    link = config.get_url_city()
    content_places = requests.get(link)
    if content_places.status_code == 200:
        s_content_places = BeautifulSoup(content_places.text,'html.parser')
        activities_per_city_links = get_city_activities_link(link, url_scraping)
        results_per_city = content_information(s_content_places, activities_per_city_links)
        results_dic_activities = organize_info(results_per_city)
            #  activities_per_city_ links = get_links_activities_final(link)
            #print(activities_per_city_links)
            #results_per_city.append(content_information(s_content_places, activities_per_city_links))
            #results_per_activity = get_activity_info(activities_content_links)
            #extract_information(results_per_city)
    
    return results_dic_activities