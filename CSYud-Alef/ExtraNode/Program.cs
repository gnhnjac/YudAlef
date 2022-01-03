using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ExtraNode
{
    class Program
    {

        public static Node<int> CreateListFromArray2(int[] a)
        {

            Node<int> head, tail = null;

            head = new Node<int>(a[0]);

            tail = head;

            for (int i = 1; i < a.Length; i++)
            {

                tail.SetNext(new Node<int>(a[i]));

                tail = tail.GetNext();


            }

            return head;


        }

        public static void PrintList(Node<int> head)
        {

            while (head != null)
            {

                Console.Write(head.GetValue() + ", ");
                head = head.GetNext();

            }

        }

        static Node<int> ReverseList(Node<int> lst)
        {

            Node<int> reversed = null;

            while (lst != null)
            {

                reversed = new Node<int>(lst.GetValue(), reversed);

                lst = lst.GetNext();

            }

            return reversed;


        }

        static Node<int> ReverseListR(Node<int> lst)
        {

            if (!lst.HasNext())
                return lst;

            Node<int> temp = lst.GetNext();
            Node<int> r = ReverseListR(temp);
            lst.SetNext(null);
            temp.SetNext(lst);

            return r;


        }

        static void Main(string[] args)
        {

            int[] arr = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 };

            Node<int> lst = CreateListFromArray2(arr);

            PrintList(lst);

            lst = ReverseListR(lst);

            Console.WriteLine();

            PrintList(lst);

        }
    }
}
