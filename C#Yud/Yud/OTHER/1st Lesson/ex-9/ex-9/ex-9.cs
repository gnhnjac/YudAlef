using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ex_9
{
    class Program
    {
        static void Main(string[] args)
        {

            Console.WriteLine("1st game price: ");

            double first = double.Parse(Console.ReadLine());

            Console.WriteLine("2nd game price: ");

            double second = double.Parse(Console.ReadLine());

            Console.WriteLine("3rd game price: ");

            double third = double.Parse(Console.ReadLine());

            double total = first + second + third;

            Console.WriteLine("Total price: " + total);

        }
    }
}
