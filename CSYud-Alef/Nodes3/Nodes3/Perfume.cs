using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Nodes3
{
    class Perfume
    {

        private Node<Smell> smells;

        public Perfume()
        {
        }

        public bool isSmellComplete()
        {

            int p = 0;

            Node<Smell> head = smells;

            while (head != null)
            {

                p += head.GetValue().GetPercent();

                head = head.GetNext();

            }

            return p == 100;

        }


    }
}
