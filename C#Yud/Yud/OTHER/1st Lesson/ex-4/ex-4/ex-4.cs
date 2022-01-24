using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ex_4
{
    class Program
    {
        static void Main(string[] args)
        {

            double price = 0.3;

            Console.WriteLine("Enter number of pages: ");

            int pages = int.Parse(Console.ReadLine());

            double total = price * pages;

            Console.WriteLine("Total: " + total);
            
        }
    }
}
