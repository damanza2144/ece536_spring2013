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

// given A and B (both N x N), compute  X = A x B.            
int N;  	// matrix size
int M;  	// number of threads, must >=1
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
pthread_t		idThreads[ _POSIX_THREAD_THREADS_MAX ];
pthread_mutex_t	Mutex		= PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t	CountLock	= PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t	NextIter	= PTHREAD_COND_INITIALIZER;

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
	int *pK = (int*) arg;
	int k = *pK;
	int b = *( pK + 1 );

	double multiplier;

	printf( "*rowMcol ...\n" );
	printf( "i=%d, k=%d, b=%d, N=%d\n", i, k, b, N );
	
	// Actual N inner product for row k happen here.
	//do multiple times, b 
	for( i = k; i < ( k + b ) && i < N; i++ ) {

		//computer colX[i][col] 
		for( col = 0; col < N; col++ ) {

			rowX[ i ][ col ] = 0.0;

			for( j = 0; j < N; j++ ) {

				rowX[ i ][ col ] += rowA[ i ][ j ] * colB[ col ][ j ];
				//printf( "rowX[%d][%d]=%d\n", i, col, rowX[i][col] );
			}
		}
	}
}

// MAIN routine
main( int argc, char **argv ) {

	//Elapsed times using <times()>
	clock_t clkStart;
	clock_t clkStop;

	//CPU times for the threads
	struct tms tStart;
	struct tms tStop;

	int k;
	int i;
	int j;
	int temp;
	int param[ 2 ];

	double max;

	vFlag = 0;
	GetParam( argc, argv );

	printf( "Starting timing ... computing ...\n" );
	clkStart = times( &tStart );

	param[ 0 ] = 0;
	param[ 1 ] = N;
	rowMcol( param );

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
}
