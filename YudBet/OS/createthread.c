#include "pch.h"
#include <stdio.h>

struct params
{

	INT p1;
	INT p2;

};

DWORD WINAPI bla(LPVOID lparam) {
	struct params* parameters = (struct params*)lparam;
	INT tot = parameters->p1 + parameters->p2;
	for (INT i = 1; i <= tot; i++) {
		printf("bla\n");
	}

	Sleep(1000 * 10);

	return 1;
}

int main()
{
	struct params* lparam = (struct params*)malloc(sizeof(struct params));
	lparam->p1 = 2;
	lparam->p2 = 3;

	HANDLE hThread = CreateThread(NULL, 0, bla, lparam, 0, NULL);

	WaitForSingleObject(hThread, INFINITE);

	free(lparam);
}
