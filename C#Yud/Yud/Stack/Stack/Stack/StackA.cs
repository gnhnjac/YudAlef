using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Stack
{
    class StackA <T>
    {

        private int head = 0;

        private T[] stack;

        public StackA(int len)
        {
            stack = new T [len];
        }

        public bool push(T val)
        {

            if (head == stack.Length)
                return false;

            stack[head] = val;

            head++;

            return true;

        }

        public T pop()
        {

            if (head == 0)
            {

                throw new InvalidOperationException("Cannot pop stack is empty");

            }
              

            head--;

            return stack[head];
        }

        public bool isEmpty()
        {

            if (head == 0)
                return true;

            return false;

        }

        public override string ToString()
        {

            string str = "";

            for (int i = 0; i < head; i++)
            {

                str += stack[i].ToString() + ", ";
                
            }

            return str;

        }

    }
}
