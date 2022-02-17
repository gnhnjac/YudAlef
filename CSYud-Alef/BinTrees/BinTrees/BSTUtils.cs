using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Unit4;

namespace BinTrees
{
    internal static class BSTUtils
    {

        public static BinNode<int> BuildBST(int[] arr)
        {
            arr = arr.Distinct().ToArray();
            Array.Sort(arr);

            BinNode<int> t = new BinNode<int>(0);

            BuildBSTRec(t,arr,0,arr.Length);

            return t;

        }

        public static void BuildBSTRec(BinNode<int> t,int[] arr,int ind1, int ind2)
        {

            t.SetValue(arr[ind1 + ((ind2-ind1) / 2)]);

            if ((ind1 + ind2) / 2 - ind1 > 1)
            {
                t.SetLeft(new BinNode<int>(0));
                BuildBSTRec(t.GetLeft(), arr, ind1, (ind1 + ind2) / 2);
            }
            if (ind2 - (ind1 + ind2) / 2 > 1)
            {
                t.SetRight(new BinNode<int>(0));
                BuildBSTRec(t.GetRight(), arr, (ind1 + ind2) / 2, ind2);
            }

        }

        public static void InsertIntoBSTRec(BinNode<int> t, int val)
        {

            if (val > t.GetValue())
            {
                if (t.GetRight() == null)
                {
                    t.SetRight(new BinNode<int>(val));
                    return;
                }
                InsertIntoBSTRec(t.GetRight(), val);
            }
            else if (val < t.GetValue())
            {

                if (t.GetLeft() == null)
                {
                    t.SetLeft(new BinNode<int>(val));
                    return;
                }
                InsertIntoBSTRec(t.GetLeft(), val);
            }
        }

        public static void InsertIntoBST(BinNode<int> t, int val)
        {
            bool done = false;
            while(!done)
            {

                if (val > t.GetValue() && t.GetRight() == null)
                {
                    t.SetRight(new BinNode<int>(val));
                    done = true;
                }
                else if (val > t.GetValue())
                {

                    t = t.GetRight();

                }
                else if (val < t.GetValue() && t.GetLeft() == null)
                {
                    t.SetLeft(new BinNode<int>(val));
                    done = true;
                }
                else if(val < t.GetValue())
                {

                    t = t.GetLeft();

                }

            }

        }

        public static bool IsExist(BinNode<int> t, int val)
        {

            while(t != null)
            {

                if (t.GetRight() != null && t.GetRight().GetValue() == val)
                    return true;
                else if (t.GetValue() < val)
                    t = t.GetRight();
                else if (t.GetLeft() != null && t.GetLeft().GetValue() == val)
                    return true;
                else if (t.GetValue() > val)
                    t = t.GetLeft();

            }

            return false;

        }

        public static bool IsExistRec(BinNode<int> t, int val)
        {

            if (t == null)
                return false;

            if (t.GetRight() != null && t.GetRight().GetValue() == val)
                return true;
            if (t.GetLeft() != null && t.GetLeft().GetValue() == val)
                return true;

            return IsExistRec(t.GetLeft(), val) || IsExistRec(t.GetRight(),val);

        }

        public static int GetMin(BinNode<int> t)
        {

            while (t.GetLeft() != null)
                t = t.GetLeft();

            return t.GetValue();

        }


        public static int GetMinRec(BinNode<int> t)
        {

            if(t.GetLeft() == null)
                return t.GetValue();

            return GetMinRec(t.GetLeft());

        }

        public static int GetMax(BinNode<int> t)
        {

            while (t.GetRight() != null)
                t = t.GetRight();

            return t.GetValue();

        }


        public static int GetMaxRec(BinNode<int> t)
        {

            if (t.GetRight() == null)
                return t.GetValue();

            return GetMaxRec(t.GetRight());

        }

        public static BinNode<int> GetParent(BinNode<int> t, int val)
        {

            if (t == null)
                return new BinNode<int>(0);

            if ((t.GetLeft() != null && t.GetLeft().GetValue() == val) || (t.GetRight() != null && t.GetRight().GetValue() == val))
                return t;
            
            if (t.GetValue() < val)
                return GetParent(t.GetRight(), val);

            return GetParent(t.GetLeft(), val);

        }
        
        public static void InsertToEnd(Node<BinNode<int>> n,BinNode<int> n2)
        {

            while (n.GetNext() != null)
                n = n.GetNext();

            n.SetNext(new Node<BinNode<int>>(n2));

        }

        public static Node<BinNode<int>> GetHeritage(BinNode<int> t, BinNode<int> node)
        {

            if (t == null)
                return new Node<BinNode<int>>(new BinNode<int>(0));
           

            if ((t.GetLeft() != null && t.GetLeft().GetValue() == node.GetValue()) || (t.GetRight() != null && t.GetRight().GetValue() == node.GetValue()))
                return new Node<BinNode<int>>(t);

            Node<BinNode<int>> n;
            if (t.GetValue() < node.GetValue())
            {
                n = GetHeritage(t.GetRight(), node);
                InsertToEnd(n, t);
                return n;
            }

            n = GetHeritage(t.GetLeft(), node);
            InsertToEnd(n, t);
            return n;

        }

        public static BinNode<int> Successor(BinNode<int> bt, BinNode<int> n)
        {

            Node<BinNode<int>> heritage = GetHeritage(bt,n);

            while (heritage != null)
            {

                if (heritage.GetValue().GetValue() > n.GetValue())
                    return heritage.GetValue();

                heritage = heritage.GetNext();

            }

            return null;

        }

    }
}
