using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Animation
{
    class PlayerManager
    {

        ConsoleKeyInfo ki;

        Person player = new Person(1, 35);

        public PlayerManager()
        {

        }

        public void readKey()
        {

            do
            {

                ki = Console.ReadKey();

            }
            while (Console.KeyAvailable);

        }

        public void Act()
        {

            switch (ki.Key)
            {

                case ConsoleKey.RightArrow:
                    player.Move('r');
                    break;
                case ConsoleKey.LeftArrow:
                    player.Move('l');
                    break;
                case ConsoleKey.Spacebar:
                    player.OpenMouth();
                    break;

            }

        }

        public void showPlayer()
        {

            player.Show();

        }

        public Person Player
        {

            get => player;

        }

    }
}
