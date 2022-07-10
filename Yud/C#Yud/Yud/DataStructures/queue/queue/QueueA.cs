using System;
using System.Collections.Generic;
using System.Text;

namespace queue
{
    class QueueA<T>
    {

        public T[] queue { get; private set; }

        public int FIPointer { get; private set; }

        public int FOPointer { get; private set; }

        public QueueA(int N)
        {

            queue = new T[N];
            FIPointer = 0;
            FOPointer = 0;

        }

        public QueueA(QueueA<T>q)
        {

            queue = new T[q.queue.Length];
            FIPointer = q.FIPointer;
            FOPointer = q.FOPointer;

        }

        public bool Insert(T x)
        {

            if (FIPointer-FOPointer == queue.Length)
                return false;

            queue[FIPointer%queue.Length] = x;

            FIPointer++;

            return true;

        }

        public T Remove()
        {

            if (IsEmpty())
                throw new Exception("Queue is empty");

            T val = queue[FOPointer%queue.Length];

            FOPointer++;

            return val;

        }

        public bool IsEmpty()
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

                s += queue[i].ToString() + ',';
            }

            return s + "\n First In: " + FIPointer + "\n First Out: " + FOPointer;
        }


    }
}
