using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BinNodeUtils
{
    class BinNode<T>
    {

        private BinNode<T> left;
        private BinNode<T> right;
        T val;


        public BinNode(T x)
        {

            val = x;

        }

        public BinNode(BinNode<T> left, T x, BinNode<T> right)
        {

            val = x;
            this.left = left;
            this.right = right;

        }

        public T GetValue()
        {

            return val;

        }

        public void SetValue(T x)
        {

            val = x;

        }

        public BinNode<T> GetLeft()
        {

            return left;

        }

        public BinNode<T> GetRight()
        {

            return right;

        }

        public void SetLeft(BinNode<T> n)
        {

            left = n;

        }

        public void SetRight(BinNode<T> n)
        {

            right = n;

        }

        public override string ToString()
        {

            return $"Value: {val}";

        }

    }
}
