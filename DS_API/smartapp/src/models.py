from enum import Enum #just if necessary
from pydantic import BaseModel

class MyException(Exception):
    pass

class Country(str, Enum):
    COLOMBIA = 'COLOMBIA'
    MEXICO = 'MEXICO'
    
class Configuration(BaseModel):
    country: str = None
    country_map = {
        Country.COLOMBIA:'https://www.tripadvisor.com/Attractions-g294073-Activities-Colombia.html',
        Country.MEXICO:'https://www.tripadvisor.com/Attractions-g150768-Activities-Mexico.html'
    }

    def get_url(self):
        return self.country_map[self.country]


class City:
    pass
    #def __init__(self):
     #   self.name = 
class Activities:
    pass