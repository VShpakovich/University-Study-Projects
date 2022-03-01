Using monitors:
Two monitors (for command buffer and output buffer). Monitor and Condition were implemented using semaphores.
The behavior of threads is as follows: Consumer waits n seconds (depends on consumer's type 2 or 1) to place a command. If he managed, he waits until he can receive the result from the appropriate place in the result buffer (places index 0 or 1).
The Producer waits for the command to come in, then positions the result in the right place informing relevant Consumer.

Running(Linux):
gcc monitor.cpp -o main -lpthread -lm -lstdc++ ;./main
