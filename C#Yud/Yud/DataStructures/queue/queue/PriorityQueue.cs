using System;
using System.Collections.Generic;
using System.Text;

namespace queue
{
    class PriorityQueue<T>
    {

        public T[] queue { get; private set; }

        public int[] priority { get; private set; }

        public int FIPointer { get; private set; }

        public int FOPointer { get; private set; }

        public PriorityQueue(int N)
        {

            queue = new T[N];
            priority = new int[N];
            FIPointer = 0;
            FOPointer = 0;

        }

        public PriorityQueue(PriorityQueue<T> q)
        {

            queue = new T[q.queue.Length];
            priority = new int[q.queue.Length];
            FIPointer = q.FIPointer;
            FOPointer = q.FOPointer;

        }

        public bool PqInsert(T x, int priorityx)
        {

            if (FIPointer - FOPointer == queue.Length)
                return false;

            queue[FIPointer % queue.Length] = x;
            priority[FIPointer % queue.Length] = priorityx;

            FIPointer++;

            return true;

        }

        public T PqRemove()
        {

            if (PqIsEmpty())
                throw new Exception("Queue is empty");

            int highest_ind = FOPointer % priority.Length;
            int highest_val = priority[FOPointer % priority.Length];
            if (highest_val != 1)
            {
                for (int i = FOPointer + 1; i < priority.Length; i++)
                {


                    if (priority[i % priority.Length] < highest_val)
                    {

                        highest_ind = i % priority.Length;
                        highest_val = priority[i % priority.Length];

                        if (highest_val == 1)
                            break;

                    }

                }
            }

            T val = queue[highest_ind];

            for (int i = highest_ind; i > FOPointer; i--)
            {
                queue[i%queue.Length] = queue[i-1 % queue.Length];
            }

            FOPointer++;

            return val;

        }

        public bool PqIsEmpty()
        {

            if (FOPointer == FIPointer)
                return true;

            return false;

        }

        public override string ToString()
        {
            string s = "";

            for (int i = 0; i < queue.Length; i++)
            {

                s += queue[i].ToString() + '(' + priority[i].ToString() + ')' + ',';
            }

            return s + "\n First In: " + FIPointer + "\n First Out: " + FOPointer;
        }

    }
}
