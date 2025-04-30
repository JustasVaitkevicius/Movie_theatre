import unittest
from datetime import datetime, time
from main import Movie, CinemaHall, Screening, Ticket, CinemaManager # type: ignore

class TestMovie(unittest.TestCase):
    def test_movie_creation(self):
        """Testuojama filmo kūrimo funkcionalumas"""
        movie = Movie("The Matrix", 120, "Sci-Fi")
        self.assertEqual(movie.title, "The Matrix")
        self.assertEqual(movie.duration, 120)
        self.assertEqual(movie.genre, "Sci-Fi")
    
    def test_movie_properties(self):
        """Testuojamos filmo savybių keitimo funkcijos"""
        movie = Movie("Inception", 150, "Thriller")
        
        movie.title = "Inception 2"
        self.assertEqual(movie.title, "Inception 2")
        
        movie.duration = 160
        self.assertEqual(movie.duration, 160)
        
        with self.assertRaises(ValueError):
            movie.title = ""
        
        with self.assertRaises(ValueError):
            movie.duration = -10

class TestCinemaHall(unittest.TestCase):
    def test_hall_creation(self):
        """Testuojama kino salės kūrimas"""
        hall = CinemaHall(1, 100)

        self.assertEqual(hall.hall_number, 1)
        self.assertEqual(hall.capacity, 100)
        
    def test_hall_to_dict(self):
        """Testuojama salės konvertavimas į žodyną"""
        hall = CinemaHall(2, 50)
        hall_dict = hall.to_dict()
        self.assertEqual(hall_dict['hall_number'], 2)
        self.assertEqual(hall_dict['capacity'], 50)

class TestScreening(unittest.TestCase):
    def setUp(self):
        self.movie = Movie("The Shawshank Redemption", 142, "Drama")
        self.hall = CinemaHall(3, 80)
        self.screening_time = datetime(2024, 6, 15, 18, 30)
    
    def test_screening_creation(self):
        """Testuojamas seanso kūrimas"""
        screening = Screening(self.movie, self.screening_time, self.hall)
        self.assertEqual(screening.movie.title, "The Shawshank Redemption")
        self.assertEqual(screening.hall.capacity, 80)
        self.assertEqual(screening.available_seats, 80)
        
    def test_screening_to_dict(self):
        """Testuojamas seanso konvertavimas į žodyną"""
        screening = Screening(self.movie, self.screening_time, self.hall)
        screening_dict = screening.to_dict()
        self.assertEqual(screening_dict['movie']['title'], "The Shawshank Redemption")

class TestTicket(unittest.TestCase):
    def setUp(self):
        movie = Movie("Avatar", 162, "Adventure")
        hall = CinemaHall(4, 120)
        screening_time = datetime(2024, 6, 20, 20, 0)
        self.screening = Screening(movie, screening_time, hall)
    
    def test_ticket_creation(self):
        """Testuojamas bilieto kūrimas"""
        ticket = Ticket(self.screening, "A5", 12.50)
        self.assertEqual(ticket.seat_number, "A5")
        self.assertEqual(ticket.price, 12.50)
        self.assertEqual(ticket.screening.movie.title, "Avatar")

class TestCinemaManager(unittest.TestCase):
    def setUp(self):
        """Prieš kiekvieną testą sukuriame naują CinemaManager egzempliorių"""
        self.cinema = CinemaManager()
        self.cinema.movies = []
        self.cinema.halls = []
        self.cinema.screenings = []
        self.cinema.tickets = []
        
        # Pridedame testinius duomenis
        self.movie1 = self.cinema.add_movie("Interstellar", 169, "Sci-Fi")
        self.movie2 = self.cinema.add_movie("The Dark Knight", 152, "Action")
        self.hall1 = self.cinema.add_hall(1, 50)
        self.hall2 = self.cinema.add_hall(2, 100)
        
    def test_singleton_pattern(self):
        """Testuojamas Singleton šablonas"""
        cinema1 = CinemaManager()
        cinema2 = CinemaManager()
        self.assertIs(cinema1, cinema2)
    
    def test_add_movie(self):
        """Testuojamas filmo pridėjimas"""
        initial_count = len(self.cinema.movies)
        new_movie = self.cinema.add_movie("Pulp Fiction", 154, "Crime")
        self.assertEqual(len(self.cinema.movies), initial_count + 1)
        self.assertEqual(new_movie.title, "Pulp Fiction")
    
    def test_add_screening(self):
        """Testuojamas seanso sukūrimas"""
        screening = self.cinema.add_screening(
            "Interstellar",
            datetime(2024, 6, 25, 19, 0),
            1
        )
        self.assertIsNotNone(screening)
        self.assertEqual(len(self.cinema.screenings), 1)
        self.assertEqual(screening.movie.title, "Interstellar")
        
        # Testuojamas neteisingas seanso sukūrimas
        bad_screening = self.cinema.add_screening(
            "Nonexistent Movie",
            datetime(2024, 6, 25, 19, 0),
            1
        )
        self.assertIsNone(bad_screening)
    
    def test_buy_ticket(self):
        """Testuojamas bilieto pirkimas"""
        screening = self.cinema.add_screening(
            "The Dark Knight",
            datetime(2024, 6, 26, 20, 0),
            2
        )
        
        # Pirkimas sėkmingas
        ticket = self.cinema.buy_ticket(0, "B10")
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.seat_number, "B10")
        self.assertEqual(screening.available_seats, 99)
        
        # Bandymas pirkti užimtą vietą
        bad_ticket = self.cinema.buy_ticket(0, "B10")
        self.assertIsNone(bad_ticket)
    
    def test_calculate_ticket_price(self):
        """Testuojamas bilieto kainos skaičiavimas"""
        morning_screening = Screening(
            self.movie1,
            datetime(2024, 6, 27, 14, 0),
            self.hall1
        )
        evening_screening = Screening(
            self.movie2,
            datetime(2024, 6, 27, 20, 0),
            self.hall2
        )
        
        # Tikriname bazinę kainą
        base_price = self.cinema.calculate_ticket_price(morning_screening)
        self.assertEqual(base_price, 8)
        
        # Tikriname vakaro seanso kainą
        evening_price = self.cinema.calculate_ticket_price(evening_screening)
        self.assertEqual(evening_price, 14)  # 8 + 3 (populiarus) + 2 (vakaras) + 1 (didelė salė)
    
    def test_save_and_load_data(self):
        """Testuojamas duomenų išsaugojimas ir įkėlimas"""
        # Pridedame testinius duomenis
        self.cinema.add_screening(
            "Interstellar",
            datetime(2024, 6, 28, 18, 0),
            1
        )
        self.cinema.buy_ticket(0, "A1")
        
        # Išsaugome duomenis
        self.cinema.save_data("test_data.json")
        
        # Sukuriame naują managerį ir įkeliam duomenis
        new_cinema = CinemaManager()
        new_cinema.movies = []
        new_cinema.load_data("test_data.json")
        
        # Tikriname ar duomenys įkelti teisingai
        self.assertEqual(len(new_cinema.movies), 2)
        self.assertEqual(len(new_cinema.screenings), 1)
        self.assertEqual(len(new_cinema.tickets), 1)
        self.assertEqual(new_cinema.screenings[0].movie.title, "Interstellar")

if __name__ == '__main__':
    unittest.main()