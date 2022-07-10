using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ex_6
{
    class Program
    {
        static void Main(string[] args)
        {

            Console.WriteLine("What's the hamburger price? ");

            double hamburger = double.Parse(Console.ReadLine());

            Console.WriteLine("What's the coke price? ");

            double cocaCola = double.Parse(Console.ReadLine());

            double total = hamburger + cocaCola;

            Console.WriteLine("Total: " + total);

        }
    }
}
