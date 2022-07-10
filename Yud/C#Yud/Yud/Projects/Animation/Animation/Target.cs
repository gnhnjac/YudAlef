using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Animation
{

    class Target
    {

        Random rnd = new Random();

        int x;
        double y = 1;

        static char block = '█';

        public Target()
        {

            x = rnd.Next(1, 79);

        }

        public void Show()
        {

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.SetCursorPosition(x, (int)y);
            Console.Write(block);

            Console.ForegroundColor = ConsoleColor.Black;
            Console.SetCursorPosition(x, (int)y-1);
            Console.Write(block);
            Console.SetCursorPosition(80, 50);

        }

        public bool InBounds()
        {

            if (y < 47)
                return true;

            return false;

        }

        public void Update()
        {
            y += 0.25;
        }

        public void Clear()
        {

            Console.ForegroundColor = ConsoleColor.Black;
            Console.SetCursorPosition(x, (int)y);
            Console.Write(block);
            Console.SetCursorPosition(80, 50);

        }

        public int X
        {

            get => x;

        }

        public double Y
        {

            get => y;

        }

    }
}
