#include <stdio.h>

int main(int argc, char* argv[])
{
	if (argc != 2) {
		printf("Incorrect number of arguments\n");
		return 0;
	}
	int id = atoi(argv[1]);
	printf("Hello World! Process got argument %d\n", id);
	return 1;
}