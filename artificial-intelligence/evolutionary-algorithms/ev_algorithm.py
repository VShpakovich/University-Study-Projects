import networkx as nx
import matplotlib.pyplot as plt
import random


# Type 1 - complete graph, 2 - bipartite graph, 3 - random graph
def create_graph(n, type=3):
        if type == 1:
            graph = nx.complete_graph(n)
            return graph
        elif type == 2:
            half = round(n/2)
            graph = nx.complete_bipartite_graph(half, n-half)
            return graph
        else:
            graph = nx.complete_graph(n)
            edges_to_delete_number = round((n*(n-1))/2 * 0.7)
            for i in range(edges_to_delete_number):
                number_of_edges = len(list(graph.edges))
                edge_to_delete = list(graph.edges)[random.randint(1, number_of_edges-1)]
                graph.remove_edge(edge_to_delete[0], edge_to_delete[1])
            return graph


# Population
def start_population(graph, size):
    members = []
    for i in range(size):
        member = []
        for i in range(len(graph.nodes)):
            member.append(random.randint(0, 1))
        members.append(member)
    return members


# Color to show
def color_solution(graph, member):
    color_map = []
    for i in range(len(member)):
        if member[i] == 1:
           color_map.append('red')
        else:
            color_map.append('blue')
    return color_map


def show(graph, member, file_name):
    colors = color_solution(graph, member)
    nx.draw(graph, node_color=colors)
    plt.savefig(file_name)
    #plt.show()


#########################################################################
# Rating
def cost(solution, edges):
    penalty = 0
    for edge in edges:
        (u, v) = edge
        if ((solution[u] == 0) and (solution[v] == 0)):
            penalty += 1
    number_of_nodes = solution.count(1)
    return penalty, number_of_nodes


def cost_for_each(solutions, edges):
    costs = []
    for solution in solutions:
        costs.append(cost(solution, edges))
    return costs


# Among members with min penalty find one with min number of edges
def find_the_best(results, number_of_edges, number_of_nodes):
    best_penalty = number_of_edges
    best_nodes = number_of_nodes
    number_of_solution = 0
    for i in range(len(results)):
        if results[i][0] < best_penalty:
            best_penalty = results[i][0]
            best_nodes = results[i][1]
            number_of_solution = i
        elif results[i][0] == best_penalty:
            if results[i][1] < best_nodes:
                best_penalty = results[i][0]
                best_nodes = results[i][1]
                number_of_solution = i
    return number_of_solution


# Generate "number"(number = {1, 2, 3...}) numbers
def generate_uniq(left, right, number):
    result = random.sample(range(left, right), k=number)
    return result


# Tournament selection, k = 2
def selection(population, number_of_edges, number_of_nodes):
    new_population = []
    n = len(population)
    for i in range(n):
        competitor1, competitor2 = generate_uniq(0,n-1,2)
        competitors = [population[competitor1], population[competitor2]]
        winner = competitors[find_the_best(competitors, number_of_edges, number_of_nodes)]
        new_population.append(winner)
    return new_population


# Probability of mutation - whether a given element will mutate?By default, 30%
# Power - how many genes will be changed in the "mutant"?By default, 10% of genes it has
def mutation(population, probability_of_mutation=30, power_procent=10):
    new_population = []
    chromosom_size = len(population[0])
    power = round((chromosom_size * power_procent) / 100)
    for member in population:
        if random.randint(1, 100) <= probability_of_mutation:
            mutate_genes_id = generate_uniq(0, chromosom_size-1, power)
            for gen in mutate_genes_id:
                member[gen] = 0 if member[gen] == 1 else 1
        new_population.append(member)
    return new_population


def evolutionary_algorithm(graph, population_size, number_of_iterations=100, probability_of_mutation=30, power_procent=10):
    population = start_population(graph, population_size)
    number_of_edges = len(graph.edges)
    number_of_nodes = len(graph.nodes)

    results = cost_for_each(population, graph.edges)
    number_of_best_solution = find_the_best(results, number_of_edges, number_of_nodes)
    for i in range(number_of_iterations):
        new_population = selection(population, number_of_edges, number_of_nodes)
        mutate_population = mutation(new_population, probability_of_mutation, power_procent)
        population = mutate_population

        results = cost_for_each(population, graph.edges)
        number_of_best_solution = find_the_best(results, number_of_edges, number_of_nodes)
    return population[number_of_best_solution], results[number_of_best_solution]


##############################################################################
def ilustrate(graph, file_name):
    member = evolutionary_algorithm(graph, 5, 5, 20, 30)[0]
    show(graph, member, file_name)
