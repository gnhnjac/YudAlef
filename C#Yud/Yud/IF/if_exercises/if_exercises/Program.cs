using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace if_exercises
{
    class Program
    {

        static void ex_math()
        {

            Console.WriteLine("A: ");

            int a = int.Parse(Console.ReadLine());

            Console.WriteLine("B: ");

            int b = int.Parse(Console.ReadLine());

            Console.WriteLine("C: ");

            int c = int.Parse(Console.ReadLine());

            if (Math.Pow(b, 2) - 4 * a * c < 0)
            {

                Console.WriteLine("Answer not on the real number plane");

            }
            else
            {

                double x1 = (-b + Math.Sqrt(Math.Pow(b, 2) - 4 * a * c)) / (a * 2);

                double x2 = (-b - Math.Sqrt(Math.Pow(b, 2) - 4 * a * c)) / (a * 2);

                Console.WriteLine($"x1: {x1}, x2: {x2}");

            }

        }

        static void ex_1()
        {

            Console.WriteLine("Enter a whole number: ");

            int num = int.Parse(Console.ReadLine());

            if(num > 100)
            {

                Console.WriteLine("Big");

            }

        }

        static void ex_2()
        {

            Console.WriteLine("Enter a whole number: ");

            int num = int.Parse(Console.ReadLine());

            if(num > 7)
            {

                Console.WriteLine("A lot");

            }
            else if(num < 7)
            {

                Console.WriteLine("A little");

            }
            else
            {

                Console.WriteLine("Bingo!");

            }

        }

        static void ex_3()
        {

            Console.WriteLine("Enter a whole number: ");

            int num = int.Parse(Console.ReadLine());

            if(num > 0)
            {

                Console.WriteLine("Positive");

            }
            else if(num < 0)
            {

                Console.WriteLine("Negative");

            }
            else
            {

                Console.WriteLine("Zero");

            }

        }

        static void ex_4()
        {

            Console.WriteLine("Enter 1st whole number: ");

            int num1 = int.Parse(Console.ReadLine());
            
            Console.WriteLine("Enter 2nd whole number: ");

            int num2 = int.Parse(Console.ReadLine());

            if(num1 > num2)
            {

                Console.WriteLine("First number is bigger");

            }
            else if(num2 > num1)
            {

                Console.WriteLine("Second number is bigger");

            }
            else
            {

                Console.WriteLine("Numbers are the same");

            }
        }

        static void ex_5()
        {

            Console.WriteLine("Enter 1st number: ");

            double num1 = double.Parse(Console.ReadLine());

            Console.WriteLine("Enter 2nd number: ");

            double num2 = double.Parse(Console.ReadLine());

            Console.WriteLine($"Big: {Math.Max(num1, num2)}, Small: {Math.Min(num1, num2)}");

        }

        static void ex_6()
        {

            Console.WriteLine("Enter a whole number: ");

            int num = int.Parse(Console.ReadLine());

            if(num/100 == 0 && num/10 != 0)
            {

                Console.WriteLine(num * 10);

            }

        }

        static void ex_7()
        {

            Console.WriteLine("Num 1: ");

            int n1 = int.Parse(Console.ReadLine());

            Console.WriteLine("Num 2: ");

            int n2 = int.Parse(Console.ReadLine());
            
            Console.WriteLine("Num 3: ");

            int n3 = int.Parse(Console.ReadLine());

            Console.WriteLine("Biggest: " + Math.Max(n1, Math.Max(n2, n3)));
        
        }

        static void ex_8()
        {

            Console.WriteLine("Triple digit number: ");

            int num = int.Parse(Console.ReadLine());

            if(num/10%10 == (num/100 + num%10)/2 && num/100 == Math.Sqrt(num%10))
            {

                Console.WriteLine("YES");

            }
            else
            {

                Console.WriteLine("NO");

            }

        }

        static void Main(string[] args)
        {

            // ex_math();
            // ex_1();
            // ex_2();
            // ex_3();
            // ex_4();
            // ex_5();
            // ex_6();
            // ex_7();
            // ex_8();

        }
    }
}
