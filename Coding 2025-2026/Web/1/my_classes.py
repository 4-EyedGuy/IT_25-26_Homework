class Employee:
    def __init__(self, position, salary, experience):
        self.position: str = position
        self.salary: float = salary
        self.experience: float = experience

    def promotion(self, years=1):
        self.experience += years
        self.salary += (10000 * years)

    def __str__(self):
        return f'должность: {self.position}: зарплата: {self.salary}, стаж: {self.experience}'
    
if __name__ == '__main__':
    e1 = Employee('Бухгалтер', 60000, 1)
    print(e1)

    e1.promotion()
    print(e1)

    e1.promotion(1.5)
    print(e1)