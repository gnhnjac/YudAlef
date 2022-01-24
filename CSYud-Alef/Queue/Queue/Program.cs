using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Queue
{
    class Program
    {
        static void Main(string[] args)
        {
            
            int[] arr = { 1,1,5,4,3,6,8,8,3,8,4,1,4,9,7,9};

            Queue<int> q = QueueUtils<int>.CreateQueueFromArr(arr);

            Console.WriteLine(q.ToString());

            //q = QueueUtils<int>.ExactlyTwice(q);

            Queue<NumberLog> q2 = QueueUtils<int>.NumberLogQueue(q);

            Console.WriteLine(q2.ToString());
            
        }
    }
}
