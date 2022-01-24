
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Input;

namespace Animation
{

    class Program
    {

        static void Main(string[] args)
        {

            TargetManager t_manager = new TargetManager(5);

            PlayerManager p_manager = new PlayerManager();

            int score = 0;

            int lives = 3;

            p_manager.showPlayer();

            while (true)
            {

                t_manager.showTargets();

                int code = t_manager.updateTargets(p_manager.Player);

                if (code == -1)
                {

                    lives--;

                }
                else if (code == 1)
                {

                    score++;

                }

                if (lives == 0)
                    break;

                Console.ForegroundColor = ConsoleColor.White;
                Console.SetCursorPosition(0, 0);
                Console.WriteLine($"Score: {score}");
                Console.Write($"Lives: {lives}");

                Thread.Sleep(50);

                if (!Console.KeyAvailable)
                    continue;

                p_manager.readKey();

                p_manager.Act();

                p_manager.showPlayer();

            }

            Console.Clear();

            Console.ForegroundColor = ConsoleColor.White;
            Console.SetCursorPosition(40, 25);
            Console.WriteLine($"You Lost! You had a score of {score}");

        }
    }
}
