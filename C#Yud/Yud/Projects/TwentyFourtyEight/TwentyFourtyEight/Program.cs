using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace TwentyFourtyEight
{
    class Program
    {

        static void Main(string[] args)
        {

            ConsoleKeyInfo cki;

            BoardManager bm = new BoardManager();

            bm.addRandomTile();

            bm.Show();

            while (true)
            {

                if (!bm.spaceAvailable() && !bm.neighborAvailable())
                    break;

                do
                {

                    cki = Console.ReadKey();

                }
                while (Console.KeyAvailable);

                Thread.Sleep(500);

                bm.Update(cki.Key);

                bm.Show();

            }

            bm.gameOver();

        }
    }
}
