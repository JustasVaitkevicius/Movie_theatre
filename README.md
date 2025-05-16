1. Įvadas
a. Programos aprašymas
Ši programa yra kino teatro valdymo sistema, sukurta naudojant Python programavimo kalbą ir objektinio programavimo (OOP) principus. Sistema leidžia:

✅ Valdyti filmų katalogą (pridėti, peržiūrėti filmus)

✅ Tvarkyti kino sales (pridėti naujas sales, peržiūrėti esamas)

✅ Kurti seansus ir tvarkyti jų grafiką

✅ Vykdyti bilietų pardavimą su vietų rezervavimu

✅ Automatiškai skaičiuoti bilietų kainas

✅ Saugoti ir atkurti duomenis iš failo (JSON)

b. Kaip paleisti programą?
Atsisiųskite Python 3.x

Klonuokite šią GitHub repozitoriją:

bash
Copy
Edit
git clone https://github.com/jusu-vardas/kino-teatras.git
cd kino-teatras
Paleiskite programą terminale:

bash
Copy
Edit
python cinema_system.py
c. Kaip naudotis programa?
Programa pateikia tekstinę meniu sąsają:

markdown
Copy
Edit
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
Naudotojas gali pasirinkti veiksmą įvedant atitinkamą skaičių.

2. Analizė
a. Funkcionalūs reikalavimai ir jų įgyvendinimas
1. Objektinio programavimo principai
Abstrakcija:

python
Copy
Edit
class DataHandler(ABC):
    @abstractmethod
    def save_data(self, data, filename):
        pass
Paveldėjimas:

python
Copy
Edit
class JSONDataHandler(DataHandler):
    def save_data(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
Inkapsuliacija:

python
Copy
Edit
class Movie:
    def __init__(self, title, duration, genre):
        self.__title = title
        self.__duration = duration
        self.__genre = genre
Polimorfizmas:

python
Copy
Edit
json_handler.save_data(data)  # Skiriasi nuo CSVHandler elgsenos
2. Singleton dizaino šablonas
python
Copy
Edit
class CinemaManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Inicializacija
        return cls._instance
3. Kompozicija ir agregacija
Kompozicija – seansas negali egzistuoti be filmo:

python
Copy
Edit
class Screening:
    def __init__(self, movie, screening_time, hall):
        self.movie = movie
Agregacija – bilietas gali egzistuoti ir be seanso:

python
Copy
Edit
class Ticket:
    def __init__(self, screening, seat_number, price):
        self.screening = screening
4. Duomenų saugojimas JSON formatu
python
Copy
Edit
def save_data(self, filename='cinema_data.json'):
    data = {
        'movies': [m.to_dict() for m in self.movies],
        'halls': [h.to_dict() for h in self.halls],
        'screenings': [s.to_dict() for s in self.screenings],
        'tickets': [t.to_dict() for t in self.tickets]
    }
    self.data_handler.save_data(data, filename)
3. Rezultatai ir išvados
a. Rezultatai
✅ Sukurta pilnai veikianti kino teatro valdymo sistema
✅ Įgyvendinti visi 4 pagrindiniai OOP principai
✅ Naudotas Singleton dizaino šablonas
✅ Duomenų saugojimas realizuotas JSON formatu
✅ Veikia bilietų kainodaros logika

b. Iššūkiai
Sudėtinga derinti Singleton naudojimą su duomenų įkėlimu

Vietų rezervacijos logika reikalavo papildomo testavimo

Iškilo klaidų serializuojant duomenis

c. Galimos plėtros kryptys
 Grafinė vartotojo sąsaja (GUI)

 Mokėjimų integracija

 Vartotojų rolės ir prieigos valdymas

 Migracija į duomenų bazę (pvz., SQLite, PostgreSQL)

 Atsiliepimų ir įvertinimų sistema

4. Galutinės išvados
Ši sistema:

✅ Atitinka visus keliamus funkcinius reikalavimus

✅ Demonstruoja gerą objektinio programavimo praktiką

✅ Naudoja pažangius architektūrinius principus

✅ Yra tinkama plėsti ar integruoti su kitomis sistemomis

Potencialas: Gali būti naudojama kaip pagrindas profesionalioms kino teatro sistemoms kurti.
