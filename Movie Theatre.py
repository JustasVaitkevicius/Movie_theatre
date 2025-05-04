import json
from abc import ABC, abstractmethod
from datetime import datetime, time


class DataHandler(ABC):
    @abstractmethod
    def save_data(self, data, filename):
        pass
    
    @abstractmethod
    def load_data(self, filename):
        pass


class JSONDataHandler(DataHandler):
    def save_data(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
            
    def load_data(self, filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None


class Movie:
    def __init__(self, title, duration, genre):
        self.__title = title
        self.__duration = duration
        self.__genre = genre
        
    @property
    def title(self):
        return self.__title
        
    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Pavadinimas negali būti tuščias")
        self.__title = value
        
    @property
    def duration(self):
        return self.__duration
        
    @duration.setter
    def duration(self, value):
        if value <= 0:
            raise ValueError("Trukmė turi būti teigiamas skaičius")
        self.__duration = value
        
    @property
    def genre(self):
        return self.__genre
        
    @genre.setter
    def genre(self, value):
        self.__genre = value
        
    def to_dict(self):
        return {
            'title': self.__title,
            'duration': self.__duration,
            'genre': self.__genre
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(data['title'], data['duration'], data['genre'])


class CinemaHall:
    def __init__(self, hall_number, capacity):
        self.hall_number = hall_number
        self.capacity = capacity
        
    def to_dict(self):
        return {
            'hall_number': self.hall_number,
            'capacity': self.capacity
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(data['hall_number'], data['capacity'])


class Screening:
    def __init__(self, movie, screening_time, hall):
        self.movie = movie  
        self.screening_time = screening_time
        self.hall = hall
        self.available_seats = hall.capacity
        self.tickets_sold = 0
        
    def to_dict(self):
        return {
            'movie': self.movie.to_dict(),
            'screening_time': self.screening_time.strftime("%Y-%m-%d %H:%M"),
            'hall': self.hall.to_dict(),
            'available_seats': self.available_seats,
            'tickets_sold': self.tickets_sold
        }
        
    @classmethod
    def from_dict(cls, data):
        movie = Movie.from_dict(data['movie'])
        hall = CinemaHall.from_dict(data['hall'])
        screening_time = datetime.strptime(data['screening_time'], "%Y-%m-%d %H:%M")
        screening = cls(movie, screening_time, hall)
        screening.available_seats = data['available_seats']
        screening.tickets_sold = data['tickets_sold']
        return screening


class Ticket:
    def __init__(self, screening, seat_number, price):
        self.screening = screening  
        self.seat_number = seat_number
        self.price = price
        
    def to_dict(self):
        return {
            'screening': self.screening.to_dict(),
            'seat_number': self.seat_number,
            'price': self.price
        }
        
    @classmethod
    def from_dict(cls, data):
        screening = Screening.from_dict(data['screening'])
        return cls(screening, data['seat_number'], data['price'])


class CinemaManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.movies = []
            cls._instance.screenings = []
            cls._instance.halls = []
            cls._instance.tickets = []
            cls._instance.data_handler = JSONDataHandler()
            cls._instance.initialize_sample_data()
            cls._instance.load_data()
        return cls._instance
    
    def initialize_sample_data(self):
        if not self.movies:
            self.movies.extend([
                Movie("The Matrix", 120, "Sci-Fi"),
                Movie("Inception", 150, "Thriller"),
                Movie("The Shawshank Redemption", 142, "Drama")
            ])
        
        if not self.halls:
            self.halls.extend([
                CinemaHall(1, 50),
                CinemaHall(2, 100)
            ])
    
    def calculate_ticket_price(self, screening):
        base_price = 8
        
        popular_movies = ["The Matrix", "Inception", "Avatar"]
        if screening.movie.title in popular_movies:
            base_price += 3
            
        if screening.screening_time.time() > time(18, 0):
            base_price += 2
            
        if screening.hall.capacity > 80:
            base_price += 1
            
        return base_price
    
    def get_available_seats(self, screening):
        all_seats = [f"{row}{seat}" for row in "ABCDEFGHIJ"[:10] 
                    for seat in range(1, 11)][:screening.hall.capacity]
        sold_seats = [t.seat_number for t in self.tickets 
                     if t.screening == screening]
        return [seat for seat in all_seats if seat not in sold_seats]
    
    def add_movie(self, title, duration, genre):
        movie = Movie(title, duration, genre)
        self.movies.append(movie)
        return movie
        
    def add_hall(self, hall_number, capacity):
        hall = CinemaHall(hall_number, capacity)
        self.halls.append(hall)
        return hall
        
    def add_screening(self, movie_title, screening_time, hall_number):
        movie = next((m for m in self.movies if m.title == movie_title), None)
        hall = next((h for h in self.halls if h.hall_number == hall_number), None)
        
        if not movie or not hall:
            return None
            
        screening = Screening(movie, screening_time, hall)
        self.screenings.append(screening)
        return screening
        
    def buy_ticket(self, screening_id, seat_number):
        if screening_id < 0 or screening_id >= len(self.screenings):
            return None
            
        screening = self.screenings[screening_id]
        
        if seat_number not in self.get_available_seats(screening):
            return None
            
        price = self.calculate_ticket_price(screening)
        ticket = Ticket(screening, seat_number, price)
        self.tickets.append(ticket)
        screening.available_seats -= 1
        screening.tickets_sold += 1
        return ticket
        
    def save_data(self, filename='cinema_data.json'):
        data = {
            'movies': [m.to_dict() for m in self.movies],
            'halls': [h.to_dict() for h in self.halls],
            'screenings': [s.to_dict() for s in self.screenings],
            'tickets': [t.to_dict() for t in self.tickets]
        }
        self.data_handler.save_data(data, filename)
        print(f"Duomenys sėkmingai išsaugoti į {filename}")
        
    def load_data(self, filename='cinema_data.json'):
        data = self.data_handler.load_data(filename)
        if data:
            self.movies = [Movie.from_dict(m) for m in data.get('movies', [])]
            self.halls = [CinemaHall.from_dict(h) for h in data.get('halls', [])]
            self.screenings = [Screening.from_dict(s) for s in data.get('screenings', [])]
            self.tickets = [Ticket.from_dict(t) for t in data.get('tickets', [])]
            print(f"Duomenys sėkmingai įkelti iš {filename}")


def display_menu():
    print("\n=== KINO TEATRO VALDYMO SISTEMA ===")
    print("1. Peržiūrėti filmus")
    print("2. Peržiūrėti sales")
    print("3. Peržiūrėti seansus")
    print("4. Pridėti filmą")
    print("5. Pridėti salę")
    print("6. Sukurti seansą")
    print("7. Pirkti bilietą")
    print("8. Peržiūrėti salės planą")
    print("9. Išsaugoti duomenis")
    print("10. Įkelti duomenis")
    print("0. Išeiti")

def display_movies(cinema):
    print("\n=== FILMŲ SĄRAŠAS ===")
    for i, movie in enumerate(cinema.movies, 1):
        print(f"{i}. {movie.title} ({movie.duration} min.) - {movie.genre}")

def display_halls(cinema):
    print("\n=== SALĖS ===")
    for hall in cinema.halls:
        print(f"Salė {hall.hall_number}: {hall.capacity} vietų")

def display_screenings(cinema):
    print("\n=== SEANSAI ===")
    for i, screening in enumerate(cinema.screenings, 1):
        price = cinema.calculate_ticket_price(screening)
        print(f"{i}. {screening.movie.title} | {screening.screening_time} | "
              f"Salė {screening.hall.hall_number} | Kaina: {price}€ | "
              f"Laisvos vietos: {screening.available_seats}/{screening.hall.capacity}")

def display_seat_map(cinema, screening_id):
    if screening_id < 0 or screening_id >= len(cinema.screenings):
        print("Neteisingas seanso ID!")
        return
        
    screening = cinema.screenings[screening_id]
    available_seats = cinema.get_available_seats(screening)
    
    print(f"\n=== SALĖS {screening.hall.hall_number} PLANAS ===")
    print("Filmas:", screening.movie.title)
    print("Laikas:", screening.screening_time)
    print("\n  " + " ".join(f"{i:2}" for i in range(1, 11)))
    
    for row in "ABCDEFGHIJ"[:10]:
        print(f"{row}: ", end="")
        for seat in range(1, 11):
            seat_code = f"{row}{seat}"
            if seat_code in available_seats:
                print("O ", end="")
            else:
                print("X ", end="")
        print()
    
    print("\nO - laisva, X - užimta")

def main():
    cinema = CinemaManager()
    
    while True:
        display_menu()
        choice = input("Pasirinkite veiksmą: ")
        
        if choice == "1":
            display_movies(cinema)
            
        elif choice == "2":
            display_halls(cinema)
            
        elif choice == "3":
            display_screenings(cinema)
            
        elif choice == "4":
            title = input("Filmo pavadinimas: ")
            duration = int(input("Trukmė (minutės): "))
            genre = input("Žanras: ")
            cinema.add_movie(title, duration, genre)
            print(f"Filmas '{title}' sėkmingai pridėtas!")
            
        elif choice == "5":
            hall_number = input("Salės numeris: ")
            capacity = int(input("Vietų skaičius: "))
            cinema.add_hall(hall_number, capacity)
            print(f"Salė {hall_number} su {capacity} vietų sėkmingai pridėta!")
            
        elif choice == "6":
            display_movies(cinema)
            movie_title = input("Filmo pavadinimas: ")
            
            display_halls(cinema)
            hall_number = input("Salės numeris: ")
            
            screening_time = input("Seanso laikas (YYYY-MM-DD HH:MM): ")
            try:
                screening_time = datetime.strptime(screening_time, "%Y-%m-%d %H:%M")
                cinema.add_screening(movie_title, screening_time, hall_number)
                print("Seansas sėkmingai sukurtas!")
            except ValueError:
                print("Neteisingas datos formatas! Naudokite YYYY-MM-DD HH:MM")
                
        elif choice == "7":
            display_screenings(cinema)
            try:
                screening_id = int(input("Pasirinkite seanso ID: ")) - 1
                if screening_id < 0 or screening_id >= len(cinema.screenings):
                    raise ValueError
                
                display_seat_map(cinema, screening_id)
                seat_number = input("Pasirinkite vietą (pvz., A5): ").upper()
                
                ticket = cinema.buy_ticket(screening_id, seat_number)
                if ticket:
                    print(f"\nBilietas į {ticket.screening.movie.title} "
                          f"vietoje {seat_number} nupirktas už {ticket.price}€!")
                else:
                    print("Nepavyko nusipirkti bilieto - vieta užimta arba neteisinga!")
            except (ValueError, IndexError):
                print("Neteisingas seanso ID!")
                
        elif choice == "8":
            display_screenings(cinema)
            try:
                screening_id = int(input("Pasirinkite seanso ID: ")) - 1
                display_seat_map(cinema, screening_id)
            except (ValueError, IndexError):
                print("Neteisingas seanso ID!")
                
        elif choice == "9":
            cinema.save_data()
            
        elif choice == "10":
            cinema.load_data()
            
        elif choice == "0":
            print("Programa baigia darbą. Iki!")
            break
            
        else:
            print("Neteisingas pasirinkimas! Bandykite dar kartą.")
        
        input("\nSpauskite Enter, kad tęsti...")

if __name__ == "__main__":
    main()
