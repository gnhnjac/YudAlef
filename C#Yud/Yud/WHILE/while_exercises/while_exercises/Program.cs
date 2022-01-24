using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace while_exercises
{
    class Program
    {

        static void ex1()
        {

            int boysIsGirls = 0;

            int boys;
            int girls;

            do
            {

                Console.WriteLine("Number of boys: ");

                boys = int.Parse(Console.ReadLine());

                Console.WriteLine("Number of girls: ");

                girls = int.Parse(Console.ReadLine());

                if (boys == girls)
                    boysIsGirls++;

            } while (boys != -1 && girls != -1);

            Console.WriteLine($"Boys and girls were equal in {boysIsGirls} families");

        }

        static void ex2()
        {

            int num1;
            int num2;

            do
            {

                Console.WriteLine("Num 1: ");

                num1 = int.Parse(Console.ReadLine());

                Console.WriteLine("Num 2: ");

                num2 = int.Parse(Console.ReadLine());

                Console.WriteLine((num1 + num2) / 2);

            } while (num1 != 0 || num2 != 0);

        }

        static void ex3()
        {

            int onesBiggerHundrersSum = 0;

            int tensEvenHundredsNot = 0;

            while (true)
            {

                Console.WriteLine("Enter 3 digit number: ");

                int num = int.Parse(Console.ReadLine());

                if (num >= 1000 || num < 100)
                    break;

                if (num % 10 > num / 100 % 10)
                    onesBiggerHundrersSum += num;

                if (num / 10 % 2 == 0 && num / 100 % 2 == 1)
                    tensEvenHundredsNot++;

            }

            Console.WriteLine("Sum of ones bigger than hundreds numbers: " + onesBiggerHundrersSum);

            Console.WriteLine("Amount of numbers where tens is even and hundreds isn't: " + tensEvenHundredsNot);

        }

        static void ex4()
        {

            int num;

            do
            {

                Console.WriteLine("Enter 2 digit number.");

                num = int.Parse(Console.ReadLine());

                if (num / 10 == 0 || num / 10 >= 10)
                    break;

                if (num % 10 == num / 10 % 10 + 2)
                    Console.WriteLine(num);

            } while (true);

        }

        static void ex5()
        {

            int num;

            while (true)
            {

                Console.WriteLine("Enter whole number: ");

                num = int.Parse(Console.ReadLine());

                if (num == 0)
                    break;

                bool prime = true;

                for (int i = 2; i < num; i++)
                {

                    if (num % i == 0)
                    {

                        prime = false;
                        break;

                    }

                }

                if (prime)
                    Console.WriteLine("Number is prime.");

                else
                    Console.WriteLine("Number isn't prime.");

            }

        }

        static void ex6()
        {

            while (true)
            {

                Console.WriteLine("Enter a number: ");

                int num = int.Parse(Console.ReadLine());

                if (num == -1)
                    break;

                int sum = 0;
                int digits = 0;

                while (num > 0)
                {

                    sum += num % 10;

                    digits++;

                    num /= 10;

                }

                Console.WriteLine("Number of digits: " + digits);
                Console.WriteLine("Sum of digits: " + sum);
            }

        }

        static void ex7()
        {

            int noMudulo = 0;

            while (true)
            {

                Console.WriteLine("Enter whole positive number: ");

                int num = int.Parse(Console.ReadLine());

                if (num == -1)
                    break;

                if (num % 4 == 0 && num % 3 == 0)
                    noMudulo++;

            }

            Console.WriteLine("Numbers that share 4, 3 divisors: " + noMudulo);

        }

        static void ex8()
        {

            int num1;
            int num2;

            do
            {

                Console.WriteLine("Enter 3 digit number:");

                num1 = int.Parse(Console.ReadLine());

                Console.WriteLine("Enter 3 digit number: ");

                num2 = int.Parse(Console.ReadLine());

                if (num1 % 10 + num1 / 10 % 10 >= num2 % 10 + num2 / 10 % 10)
                    Console.WriteLine(num1);

                else
                    Console.WriteLine(num2);


            } while (num1 != 100 || num2 != 100);

        }

        static void ex9()
        {

            int nineties = 0;

            while (true)
            {

                Console.WriteLine("Enter whole number: ");

                int num = int.Parse(Console.ReadLine());

                if (num == 10)
                    break;

                if (num == 90)
                    nineties++;

            }

            Console.WriteLine($"There were {nineties} nineties");

        }

        static void ex10()
        {

            while (true)
            {

                Console.WriteLine("Enter 2 digit number: ");

                int num = int.Parse(Console.ReadLine());

                if (num == -10)
                    break;

                if (num % 10 % 5 == 0)
                    Console.WriteLine(num % 10 + 2);

                else
                    Console.WriteLine(num % 10);

            }

        }

        static void Main(string[] args)
        {

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
