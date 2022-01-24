using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MineSweeper
{

    enum State { Closed, Flagged, Revealed };

    class Cell
    {

        public State state { get; set; }

        public bool isBomb { get; set; }

        public int value { get; set; }

        public Cell()
        {

            state = State.Closed;

            isBomb = false;

            value = 0;

        }


    }
}
