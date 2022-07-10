using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace complex_while
{
    class Program
    {

        static void ex1()
        {

            Console.WriteLine("Enter a whole positive number: ");

            int num = int.Parse(Console.ReadLine());

            int sum = 0;

            while (num > 0)
            {

                Console.WriteLine(num % 10);

                sum += num % 10;

                num /= 10;

            }

            Console.WriteLine("Sum of digits: " + sum);

        }

        static void ex2()
        {

            Console.WriteLine("Enter a whole positive number: ");

            int num = int.Parse(Console.ReadLine());

            Console.WriteLine("Enter a digit: ");

            int digit = int.Parse(Console.ReadLine());

            int i = 1;

            while (num > 0)
            {

                if (i == digit)
                {

                    Console.WriteLine(num % 10);
                    return;

                }

                num /= 10;

                i++;

            }

            Console.WriteLine(-1);

        }

        static void ex3()
        {

            Console.WriteLine("Enter a whole positive number: ");

            int num = int.Parse(Console.ReadLine());

            while (num / 10 > 0)
            {

                if (num % 10 != num / 10 % 10)
                {

                    Console.WriteLine("DIFFERENT");
                    return;

                }

                num /= 10;

            }

            Console.WriteLine("ALL EQUAL");

        }

        static void ex4()
        {

            Console.WriteLine("Enter natural number: ");

            int natural = int.Parse(Console.ReadLine());

            if (natural <= 0)
            {

                Console.WriteLine("Number not natural.");
                return;

            }

            Console.WriteLine("Enter natural digit: ");

            int n_digit = int.Parse(Console.ReadLine());

            if (n_digit <= 0)
            {

                Console.WriteLine("Digit not natural.");
                return;

            }

            int occurunces = 0;

            while (natural > 0)
            {

                if (natural % 10 == n_digit)
                    occurunces++;

                natural /= 10;

            }

            Console.WriteLine("Digit occurunces in number: " + occurunces);


        }

        static void ex5()
        {

            Console.WriteLine("Enter whole positive number: ");

            int num = int.Parse(Console.ReadLine());

            int biggest = 0;
            int index = 0;

            int i = 0;

            while (num > 0)
            {

                if (num % 10 > biggest)
                {

                    biggest = num % 10;
                    index = i;

                }

                num /= 10;

                i++;

            }

            Console.WriteLine("Biggest digit index: " + (index + 1));

        }

        static void ex5b()
        {

            Random rnd = new Random();

            int biggest_index_number = 0;
            int biggest_index = 0;

            for (int i = 0; i < 10; i++)
            {

                int num = rnd.Next(100, 10000);
                int n_copy = num;

                int biggest = 0;
                int index = 0;

                int j = 0;

                while (num > 0)
                {

                    if (num % 10 > biggest)
                    {

                        biggest = num % 10;
                        index = j;

                    }

                    num /= 10;

                    j++;

                }

                Console.WriteLine("Biggest digit index: " + (index + 1));

                if (index > biggest_index)
                {

                    biggest_index = index;
                    biggest_index_number = n_copy;

                }

            }

            Console.WriteLine("Number with biggest biggest index: " + biggest_index_number);

        }

        static void ex6()
        {

            Console.WriteLine("Enter whole number: ");
            int num = int.Parse(Console.ReadLine());

            int multiplier = 1;
            int n_copy = num;
            while (n_copy/10 > 0)
            {

                multiplier *= 10;

                n_copy /= 10;

            }

            int new_num = 0;

            new_num += num % 10 * multiplier;

            num /= 10;

            multiplier = 1;

            while (num > 0)
            {

                new_num += num % 10 * multiplier;

                multiplier *= 10;

                num /= 10;

            }

            Console.WriteLine(new_num);

        }

        static void ex6b()
        {

            Random rnd = new Random();

            for(int i = 0; i < 10; i++)
            {

                int num = rnd.Next(45, 139);

                int multiplier = 1;
                int n_copy = num;
                while (n_copy / 10 > 0)
                {

                    multiplier *= 10;

                    n_copy /= 10;

                }
                n_copy = num;

                int new_num = 0;

                new_num += num % 10 * multiplier;

                num /= 10;

                multiplier = 1;

                while (num > 0)
                {

                    new_num += num % 10 * multiplier;

                    multiplier *= 10;

                    num /= 10;

                }

                Console.WriteLine("Before: " + n_copy);

                Console.WriteLine("After: " + new_num);

            }

        }

        static void Main(string[] args)
        {

            // ex1();
            // ex2();
            // ex3();
            // ex4();
            // ex5();
            // ex5b();
             ex6();
            // ex6b();
        }
    }
}
