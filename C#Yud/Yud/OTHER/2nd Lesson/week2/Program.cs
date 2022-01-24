using System;
using System.Transactions;

namespace week2
{
    class Program
    {

        static void ex3_1()
        {

            Console.WriteLine("2 digit number: ");

            String number = Console.ReadLine();

            while(number.Length != 2)
            {

                Console.WriteLine("2 digit number: ");
                number = Console.ReadLine();

            }

            Console.WriteLine("Sum of digits: " + (int.Parse(number)/10 + int.Parse(number) % 10));

        }

        static void ex3_2()
        {

            Console.WriteLine("3 digit number: ");

            String number = Console.ReadLine();

            while(number.Length != 3)
            {

                Console.WriteLine("3 digit number: ");
                number = Console.ReadLine();

            }

            int hundreds = int.Parse(number) / 100;

            int tens = int.Parse(number) / 10 % 10;

            int ones = int.Parse(number) % 10;

            Console.WriteLine("Hundreds: " + hundreds);
            Console.WriteLine("Tens: " + tens);
            Console.WriteLine("Ones: " + ones);

            Console.WriteLine("Digit multiplication: " + hundreds * tens * ones);

        }

        static void ex3_3()
        {

            Console.WriteLine("2 digit number: ");

            String number = Console.ReadLine();

            while (number.Length != 2)
            {

                Console.WriteLine("2 digit number: ");
                number = Console.ReadLine();

            }

            Console.WriteLine("Reverse number: "  + int.Parse(number) % 10 + int.Parse(number) / 10);

        }

        static void ex3_4()
        {

            Console.WriteLine("Time in seconds: ");

            int total_seconds = int.Parse(Console.ReadLine());

            int seconds = total_seconds % 60;

            int minutes = total_seconds / 60 % 60;

            int hours = total_seconds / 60 / 60;

            Console.WriteLine($"{hours.ToString("D2")}:{minutes.ToString("D2")}:{seconds.ToString("D2")}");

        }

        static void ex3_5()
        {

            Console.WriteLine("People waiting for taxis: ");

            int people = int.Parse(Console.ReadLine());

            Console.WriteLine("People left behind: " + people % 6);

            Console.WriteLine("Taxis that drove away: " + people / 6);

        }

        static void ex3_6()
        {

            Console.WriteLine("Children going for the trip: ");

            int children = int.Parse(Console.ReadLine());

            int buses = children / 46;

            if(children % 46 != 0)
            {

                buses++;

            }

            Console.WriteLine("Number of buses: " + buses);

        }

        static void ex3_7()
        {

            Console.WriteLine("Number of days: ");

            int days = int.Parse(Console.ReadLine());

            Console.WriteLine("Whole weeks: " + days / 7);

            Console.WriteLine("Days left until end of week: " + (7 - days % 7));

        }

        static void ex3_8()
        {

            Console.WriteLine("Money allocated for light changing: ");

            int allocated = int.Parse(Console.ReadLine());

            Console.WriteLine("Price of 1 light post: ");

            int price = int.Parse(Console.ReadLine());

            Console.WriteLine("Amount of light posts that can be changed: " + allocated / price);

            Console.WriteLine("Money left: " + allocated % price);

        }

        static void ex2_16()
        {

            Console.WriteLine("Enter 3 whole numbers: ");

            int n1 = int.Parse(Console.ReadLine());

            int n2 = int.Parse(Console.ReadLine());

            int n3 = int.Parse(Console.ReadLine());

            Console.WriteLine("Average: " + (n1 + n2 + n3) / 3);

        }

        static void ex2_17()
        {

            Console.WriteLine("Biggest brother age: ");

            int big_brother = int.Parse(Console.ReadLine());

            int small_brother = big_brother - 10;

            int small_sister = small_brother;

            int big_sister = small_sister + 3;

            Console.WriteLine("Big brother age: " + big_brother);

            Console.WriteLine("Small brother age: " + small_brother);

            Console.WriteLine($"Small sister age: {small_sister} minus a second");

            Console.WriteLine($"Second sister age: {big_sister} minus a second");

        }

        static void Main(string[] args)
        {
            // ex[presentation]_[exercise]

            //ex3_1();

            //ex3_2();

            //ex3_3();

            //ex3_4();

            //ex3_5();

            //ex3_6();

            //ex3_7();

            //ex3_8();

            //ex2_16();

            ex2_17();
        }
    }
}
