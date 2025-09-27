import random
from random import random as rand
import matplotlib.pyplot as plt
#random.seed(40)


class Food_behavior:
    SELFISH = 0
    QUEEN_LOVER = 1
    QUEEN_DONATOR = 2

class Sex:
    MALE = 0
    FEMALE = 1

class Chromosome:
    behavior: int

    def __init__(self, behavior=None):
        if behavior == None:
            self.behavior = int(3*rand())
        else:
            self.behavior = behavior


class Ant:
    chromosomes: list
    sex: int
    mate_chromosome: int
    food: int
    received_food: int
    alive: bool

    def __init__(self, chromosomes, mother):
        if type(chromosomes) is not list:
            raise Exception("type of chromosomes must be list")
        if len(chromosomes) > 2 or len(chromosomes) == 0:
            raise Exception("incorrect length of chromosomes")
        if len(chromosomes) == 2:
            self.sex = Sex.FEMALE
        else:
            self.sex = Sex.MALE
        self.chromosomes = chromosomes
        self.mate_chromosome = None
        self.mother = mother
        self.food = 0
        self.alive = True
        self.received_food = 0

    def is_fertilized(self):
        if self.sex == Sex.MALE:
            raise Exception("Only applies to female")
        return self.mate_chromosome != None

    def receive(self, mate):
        if self.sex == Sex.MALE:
            raise Exception("Sex of recipient must be female")
        if mate.sex == Sex.FEMALE:
            raise Exception("Sex of contributor must be male")
        self.mate_chromosome = mate.chromosomes[0]


    def produce_female(self):
        if self.sex == Sex.MALE:
            raise Exception("Sex of mother must be female")
        if self.mate_chromosome == None:
            raise Exception("Mother must be fertilized")
                # female
        if rand() < 0.5:
            # from left
            chromosomes = [self.chromosomes[0], self.mate_chromosome]
        else:
            # from right
            chromosomes = [self.chromosomes[1], self.mate_chromosome]
        return Ant(chromosomes, self)


    def produce_male(self):
        if self.sex == Sex.MALE:
            raise Exception("Sex of mother must be female")

            # male
        if True:
            # from mom
            if rand() < 0.5:
                # from left
                chromosomes = [self.chromosomes[0]]
            else:
                # from right
                chromosomes = [self.chromosomes[1]]
        else:
            # from dad
            chromosomes = [self.mate_chromosome]


        return Ant(chromosomes, self)


    def produce_offspring(self):
        if self.sex == Sex.MALE:
            raise Exception("Sex of mother must be female")
        if self.mate_chromosome == None:
            raise Exception("Mother must be fertilized")
        if rand() < 0.5:
            # male
            if rand() < 0.5:
                # from mom
                if rand() < 0.5:
                    # from left
                    chromosomes = [self.chromosomes[0]]
                else:
                    # from right
                    chromosomes = [self.chromosomes[1]]
            else:
                # from dad
                chromosomes = [self.mate_chromosome]
        else:
            # female
            if rand() < 0.5:
                # from left
                chromosomes = [self.chromosomes[0], self.mate_chromosome]
            else:
                # from right
                chromosomes = [self.chromosomes[1], self.mate_chromosome]
        return Ant(chromosomes, self)

    def make_food_choice(self):
        if self.mother == None:
            return
        if self.sex == Sex.MALE:
            return
        active_chromosome = None
        if rand() < 0.5:
            active_chromosome = self.chromosomes[0].behavior
        else:
            active_chromosome = self.chromosomes[1].behavior
        
        if active_chromosome == Food_behavior.QUEEN_LOVER:
            self.mother.received_food += self.food
            self.food = 0
        elif active_chromosome == Food_behavior.QUEEN_DONATOR:
            if self.food > 1:
                self.mother.received_food += self.food - 1
                self.food = 1
        

        #donation_probability = 0
        #if self.chromosomes[0].behavior == Food_behavior.QUEEN_LOVER:
        #    donation_probability += 0.5
        #if self.chromosomes[1].behavior == Food_behavior.QUEEN_LOVER:
        #    donation_probability += 0.5
        
        #if rand() < donation_probability:
        #    self.mother.received_food += self.food
        #    self.food = 0


