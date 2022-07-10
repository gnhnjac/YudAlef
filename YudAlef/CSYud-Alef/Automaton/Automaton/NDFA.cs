using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Automaton
{
    class NDFA
    {

        Node[] nodes;
        string input;
        string[] outputs;

        public NDFA(Node[] nodes, string input, string[] outputs)
        {
            this.nodes = nodes;
            this.input = input;
            this.outputs = outputs;

        }

        public bool Exists(string word)
        {

            return ExistsRec(word, input);

        }

        public bool ExistsRec(string word, string start_node)
        {

            string current_node = start_node;
            if (start_node == input)
                Console.Write(current_node);

            for (int i = 0; i < word.Length; i++)
            {
                int letter = int.Parse(word[i].ToString());
                bool found = false;
                for (int j = 0; j < nodes.Length; j++)
                {

                    if (nodes[j].GetStart() == current_node && nodes[j].GetValue() == letter)
                    {
                        if (start_node == input)
                            Console.Write("->" + letter + "->" + nodes[j].GetEnd());
                        if (ExistsRec(word.Substring(i+1, word.Length-i-1), nodes[j].GetEnd()))
                        {
                            current_node = nodes[j].GetEnd();
                            found = true;
                            break;
                        }
                    }

                }

                if (!found)
                    return false;

            }

            for (int i = 0; i < outputs.Length; i++)
            {

                if (outputs[i] == current_node)
                    return true;

            }

            return false;

        }

    }
}
