#include "strings.h"

void int_to_dec(int n, char *buffer)
{
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
		temp_n /= 10;

	} while (temp_n);

	int i = 0;
	if (neg)
	{
		n_of_digits += 1;
		buffer[0] = '-';
	}
	do
	{	

		int digit = n % 10 + '0';
		*(buffer + n_of_digits - 1 - i) = digit;
		i++;
		n /= 10;

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