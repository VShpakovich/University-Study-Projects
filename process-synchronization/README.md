Solving acces to shared resources problem.
The task is to synchronize the operation of 3 threads operating on a 2-element buffer of shared data that is the union that holds the unsigned long int or double(output values) and on the command buffer. 
2 consumers: Fibb(every second asks for generating specified element of the fibonacci sequence) and Rand(every two seconds ask for random double).
1 producer: executes the command and puts the result in the special place.


Two solutions: using semaphores, using monitors. 

