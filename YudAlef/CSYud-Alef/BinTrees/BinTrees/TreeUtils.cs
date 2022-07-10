using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Unit4;
using VisualTree;

namespace BinTrees
{
    static class TreeUtils<T>
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

        public static void InsertIdenticalTwin(BinNode<int> t)
        {

            if (t == null)
                return;

            InsertIdenticalTwin(t.GetRight());
            InsertIdenticalTwin(t.GetLeft());

            if (t.GetRight() == null && t.GetLeft() != null)
            {
                t.SetRight(new BinNode<int>(t.GetLeft().GetValue()));

            }
            else if (t.GetRight() != null && t.GetLeft() == null)
            {

                t.SetLeft(new BinNode<int>(t.GetRight().GetValue()));

            }

        }

        public static void RemoveLeaves(BinNode<int> t)
        {

            if (t == null)
                return;

            BinNode<int> RightSon = t.GetRight();
            BinNode<int> LeftSon = t.GetLeft();

            if (RightSon.GetLeft() == null && RightSon.GetRight() == null)
                t.SetRight(null);
            if (LeftSon.GetLeft() == null && LeftSon.GetRight() == null)
                t.SetLeft(null);

            RemoveLeaves(RightSon);
            RemoveLeaves(LeftSon);

        }

        public static void PrintBiggerParents(BinNode<int> t)
        {

            if (t == null)
                return;

            if (t.GetValue() > t.GetLeft().GetValue() && t.GetValue() > t.GetRight().GetValue())
                Console.WriteLine(t.GetValue());

            PrintBiggerParents(t.GetLeft());
            PrintBiggerParents(t.GetRight());

        }

        public static int IdenticalTwins(BinNode<int> t)
        {

            if (t == null)
                return 0;

            if (t.GetLeft().GetValue() == t.GetRight().GetValue())
                return 1 + IdenticalTwins(t.GetLeft()) + IdenticalTwins(t.GetRight());
            return IdenticalTwins(t.GetLeft()) + IdenticalTwins(t.GetRight());

        }

        public static int PrintLessThanParent(BinNode<int> t)
        {

            if (t == null)
                return 0;

            int total = 0;

            if (t.GetLeft() == null)
                total++;
            else if(t.GetLeft().GetValue() < t.GetValue())
                total++;

            if (t.GetRight() == null)
                total++;
            else if (t.GetRight().GetValue() < t.GetValue())
                total++;

            return total + PrintLessThanParent(t.GetLeft()) + PrintLessThanParent(t.GetRight());

        }

        public static int GrandFatherSum(BinNode<int> t)
        {

            if (t == null)
                return 0;

            BinNode<int> RightSon = t.GetRight();
            BinNode<int> LeftSon = t.GetLeft();

            int total = 0;

            if (RightSon != null)
            {

                if (RightSon.GetRight() != null || RightSon.GetLeft() != null)
                    total++;

            }
            if (LeftSon != null)
            {

                if (LeftSon.GetRight() != null || LeftSon.GetLeft() != null)
                    total++;

            }

            return total + GrandFatherSum(RightSon) + GrandFatherSum(LeftSon);

        }

        public static bool AreAllInterchangesEven(BinNode<int> t)
        {

            if (t == null)
                return true;

            return t.GetRight().GetValue() + t.GetLeft().GetValue() % 2 == 0 && AreAllInterchangesEven(t.GetLeft()) && AreAllInterchangesEven(t.GetRight());

        }

        public static bool IsSumTree(BinNode<int> t)
        {

            if (t == null)
                return true;

            return t.GetRight().GetValue() + t.GetLeft().GetValue() == t.GetValue() && IsSumTree(t.GetRight()) && IsSumTree(t.GetLeft());

        }

        public static bool IsFull(BinNode<int> t)
        {

            if (t == null)
                return true;

            return ((t.GetLeft() != null && t.GetRight() != null) || (t.GetLeft() == null && t.GetRight() == null)) && IsFull(t.GetLeft()) && IsFull(t.GetRight());

        }

        public static int ChildSum(BinNode<int> t)
        {

            int right_sum = 0;
            int left_sum = 0;

            Queue<BinNode<int>> q = new Queue<BinNode<int>>();
            q.Insert(t);
            while(!q.IsEmpty())
            {

                t = q.Remove();

                if (t.GetLeft() != null && t.GetRight() == null)
                {
                    left_sum += t.GetLeft().GetValue();
                    q.Insert(t.GetLeft());
                } 
                else if(t.GetRight() != null && t.GetLeft() == null)
                {
                    right_sum += t.GetRight().GetValue();
                    q.Insert(t.GetRight());
                }
                else if(t.GetRight() != null && t.GetLeft() != null)
                {
                    q.Insert(t.GetLeft());
                    q.Insert(t.GetRight());
                }

            }

            return right_sum - left_sum;

        }

        public static bool AreSimilar(BinNode<int> t1, BinNode<int> t2)
        {

            if ((t1 == null && t2 != null) || (t2 == null && t1 != null))
                return false;
            else if (t1 == null && t2 == null)
                return true;

            return true && AreSimilar(t1.GetLeft(),t2.GetLeft()) && AreSimilar(t1.GetRight(),t2.GetRight());

        }

        public static int GetInterchangesAtLevel(BinNode<int> t,int lvl)
        {

            if (t == null)
                return 0;
            if (lvl == 0)
                return 1;

            return GetInterchangesAtLevel(t.GetLeft(),lvl-1) + GetInterchangesAtLevel(t.GetRight(),lvl-1);

        }

        public static int MostInterchangeHeight(BinNode<int> t)
        {
            int max = 0;
            int max_h = 0;
            for (int i = 0; i < GetHeight(t); i++)
            {
                int interchanges = GetInterchangesAtLevel(t, i);
                if (interchanges > max)
                {

                    max = interchanges;
                    max_h = i;

                }

            }

            return max_h;

        }

        public static Node<BinNode<T>> PrintFathers(BinNode<T> tree,BinNode<T> node)
        {

            Node<BinNode<int>> fathers = GetHeritage();

        }



    }
}
