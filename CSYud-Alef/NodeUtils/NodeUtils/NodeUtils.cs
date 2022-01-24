using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NodeUtils
{
    static class NodeUtils<T>
    {

        private static Random rand = new Random();

        public static Node<int> CreateRandomList(int n, int min, int max)
        {

            Node<int> head = null;

            for (int i = 0; i < n; i++)
            {

                head = new Node<int>(rand.Next(min, max), head);

            }

            return head;

        }

        public static Node<T> CreateListFromArray(T[] a)
        {

            Node<T> head = null;

            for (int i = a.Length - 1; i >= 0; i--)
            {

                head = new Node<T>(a[i], head);

            }

            return head;

        }

        public static Node<T> CreateListFromArray2(T[] a)
        {

            Node<T> head, tail = null;

            head = new Node<T>(a[0]);

            tail = head;

            for (int i = 1; i < a.Length; i++)
            {

                tail.SetNext(new Node<T>(a[i]));

                tail = tail.GetNext();


            }

            return head;


        }

        public static void PrintList(Node<T> head)
        {

            while (head != null)
            {

                Console.WriteLine(head.GetValue());
                head = head.GetNext();

            }

        }

        public static void Inc1Inc2(Node<int> head)
        {

            bool singleinc = true;
            while (head != null)
            {

                head.SetValue(head.GetValue() + ((singleinc) ? 1 : 2));
                singleinc = !singleinc;
                head = head.GetNext();

            }

        }

        public static int CountList(Node<T> lst)
        {

            int cnt = 0;

            while (lst != null)
            {

                lst = lst.GetNext();

                cnt++;

            }

            return cnt;

        }

        public static bool CompareList(Node<int> l1, Node<int> l2)
        {

            while (l1 != null && l2 != null)
            {

                if (l1.GetValue() != l2.GetValue())
                    return false;

                l1 = l1.GetNext();
                l2 = l2.GetNext();

            }

            return (l1 == l2);

        }

        public static Node<T> GetElement(Node<T> lst, int n)
        {

            int cnt = 1;

            while (lst != null)
            {

                if (cnt == n)
                    return lst;

                lst = lst.GetNext();

                cnt++;


            }

            return null;


        }

        public static T GetElementValue(Node<T> lst, int n)
        {

            return GetElement(lst, n).GetValue();

        }

        public static int SumList(Node<int> lst)
        {

            int sum = 0;

            while (lst != null)
            {

                sum += lst.GetValue();

                lst = lst.GetNext();

            }

            return sum;


        }

        public static int Max(Node<int> lst)
        {

            int max = lst.GetValue();

            while (lst != null)
            {

                if (max < lst.GetValue())
                    max = lst.GetValue();

                lst = lst.GetNext();

            }

            return max;

        }

        public static bool Exists(Node<int> lst, int n)
        {

            while (lst != null)
            {

                if (lst.GetValue() == n)
                    return true;

                lst = lst.GetNext();

            }

            return false;

        }

        public static void AbsoluteList(Node<int> lst)
        {

            while (lst != null)
            {

                lst.SetValue(Math.Abs(lst.GetValue()));

                lst = lst.GetNext();

            }

        }

        public static int GetSequence(Node<int> lst, int n)
        {

            int sequence = 0;

            bool isSequence = false;

            while (lst != null)
            {

                if (lst.GetValue() == n && !isSequence)
                {
                    sequence++;
                    isSequence = true;

                }
                    
                else
                {

                    isSequence = false;

                }

                lst = lst.GetNext();

            }

            return sequence;

        }

        public static void PrintPair(Node<T> lst, int ind1, int ind2)
        {

            int cnt = 0;

            while (lst != null)
            {

                if (cnt == ind1 || cnt == ind2)
                    Console.WriteLine(lst.GetValue());

                lst = lst.GetNext();
                cnt++;

            }

        }

        public static Node<int> RemoveDupes(Node<int> lst)
        {

            Node<int> head = null;

            while (lst != null)
            {

                if (!Exists(head, lst.GetValue()))
                {

                    head = new Node<int>(lst.GetValue(), head);

                }

            }

            return head;

        }

        public static int Avg(Node<int> lst)
        {

            return SumList(lst)/NodeUtils<int>.CountList(lst);

        }

        public static bool Balanced(Node<int> lst)
        {

            int avg = Avg(lst);

            int bigger = 0;
            int smaller = 0;

            while (lst != null)
            {

                if (lst.GetValue() > avg)
                    bigger++;

                else if (lst.GetValue() < avg)
                    smaller++;

            }

            return bigger == smaller;


        }

        public static void Q1(Node<int> head, int n)
        {

            while (head != null)
            {

                Node<int> next = new Node<int>(n-head.GetValue(), head.GetNext());
                head.SetNext(next);

                head = next.GetNext();

            }

        }

        public static void Q2(Node<int> head, int n)
        {

            while(head.GetNext() != null)
            {
                if (head.GetNext().GetValue() >= n)
                {
                    Node<int> next = new Node<int>(n, head.GetNext());
                    head.SetNext(next);
                    return;
                }

                head = head.GetNext();

            }

        }

        
        public static Node<T> Remove(Node<T> head, int index)
        {

            int count = 0;

            Node<T> pos = head;

            if (index == 0)
                return head.GetNext();

            while(pos.HasNext())
            {

                if (count+1 == index)
                {

                    pos.SetNext(pos.GetNext().GetNext());
                    return head;

                }

                pos = pos.GetNext();

                count++;

            }

            return head;


        }

        public static Node<int> RemoveAllInstances(Node<int> head, int n)
        {

            head = new Node<int>(0,head);

            Node<int> pos = head;

            while (pos.HasNext())
            {

                if (pos.GetNext().GetValue() == n)
                {

                    pos.SetNext(pos.GetNext().GetNext());

                }

                else
                {
                    pos = pos.GetNext();
                }
            }

            return head.GetNext();

        }

        public static Node<int> RemoveAllInstancesRecursive(Node<int> lst, int n)
        {
            if (lst == null)
                return null;
            if (lst.GetValue() == n)
                return RemoveAllInstancesRecursive(lst.GetNext(), n);
            lst.SetNext(RemoveAllInstancesRecursive(lst.GetNext(), n));
            return lst;

        }

        public static double Distance(Point p1, Point p2)
        {

            return Math.Sqrt(Math.Pow(p1.GetX() - p2.GetX(), 2) + Math.Pow(p1.GetY() - p2.GetY(), 2));

        }

        public static double RouteLength(Node<Point> route)
        {

            double len = 0;

            while (route.HasNext())
            {

                len += Distance(route.GetValue(), route.GetNext().GetValue());

                route = route.GetNext();

            }

            return len;

        }

        public static Node<T> CircleList(T[] arr)
        {

            Node<T> head = new Node<T>(arr[0], null);

            Node<T> pos = head;

            int i = 1;
            while (i < arr.Length)
            {

                pos.SetNext(new Node<T>(arr[i], null));
                pos = pos.GetNext();

                i++;

            }

            pos.SetNext(head);

            return head;

        }

        public static void PrintCircleList(Node<T> lst)
        {

            Node<T> pos = lst;
            bool start = true;
            while (lst != pos || start)
            {

                Console.WriteLine(pos.GetValue().ToString());
                pos = pos.GetNext();

                start = false;

            }

        }

        public static bool IsCircular(Node<T> lst)
        {

            Node<T> pos = lst;
            while (true)
            {
                pos = pos.GetNext();

                if (pos == lst)
                    return true;
                if (pos == null)
                    return false;

            }

        }

        public static void AddNodeToCircularList(Node<T> lst, int ind, T val)
        {

            int i = 0;
            while (i != ind)
            {

                lst = lst.GetNext();
                i++;

            }

            Node<T> next = new Node<T>(val, lst.GetNext());
            lst.SetNext(next);

        }

        public static Node<T> AddToStartCircularList(Node<T> lst, T val)
        {

            Node<T> pos = lst;
            while (pos.GetNext() != lst)
            {

                pos = pos.GetNext();

            }

            Node<T> next = new Node<T>(val, lst);

            pos.SetNext(next);

            return next;

        }

        public static Node<T> DeleteNodeCircularList(Node<T> lst, int ind)
        {

            Node<T> head = lst;

            if (ind == 0)
            {

                while (lst.GetNext() != head)
                {

                    lst = lst.GetNext();

                }

                lst.SetNext(lst.GetNext().GetNext());

                return lst.GetNext();

            }


             int i = 0;
             while (i < ind - 1)
             {

                 lst = lst.GetNext();
                 i++;

             }

             lst.SetNext(lst.GetNext().GetNext());

             return head;

        }



    }
}
