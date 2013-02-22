// Basic C code for Matrix Multiplication
//    Compile with "gcc -o my_mm my_mm_seq.c -lpthread"
//    No error checking

#include <stdio.h>
#include <stdlib.h>
#include <sys/times.h>
#include <limits.h>
#include <pthread.h>
#include <unistd.h>
#include <math.h>

// create a struct to pass into the thread processing method
struct thread_data {
	int i;
	int b;
	long thread_id;
};

// given A and B (both N x N), compute  X = A x B.            
int N;  	// matrix size

// set this to 1 initially other wise a core dump occurs 
// without passing M as a command-line parameter.
int M = 1;  	// number of threads, must >=1.
int vFlag;

double *matA;
double *matB;
double *matX;
double **rowA;
double **colB;
double **rowX;

#define MAXN		20000	// keep ECE's server running
#define MAXN4print	20		// safety, not to overload ECE server

// thread information
pthread_t		idThreads[ _POSIX_THREAD_THREADS_MAX ];		//64
pthread_mutex_t	Mutex		= PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t	CountLock	= PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t	NextIter	= PTHREAD_COND_INITIALIZER;

struct thread_data thread_data_arry[ _POSIX_THREAD_THREADS_MAX ];//64

void GetParam( int argc, char **argv ) {

	int opt;
	int seed;
	int i;
	int j;

	extern char *optarg;
	extern int optopt;

	// default seed
	srand( 88 );

	// get command line input
	while(( opt = getopt( argc, argv, "hf:N:M:S:V" )) != -1 ) {

		switch( opt ) {

			// leave help information here
			case 'h':
				break;

			case 'V':

				vFlag = 1;	// verification: X=1,2,...
				break;

			case 'f':		// needed to run testfile

				printf( "Take input file: %s\n", *optarg );
				break;

			case 'N':

				N = atoi( optarg );

				if( N < 1 || N > MAXN ) {

					printf( "N=%d is out of range.\n", N );
					exit( 0 );
				}

				printf( "\nMatrix size: N=%d; ", N );
				break;

			case 'M':

				M = atoi( optarg );

				if( M < 1 ) {

					printf( "Invalid # of threads=%d. M=1.\n", M );
					M = 1;

				} else if( M > _POSIX_THREAD_THREADS_MAX ) {

					printf( "%d threads requested; only %d available.\n", M, _POSIX_THREAD_THREADS_MAX );
					M = _POSIX_THREAD_THREADS_MAX;
				}

				printf( "# of Threads: M=%d \n", M );
				break;

			case 'S':

				seed = atoi( optarg );
				srand( seed );

				break;

			case ':':

				fprintf( stderr, "Err:option`%c' needs a value\n", optopt );
				break;

			default: 

				fprintf( stderr, "Err: no such option:`%c'\n", optopt );
		}
	}

	// initilize matrix
	printf( "\nInitializing ...N=%d \n", N );

	matA = (double*) malloc( sizeof( double ) * N * ( N )); 
	matB = (double*) malloc( sizeof( double ) * N * ( N )); 
	matX = (double*) malloc( sizeof( double ) * N * ( N )); 
	rowA = (double**) malloc( sizeof( double* ) * ( N ));
	colB = (double**) malloc( sizeof( double* ) * ( N ));
	rowX = (double**) malloc( sizeof( double* ) * ( N ));

	if( vFlag != 1 ) {

		for( j = 0; j < N; j++ ) {	// generate matrix A & B
			
			rowA[ j ] = matA + j * N;
			colB[ j ] = matB + j * N;
			rowX[ j ] = matX + j * N;

			for ( i = 0; i < N; i++ ) {

				rowA[ j ][ i ] = (double) rand() / RAND_MAX + 1;
				colB[ j ][ i ] = (double) rand() / RAND_MAX + 1;
			}
		}

	} else {

		for( j = 0; j < N; j++ ) {	// generate matrix A & B

			rowA[ j ] = matA + j * N;
			colB[ j ] = matB + j * N;
			rowX[ j ] = matX + j * N;

			if( j == 0 ) {

				for( i = 0; i < N; i++ ) {

					rowA[ j ][ i ] = (double) rand() / RAND_MAX + 1;
				}
			}
			
			for( i = 0; i < N; i++ ) {

				rowX[ j ][ i ] = i + j + 1;
			}
		}

		for( j = 0; j < N; j++ ) {	// generate matrix B

			for( i = 0; i < N; i++ ) {

				colB[ j ][ i ] = rowX[ 0 ][ j ] / N / rowA[ 0 ][ i ];
			}
		}

		for( j = 1; j < N; j++ ) {	// generate matrix A 

			for( i = 0; i < N; i++ ) {

				rowA[ j ][ i ] = rowX[ j ][ j ] / colB[ j ][ i ] / N;	///(0.0+N);
			}
		}
	}

	// print matrix if not too large
	if( N < MAXN4print ) {

		printf( "\nPrinting ... (if matrix is not too large)\n" );
		printf( "A = \n" );

		for( i = 0; i < N; i++ ) {

			printf( "A[%d]= ", i );

			for( j = 0; j < N; j++ ) {

				printf( "%6.3f%s", rowA[ i ][ j ], ( j % 5 != 4 ) ? "," : ",\n   " );
			}
			
			printf( "\n" );
		}

		printf( "B = \n" );

		for( i = 0; i < N; i++ ) {

			printf( "B[%d]= ", i );

			for( j = 0; j < N; j++ ) {

				printf( "%6.3f%s", colB[ j ][ i ], ( j % 5 != 4 ) ? "," : ",\n   " );
			}

			printf( "\n" );
		}

		printf( "X = \n" );

		for( i = 0; i < N; i++ ) {

			printf( "X[%d]= ", i );

			for( j = 0; j < N; j++ ) {

				printf( "%6.3f%s", rowX[ i ][ j ], ( j % 5 != 4 ) ? "," : ",\n   " );
			}

			printf( "\n" );
		}
	}
}

