using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Automaton
{
    class Program
    {
        static void Main(string[] args)
        {
            // DFA
            string input = "q0";

            Node[] nodes = new Node[]
            {

                new Node("q0",1,"q1"),
                new Node("q0",2,"q0"),
                new Node("q0",3,"q0"),
                new Node("q1",3,"q1"),
                new Node("q1",2,"q1"),
                new Node("q1",1,"q2"),
                new Node("q2",2,"q2"),
                new Node("q2",3,"q2")

            };

            string[] outputs = new string[] { "q0", "q1", "q2" };

            DFA automaton = new DFA(nodes, input, outputs);

            bool exists = automaton.Exists("121");
            Console.WriteLine();
            Console.WriteLine(exists);

            // NDFA
            string ninput = "q0";

            Node[] nnodes = new Node[]
            {

                new Node("q0",1,"q1"),
                new Node("q0",2,"q2"),
                new Node("q0",3,"q3"),
                new Node("q1",1,"q1"),
                new Node("q1",2,"q1"),
                new Node("q1",3,"q1"),
                new Node("q1",1,"q4"),
                new Node("q2",1,"q2"),
                new Node("q2",2,"q2"),
                new Node("q2",3,"q2"),
                new Node("q2",2,"q4"),
                new Node("q3",1,"q3"),
                new Node("q3",2,"q3"),
                new Node("q3",3,"q3"),
                new Node("q3",3,"q4"),
                new Node("q0",1,"q4"),
                new Node("q0",2,"q4"),
                new Node("q0",3,"q4"),

            };

            string[] noutputs = new string[] { "q4" };

            NDFA nautomaton = new NDFA(nnodes, ninput, noutputs);

            bool nexists = nautomaton.Exists("1211");
            Console.WriteLine();
            Console.WriteLine(nexists);

        }
    }
}
