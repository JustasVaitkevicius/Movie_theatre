1. Įvadas
 a. Programos aprašymas.

Ši programa yra kino teatro valdymo sistema, sukurta naudojant Python programavimo kalbą ir objektinio programavimo principus. Sistema leidžia:

+ Valdyti filmų katalogą (pridėti, peržiūrėti filmus).

+ Tvarkyti kino sales (pridėti naujas sales, peržiūrėti esamas).

+ Kurti seansus ir tvarkyti jų grafiką.

+ Vykdyti bilietų pardavimą su vietų rezervavimu.

+ Automatiškai skaičiuoti bilietų kainas.

+ Saugoti ir atkurti duomenis iš failo.

 b. Kaip paleisti programą?

+Atsisiųskite Python 3.x iš python.org

+Atsisiųskite programos failus iš GitHub repozitorijos

+Terminale įvykdykite:

python cinema_system.py

 c. Kaip naudotis programa?

Programa turi intuityvią tekstinę sąsają su meniu:

=== KINO TEATRO VALDYMO SISTEMA ===
1. Peržiūrėti filmus
2. Peržiūrėti sales
3. Peržiūrėti seansus
4. Pridėti filmą
5. Pridėti salę
6. Sukurti seansą
7. Pirkti bilietą
8. Peržiūrėti salės planą
9. Išsaugoti duomenis
10. Įkelti duomenis
0. Išeiti

Vartotojas gali lengvai naršyti meniu punktus įvedant atitinkamus skaičius.

2. Analizė
 a. Funkcionalių reikalavimų įgyvendinimas

1. Objektinio programavimo principai:

# Abstrakcija - DataHandler abstrakti klasė
class DataHandler(ABC):
    @abstractmethod
    def save_data(self, data, filename):
        pass

# Paveldėjimas - JSONDataHandler paveldi iš DataHandler
class JSONDataHandler(DataHandler):
    def save_data(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

# Inkapsuliacija - privatūs kintamieji Movie klasėje
class Movie:
    def __init__(self, title, duration, genre):
        self.__title = title
        self.__duration = duration
        self.__genre = genre

# Polimorfizmas - skirtingi DataHandler įgyvendinimai
json_handler.save_data(data)  # Veikia skirtingai nei CSV handler

2. Singleton dizaino šablonas:

class CinemaManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Inicializacija
        return cls._instance

3. Kompozicija ir agregacija:

# Kompozicija - Screening negali egzistuoti be Movie
class Screening:
    def __init__(self, movie, screening_time, hall):
        self.movie = movie

# Agregacija - Ticket gali egzistuoti ir be Screening
class Ticket:
    def __init__(self, screening, seat_number, price):
        self.screening = screening

4. Duomenų saugojimas:

def save_data(self, filename='cinema_data.json'):
    data = {
        'movies': [m.to_dict() for m in self.movies],
        'halls': [h.to_dict() for h in self.halls],
        'screenings': [s.to_dict() for s in self.screenings],
        'tickets': [t.to_dict() for t in self.tickets]
    }
    self.data_handler.save_data(data, filename)

3. Rezultatai ir Išvados
 a. Rezultatai

+ Sėkmingai sukurta pilna kino teatro valdymo sistema

+ Įgyvendinti visi 4 OOP principai (abstrakcija, paveldėjimas, inkapsuliacija, polimorfizmas)

+ Panaudotas Singleton dizaino šablonas

+ Realizuotas duomenų saugojimas JSON formatu

+ Sukurtas automatinis bilietų kainodaros mechanizmas

 b. Iššūkiai

- Sudėtinga buvo suderinti Singleton šablono naudojimą su duomenų įkėlimu iš failo

- Vietų rezervacijos logika reikalavo papildomo tobulinimo

- Testavimo metu buvo aptiktos klaidos duomenų serializacija

 c. Galimos plėtros kryptys

+ Pridėti grafinę vartotojo sąsają

+ Integruoti mokėjimo sistemą

+ Pridėti vartotojų roles ir prieigos teises

+ Įdiegti duomenų bazę vietoj failų saugojimo

+ Pridėti atsiliepimų ir įvertinimų sistemą

4. Išvados

Šis kursinis darbas sėkmingai įgyvendino kino teatro valdymo sistemą, kuri:

+ Atitinka visus pateiktus reikalavimus:

+ Pilnai įgyvendina 4 OOP principus

+ Naudoja Singleton dizaino šabloną

+ Demonstruoja kompozicijos ir agregacijos principus

+ Turi duomenų saugojimo/įkėlimo funkcionalumą

Yra praktiškai pritaikoma:

+ Turi intuityvią vartotojo sąsają

+ Automatizuoja bilietų kainodarą

+ Leidžia lengvai valdyti seansus ir sales

Toliau plėtojama:

+ Sistemą galima lengvai išplėsti naujomis funkcijomis

+ Architektūra leidžia integruoti papildomus modulius

Ši sistema gali būti naudojama kaip pagrindas profesionalioms kino teatro valdymo sistemoms kurti.