using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Test
{
    class Program
    {
        static void Main(string[] args)
        {

            int[] numbers = new int[10];

            int digit = 18515;

            Console.WriteLine(digit);

            while (digit > 0)
            {

                int num = digit % 10;

                numbers[num]++;

                digit /= 10;


            }

            for (int i = 0; i < numbers.Length; i++)
            {
                if(numbers[i] > 0)
                {

                    Console.WriteLine($"The number {i} appears: {numbers[i]} times");

                }

            }


        }
    }
}
