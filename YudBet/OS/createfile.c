#include "pch.h"
#include <stdio.h>

LPCSTR lpFileName = "F:\\ami.txt";

DWORD dwDesiredAccess = GENERIC_READ | GENERIC_WRITE;

DWORD dwShareMode = 0;

LPSECURITY_ATTRIBUTES lpSecurityAttributes = NULL;

DWORD dwCreationDisposition = OPEN_EXISTING;

DWORD dwFlagsAndAttributes = FILE_ATTRIBUTE_NORMAL;

HANDLE hTemplateFile = NULL;

int main()
{
	HANDLE hFile = CreateFileA(lpFileName, dwDesiredAccess, dwShareMode, lpSecurityAttributes, dwCreationDisposition, dwFlagsAndAttributes, hTemplateFile);

	LPVOID lpBuffer[9];

	LPDWORD lpNumberOfBytesRead = NULL;

	DWORD nNumberOfBytesToRead = 8;

	LPOVERLAPPED lpOverlapped = NULL;

	BOOL retncode = ReadFile(hFile, lpBuffer, nNumberOfBytesToRead, lpNumberOfBytesRead, lpOverlapped);

	if (retncode == TRUE)
	{
		((LPSTR)lpBuffer)[8] = 0;
		printf("%s\n", (LPSTR)lpBuffer);

	}



	retncode = CloseHandle(hFile);

	printf("Return code: %d", retncode);

	char s;

	scanf_s("%c", &s);

	return 0;

}
