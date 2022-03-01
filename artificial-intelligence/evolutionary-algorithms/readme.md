Solving vertex cover problem using evolutionary algorithm with mutation and tournament selection.

The individual is presented as a list of ones and zeros (the size of this list corresponds to the number of vertices in the graph), where "1" means to use this node.
The initial population is a random sequence of 0 and 1.

The fitness(score) consists of a penalty (how many edges in the graph are not covered) and the number of nodes in vertex cover set.
Individuals with the lowest penalty are selected, among them the one with the lowest number of nodes in vertex cover.

Tournament selection: choose 2 random individuals from population, the best one will go to next generation(continues until as many individuals are selected as there were in the previous population).

Mutation: each individual of the population can mutate with a certain probability. As he mutates, it is randomized what percentage(named power) of his genes will change in value (0 to 1,1 to 0).

Then will mutate "power" number of the genes. The problem in my implementation is that in a certain individual during a mutation the same gene may be selected several times, which means that the mutation will be less than the "power" number of genes.


Tests show the effect of changing parametr values.
 