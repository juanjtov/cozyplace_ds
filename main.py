##### START CODE REVIEW COMMENT

# Excellent code!

##### END CODE REVIEW COMMENT

import requests
from bs4 import BeautifulSoup
from scraper import get_sections, get_top_destinations, content_info, get_content, get_links_activities

def run():
    url_basic = 'http://www.tripadvisor.com/'
    sections = get_sections(url_basic)
    print(sections)

    url_attractions = sections[2]
    links_top_attractions = get_top_destinations(url_attractions)
    print(links_top_attractions)
    for link in links_top_attractions:
        content = requests.get(link)
        if content.status_code == 200:
            s_content = BeautifulSoup(content.text,'html.parser')
            activities_content_links = get_links_activities(link, url_basic)

            print(content_info(s_content, activities_content_links))



if __name__ == "__main__":
    run()
