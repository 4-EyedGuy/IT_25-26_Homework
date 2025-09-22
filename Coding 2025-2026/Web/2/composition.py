class Car:
    def __init__(self, brand, max_speed, doors, engine, wheels):
        self.brand = brand
        self.max_speed = max_speed
        self.doors = doors
        self.engine = engine
        self.wheels = wheels
    
    def __str__(self):
        wheels_info = "\n ".join(str(w) for w in self.wheels)
        return (f"Машина: {self.brand}\n"
        f"Максимальная скорость: {self.max_speed} км/ч\n"
        f"Двери: {self.doors}\n"
        f"{self.engine}\n"
        f"Колёса:\n {wheels_info}")
    

class Engine:
    def __init__(self, power, volume):
        self.power = power
        self.volume = volume
    
    def __str__(self):
        return f"Двигатель: {self.power} лошадинных сил, {self.volume} литров"
    

class Wheel:
    def __init__(self, diameter, fabricator):
        self.diameter = diameter
        self.fabricator = fabricator
    
    def __str__(self):
        return f"Колесо: {self.diameter}\" {self.fabricator}"
    
    
engine = Engine(1750, 5.9)
wheels = [Wheel(19, "Continental") for _ in range(4)]
car = Car("SSC Tuatara", 475, 4, engine, wheels)

print(car)
