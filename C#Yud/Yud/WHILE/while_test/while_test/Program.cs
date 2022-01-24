using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace while_test
{
    class Program
    {

        static void test_1()
        {

            Console.WriteLine("Enter natural number.");

            int num = int.Parse(Console.ReadLine());

            int new_num = 0;

            int num_copy = num;
            int mult = 1;

            while (num_copy / 10 > 0)
            {

                mult *= 10;

                num_copy /= 10;

            }

            num_copy = num;
            while (num_copy > 0)
            {

                new_num += num_copy % 10 * mult;

                mult /= 10;
                num_copy /= 10;

            }

            Console.WriteLine($"{num} * {new_num} = " + new_num * num);

        }

        static void test2a()
        {

            int digit = 0;
            int next = 1;

            Console.Write($"{digit},{next}");

            for (int i = 2; i < 10; i++)
            {

                int temp = next;

                next += digit;

                digit = temp;

                Console.Write("," + next);

            }

            Console.WriteLine();

        }

        static void test_2b()
        {

            Console.WriteLine("Enter number of fibonacci digits (>2)");
            int digits = int.Parse(Console.ReadLine());

            int digit = 0;
            int next = 1;

            Console.Write($"{digit},{next}");

            for (int i = 2; i < digits; i++)
            {

                int temp = next;

                next += digit;

                digit = temp;

                Console.Write("," + next);

            }

            Console.WriteLine();

        }

        static void test_2d()
        {
            Console.WriteLine("Which digit index do you want?");
            int index = int.Parse(Console.ReadLine());

            int digit = 0;
            int next = 1;

            for (int i = 2; i < index; i++)
            {

                int temp = next;

                next += digit;

                digit = temp;

            }

            Console.WriteLine(next);

        }

        static void test_2e()
        {

            Console.WriteLine("Enter number:");
            int num = int.Parse(Console.ReadLine());

            int digit = 0;
            int next = 1;

            Console.Write($"{digit},{next}");

            bool found = false;
            while(!found)
            {

                int temp = next;

                next += digit;

                digit = temp;

                if (next >= num)
                    found = true;
                else
                    Console.Write("," + next);

            }

            Console.WriteLine();


        }



        static void Main(string[] args)
        {

            // test_1();

            // test2a();
            // test_2b();
            // test_2d();
            test_2e();

        }
    }
}
