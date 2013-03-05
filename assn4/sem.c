//    Compile with "gcc -o my_mm my_mm_seq.c -lpthread"
//    No error checking

#include <stdio.h>
#include <stdlib.h>
#include <sys/times.h>
#include <limits.h>
#include <pthread.h>
#include <unistd.h>
#include <math.h>

// thread information
pthread_t		idThreads[ 2 ];

pthread_mutex_t	Mutex		= PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t	NextIter	= PTHREAD_COND_INITIALIZER;

int S;
//int condMet = 0;

void *semP( void *arg ) {

	int returnCode;
	
	while( S <= 0 ) {
		
		// do nothing
	}
	
	returnCode = pthread_mutex_lock( &Mutex );
	while( returnCode != 0 ) {
		returnCode = pthread_cond_wait( &NextIter, &Mutex );
	}
	S--;
	printf( "semP = %d.\n", S );
	pthread_mutex_unlock( &Mutex );
}

void *semV( void *arg ) {
	
	int returnCode;
	
	returnCode = pthread_mutex_lock( &Mutex );
	if( returnCode != 0 ) {
		pthread_cond_signal( &NextIter );
	}
	S++;
	printf( "semV = %d.\n", S );
	pthread_mutex_unlock( &Mutex );
}


// MAIN routine
main( int argc, char **argv ) {

	int counter = 0;
	int threadReturnCodeP = pthread_create( &idThreads[ counter ], NULL, semP, NULL );
	
	counter++;
	int threadReturnCodeV = pthread_create( &idThreads[ counter ], NULL, semV, NULL );
	
	
	pthread_join( idThreads[ 0 ], NULL );
	pthread_join( idThreads[ 1 ], NULL );

	pthread_cond_destroy( &NextIter );
	pthread_mutex_destroy( &Mutex );

	// Last thing that main() should do
	pthread_exit( NULL );
	
	return 0;
}
