using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Bulls_and_cows
{
    class Case
    {

        public Case()
        {

            valid = true;

            guess = "";

        }

        public bool valid { get; set; }
        public string guess { get; set; }

    }
}
