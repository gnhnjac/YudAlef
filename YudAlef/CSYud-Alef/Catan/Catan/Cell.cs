using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

enum Resource
{
    Brick,
    Wood,
    Stone,
    Hay,
    Sheep,
    Desert,
    None
}

namespace Catan
{
    internal class Cell
    {

        // Does the current cell have a robber?
        public bool has_robber { get; set; }

        // Roads adjacent to cell

        public Road left { get; set; }
        public Road right { get; set; }
        public Road topleft { get; set; }
        public Road topright { get; set; }
        public Road bottomleft { get; set; }
        public Road bottomright { get; set; }

        // Resource

        public Resource resource { get; set; }

        // Cube roll number

        public int number { get; set; }


        // Constructor

        public Cell()
        {

            this.has_robber = false;
            this.number = 0;
            this.resource = Resource.None;

        }

        public override string ToString()
        {
            return number.ToString() + ", " + resource.ToString();
        }
    }
}
