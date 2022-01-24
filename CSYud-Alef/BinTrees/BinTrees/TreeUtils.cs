using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Unit4;
using VisualTree;

namespace BinTrees
{
    static class TreeUtils
    {

        static public BinNode<int> BuildTree()
        {
            VisualBinTree<int>.DrawTree();
            return VisualBinTree<int>.GetTree();
        }
        static public void PrintPreOrder(BinNode<int> tree)
        {
            if (tree == null)
                return;
            Console.Write(tree.GetValue());
            PrintPreOrder(tree.GetLeft());
            PrintPreOrder(tree.GetRight());
        }
        static public void PrintInOrder(BinNode<int> tree)
        {
            if (tree == null)
                return;
            PrintInOrder(tree.GetLeft());
            Console.Write(tree.GetValue());
            PrintInOrder(tree.GetRight());
        }
        static public void PrintPostOrder(BinNode<int> tree)
        {
            if (tree == null)
                return;
            PrintPostOrder(tree.GetLeft());
            PrintPostOrder(tree.GetRight());
            Console.Write(tree.GetValue());
        }
        static public void PrintAll(BinNode<int> tree)
        {
            Console.Write("Print Pre Order: ");
            PrintPreOrder(tree);
            Console.Write("\nPrint In Order: ");
            PrintInOrder(tree);
            Console.Write("\nPrint Post Order: ");
            PrintPostOrder(tree);

        }
        static public BinNode<int> BuildTreeFromFile(string filename)
        {
            return VisualBinTree<int>.GetTree(filename);
        }
        static public int CountNodes(BinNode<int> tree)
        {
            if (tree == null)
                return 0;
            return 1 + CountNodes(tree.GetLeft()) + CountNodes(tree.GetRight());
        }
        static public int SumNodes(BinNode<int> tree)
        {
            if (tree == null)
                return 0;
            return tree.GetValue() + SumNodes(tree.GetLeft()) + SumNodes(tree.GetRight());
        }
        static public int SumEven(BinNode<int> tree)
        {
            if (tree == null)
                return 0;

            return (tree.GetValue() % 2 == 0 ? tree.GetValue() : 0) + SumEven(tree.GetLeft()) + SumEven(tree.GetRight());
        }

        static public int SumPositive(BinNode<int> tree)
        {
            if (tree == null)
                return 0;

            return (tree.GetValue() > 0 ? tree.GetValue() : 0) + SumEven(tree.GetLeft()) + SumEven(tree.GetRight());
        }

        static public bool IsLeaf(BinNode<int> tree)
        {
            return tree.GetRight() == null && tree.GetLeft() == null;
        }
        static public int CountLeaves(BinNode<int> tree)
        {
            if (tree == null)
                return 0;

            return (IsLeaf(tree) ? 1 : 0) + CountLeaves(tree.GetLeft()) + CountLeaves(tree.GetRight());
        }
        static public int MaxNum(BinNode<int> tree)
        {
            if (tree == null)
                return int.MinValue;
            return Math.Max(Math.Max(tree.GetValue(), MaxNum(tree.GetRight())), Math.Max(tree.GetValue(), MaxNum(tree.GetLeft())));
        }
        static public int SumRight(BinNode<int> tree)
        {
            if (tree == null)
                return 0;
            return SumRight(tree.GetRight()) + tree.GetValue();
        }
        static public int LeftCount(BinNode<int> tree)
        {
            if (tree == null)
                return 0;
            return LeftCount(tree.GetLeft()) + 1;
        }

        static public void BelowFather(BinNode<int> tree)
        {
            if (tree == null)
                return;
            if (tree.GetRight() != null && tree.GetValue() > tree.GetRight().GetValue())
            {
                Console.Write(tree.GetRight().GetValue() + ",");
            }
            if (tree.GetLeft() != null && tree.GetValue() > tree.GetLeft().GetValue())
            {
                Console.Write(tree.GetLeft().GetValue() + ",");
            }
            BelowFather(tree.GetRight());
            BelowFather(tree.GetLeft());
        }
        static public void TwoSons(BinNode<int> tree)
        {
            if (tree == null)
                return;

            if (tree.GetRight() != null && tree.GetLeft() != null &&
                (tree.GetValue() > tree.GetRight().GetValue() || tree.GetValue() > tree.GetLeft().GetValue()))
            {
                Console.Write(tree.GetValue() + ",");
            }

            TwoSons(tree.GetRight());
            TwoSons(tree.GetLeft());
        }

        static public int GetHeight(BinNode<int> t)
        {

            if (t == null)
                return -1;

            return 1 + Math.Max(GetHeight(t.GetLeft()), GetHeight(t.GetRight()));

        }

        public static bool IsBalanced(BinNode<int> t)
        {
            if (t == null)
                return true;
            return Math.Abs(GetHeight(t.GetLeft()) - GetHeight(t.GetRight())) <= 1 && IsBalanced(t.GetRight()) && IsBalanced(t.GetLeft());
        }
        public static int CountOrphans(BinNode<int> t)
        {
            if (t == null)
                return 0;
            if (t.GetLeft() != null && t.GetRight() == null)
                return 1 + CountOrphans(t.GetLeft());
            else if (t.GetLeft() == null && t.GetRight() != null)
                return 1 + CountOrphans(t.GetRight());
            return CountOrphans(t.GetRight()) + CountOrphans(t.GetLeft());
        }
        public static int CountParents4Twins(BinNode<int> t)
        {
            if (t == null)
                return 0;
            if (t.GetLeft() != null && t.GetRight() != null)
                return 1 + CountParents4Twins(t.GetLeft()) + CountParents4Twins(t.GetRight());
            return CountParents4Twins(t.GetLeft()) + CountParents4Twins(t.GetRight());
        }
        public static int BiggerThanX(BinNode<int> t, int x)
        {
            if (t == null)
                return 0;
            if (t.GetValue() > x)
                return 1 + BiggerThanX(t.GetLeft(), x) + BiggerThanX(t.GetRight(), x);
            return BiggerThanX(t.GetLeft(), x) + BiggerThanX(t.GetRight(), x);
        }
        public static void PrintLevelOrder(BinNode<int> t)
        {
            Queue<BinNode<int>> q = new Queue<BinNode<int>>();
            q.Insert(t);
            while (!q.IsEmpty())
            {
                BinNode<int> node = q.Remove();
                Console.Write(node.GetValue() + ", ");
                if (node.GetLeft() != null)
                    q.Insert(node.GetLeft());
                if (node.GetRight() != null)
                    q.Insert(node.GetRight());
            }
        }

    }
}
