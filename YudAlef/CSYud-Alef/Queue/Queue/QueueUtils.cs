using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Queue
{
    public static class QueueUtils<T>
    {

        public static Queue<T> CreateQueueFromArr(T[] arr)
        {

            Queue<T> q = new Queue<T>();

            foreach(T element in arr)
            {

                q.Insert(element);

            }

            return q;

        }
        
        public static Queue<T> Clone(Queue<T> q)
        {

            Queue<T> tmp = new Queue<T>();

            while (!q.IsEmpty())
            {

                tmp.Insert(q.Remove());

            }

            Queue<T> new_q = new Queue<T>();

            while (!tmp.IsEmpty())
            {

                T val = tmp.Remove();

                new_q.Insert(val);
                q.Insert(val);

            }

            return new_q;

        }

        public static int QueueLen(Queue<T> q)
        {

            Queue<T> tmp = Clone(q);

            int len = 0;
            while (!tmp.IsEmpty())
            {

                tmp.Remove();
                len++;
            }

            return len;

        }

        public static int QueueSum(Queue<int> q)
        {

            Queue<int> tmp = QueueUtils<int>.Clone(q);

            int sum = 0;
            while (!tmp.IsEmpty())
            {

                sum += tmp.Remove();

            }

            return sum;
        }

        public static bool IsExist(Queue<T> q, T x)
        {

            Queue<T> tmp = Clone(q);

            while (!tmp.IsEmpty())
            {

                if (tmp.Remove().Equals(x))
                    return true;

            }

            return false;

        }

        public static void Head2Tail(Queue<T> q)
        {

            q.Insert(q.Remove());

        }

        public static bool IsSorted(Queue<int> q)
        {

            Queue<int> tmp = QueueUtils<int>.Clone(q);

            while (!tmp.IsEmpty())
            {

                if (tmp.Remove() < tmp.GetHead() )
                    return false;

            }

            return true;

        }

        public static void InsertIntoSortedQueue(Queue<int> q, int x)
        {

            Queue<int> tmp = new Queue<int>();


            bool inserted = false;
            while (!q.IsEmpty())
            {

                int val = q.Remove();

                if (val <= x && !inserted)
                {

                    tmp.Insert(x);
                    inserted = true;

                }

                tmp.Insert(val);


            }

            if (!inserted)
                tmp.Insert(x);

            while (!tmp.IsEmpty())
            {

                q.Insert(tmp.Remove());

            }

        }

        public static void SortQueue(Queue<int> q)
        {

            Queue<int> tmp = new Queue<int>();

            while(!q.IsEmpty())
            {

                tmp.Insert(q.Remove());

            }

            q.Insert(tmp.Remove());

            while(!tmp.IsEmpty())
            {

                InsertIntoSortedQueue(q, tmp.Remove());

            }

        }

        public static Queue<int> ExactlyTwice(Queue<int> q)
        {

            QueueUtils<int>.SortQueue(q);

            Queue<int> nqueue = new Queue<int>();

            int prev = q.Remove();
            while(!q.IsEmpty())
            {

                int val = prev;
                int amount = 1;

                int val2 = q.Remove();

                while (val2 == prev && !q.IsEmpty())
                {
                    val2 = q.Remove();
                    amount ++;
                }

                if (!q.IsEmpty())
                    prev = val2;
                else
                    amount++;

                if (amount == 2)
                    nqueue.Insert(val);


            }

            return nqueue;
        }

        public static Queue<NumberLog> NumberLogQueue(Queue<int> q)
        {

            Queue<NumberLog> tmp = new Queue<NumberLog>();

            SortQueue(q);

            int num = q.Remove();
            int amount = 1;
            while (!q.IsEmpty())
            {

                int val = q.Remove();

                if (val == num)
                    amount++;
                else
                {

                    tmp.Insert(new NumberLog(amount, num));
                    num = val;
                    amount = 1;

                }

            }

            return tmp;

        }

    }
}
