import string
import random
from operator import itemgetter  # may be useful in retrieving elements of the population

pop_size = 50
crossover_rate = 0.75
mutation_rate = 0.05


# Function to calculate a candidates solution fitness - solutions closer to the goal should score higher
# Input parameters: candidate solution (string of 1's and 0's)
# Returns: fitness of the candidate solution
def fitness(solution):
    # Your code goes here
    # Your code goes here
    score = 0
    for i in solution:
        if i == "1":
            score += 1

    return score


# Generate a random string of 1's and 0's of length defined by the parameter
# Input parameters: length of the string to generate
# Returns: The randomly generated string
def gen_individual(length):
    # Your code goes here
    # Your code goes here
    solution = ""
    for i in range(length):
        solution += str(random.randrange(0, 2))
    return solution


# Input parameters: The length of the individuals (strings) to generate. The population size is determined by the global variable pop_size.
# Returns: A population of randomly generated individuals with associated fitness values (set to 0)
def gen_population(string_length):
    # Your code goes here
    # Your code goes here
    population = []
    for i in range(pop_size):
        population.append([gen_individual(string_length), 0])
    return population


# Input parameters: A population of individuals (solutions)
# Returns: The population modified with the computed fitness of each individual
def evaluate_pop(pop):
    # Your code goes here
    # Your code goes here
    newpopu = []
    for item in pop:
        item[1] = fitness(item[0])
        newpopu.append(item)
    return newpopu


# Input parameters: A population of individuals (solutions)
# Returns: The fittest individual and its score
def fittest_individual(pop):
    # Your code goes here
    # Your code goes here
    bestFitness = pop[0]

    for item in pop:
        if item[1] > bestFitness[1]:
            bestFitness = item

    return bestFitness


# Orders the list according to fitness and returns the top 50%
# Input parameters: A population of individuals
# Returns: The subset of the population drawn from the top 50% of the individuals (as ranked by fitness)
def find_top_50(pop):
    # Your code goes here
    # Your code goes here
    pop.sort(key=lambda x: x[1], reverse=True)
    return pop[:int(len(pop) / 2)]


# Input parameters: Two parents (tuples of the form <individual, fitness>)
# Returns: Two children after combining the two parents (tuples of the form <individual, 0>)
# or the original two parents if the crossover threshold is not met
def crossover(parent1, parent2):
    # Your code goes here
    doesItCrossover = random.random()

    if doesItCrossover < crossover_rate:
        location = random.randrange(0, len(parent1[0]))

        child1 = parent1[0][:location] + parent2[0][location:]
        child2 = parent2[0][:location] + parent1[0][location:]

        return [child1, 0], [child2, 0]

    else:
        return parent1.copy(), parent2.copy()


# Input parameters: a population
# Returns: The new population after selection and crossover (using the operation defined above) have been applied
def select_and_generate_new_population(parents):
    # Your code goes here
    newlist = []
    # parents = find_top_50(parents)
    if len(parents) == pop_size:
        parents = find_top_50(parents)

    # Your code goes here
    while len(newlist) < pop_size:
        parent1 = parents[random.randrange(len(parents))]
        parent2 = parents[random.randrange(len(parents))]

        child1, child2 = crossover(parent1, parent2)

        newlist.append(child1)
        newlist.append(child2)

    return newlist[:pop_size]


# Function to mutate individuals in the population according to the mutation rate
# Input parameters: A population
# Returns: A modified population
def mutate(pop):
    # Your code goes here
    # Your code goes here
    for i in range(len(pop)):
        random_Check = random.random()
        # print(random_Check)
        if random_Check < mutation_rate:
            # print(f'this is getting mutated {pop[i][0]}')
            p = random.randrange(0, len(pop[i][0]))
            if pop[i][0][p] == "0":
                pop[i][0] = (pop[i][0][:p] + "1" + pop[i][0][p + 1:])
            else:
                pop[i][0] = (pop[i][0][:p] + "0" + pop[i][0][p + 1:])
    return pop


# Main GA loop which takes the string length as an input parameter.

def GA(string_length):
    pop = gen_population(string_length)
    scored_pop = evaluate_pop(pop)
    i = 0
    while fittest_individual(scored_pop)[
        1] < string_length:  # This would usually be more general such a monitoring the change in fitness over iterations but keeping thngs simple here
        i += 1
        new_pop = []
        parents = find_top_50(scored_pop)
        new_pop = select_and_generate_new_population(parents)
        mutated_pop = mutate(new_pop)
        pop = mutated_pop
        scored_pop = evaluate_pop(pop)
    return fittest_individual(scored_pop)


# ==========================================
# GENETIC ALGORITHM - AUTOMATED TESTS
# ==========================================

import random
import copy

def check_test(test_number, actual, expected):
    if actual == expected:
        print(f"Test {test_number} = Correct")
    else:
        print(f"Test {test_number} = Incorrect")
        print(f"  Expected: {expected}")
        print(f"  Got:      {actual}")


# TEST 1 - Population generation, evaluation and fittest individual
random.seed(27)

result1 = [
    len(gen_population(7)),
    len(evaluate_pop(gen_population(7)))
]

pop1 = gen_population(7)
pop2 = evaluate_pop(gen_population(7))

result1.append(fittest_individual(pop1)[1])
result1.append(fittest_individual(pop2)[1] > fittest_individual(pop1)[1])

check_test(1, result1, [50, 50, 0, True])


# TEST 2 - Select top 50%
random.seed(27)

pop1 = gen_population(7)
pop2 = find_top_50(evaluate_pop(pop1))

avgFitnessTop50 = sum(x[1] for x in pop2) / len(pop2)
avgFitnessWholePop = sum(x[1] for x in pop1) / len(pop1)

result2 = [
    len(pop2),
    avgFitnessTop50 > avgFitnessWholePop
]

check_test(2, result2, [25, True])


# TEST 3 - Crossover
random.seed(66)

crossover_rate = 1.0

offspring1, offspring2 = crossover(["1010101", 4], ["0101010", 3])

result3 = [offspring1[0], offspring2[0]]

crossover_rate = 0.0

offspring1, offspring2 = crossover(["1010101", 4], ["0101010", 3])

result3.append(offspring1[0] == "1010101")
result3.append(offspring2[0] == "0101010")

crossover_rate = 0.75

check_test(3, result3, ["1011010", "0100101", True, True])


# TEST 4 - Selection and new population generation
random.seed(17)

pop1 = evaluate_pop(gen_population(7))
pop2 = evaluate_pop(select_and_generate_new_population(pop1))

avgFitnessNewGen = sum(x[1] for x in pop2) / len(pop2)
avgFitnessParents = sum(x[1] for x in pop1) / len(pop1)

result4 = avgFitnessNewGen > avgFitnessParents

check_test(4, result4, True)


# TEST 5 - Mutation
random.seed(99)

mutation_rate = 1.0

pop1 = evaluate_pop(gen_population(7))
pop2 = copy.deepcopy(pop1)
pop2 = mutate(pop2)

result5 = [pop1 == pop2]

mutation_rate = 0.0

pop1 = evaluate_pop(gen_population(7))
pop2 = copy.deepcopy(pop1)
pop2 = mutate(pop2)

result5.append(pop1 == pop2)

mutation_rate = 0.05

check_test(5, result5, [False, True])


# TEST 6 - Complete genetic algorithm
random.seed(21)

result6 = [
    GA(7)[0],
    GA(17)[0],
    GA(30)[0]
]

check_test(6, result6, [
    "1111111",
    "11111111111111111",
    "111111111111111111111111111111"
])