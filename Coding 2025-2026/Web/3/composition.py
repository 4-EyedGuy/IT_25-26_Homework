import random

class Athlete:
    def __init__(self, athlete_name, personal_best):
        self.athlete_name = athlete_name
        self.personal_best = personal_best

    def improve_performance(self):
        pass

    def __str__(self):
        return f"{self.athlete_name} - лучший результат: {self.personal_best:.2f}"


class Sprinter(Athlete):
    def __init__(self, athlete_name, personal_best, sprint_distance):
        super().__init__(athlete_name, personal_best)
        self.sprint_distance = sprint_distance

    def improve_performance(self):
        if self.sprint_distance <= 100:
            improvement = random.uniform(-0.5, -0.1)
        else:
            improvement = random.uniform(-1.0, -0.2)
        self.personal_best += improvement
        return f"{self.athlete_name} улучшил результат на {abs(improvement):.2f} секунд."


class Jumper(Athlete):
    def __init__(self, athlete_name, personal_best, jump_category):
        super().__init__(athlete_name, personal_best)
        self.jump_category = jump_category

    def improve_performance(self):
        if self.jump_category == "в длину":
            improvement = random.uniform(0.05, 0.2)
        elif self.jump_category == "в высоту":
            improvement = random.uniform(0.02, 0.1)
        else:
            improvement = random.uniform(0.01, 0.05)
        self.personal_best += improvement
        return f"{self.athlete_name} улучшил результат на {improvement:.2f} метров."


sprinter = Sprinter("Алексей", 9.10, 100)
jumper = Jumper("Пётр", 7.40, "в длину")

print(sprinter)
print(jumper)

print(sprinter.improve_performance())
print(jumper.improve_performance())

print(sprinter)
print(jumper)