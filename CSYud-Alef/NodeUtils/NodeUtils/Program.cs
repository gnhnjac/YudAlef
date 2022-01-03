using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NodeUtils
{
    class Program
    {

        

        

        static void Main(string[] args)

        {

            int[] arr = new int[] { 1, 2, 3, 4, 43, 6, 45, 475, 7, 567, 6547, 8, 64, 8, 64778, 7, 9866, 498, 64798 };

            Node<int> lst = NodeUtils<int>.CircleList(arr);
            NodeUtils<int>.AddNodeToCircularList(lst, 0, 10);
            Console.WriteLine("Before: ");
            NodeUtils<int>.PrintCircleList(lst);
            lst = NodeUtils<int>.DeleteNodeCircularList(lst, 1);
            Console.WriteLine("After: ");
            NodeUtils<int>.PrintCircleList(lst);
            Console.WriteLine(NodeUtils<int>.IsCircular(lst));


        }
    }
}
