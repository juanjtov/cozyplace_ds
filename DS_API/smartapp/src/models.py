from enum import Enum #just if necessary
from pydantic import BaseModel

class MyException(Exception):
    pass

class Country(str, Enum):
    COLOMBIA = "COLOMBIA"
    MEXICO = "MEXICO"

class City(str, Enum):
    CANCUN = "CANCUN"
    MEXICO_CITY = "MEXICO CITY"
    PLAYA_DEL_CARMEN = "PLAYA DEL CARMEN"
    PUERTO_VALLARTA = "PUERTO VALLARTA"
    TULUM = "TULUM"
    CABO_SAN_LUCAS = "CABO SAN LUCAS"
    GUADALAJARA = "GUADALAJARA"
    SAN_MIGUEL_DE_ALLENDE = "SAN MIGUEL DE ALLENDE"
    BOGOTA = "BOGOTA"
    CARTAGENA = "CARTAGENA"
    MEDELLIN = "MEDELLIN"
    SANTA_MARTA = "SANTA MARTA"
    CALI = "CALI"
    BARRANQUILLA = "BARRANQUILLA"
    VILLA_DE_LEYVA = "VILLA DE LEYVA"
    BUCARAMANGA = "BUCARAMANGA"

class Configuration(BaseModel):
    country: str = None
    city: str = None
    country_map = {
        Country.COLOMBIA:'https://www.tripadvisor.com/Attractions-g294073-Activities-Colombia.html',
        Country.MEXICO:'https://www.tripadvisor.com/Attractions-g150768-Activities-Mexico.html'
     }

    city_map = {
        City.CANCUN:'http://www.tripadvisor.com/Attractions-g150807-Activities-Cancun_Yucatan_Peninsula.html',
        City.MEXICO_CITY:'http://www.tripadvisor.com/Attractions-g150800-Activities-Mexico_City_Central_Mexico_and_Gulf_Coast.html',
        City.PLAYA_DEL_CARMEN:'http://www.tripadvisor.com/Attractions-g150812-Activities-Playa_del_Carmen_Yucatan_Peninsula.html',
        City.PUERTO_VALLARTA:'http://www.tripadvisor.com/Attractions-g150793-Activities-Puerto_Vallarta.html',
        City.TULUM:'http://www.tripadvisor.com/Attractions-g150813-Activities-Tulum_Yucatan_Peninsula.html',
        City.CABO_SAN_LUCAS:'http://www.tripadvisor.com/Attractions-g152515-Activities-Cabo_San_Lucas_Los_Cabos_Baja_California.html',
        City.GUADALAJARA:'http://www.tripadvisor.com/Attractions-g150798-Activities-Guadalajara_Guadalajara_Metropolitan_Area.html',
        City.SAN_MIGUEL_DE_ALLENDE:'http://www.tripadvisor.com/Attractions-g151932-Activities-San_Miguel_de_Allende_Central_Mexico_and_Gulf_Coast.html',
        City.BOGOTA:'http://www.tripadvisor.com/Attractions-g294074-Activities-Bogota.html',
        City.CARTAGENA:'http://www.tripadvisor.com/Attractions-g297476-Activities-Cartagena_Cartagena_District_Bolivar_Department.html',
        City.MEDELLIN:'http://www.tripadvisor.com/Attractions-g297478-Activities-Medellin_Antioquia_Department.html',
        City.SANTA_MARTA:'http://www.tripadvisor.com/Attractions-g297484-Activities-Santa_Marta_Santa_Marta_Municipality_Magdalena_Department.html',
        City.CALI:'http://www.tripadvisor.com/Attractions-g297475-Activities-Cali_Valle_del_Cauca_Department.html',
        City.BARRANQUILLA:'http://www.tripadvisor.com/Attractions-g297473-Activities-Barranquilla_Atlantico_Department.html',
        City.VILLA_DE_LEYVA:'http://www.tripadvisor.com/Attractions-g676524-Activities-Villa_de_Leyva_Boyaca_Department.html',
        City.BUCARAMANGA:'http://www.tripadvisor.com/Attractions-g297474-Activities-Bucaramanga_Santander_Department.html'        
    }

    #web_site = 'http://www.tripadvisor.com'

    def get_url_country(self):
        return self.country_map[self.country]
    
    def get_url_city(self):
        return self.city_map[self.city]

class Cities(BaseModel):
    country: list

class Activities(BaseModel):
    title: str
    user : str
    date: str
    duration: str
    city : str
    description: str
    tags: str
    image: str

    

