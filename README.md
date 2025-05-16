1. Įvadas

a. Programos aprašymas

Ši programa yra kino teatro valdymo sistema, sukurta naudojant Python programavimo kalbą ir objektinio programavimo (OOP) principus. Sistema leidžia:

Valdyti filmų katalogą (pridėti, peržiūrėti filmus)

Tvarkyti kino sales (pridėti naujas sales, peržiūrėti esamas)

Kurti seansus ir tvarkyti jų grafiką

Vykdyti bilietų pardavimą su vietų rezervavimu

Automatiškai skaičiuoti bilietų kainas

Saugoti ir atkurti duomenis iš failo (JSON)

b. Kaip paleisti programą?

Atsisiųskite Python 3.x iš python.org

Klonuokite šią GitHub repozitoriją:

git clone https://github.com/jusu-vardas/kino-teatras.git
cd kino-teatras

Paleiskite programą terminale:

python cinema_system.py

c. Kaip naudotis programa?

Programa turi intuityvią tekstinę meniu sąsają:

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
11. Išeiti

Vartotojas gali naviguoti meniu įvesdamas atitinkamą numerį.

2. Analizė

a. Funkcionalių reikalavimų įgyvendinimas

1. Objektinio programavimo principai

Abstrakcija – DataHandler abstrakti klasė:

from abc import ABC, abstractmethod

class DataHandler(ABC):
    @abstractmethod
    def save_data(self, data, filename):
        pass

Paveldėjimas – JSONDataHandler paveldi iš DataHandler:

import json

class JSONDataHandler(DataHandler):
    def save_data(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

Inkapsuliacija – privatūs kintamieji Movie klasėje:

class Movie:
    def __init__(self, title, duration, genre):
        self.__title = title
        self.__duration = duration
        self.__genre = genre

Polimorfizmas – skirtingi DataHandler implementacijos:

json_handler.save_data(data)  # Veikia kitaip nei CSVDataHandler

2. Singleton dizaino šablonas

class CinemaManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Inicializacija
        return cls._instance

3. Kompozicija ir agregacija

Kompozicija – Screening egzistuoja tik kartu su Movie:

class Screening:
    def __init__(self, movie, screening_time, hall):
        self.movie = movie

Agregacija – Ticket gali egzistuoti be Screening:

class Ticket:
    def __init__(self, screening, seat_number, price):
        self.screening = screening

4. Duomenų saugojimas JSON formatu

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

Sėkmingai sukurta pilnai veikianti sistema

Įgyvendinti visi 4 OOP principai

Naudotas Singleton dizaino šablonas

Duomenų saugojimas JSON formatu

Veikia automatinė bilietų kainodara

b. Iššūkiai

Sudėtinga derinti Singleton šabloną su duomenų įkėlimu

Vietų rezervacijos logika reikalavo tobulinimo

Aptiktos klaidos serializacijoje testavimo metu

c. Galimos plėtros kryptys

Grafinė vartotojo sąsaja (GUI)

Mokėjimų sistemos integracija

Vartotojų rolės ir prieigos teisės

Duomenų bazės palaikymas (SQLite, PostgreSQL)

Atsiliepimų ir įvertinimų sistema

4. Galutinės išvados

Ši sistema:

Atitinka visus funkcinius reikalavimus

Demonstruoja gerą OOP praktiką

Naudoja pažangius architektūrinius principus

Lengvai išplečiama ir integruojama

Potencialas: gali tapti pagrindu profesionalioms kino teatro valdymo sistemoms kūrimui.

