class Vehicle:
    # Base class for all vehicles, handles fare calculation and type retrieval
    def __init__(self, base_rate, rate_per_km):
        # Initialize vehicle with base rate and rate per kilometer
        self._base_rate = base_rate
        self._rate_per_km = rate_per_km

    def calculate_fare(self, distance_km):
        # Calculate fare based on distance
        return self._base_rate + (self._rate_per_km * distance_km)

    def get_type(self):
        # Return the vehicle type as a string
        return self.__class__.__name__.replace("_", " ")


class Horse(Vehicle):
    # Horse vehicle type
    def __init__(self):
        super().__init__(base_rate=30, rate_per_km=5)


class Motorcycle(Vehicle):
    # Motorcycle vehicle type
    def __init__(self):
        super().__init__(base_rate=40, rate_per_km=10)


class Sedan(Vehicle):
    # Sedan vehicle type
    def __init__(self):
        super().__init__(base_rate=50, rate_per_km=15)


class SUV(Vehicle):
    # SUV vehicle type
    def __init__(self):
        super().__init__(base_rate=60, rate_per_km=20)


class Van(Vehicle):
    # Van vehicle type
    def __init__(self):
        super().__init__(base_rate=70, rate_per_km=30)


class Monster_Truck(Vehicle):
    # Monster Truck vehicle type
    def __init__(self):
        super().__init__(base_rate=150, rate_per_km=60)


class Helicopter(Vehicle):
    # Helicopter vehicle type
    def __init__(self):
        super().__init__(base_rate=1000, rate_per_km=200)


class Elevator_of_Willy_Wonka(Vehicle):
    # Elevator of Willy Wonka vehicle type
    def __init__(self):
        super().__init__(base_rate=3000, rate_per_km=500)


class Magic_Carpet(Vehicle):
    # Magic Carpet vehicle type
    def __init__(self):
        super().__init__(base_rate=5000, rate_per_km=800)


class Tardis(Vehicle):
    # Tardis vehicle type
    def __init__(self):
        super().__init__(base_rate=8000, rate_per_km=1100)


class Dragon(Vehicle):
    # Dragon vehicle type
    def __init__(self):
        super().__init__(base_rate=50000, rate_per_km=10000)


class UFO(Vehicle):
    # UFO vehicle type
    def __init__(self):
        super().__init__(base_rate=100000, rate_per_km=25000)


def create_vehicle(vehicle_type):
    # Factory function to create a vehicle instance based on the type string
    vehicles = {
        "Horse": Horse,
        "Motorcycle": Motorcycle,
        "Sedan": Sedan,
        "SUV": SUV,
        "Van": Van,
        "Monster Truck": Monster_Truck,
        "Helicopter": Helicopter,
        "Elevator of Willy Wonka": Elevator_of_Willy_Wonka,
        "Magic Carpet": Magic_Carpet,
        "Tardis": Tardis,
        "Dragon": Dragon,
        "UFO": UFO,
    }
    return vehicles.get(vehicle_type, Sedan)()