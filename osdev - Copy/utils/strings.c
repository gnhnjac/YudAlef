#include "strings.h"

void num_to_str(int n, char *buffer, int base)
{
	char digits[] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};

	int neg = 0;
	if (n < 0)
	{
		n = -n;
		neg = 1;
	}
	int temp_n = n;
	int n_of_digits = 0;
	do
	{

		n_of_digits++;
		temp_n /= base;

	} while (temp_n);

	int i = 0;
	if (neg)
	{
		n_of_digits += 1;
		buffer[0] = '-';
	}
	do
	{	

		int digit = digits[n%base];
		*(buffer + n_of_digits - 1 - i) = digit;
		i++;
		n /= base;

	} while(n);

	buffer[n_of_digits] = 0;

}

int strlen(char *str)
{
	int len = 0;
	while (*str++)
	{

		len++;
	}

	return len;

}