using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Nodes2
{
    class Program
    {

        static Node<int> Q1(Node<int> head, int n)
        {
            /*
            Time Complexity: O(n)
            n is the number of elements in the list.
            Because the best case scenario is O(1), which means immediately finding a matching place to place the number in,
            And the worst case scenario is O(n), which means finding the matching place in the end of the list.
            The worst case scenario outweights the best case scenario when were talking about very very big lists, because in average the best case scenario rarely
            happens and the worst case is a much more reasonable estimate of runtime, the O(n) complexity wins and is chosen.
            */

            if (head == null)
                return new Node<int>(n, null);

            Node<int> temp_head = new Node<int>(0, head);
            Node<int> save = temp_head;
            while (temp_head.HasNext())
            {
                if (temp_head.GetNext().GetValue() >= n)
                {
                    Node<int> next = new Node<int>(n, temp_head.GetNext());
                    temp_head.SetNext(next);
                    return save.GetNext();
                }

                temp_head = temp_head.GetNext();

            }

            if (head.GetValue() < n)
            {

                Node<int> next = new Node<int>(n, null);
                head.SetNext(next);
                return head;

            }

            return new Node<int>(n, head);

        }

        static Node<int> Q2(Node<int> lst)
        {
            /*
            Time Complexity: O(n^2)
            n is the number of elements in the list.
            We are going over the list once here, and once for each time here in Q1()
            so we are in total going n^2 times over the list.
             */

            Node<int> sorted = null;
            
            while (lst != null)
            {

                sorted = Q1(sorted, lst.GetValue());

                lst = lst.GetNext();

            }

            return sorted;

        }

        static int NegSequence(Node<int> lst)
        {

            /*
            Time Complexity: O(n)
            n is the number of elements in the list.
            we are going over the list once (each node)
            */

            int seq = 0;
            int biggest = 0;

            bool inSeq = false;

            while (lst != null)
            {

                if (lst.GetValue() < 0)
                {

                    inSeq = true;
                    seq++;

                }
                else if(inSeq && lst.GetValue() >= 0)
                {

                    inSeq = false;

                    if (seq > biggest)
                        biggest = seq;

                    seq = 0;

                }

                if(inSeq && lst.GetNext() == null)
                {

                    if (seq > biggest)
                        biggest = seq;

                }

                lst = lst.GetNext();

            }

            return biggest;

        }

        static Node<int> Q4(Node<int> lst1, Node<int> lst2)
        {

            /*
            Time Complexity: O(n+m)
            n is the number of elements in list 1,
            m is the number of elements in list 2
            we are going over each node of each list once so the total time complexity is their lengths combined.
            */
            

            Node<int> sorted = new Node<int>(0, null);
            Node<int> sorted_head_ptr = sorted;

            while (lst1 != null)
            {

                Node<int> next = new Node<int>(lst1.GetValue(), null);
                sorted.SetNext(next);
                sorted = next;

                lst1 = lst1.GetNext();

            }

            sorted = sorted_head_ptr.GetNext();

            while (lst2 != null)
            {

                sorted = Q1(sorted, lst2.GetValue());

                lst2 = lst2.GetNext();

            }

            return sorted;

        }

        static void Q5(Node<int> lst, int n)
        {

            /*
            Time Complexity: O(n)
            n is the number of elements in the list.
            best case scenario is going over 1 element and finding it (O(1))
            worst case is the last element being it (O(n)) which means going over the whole array.
            worst case beats best case when were talking about very big lists so the complexity is going over each element once, O(n)
             */

            while (lst != null)
            {

                if (lst.GetValue() == n)
                {

                    Node<int> next = new Node<int>(n + 1, lst.GetNext());
                    lst.SetNext(next);
                    lst = next;

                }
                else
                    lst = lst.GetNext();

            }

        }

        static Node<int> Q6(Node<int> lst, int n)
        {
            /*
             Time Complexity: O(1)
            It only does 1 operation, add 1 node to the beginning of the list.
             */
            return new Node<int>(n, lst);

        }

        static int SumListR(Node<int> lst)
        {
            /*
             Time Complexity: O(n)
            n is the number of elements in the list.
            it goes over each node in the array once.
            */

            if (lst == null)
                return 0;

            return lst.GetValue() + SumListR(lst.GetNext());

        }

        static void PrintListR(Node<int> lst)
        {
            /*
             Time Complexity: O(n)
            n is the number of elements in the list.
            it goes over each node in the array once.
            */
            if (lst == null)
                return;

            Console.Write(lst.GetValue() + ", ");

            PrintListR(lst.GetNext());

        }

        static bool ExistsR(Node<int> lst, int n)
        {
            /*
             Time Complexity: O(n)
            n is the number of elements in the list.
            it goes over each node in the array once.
            */
            if (lst == null)
                return false;

            return lst.GetValue() == n || ExistsR(lst.GetNext(), n);


        }

        static bool AreListsIndenticalR(Node<int> lst1, Node<int> lst2)
        {
            /*
             Time Complexity: O(n)
            n is the number of elements in list 1.
            it goes over each node in the list once.
            if list 2 ends before 1 then its less (best case scenario)
            if list 1 ends before 2 then its still o(n)
            if both end the same then its still len list 1.
            */
            if (lst1 == null ^ lst2 == null)
                return false;
            if (lst1 == null && lst2 == null)
                return true;

            return lst1.GetValue() == lst2.GetValue() && AreListsIndenticalR(lst1.GetNext(), lst2.GetNext());

        }

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

        static void Main(string[] args)
        {

            // Q1 Test
            int[] arr2 = { 1 };

            Node<int> lst2 = CreateListFromArray2(arr2);

            lst2 = Q1(lst2, 0);

            //PrintList(lst2);

            // Q2 Test
            int[] arr = { 4, 6, 7, 2, 7, 3, 1354, 7, 45, 65, 21, 6, 8, 367, 568, 356, 2, 6, 546 };

            Node<int> lst = CreateListFromArray2(arr);

            lst = Q2(lst);

            //PrintList(lst);

            // Q3 Test

            int[] arr3 = { -4, -6, -7, -2, 7, 3, -1354, -7, -45, 65, 21, -6, -8, -367, -568, -356, -2, -6, -546 };

            Node<int> lst3 = CreateListFromArray2(arr3);

            // Console.WriteLine(NegSequence(lst3));

            // Q4 Test

            Node<int> res = Q4(lst, lst3);

            // PrintList(res);

            // Q5 Test

            Q5(lst3, -6);

            // PrintList(lst3);

            // Q7 Test

            int[] arr71 = { 1,2,3 };

            Node<int> lst71 = CreateListFromArray2(arr71);

            Console.WriteLine(SumListR(lst71));

            PrintListR(lst71);
            Console.WriteLine();
            Console.WriteLine(ExistsR(lst71, 2));
            Console.WriteLine(ExistsR(lst71, 5));

            int[] arr72 = { 1, 2, 3 };

            Node<int> lst72 = CreateListFromArray2(arr72);

            Console.WriteLine(AreListsIndenticalR(lst71, lst72));
            Console.WriteLine(AreListsIndenticalR(lst71, lst));

        }
    }
}
