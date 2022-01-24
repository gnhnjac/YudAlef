using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ex_5
{
    class Program
    {
        static void Main(string[] args)
        {

            Console.WriteLine("What's the price of the meal deal in the restaurant?");

            double price = double.Parse(Console.ReadLine());

            Console.WriteLine("How many meals were ordered?");

            int num = int.Parse(Console.ReadLine());

            double total = price * num;

            Console.WriteLine("Total: " + total);

        }
    }
}