def simulation(initial_size, number_of_pellets, rounds, MATE_SELECTION_COST=0, MATE_RESELECTION_PROB=0.1):
    female_population = []
    male_population = []

    for i in range(initial_size):

        if rand() < 0.5:
            female_population.append(Ant([Chromosome(behavior=None), Chromosome(behavior=None)], None))
        else:
            male_population.append(Ant([Chromosome(behavior=None)], None))
    
    number_of_queen_lovers_overtime = []
    number_of_queen_donators_overtime = []
    number_of_selfish_overtime = []

    for i in range(rounds):
        #print(len(female_population))
        print("ROUND: " + str(i))
        print("POPULATION: " + str(len(female_population) + len(male_population)))
        number_of_queen_lovers = 0
        number_of_selfish = 0
        number_of_queen_donators = 0

        for ant in female_population:
            if ant.chromosomes[0].behavior == Food_behavior.SELFISH:
                number_of_selfish += 1
            elif ant.chromosomes[0].behavior == Food_behavior.QUEEN_DONATOR:
                number_of_queen_donators += 1
            elif ant.chromosomes[0].behavior == Food_behavior.QUEEN_LOVER:
                number_of_queen_lovers += 1
            
            if ant.chromosomes[1].behavior == Food_behavior.SELFISH:
                number_of_selfish += 1
            elif ant.chromosomes[1].behavior == Food_behavior.QUEEN_DONATOR:
                number_of_queen_donators += 1
            elif ant.chromosomes[1].behavior == Food_behavior.QUEEN_LOVER:
                number_of_queen_lovers += 1
            
        number_of_queen_lovers_overtime.append(number_of_queen_lovers)
        number_of_selfish_overtime.append(number_of_selfish)
        number_of_queen_donators_overtime.append(number_of_queen_donators)

        female_babies = []
        male_babies = []

        # reset food and check if mom is alive
        for female in female_population:
            female.food = 0
            female.received_food = 0
            if female.mother != None and not female.mother.alive:
                female.mother = None

        test_count = 0
        test_count2 = 0
        test_count3 = 0
        for female in female_population:
            if female.chromosomes[0].behavior == Food_behavior.QUEEN_LOVER and female.mate_chromosome != None and female.chromosomes[1].behavior == Food_behavior.QUEEN_LOVER:
                test_count3 += 1
            if female.chromosomes[0].behavior == Food_behavior.QUEEN_LOVER and female.mate_chromosome != None and female.chromosomes[1].behavior == Food_behavior.QUEEN_LOVER and female.mate_chromosome.behavior == Food_behavior.QUEEN_LOVER and female.mother != None:
                test_count2 += 1
            if female.chromosomes[0].behavior == Food_behavior.QUEEN_LOVER and female.mate_chromosome != None and female.chromosomes[1].behavior == Food_behavior.QUEEN_LOVER and female.mate_chromosome.behavior == Food_behavior.QUEEN_LOVER and female.mother == None:
                test_count += 1
            #print(str(female.chromosomes[0].behavior) + "," + str(female.chromosomes[1].behavior))
        print("Fertilized super queen loving ants with dead moms: " + str(test_count))
        print("Fertilized super queen loving ants with alive moms: " + str(test_count2))
        print("queen loving ants: " + str(test_count3))


        # harvest food
        for i in range(number_of_pellets):
            random.choice(female_population).food += 1
        
        # decide whether to give your food to your queen
        for female in female_population:
            female.make_food_choice()
        
        for female in female_population:
            female.food = female.food + female.received_food
            female.received_food = 0

        # mate selection for unfertilized females
        if len(male_population) > 0:
            for female in female_population:
                if not female.is_fertilized() or rand() < MATE_RESELECTION_PROB:
                    if female.food > MATE_SELECTION_COST + 1:
                        female.receive(random.choice(male_population))
                        female.food -= MATE_SELECTION_COST

        
        # reproduction

        # old
        #for female in female_population:
        #    if female.is_fertilized():
        #        while female.food > 1:
        #            baby = female.produce_offspring()
        #            female.food -= 1
        #            if baby.sex == Sex.FEMALE:
        #                female_babies.append(baby)
        #            else:
        #                male_babies.append(baby)

        # new
        for female in female_population:
            if female.is_fertilized():
                while female.food > 1:
                    female_babies.append(female.produce_female())
                    female.food -= 1

        for female in female_population:
            if female.is_fertilized():
                male_population.append(female.produce_male())


        # new population
        new_females = []
        new_males = []

        for baby in female_babies:
            new_females.append(baby)
        
        for baby in male_babies:
            new_males.append(baby)
        
        # survival
        for female in female_population:
            if female.food >= 1:
                new_females.append(female)
            else:
                female.alive = False
        
        for male in male_population:
            if male.food >= 1:
                new_males.append(male)
            else:
                male.alive = False
        
        female_population = new_females
        male_population = new_males
        random.shuffle(female_population)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(range(rounds), number_of_selfish_overtime, label="Selfish Genes")
    plt.plot(range(rounds), number_of_queen_lovers_overtime, label="Queen Lover Genes")
    plt.plot(range(rounds), number_of_queen_donators_overtime, label="Queen Donator Genes")
    plt.xlabel("Rounds")
    plt.ylabel("Number of Genes")
    plt.title("Selfish vs Queen Lover Genes Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    simulation(30, 800, 500, MATE_SELECTION_COST=0, MATE_RESELECTION_PROB=0)


if __name__ == "__main__":
    main()
    
