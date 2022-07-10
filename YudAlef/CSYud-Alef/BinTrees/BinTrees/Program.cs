using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Unit4;
using VisualTree;

namespace BinTrees
{
    internal class Program
    {
        static void Main(string[] args)
        {
            //BinNode<int> t = TreeUtils.BuildTree();
            BinNode<int> t = BSTUtils.BuildBST(new int[] {1,54,6,7,8,9,6,456,8,7564,256,67,78,678,4567,679,78,45,87,9,3,9,498,500,450,498,497});
            VisualBinTree<int>.DrawTree(t);
            BSTUtils.InsertIntoBST(t, 4566);
            VisualBinTree<int>.DrawTree(t);
            Console.WriteLine(BSTUtils.IsExist(t, 4556));
            Console.WriteLine(BSTUtils.GetMin(t));
            Console.WriteLine(BSTUtils.GetParent(t,4566).GetValue());

            Console.WriteLine("GETTING HERITAGE");

            Node<BinNode<int>> n = BSTUtils.GetHeritage(t, new BinNode<int>(496));

            while (n != null)
            {
                Console.WriteLine(n.GetValue());
                n = n.GetNext();
            }
            Console.WriteLine("SUCCESSOR");
            BinNode<int> succ = BSTUtils.Successor(t, new BinNode<int>(497));
            Console.WriteLine(succ.GetValue());

        }
    }
}
