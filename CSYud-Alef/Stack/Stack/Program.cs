using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Stack
{
    class Program
    {

        public static void PrintList<T>(Node<T> head)
        {

            while (head != null)
            {

                Console.WriteLine(head.GetValue());
                head = head.GetNext();

            }

        }

        public static Node<T> CreateListFromArray<T>(T[] a)
        {

            Node<T> head = null;

            for (int i = a.Length - 1; i >= 0; i--)
            {

                head = new Node<T> (a[i], head);

            }

            return head;

        }

        static void Main(string[] args)
        {
                int[] a1 = { 1, 8, 5, 10 };
                int[] a2 = { 7, 10, 30, 7 };
                int[] a3 = { 30, 45, 10, 70, 90 };
                int[] a4 = { 17, 80, 50, 3 };
                StackL<int> s1 = StackUtils<int>.CreateStackFromArray(a1);
                StackL<int> s2 = StackUtils<int>.CreateStackFromArray(a2);
                StackL<int> s3 = StackUtils<int>.CreateStackFromArray(a3);
                StackL<int> s4 = StackUtils<int>.CreateStackFromArray(a4);
                StackL<int>[] s_arr = { s1, s2, s3, s4 };
                Node<StackL<int>> lst = CreateListFromArray(s_arr);
                Node<TwoItems> l2 = StackUtils<Node<StackL<int>>>.isRanged(lst);
                PrintList<StackL<int>>(lst);
                PrintList<TwoItems>(l2);
            



        }
    }
}
