using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Automaton
{
    class Node
    {
       
        private string start;
        private int value;
        private string end;

        public Node(string start, int value, string end)
        {

            this.start = start;
            this.value = value;
            this.end = end;

        }

        public int GetValue()
        {

            return this.value;

        }

        public string GetStart()
        {

            return this.start;

        }

        public string GetEnd()
        {

            return this.end;

        }

    }
}
