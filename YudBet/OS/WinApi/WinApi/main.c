#include "pch.h"
#include <stdio.h>
#define THREADS 4

DWORD WINAPI bla(LPVOID ptid) {
	INT tid = *(LPINT)ptid;

	for (INT i = 0; i < 1000; i++)
	{

		printf("Thread %d, var = %d\n", tid, i);

	}


	return 1;
}

int main()
{

	HANDLE lpHandles[THREADS];
	INT tids[THREADS];

	for (INT i = 0; i < THREADS; i++)
	{
		tids[i] = i;

		lpHandles[i] = CreateThread(NULL, 0, bla, tids + i, 0, NULL);
	}
	WaitForMultipleObjects(THREADS, lpHandles, TRUE, INFINITE);

}
