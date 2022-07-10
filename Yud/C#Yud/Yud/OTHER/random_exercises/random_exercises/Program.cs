using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace random_exercises
{

    class Program
    {

        static Random rnd = new Random();

        static void ex_1()
        {

            int num = rnd.Next(1, 100);

            Console.WriteLine("Guess the number: ");

            int guess = int.Parse(Console.ReadLine());

            if (guess == num)
            {

                Console.WriteLine("Correct!!!");

            }
            else if (guess > num)
            {

                Console.WriteLine("Sorry, too big");

            }
            else if (guess < num)
            {

                Console.WriteLine("Sorry, too small");

            }

            Console.WriteLine("Goodbye");


        }

        static void ex_2()
        {

            int n1 = rnd.Next(1, 100);

            int n2 = rnd.Next(1, 100);

            int operation = rnd.Next(2);

            double ans;
            double user_ans;

            if(operation == 0)
            {

                Console.Write($"{n1} + {n2} = ");

                user_ans = double.Parse(Console.ReadLine());

                ans = n1 + n2;

            }
            else if(operation == 2)
            {

                Console.Write($"{n1} - {n2} = ");

                user_ans = double.Parse(Console.ReadLine());

                ans = n1 - n2;

            }
            else
            {

                Console.Write($"{n1} * {n2} = ");

                user_ans = double.Parse(Console.ReadLine());

                ans = n1 * n2;

            }

            if(ans == user_ans)
            {

                Console.WriteLine("Correct!");

            }
            else
            {

                Console.WriteLine("Wrong, the correct answer was " + ans);

            }

        }

        static void Main(string[] args)
        {

            // ex_1();

            ex_2();

        }
    }
}
