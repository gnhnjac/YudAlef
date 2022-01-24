using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NodeUtils
{
    class Point
    {

        private int x = 0;
        private int y = 0;

        public Point(int _x, int _y)
        {

            x = _x;
            y = _y;

        }

        public bool Equal(Point p1)
        {

            return x == p1.x && y == p1.y;


        } 

        public int GetX()
        {

            return x;

        }

        public int GetY()
        {

            return y;

        }

        public void SetX(int n)
        {

            x = n;

        }

        public void SetY(int n)
        {

            y = n;

        }

        public override string ToString()
        {
            return $"x: {x}, y: {y}";
        }

    }
}
