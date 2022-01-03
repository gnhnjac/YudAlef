using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Stack
{

        class StackL<T>
        {

            private Node<T> stack;

            public StackL()
            {
                stack = null;
            }

            public void Push(T val)
            {

                stack = new Node<T>(val, stack);

            }

            public T Pop()
            {

                T val = stack.GetValue();

                stack = stack.GetNext();

                return val;
                
            }

            public bool IsEmpty()
            {

                if (stack == null)
                    return true;

                return false;

            }

            public override string ToString()
            {

                string str = "";

                Node<T> head = stack;

                while (head != null)
                {

                    str += "| " + head.GetValue().ToString() + " |\n";
                    
                    head = head.GetNext();

                }


                return str;

            }

        }
    

}
