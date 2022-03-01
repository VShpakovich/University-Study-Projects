from ev_algorithm import create_graph, evolutionary_algorithm, ilustrate
import timeit
import matplotlib.pyplot as plt
import numpy as np


def write_to_file(parametrs, penaltys, nodes, file_name):
    np.savetxt(file_name, [p for p in zip(parametrs, penaltys,nodes)], delimiter=',', fmt='%s')


def make_time_plot(parametrs, times, file_name, plot_name):
    fig, ax = plt.subplots()
    ax.scatter(parametrs, times)
    ax.legend()
    fig.set_figheight(5)
    fig.set_figwidth(8)
    plt.xlabel(plot_name)
    plt.ylabel('time')
    plt.savefig(file_name)


# Population size impact
def test1():
    graph = create_graph(25)
    population_sizes = [5, 50, 100, 500, 1000]
    sizes_for_plot = []
    times = []
    penaltys = ['Penalty']
    nodes = ['Number of nodes']
    for size in population_sizes:
        for i in range(25):
            sizes_for_plot.append(size)
            result = evolutionary_algorithm(graph, size)[1]
            penaltys.append(result[0])
            nodes.append(result[1])
            time = timeit.timeit(lambda:evolutionary_algorithm(graph, size), number=1)
            times.append(time)
       
    make_time_plot(sizes_for_plot, times, 'test1.png', 'population size')
    sizes_for_plot.insert(0,'Population size')
    write_to_file(sizes_for_plot, penaltys, nodes, 'Test1.csv')


# Number of iterations impact, population size = 50
def test2():
    graph = create_graph(25)
    number_of_iterations = [100, 500, 1000, 2000, 10000]
    iterations_for_plot = []
    times = []
    penaltys = ['Penalty']
    nodes = ['Number of nodes']
    for number in number_of_iterations:
        for i in range(25):
            iterations_for_plot.append(number)
            result = evolutionary_algorithm(graph, 50, number)[1]
            penaltys.append(result[0])
            nodes.append(result[1])
            time = timeit.timeit(lambda:evolutionary_algorithm(graph, 50, number), number=1)
            times.append(time)
    make_time_plot(iterations_for_plot, times, 'test2.png', 'Number of iterations')
    iterations_for_plot.insert(0,'Number of iterations')
    write_to_file(iterations_for_plot, penaltys, nodes, 'Test2.csv')   


# Probability of mutation impact, population size = 50, number of iterations = 1000
def test3():
    graph = create_graph(25)
    number_of_probabilities = [1, 20, 50, 80, 100]
    probabilities_for_plot = []
    times = []
    penaltys = ['Penalty']
    nodes = ['Number of nodes']
    for number in number_of_probabilities:
        for i in range(25):
            probabilities_for_plot.append(number)
            result = evolutionary_algorithm(graph, 50, 1000, number)[1]
            penaltys.append(result[0])
            nodes.append(result[1])
            time = timeit.timeit(lambda:evolutionary_algorithm(graph, 50, 1000, number), number=1)
            times.append(time)
    make_time_plot(probabilities_for_plot, times, 'test3.png', 'Probability of mutation')
    probabilities_for_plot.insert(0,'Probability of mutation')
    write_to_file(probabilities_for_plot, penaltys, nodes, 'Test3.csv')  


# Power of mutation impact, population size = 50, number of iterations = 1000, prob. of mutation = 20
def test4():
    graph = create_graph(25)
    number_of_powers = [1, 20, 50, 80, 90]
    power_for_plot = []
    times = []
    penaltys = ['Penalty']
    nodes = ['Number of nodes']
    for number in number_of_powers :
        for i in range(25):
            power_for_plot.append(number)
            result = evolutionary_algorithm(graph, 50, 1000, 20, number)[1]
            penaltys.append(result[0])
            nodes.append(result[1])
            time = timeit.timeit(lambda:evolutionary_algorithm(graph, 50, 1000, 20, number), number=1)
            times.append(time)
    make_time_plot(power_for_plot , times, 'test4.png', 'Power of mutation')
    power_for_plot .insert(0,'Power of mutation')
    write_to_file(power_for_plot , penaltys, nodes, 'Test4.csv')  


# How it's works for different graphs. Population size = 50, number of iterations = 1000, prob. of mutation = 20, power of mutation = 50
def test5():
    graph1 = create_graph(25, 1)
    graph2 = create_graph(25, 2)
    graph3 = create_graph(25, 3)
    graphs = [graph1, graph2, graph3]
    power_for_plot = []
    times = []
    penaltys = ['Penalty']
    nodes = ['Number of nodes']
    for graph in graphs :
        if graph == graph1:
            number = 1
        if graph == graph2:
            number = 2
        if graph == graph3:
            number = 3
        for i in range(25):
            power_for_plot.append(number)
            result = evolutionary_algorithm(graph, 50, 1000, 20, 50)[1]
            penaltys.append(result[0])
            nodes.append(result[1])
            time = timeit.timeit(lambda:evolutionary_algorithm(graph, 50, 1000, 20, 50), number=1)
            times.append(time)
    make_time_plot(power_for_plot, times, 'test5.png', 'Graph category')
    power_for_plot .insert(0, 'Graph category')
    write_to_file(power_for_plot, penaltys, nodes, 'Test5.csv')  

#graph_c = create_graph(6,1)
#graph_b = create_graph(7,2)
#graph_r = create_graph(9,3)
#ilustrate(graph_c, "complete graph.png")
#ilustrate(graph_b, "bipatriary graph.png")
ilustrate(graph_r, "random graph.png")


# Start test
#test1()
#test2()
#test3()
#test4()
#test5()
