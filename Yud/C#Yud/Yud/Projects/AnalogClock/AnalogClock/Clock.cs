using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace AnalogClock
{

    class Clock
    {

        int x;

        int y;

        int rad;

        public Clock(int _x, int _y, int radius)
        {

            x = _x;

            y = _y;

            rad = radius;

            // Circle

            int cx = x + rad*2;
            int cy = y + rad;

            double current_x = cx + rad;

            double degree = 270;

            double rdegree = degree * Math.PI / 180;

            for (int i = 0; i < 360; i++)
            {

                double rotated_x = cx + (current_x - cx) * Math.Cos(rdegree);

                double rotated_y = cy + (current_x - cx) * Math.Sin(rdegree);

                Console.SetCursorPosition((int)rotated_x, (int)rotated_y);
                Console.Write('█');

                degree += 1;
                rdegree = degree * Math.PI / 180;

            }

            current_x = cx + rad * 3 / 4;

            degree = 270;

            rdegree = degree * Math.PI / 180;

            for (int i = 0; i < 12; i++)
            {

                double rotated_x = cx + (current_x - cx) * Math.Cos(rdegree);

                double rotated_y = cy + (current_x - cx) * Math.Sin(rdegree);

                Console.SetCursorPosition((int)rotated_x, (int)rotated_y);
                Console.Write((i + 11) % 12 + 1);

                degree += 360 / 12;
                rdegree = degree * Math.PI / 180;

            }

        }

        public void Update()
        {

            DateTime now = DateTime.Now;

        }

        public void DrawHand(double d, bool clear, double len)
        {

            char symbol = '█';

            if (clear)
                symbol = ' ';

            // Draw Hand

            int cx = x + rad * 2;
            int cy = y + rad;

            double degree = d;

            double rdegree = degree * Math.PI / 180;

            double hour_hand_len = len - rdegree;

            for (int i = 0; i < hour_hand_len; i++)
            {

                int current_x = cx + i;

                double rotated_x = cx + (current_x - cx) * Math.Cos(rdegree);

                double rotated_y = cy + (current_x - cx) * Math.Sin(rdegree);

                Console.SetCursorPosition((int)rotated_x, (int)rotated_y);
                Console.Write(symbol);

            }

        }

    }
}
