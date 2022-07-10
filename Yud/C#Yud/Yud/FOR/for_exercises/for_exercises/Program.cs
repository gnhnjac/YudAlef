using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace for_exercises
{
    class Program
    {

        static int factorial(int n)
        {

            if (n == 0)
                return 1;

            int num = 1;

            for(int i = 1; i <= n; i++)
            {

                num *= i;

            }

            return num;

        }

        static void pascal()
        {

            Console.WriteLine("Triangle height: ");

            int height = int.Parse(Console.ReadLine());

            for (int i = 0; i < height; i++)
            {

                String text = "|";

                for (int j = 0; j <= i; j++)
                {

                    text += factorial(i) / (factorial(j) * factorial(i - j));

                    if (j != i)
                        text += "| |";

                }

                text += "|";

                Console.Write(new string(' ', (Console.WindowWidth - text.Length) / 2));

                Console.WriteLine(text);

            }

        }

        static void diamond()
        {


            Console.WriteLine("Enter odd height: ");
            int height = int.Parse(Console.ReadLine());

            while (height % 2 == 0)
            {

                Console.WriteLine("Enter odd height: ");
                height = int.Parse(Console.ReadLine());

            }

            for (int i = -height / 2; i < Math.Ceiling(height / 2.0); i++)
            {

                Console.Write(new String(' ', Math.Abs(i)));

                Console.WriteLine(new String('*', ((height / 2 - Math.Abs(i) + 1) + (height / 2 - Math.Abs(i)))));

            }

        }

        static void extra_ex1()
        {

            Console.WriteLine("Enter a whole number: ");

            int num = int.Parse(Console.ReadLine());

            Console.WriteLine("Divisors: ");

            for(int i = 1; i <= num; i++)
            {

                if (((double)num / i) % 1 == 0)
                {

                    Console.WriteLine(i);

                }

            }

        }

        static void extra_ex2()
        {

            Console.WriteLine("Enter a whole number: ");
            int num = int.Parse(Console.ReadLine());

            int sum = 0;

            for (int i = 1; i < num; i++)
            {

                if (((double)num / i) % 1 == 0)
                {

                    sum += i;

                }

            }

            if (sum == num)
            {

                Console.WriteLine($"{num} is a perfect number.");

            }
            else
            {

                Console.WriteLine($"{num} is not a perfect number.");

            }

        }

        static void extra_ex3()
        {

            Console.WriteLine("Enter prime number: ");

            int prime = int.Parse(Console.ReadLine());

            for (int i = 2; i < prime; i++)
            {

                if (((double)prime / i) % 1 == 0)
                {

                    Console.WriteLine("Number not prime.");
                    return;

                }

            }

            Console.WriteLine("Number is prime.");

        }

        static void ex1()
        {

            for (int i = 1; i <= 200; i++)
            {

                Console.WriteLine(i);

                if (i % 8 == 0)
                    Console.WriteLine("Good.");

            }

        }

        static void ex2()
        {

            Console.WriteLine("Enter number: ");

            int num = int.Parse(Console.ReadLine());

            Console.WriteLine("Enter number: ");

            int num2 = int.Parse(Console.ReadLine());

            for (int i = num + 1; i < num2; i++)
                Console.WriteLine(i);

        }

        static void ex3()
        {

            for (int i = 10; i <= 60; i += 5)
                Console.WriteLine(i);

        }

        static void ex4()
        {

            for (int i = 0; i < 10; i++)
                Console.Write("Ami ");

            for (int i = 0; i < 10; i++)
                Console.WriteLine("Ami");

        }

        static void ex5()
        {

            for(int i = 5; i <= 50; i ++)
                    Console.WriteLine(i + ", Squared: " + i*i);

        }

        static void ex6()
        {

            for (int i = 1; i <= 100; i++)
                Console.WriteLine($"1/{i}");

        }

        static void ex7()
        {

            for (int i = 0; i < 100; i++)
            {

                Console.WriteLine("Enter num: ");
                int num1 = int.Parse(Console.ReadLine());

                Console.WriteLine("Enter num: ");
                int num2 = int.Parse(Console.ReadLine());

                Console.WriteLine("Enter num: ");
                int num3 = int.Parse(Console.ReadLine());

                int avg = (num1 + num2 + num3) / 3;

                Console.WriteLine("Average: " + avg);

                if(avg == num2)
                {

                    Console.WriteLine("Yes.");

                }
                else
                {

                    Console.WriteLine("No.");

                }

            }

        }

        static void ex8()
        {

            Console.WriteLine("Enter character: ");

            char c = char.Parse(Console.ReadLine());

            Console.WriteLine("Enter num: ");

            int num = int.Parse(Console.ReadLine());

            for (int i = 0; i < num; i++)
                Console.WriteLine(c);

        }

        static void ex9()
        {

            Console.WriteLine("Number of families: ");

            int families = int.Parse(Console.ReadLine());

            for(int i = 0; i < families; i++)
            {

                Console.WriteLine("Number of boys: ");

                int boys = int.Parse(Console.ReadLine());

                Console.WriteLine("Number of girls: ");

                int girls = int.Parse(Console.ReadLine());

                if (boys == girls)
                    Console.WriteLine("Boys and girls are equal in this family!");

            }

        }

        static void ex10()
        {
               
            for(int i = 0; i < 5; i++)
            {

                Console.WriteLine("Enter num:");

                int num = int.Parse(Console.ReadLine());

                Console.WriteLine(num + " " + num % 10);

                if (num % 2 == 0)
                    Console.WriteLine("Even.");

            }
         
        }

        static void Main(string[] args)
        {

            // pascal();
            // diamond();

            // extra_ex1();
            // extra_ex2();
            // extra_ex3();

            /* extra_ex4:
            
            Task 1: 16 10

            Task 2: 27 27

            Task 3: 27 40

             */

            // ex1();
            // ex2();
            // ex3();
            // ex4();
            // ex5();
            // ex6();
            // ex7();
            // ex8();
            // ex9();
            // ex10();

        }
    }
}
