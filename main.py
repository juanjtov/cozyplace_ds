import requests
from bs4 import BeautifulSoup
from scraper import get_sections, get_top_destinations, content_info

def run():
    url_basic = 'https://www.tripadvisor.com/'
    sections = get_sections(url_basic)
    print(sections)

    url_attractions = sections[2]
    links_top_attractions = get_top_destinations(url_attractions)
    print(links_top_attractions)
    for link in links_top_attractions:
        content = requests.get(link)
        if content.status_code == 200:
            s_content = BeautifulSoup(content.text,'lxml')
            print(content_info(s_content))




if __name__ == "__main__":
    run()