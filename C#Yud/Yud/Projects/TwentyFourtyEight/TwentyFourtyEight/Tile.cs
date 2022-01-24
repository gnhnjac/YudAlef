using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TwentyFourtyEight
{
    class Tile
    {
        public Tile()
        {

            Value = 0;
            Merged = false;
            Latest = false;

        }

        public int Value { get; set; }

        public bool Merged { get; set; }

        public bool Latest { get; set; }


    }
}
