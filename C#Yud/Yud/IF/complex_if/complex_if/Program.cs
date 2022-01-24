using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Remoting.Metadata.W3cXsd2001;
using System.Text;
using System.Threading.Tasks;

namespace complex_if
{
    class Program
    {

        static Random rnd = new Random();

        static void ex1()
        {

            Console.WriteLine("Enter student grade:");

            int grade = int.Parse(Console.ReadLine());

            if(grade >= 90)
            {

                Console.WriteLine("Great");

            }
            else if(grade >= 65 && grade <= 89)
            {

                Console.WriteLine("OK");

            }
            else
            {

                Console.WriteLine("Not so good");

                Console.WriteLine("Enter previous test's grade:");

                int pre_grade = int.Parse(Console.ReadLine());

                Console.WriteLine("Average: " + (grade + pre_grade) / 2.0);

            }

        }

        static void ex3()
        {

            Console.WriteLine("Amount of gas used:");

            int liters = int.Parse(Console.ReadLine());

            double pay;

            if(liters <= 5)
            {

                pay = liters * 10 * 1.18;

                Console.WriteLine("Payment: " + pay);

            }
            else
            {

                pay = (50 + (liters - 5) * 7) * 1.18;

                Console.WriteLine("Payment: " + pay);

            }

            Console.WriteLine($"Average payment per liter: " + pay / liters);

        }

        static void ex5()
        {

            Console.WriteLine("Enter a number between 1-100:");

            int num = int.Parse(Console.ReadLine());

            if(num > 100 || num < 0)
            {

                Console.WriteLine("ERROR");
                Environment.Exit(0);

            }

            if(num % 7 == 0 || num % 10 == 7 || num / 10 % 10 == 7)
            {

                Console.WriteLine("BOOM");

            }
            else
            {

                Console.WriteLine("OOPS");

            }

        }

        static void ex6()
        {

            int digit = rnd.Next(9999);

            Console.WriteLine(digit);

            if(digit < 10)
            {

                Console.WriteLine("1 digit");

            }
            else if(digit < 100)
            {

                Console.WriteLine("2 digit");

            }
            else if (digit < 1000)
            {

                Console.WriteLine("3 digit");

            }
            else if (digit < 10000)
            {

                Console.WriteLine("4 digit");

            }


        }

        static void ex7()
        {

            Console.WriteLine("Enter sign (spade/heart/diamond/club):");

            string sign = Console.ReadLine();

            if(sign != "spade" && sign != "heart" && sign != "diamond" && sign != "club")
            {

                Console.WriteLine("Sign doesn't exist.");
                Environment.Exit(0);

            }

            int num = rnd.Next(2, 14);

            if(num >= 2 && num <= 10)
            {

                Console.WriteLine($"{num} of {sign}s");

            }
            else if(num == 11)
            {

                Console.WriteLine($"Prince of {sign}s");

            }
            else if(num == 12)
            {

                Console.WriteLine($"Queen of {sign}s");

            }
            else if (num == 13)
            {

                Console.WriteLine($"King of {sign}s");

            }
            else if (num == 14)
            {

                Console.WriteLine($"Ace of {sign}s");

            }

        }

        static void ex8()
        {

            int currentYear = DateTime.Now.Year;

            int year = rnd.Next(currentYear);

            if((year % 4 == 0 && year % 100 != 0) || year % 400 == 0)
            {

                Console.WriteLine($"{year} is a leap year");

            }
            else
            {

                Console.WriteLine($"{year} isn't a leap year");

            }

        }

        static void ex9()
        {

            int dice1 = rnd.Next(1, 6);

            int dice2 = rnd.Next(1, 6);

            Console.WriteLine($"{dice1} {dice2}");

            if(dice1 == dice2)
            {

                Console.WriteLine("It's a double!");

            }
            else
            {

                Console.WriteLine("The game continues.");

            }

        }

        static void ex10()
        {

            Console.WriteLine("Name of kid:");

            string name = Console.ReadLine();

            Console.WriteLine("Amount of classes:");

            int classes = int.Parse(Console.ReadLine());

            Console.WriteLine($"{name}'s Payment: {classes*100}");

            if(classes > 5)
            {

                Console.WriteLine($"{name} gets a gift!");

            }

        }

        static void Main(string[] args)
        {

            // ex1();
            // ex3();
            // ex5();
            // ex6();
            // ex7();
            // ex8();
            // ex9();
            // ex10();

        }
    }
}
