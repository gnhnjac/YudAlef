using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Animation
{
    public class Person
    {

        int x;
        int y;

        bool walking = false;

        bool eating = false;

        static char block = '█';

        public int X
        {

            get => x;

        }

        public int Y
        {

            get => y;

        }

        public Person(int _x, int _y)
        {

            x = _x;
            y = _y;

        }

        public void Show()
        {

            if (eating)
                return;

            Clear();

            Console.ForegroundColor = ConsoleColor.White;

            // Head
            for (int i = 0; i < 3; i++)
            {

                for (int j = 0; j < 3; j++)
                {

                    Console.SetCursorPosition(x + 1 + i, y + j);
                    Console.Write(block);

                }

            }

            // Left Arm
            Console.SetCursorPosition(x, y + 5);
            Console.Write(block);

            Console.SetCursorPosition(x + 1, y + 4);
            Console.Write(block);


            // Right Arm
            Console.SetCursorPosition(x + 3, y + 4);
            Console.Write(block);

            Console.SetCursorPosition(x + 4, y + 5);
            Console.Write(block);

            // Body

            for (int i = 0; i < 8; i++)
            {

                Console.SetCursorPosition(x + 2, y + 3 + i);
                Console.Write(block);

            }

            if (walking)
            {

                Walk();

            }
            else
            {

                Stay();

            }

        }

        public void Walk()
        {

            Console.ForegroundColor = ConsoleColor.White;

            Console.SetCursorPosition(x + 1, y + 11);
            Console.Write(block);

            Console.SetCursorPosition(x, y + 12);
            Console.Write(block);

            Console.SetCursorPosition(x + 3, y + 11);
            Console.Write(block);

            Console.SetCursorPosition(x + 4, y + 12);
            Console.Write(block);

        }

        public void Stay()
        {

            Console.ForegroundColor = ConsoleColor.White;

            Console.SetCursorPosition(x + 1, y + 11);
            Console.Write(block);

            Console.SetCursorPosition(x + 1, y + 12);
            Console.Write(block);

            Console.SetCursorPosition(x + 3, y + 11);
            Console.Write(block);

            Console.SetCursorPosition(x + 3, y + 12);
            Console.Write(block);

        }

        public void OpenMouth()
        {
            Console.ForegroundColor = ConsoleColor.White;

            Console.SetCursorPosition(x, y);
            Console.Write(block);

            Console.SetCursorPosition(x, y+1);
            Console.Write(block);

            Console.SetCursorPosition(x+4, y);
            Console.Write(block);

            Console.SetCursorPosition(x+4, y + 1);
            Console.Write(block);

            Console.ForegroundColor = ConsoleColor.Black;

            Console.SetCursorPosition(x+1, y);
            Console.Write(block);

            Console.SetCursorPosition(x+2, y);
            Console.Write(block);

            Console.SetCursorPosition(x+3, y);
            Console.Write(block);

            Console.SetCursorPosition(x + 2, y + 1);
            Console.Write(block);

            eating = true;

        }

        public bool isEating(int target_x, int target_y)
        {
            if (eating)
            {

                if (target_x >= x + 1 && target_x <= x + 3 && target_y == y)
                    return true;

            }

            return false;

        }

        public bool isBumping(int target_x, int target_y)
        {

            if (target_x >= x + 1 && target_x <= x + 3 && target_y >= y && !eating)
                return true;

            return false;

        }

        public void Clear()
        {

            // Clear previous iteration
            Console.ForegroundColor = ConsoleColor.Black;

            for (int i = -1; i < 6; i++)
            {

                for (int j = 0; j < 13; j++)
                {

                    Console.SetCursorPosition(x + i, y + j);
                    Console.Write(block);

                }

            }

        }

        public void Move(char dir)
        {

            if (dir == 'r' && x+5 < 80)
            {
                x++;

            }
            else if (dir == 'l' && x > 1)
            {

                x--;

            }

            eating = false;

            walking = !walking;

        }

    }
}
