using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

enum Players
{

    Red,
    Blue,
    Green,
    White,
    Orange,
    Brown,
    None

}

namespace CatanGame
{
    internal class Road
    {

        public Cell parent1 { get; set; }
        public Cell parent2 { get; set; }

        public Players occupant { get; set; }

        public Players house_top { get; set; }

        public Players house_bot { get; set; }

        public Road(Cell p1, Cell p2)
        {

            this.parent2 = p2;
            this.parent1 = p1;

            this.occupant = Players.None;

            this.house_bot = Players.None;

            this.house_top = Players.None;

        }

    }
}
