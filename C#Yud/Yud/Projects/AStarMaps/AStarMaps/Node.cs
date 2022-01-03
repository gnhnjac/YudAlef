using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace AStarMaps
{
    class Node
    {

        public double gcost { get; set; }

        public double hcost { get; set; }

        public double fcost
        {

            get { return gcost + hcost; }

        }

        public int x { get; set; }

        public int y { get; set; }

        public bool isObstacle { get; set; }

        public Node parent { get; set; }

        public Node(int _x, int _y)
        {

            x = _x;
            y = _y;

            isObstacle = false;

            gcost = double.PositiveInfinity;

        }

    }
}