void PrintX( void ) {

	int i;
	int j;

	printf( "\nX =  \n" );

	for( i = 0; i < N; i++ ) {

		printf( "X[%d]=", i );

		for( j = 0; j < N; j++ ) {

			printf( "%6.3f%s", rowX[ i ][ j ], ( j % 5 != 4 ) ? "," : ",\n   " );
		}

		printf( "\n" );
	}
}

void CheckX( void ) {

	int right = 1;
	int j;
	double w;
	
	// verify row 0
	for( j = 0; j < N; j++ ) {

		if( w = fabs( rowX[ 0 ][ j ] - ( 0 + j + 1 )) > .1 ) {

			printf( "X[0,%d]=%f fabs %f \n", j, rowX[ 0 ][ j ], w );
			right = 0;
		}
	}

	// verify diag i,i
	for( j = 0; j < N; j++ ) {

		if( w = fabs( rowX[ j ][ j ] - ( j + j + 1 )) > .1 ) {

			printf( "X[%d,%d]=%f fabs %f\n", j, j, rowX[ j ][ j ], w );
			right = 0;
		}
	}
	
	if( right == 1 ) {

		printf( "\nPartial verification passed!\n\n" );

	} else {

		printf( "\nFail to pass verification.\n\n" );
	}
}

void *rowMcol( void *arg ) {

	int i;
	int j;
	int col;

	struct thread_data *my_data = (struct thread_data *) arg;
	int b = my_data->b;
	long lThreadID = my_data->thread_id;

	int startIndex = (lThreadID * N) / M;
	int endIndex = ((lThreadID + 1) * N ) / M;

	printf( "\tHello, it's me ... thread #%d! My task is: startIndex=%d, endIndex=%d\n", lThreadID, startIndex, endIndex );

	for( i = startIndex; i < endIndex; i++ ) {

		// computer colX[i][col] 
		for( col = 0; col < N; col++ ) {

			rowX[ i ][ col ] = 0.0;

			for( j = 0; j < N; j++ ) {

				rowX[ i ][ col ] += rowA[ i ][ j ] * colB[ col ][ j ];
			}
		}
	}

	return 0;
}

// MAIN routine
main( int argc, char **argv ) {

	// Elapsed times using <times()>
	clock_t clkStart;
	clock_t clkStop;

	// CPU times for the threads
	struct tms tStart;
	struct tms tStop;

	int k;
	int i;
	int j;
	int temp;

	double max;

	vFlag = 0;
	GetParam( argc, argv );

	printf( "Starting timing ... computing ...\n" );
	clkStart = times( &tStart );

	long threadCounter;
	for( threadCounter = 0; threadCounter < M; threadCounter++ ) {
	
		thread_data_arry[ threadCounter ].i = 0;
		thread_data_arry[ threadCounter ].b = N;
		thread_data_arry[ threadCounter ].thread_id = threadCounter;
		
		printf( "\tmain: creating thread %ld\n", threadCounter );
		
		int threadReturnCode = pthread_create( &idThreads[ threadCounter ], NULL, rowMcol, (void *) &thread_data_arry[ threadCounter ]);
		
		if( threadReturnCode ) {
		
			printf( "ERROR; return code from pthread_create() is %d\n", threadReturnCode );
			
			exit( -1 );
		}
	}

	printf( "\tcompleted thread creation ... going to try to join all threads!\n" );

	// for loop processes until all threads terminate
	for( threadCounter = 0; threadCounter < M; threadCounter++ ) {

		pthread_join( idThreads[ threadCounter ], NULL );
	}

	printf( "\tall threads have terminated!\n" );
	clkStop = times( &tStop );
	printf( "Stopped timing.\n" );

	if( N < MAXN4print ) {

		PrintX();
	}

	if( vFlag == 1 ) {

		CheckX();
	}

	printf( "Elapsed time = %g ms.\n",  (float)( clkStop - clkStart ) / (float) sysconf( _SC_CLK_TCK ) * 1000 );
	printf( "The total CPU time comsumed = %g ms.\n", (float)(( tStop.tms_utime - tStart.tms_utime ) + ( tStop.tms_stime - tStart.tms_stime )) / (float)sysconf( _SC_CLK_TCK ) * 1000 );

	// Last thing that main() should do
	pthread_exit( NULL );

	return 0;
}
