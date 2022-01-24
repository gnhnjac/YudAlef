using System;

namespace queue
{
    class Program
    {

        static Random rnd = new Random();

        static void QueueCopy<T>(QueueA <T>q1, QueueA<T>q2)
        {

            QueueA<T> temp = new QueueA<T>(q1);

            while (!q1.IsEmpty())
            {

                q2.Insert(q1.Remove());

            }

            q1 = new QueueA<T>(temp);
            temp = null;
            GC.Collect();


        }

        static void QueueReverse<T>(QueueA<T> q1, QueueA<T> q2)
        {

            QueueA<T> temp = new QueueA<T>(q1);

            T[] temparr = new T[q1.queue.Length];

            int i = q1.queue.Length-1;
            while (!q1.IsEmpty())
            {

                temparr[i] = q1.Remove();
                i--;

            }

            i = 0;
            while (q2.Insert(temparr[i == q1.queue.Length ? 0 : i]))
                i++;

            q1 = new QueueA<T>(temp);
            temp = null;
            GC.Collect();
            temparr = null;
            GC.Collect();


        }

        public static void queueShfoch<T>(QueueA<T> q1, QueueA<T> q2)

        {

            while (!q1.IsEmpty())

                q2.Insert(q1.Remove());

        }

        public static QueueA<int> whatDoIDo(QueueA<int> q)

        {

            QueueA<int> qsod = new QueueA<int>(10);

            QueueA<int> qwhat = new QueueA<int>(10);

            int firstValue, currValue;

            if (!q.IsEmpty())

            {

                firstValue = q.Remove();

                while (!q.IsEmpty())

                {

                    currValue = q.Remove();

                    if (currValue <= firstValue)

                        qsod.Insert(currValue);

                    else

                        qwhat.Insert(currValue);

                }

                qsod = whatDoIDo(qsod);

                qwhat = whatDoIDo(qwhat);

                queueShfoch(qsod, q);

                q.Insert(firstValue);

                queueShfoch(qwhat, q);

            }

            return q;

        }


        static void Main(string[] args)
        {
            QueueA <int>q = new QueueA<int>(9);
            q.Insert(8);
            q.Insert(7);
            q.Insert(0);
            q.Insert(7);
            q.Insert(0);
            q.Insert(-1);
            q.Insert(85);
            q.Insert(-3);
            q.Insert(2);
            q.Insert(124);

            Console.WriteLine(q.ToString());

            while (!q.IsEmpty())
            {

                Console.WriteLine(q.Remove());

            }

            QueueA<int> q1 = new QueueA<int>(7);
            QueueA<int> q2 = new QueueA<int>(7);

            for (int i = 0; i < 7; i++)
                q1.Insert(rnd.Next(1000));

            /*Console.WriteLine("Queue Copy: ");

            Console.WriteLine(q1.ToString());
            Console.WriteLine(q2.ToString());

            QueueCopy(q1, q2);

            Console.WriteLine(q1.ToString());
            Console.WriteLine(q2.ToString());*/

            q2 = new QueueA<int>(7);

            Console.WriteLine("\n Queue Reverse: ");

            Console.WriteLine(q1.ToString());
            Console.WriteLine(q2.ToString());

            QueueReverse(q1, q2);

            Console.WriteLine(q1.ToString());
            Console.WriteLine(q2.ToString());

            // לפני שהרצתי עשיתי טבלת מעקב והפעולה מסדרת את התור מהקטן לגדול בצורה רקורסיבית

            Console.WriteLine("What Do I Do: ");

            QueueA<int> qsort = new QueueA<int>(10);


            for (int i = 0; i < 10; i++)
                qsort.Insert(rnd.Next(100));

            Console.WriteLine(qsort.ToString());

            qsort = whatDoIDo(qsort);

            Console.WriteLine(qsort.ToString());

            // צדקתי!! :)

            PriorityQueue<int> queue = new PriorityQueue<int>(5);
            queue.PqInsert(0,5);
            queue.PqInsert(7,5);
            queue.PqInsert(0,3);
            queue.PqInsert(-1,3);
            queue.PqInsert(85,2);
            Console.WriteLine(queue.ToString());
            queue.PqRemove();
            Console.WriteLine(queue.ToString());

        }

    }
}
