using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Calculator
{
    class Program
    {
        static void Main(string[] args)
        {

            Console.WriteLine("First number: ");

            double n1 = double.Parse(Console.ReadLine());

            Console.WriteLine("Second number: ");

            double n2 = double.Parse(Console.ReadLine());

            Console.WriteLine("Operation (+, -, *, :): ");

            char op = char.Parse(Console.ReadLine());

            Console.Write($"{n1} {op} {n2} = ");

            if (op == '+')
            {

                Console.WriteLine(n1 + n2);

            }
            else if (op == '-')
            {
                Console.WriteLine(n1 - n2);

            }
            else if (op == '*')
            {
                Console.WriteLine(n1 * n2);

            }
            else if (op == ':')
            {

                Console.WriteLine(n1 / n2);
            }
            else
            {

                Console.WriteLine("ERROR");

            }

        }
    }
}
