#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <math.h>
#include <iostream>

/////////////////////////////////////////////////////////////////////////////////////////////////////////
//Structures
typedef union {
    unsigned long int fibi;
    double randi;
} results;

typedef struct {
    int command_code;
    int buffer_index;
    int optional_arg;
} command;


typedef struct{
    results *buffer;
    command *com;
}arguments;
////////////////////////////////////////////////////////////////////////////////////////////////////////
//Producer's functios
unsigned long int generateFib(int arg){
    unsigned long int  value;
    value = arg + 1;
    double phi = (1 + sqrt(5))/2;
    double fi =(1 - sqrt(5))/2;
    double f = (pow(phi, (double)arg) - pow(fi,(double)arg))/sqrt(5);
    value = (unsigned long)f;
    return value;
}

double generateDouble(){
    double value;
    int a = rand() % 100;
    int b = rand() % 100;

    value = (double)a / (double)b ;
    return value;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////
//"Monitor" implementation
class Condition
{
    friend class Monitor;
    private:
        sem_t sem;
        int waiting_count;
    public:
        Condition()
        {
            sem_init(&sem, 0, 0);
            waiting_count = 0;
        }
        ~Condition() { sem_destroy(&sem); }
        void wait()
        {
            sem_wait(&sem);
        }
        bool signal()
        {
            if(waiting_count)
            {
                --waiting_count;
			    sem_post(&sem);
			    return true;
            }else{
                return false;
            }
        }


};

class Monitor {
    private:
        sem_t sem;
    public:
        Monitor()
        {
            sem_init(&sem, 0, 1);
        }
        ~Monitor() { sem_destroy(&sem); }


        void enter()
        {
            sem_wait(&sem);
        }
        void leave()
        {
            sem_post(&sem);
        }

        
        void wait(Condition& cond)
        {
            ++cond.waiting_count;
            leave();
            cond.wait();
        }
        void signal(Condition& cond)
        {
            if(cond.signal()) 
            {
                enter();
            }
        }


};


////////////////////////////////////////////////////////////////////////////////////////////////////////
//Two monitors:for control command and output buffers
Monitor command_monitor;
Condition cbfull;

Monitor output_monitor;
Condition randiempty, fibiempty;
////////////////////////////////////////////////////////////////////////////////////////////////////////
//Producer and consumers.
void* producer(void* arg)
{   
   
    arguments *ars = (arguments*)arg; 
    command *gcom = ars->com;
    while(1)
    {   
        int command_code;
        int buffer_index;
        int optional_arg;
        //getting command
        command_monitor.enter();
        //Wait for full command buffer
        command_monitor.wait(cbfull);
        std::cout<<"\nProducer:got command from ";
        
        command_code = gcom->command_code;
        buffer_index = gcom->buffer_index;
        optional_arg = gcom->optional_arg;

        if (command_code==0){std::cout<<"Fibi";}else{std::cout<<"Randi";}
        command_monitor.leave();
        //placing output
        if(command_code == 0){
            std::cout<<"\nProducer:Produced for fibi\n";
            unsigned long int value = generateFib(gcom->optional_arg);
            output_monitor.enter();
            std::cout<<"\nProducer:Placed output fibi\n";
            (ars->buffer+buffer_index)->fibi = value;
            output_monitor.leave();
            //Signal that fibb buffer is full
            output_monitor.signal(fibiempty);

        }
        if(command_code == 1){
            std::cout<<"\nProducer:Produced for randi\n";
            double val = generateDouble();
            output_monitor.enter();
            std::cout<<"\nProducer:Placed output randi\n";
            (ars->buffer+buffer_index)->randi = val;
            output_monitor.leave();
            //Signal that rand buffer is full
            output_monitor.signal(randiempty);
        }



    }
}
//Consumer Fibb
void* consumer1(void* arg)
{    
    arguments *ars = (arguments*)arg; 
    command *ncom = ars->com;  
    while(1)
    {   
        sleep(1);
        int arg = rand() % 100;
        command_monitor.enter();
        
        std::cout<<"\nFibi:I want element number "<<arg;
        ncom->buffer_index = 0;
        ncom->command_code = 0;
        ncom->optional_arg = arg;
        
        command_monitor.leave();
        //Signal that command buffer is full
        command_monitor.signal(cbfull);
        
        output_monitor.enter();
        //Wait for full fibi buffer
        output_monitor.wait(fibiempty);
        std::cout<<"\nFibi:I get "<<ars->buffer->fibi<<"\n";
        output_monitor.leave();
    }
}
//Consumer Rand
void* consumer2(void* arg)
{
    arguments *ars = (arguments*)arg; 
    command *ncom = ars->com;  
    while(1)
    {   sleep(2);
        command_monitor.enter();
      
        std::cout<<"\nRandi:I want random double";
        ncom->buffer_index = 1;
        ncom->command_code = 1;
        command_monitor.leave();
        //Signal that command buffer is full
        command_monitor.signal(cbfull);
        
        output_monitor.enter();
        //Wait for full randi buffer
        output_monitor.wait(randiempty);
        std::cout<<"\nRandi: I get "<<(ars->buffer+1)->randi<<"\n";
        output_monitor.leave();
    }
}
int main()
{
    results buff[2];
    results *p;
    p = buff;
    command co;
    arguments args_for_treads;
    args_for_treads.buffer = p;
    args_for_treads.com = &co;
    
    pthread_t t1,t2,t3;
    pthread_create(&t1,NULL,consumer1,(void*)&args_for_treads);
    pthread_create(&t3,NULL,consumer2,(void*)&args_for_treads);
    pthread_create(&t2,NULL,producer,(void*)&args_for_treads);

    pthread_join(t1,NULL);
    pthread_join(t2,NULL);
    pthread_join(t3,NULL);

}