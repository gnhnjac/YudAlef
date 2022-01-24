using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BinTrees
{
    public class Queue<T>
    {

        Node<T> head;
        Node<T> tail;

        public Queue()
        {

            head = null;
            tail = null;

        }

        public void Insert(T x)
        {

            if (head == null)
            {

                head = new Node<T>(x, null);
                tail = head;
                return;

            }
            tail.SetNext(new Node<T>(x));
            tail = tail.GetNext();
        }

        public T Remove()
        {

            T v = head.GetValue();
            head = head.GetNext();
            return v;

        }

        public T GetHead()
        {

            return head.GetValue();

        }

        public bool IsEmpty()
        {

            return head == null;

        }

        public override string ToString()
        {
            string str = "";

            Node<T> tmp = head;

            while (tmp != null)
            {

                str += tmp.GetValue() + ", ";

                tmp = tmp.GetNext();

            }
            return str;
        }

    }
}
