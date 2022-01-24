using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Backgammon
{
    class Program
    {

        static Random rnd = new Random();

        static void Main(string[] args)
        {

            int doubles, sixes, double_sixes, backgammons, sum1;

            doubles = sixes = double_sixes = backgammons = sum1 = 0;

            for (int i = 0; i < 1000; i++)
            {

                int dice1 = rnd.Next(1, 7);
                int dice2 = rnd.Next(1, 7);

                if (dice1 == dice2)
                {

                    doubles++;

                    if (dice1 == 6)
                        double_sixes++;

                }

                if (dice1 == 6)
                    sixes++;

                if (dice2 == 6)
                    sixes++;

                if ((dice1 == 6 && dice2 == 5) || (dice1 == 5 && dice2 == 6))
                        backgammons++;

                sum1 += dice1;

            }

            Console.WriteLine("Doubles: " + doubles);
            Console.WriteLine("Double Sixes: " + double_sixes);
            Console.WriteLine("Sixes: " + sixes);
            Console.WriteLine("Backgammons: " + backgammons);
            Console.WriteLine("Sum of 1st dice: " + sum1);

            /* The reason why the number of backgammons is roughly
             twice the number of double sixes is because probability wise double sixes only occur when the dice roll a 6 6,
            and a five and a six occur when either 5 6 or 6 5, which is twice the options as 6 6.
             */

        }
    }
}
