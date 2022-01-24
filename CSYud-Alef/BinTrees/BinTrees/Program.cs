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
            BinNode<int> t = TreeUtils.BuildTree();
            TreeUtils.PrintLevelOrder(t);

        }
    }
}
