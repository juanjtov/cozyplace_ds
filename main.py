from scraper import get_sections, get_top_destinations

def run():
    url_basic = 'https://www.tripadvisor.com/'
    sections = get_sections(url_basic)
    print(sections)

    url_attractions = sections[2]
    print(get_top_destinations(url_attractions))

if __name__ == "__main__":
    run()