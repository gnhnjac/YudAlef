using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Stack
{
    class Point
    {

        private int x;
        private int y;

        public Point(int _x, int _y)
        {

            x = _x;
            y = _y;

        }

        public int GetX()
        {

            return x;

        }

        public int GetY()
        {

            return y;

        }

        public void SetX(int _x)
        {

            x = _x;

        }

        public void SetY(int _y)
        {

            y = _y;

        }


    }
}
