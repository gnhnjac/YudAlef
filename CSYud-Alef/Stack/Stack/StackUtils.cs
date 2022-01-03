using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Stack
{
    static class StackUtils<T>
    {

        public static void PrintStack(StackL<T> st)
        {

            Console.WriteLine(st.ToString());

        }

        public static StackL<T> CreateStackFromArray(T[] arr)
        {

            StackL< T > new_stack = new StackL<T>();

            for (int i = arr.Length-1; i>=0; i--)
            {

                new_stack.Push(arr[i]);

            }

            return new_stack;

        }

        public static int SpilledOn<T>(StackL<T> to, StackL<T> from)
        {

            int i = 0;

            while (!from.IsEmpty())
            {

                to.Push(from.Pop());

                i++;

            }

            return i;


        }

        public static StackL<T> Clone<T>(StackL<T> s)
        {

            StackL<T> temp_s = new StackL<T>();
            while (!s.IsEmpty())
            {

                temp_s.Push(s.Pop());

            }

            StackL<T> new_s = new StackL<T>();
            while (!temp_s.IsEmpty())
            {

                T val = temp_s.Pop();

                s.Push(val);
                new_s.Push(val);

            }

            return new_s;
            

        }

        public static int GetSize<T>(StackL<T> s)
        {

            StackL<T> temp_s = Clone(s);

            int len = 0;
            while (!temp_s.IsEmpty())
            {

                temp_s.Pop();
                len++;

            }

            return len;

        }

        public static int GetSizeRec<T>(StackL<T> s)
        {

            if (s.IsEmpty())
                return 0;

            T val = s.Pop();
            int prev = GetSizeRec(s);
            s.Push(val);

            return 1 + prev;

        }

        public static int Sum(StackL<int> s)
        {

            StackL<int> temp_s = Clone(s);

            int sum = 0;
            while (!temp_s.IsEmpty())
            {

                sum += temp_s.Pop();

            }

            return sum;

        }

        public static int SumRec(StackL<int> s)
        {

            if (s.IsEmpty())
                return 0;

            int val = s.Pop();
            int prev = SumRec(s);
            s.Push(val);

            return val + prev;

        }

        public static T RemoveButtom<T>(StackL<T> stk)
        {

            StackL<T> temp_s = new StackL<T>();

            T val = default(T);
            while (!stk.IsEmpty())
            {

                val = stk.Pop();

                if (!stk.IsEmpty())
                    temp_s.Push(val);
            }

            while (!temp_s.IsEmpty())
                stk.Push(temp_s.Pop());

            return val;

        }

        public static T RemovePos<T>(StackL<T> st, int n)
        {

            StackL<T> temp_s = new StackL<T>();

            int count = 0;
            T val = default(T);
            while (count != n)
            {

                val = st.Pop();

                count++;

                if (count != n)
                    temp_s.Push(val);

            }

            while (!temp_s.IsEmpty())
                st.Push(temp_s.Pop());

            return val;

        }

        public static void AddValueToStackButtom<T>(StackL<T> stk, T e)
        {

            StackL<T> temp = new StackL<T>();

            while (!stk.IsEmpty())
                temp.Push(stk.Pop());

            stk.Push(e);

            while (!temp.IsEmpty())
                stk.Push(temp.Pop());


        }

        public static void InsertAtPos<T>(StackL<T> st, T e, int n)
        {

            StackL<T> temp = new StackL<T>();

            int count = 0;
            while (count != n)
            {

                temp.Push(st.Pop());

                count++;

            }

            st.Push(e);

            while (!temp.IsEmpty())
                st.Push(temp.Pop());


        }

        public static bool IsSorted(StackL<int> s)
        {

            StackL<int> tmp = Clone(s);

            while (!tmp.IsEmpty())
            {

                int val = tmp.Pop();
                if (!tmp.IsEmpty())
                {
                    int val2 = tmp.Pop();
                    tmp.Push(val2);

                    if (val > val2)
                        return false;
                }
            }

            return true;

        }

        public static bool IsSortedRec(StackL<int> s)
        {

            if (s.IsEmpty())
                return true;

            int val = s.Pop();
            bool prev = IsSortedRec(s);

            bool conclusion = true;

            if (!s.IsEmpty())
            {
                int val2 = s.Pop();
                s.Push(val2);

                conclusion = val < val2;

            }

            s.Push(val);

            return conclusion && prev;

        }

        public static bool IsExist(StackL<int> s, int val)
        {

            StackL<int> tmp = Clone(s);

            while (!tmp.IsEmpty())
            {

                if (val == tmp.Pop())
                    return true;

            }
            return false;

        }

        public static bool IsExistRec(StackL<int> s, int val)
        {

            if (s.IsEmpty())
                return false;

            int s_val = s.Pop();
            bool prev = IsExistRec(s, val);
            s.Push(s_val);

            return val == s_val && prev;


        }

        public static StackL<int> BuildSort(int[] arr)
        {

            Array.Sort(arr);

            return StackUtils<int>.CreateStackFromArray(arr);

        }

        public static StackL<int> BuildSort(Node<int> ls)
        {
            int len = 0;
            Node<int> head = ls;
            while (head != null)
            {

                head = head.GetNext();
                len++;
            
            }

            int[] arr = new int[len];

            int i = 0;
            while (ls != null)
            {

                arr[i] = ls.GetValue();

                ls = ls.GetNext();

                i++;

            }

            return BuildSort(arr);


        }

        public static void MoveTop2Buttom<T>(StackL<T> stk)
        {

            AddValueToStackButtom(stk, stk.Pop());

        }

        public static void MoveButtom2Top<T>(StackL<T> stk)
        {

            stk.Push(RemoveButtom(stk));

        }

        public static void PrintHead2Bot(StackL<T> stk)
        {

            StackL<T> tmp = Clone(stk);

            while (!tmp.IsEmpty())
            {

                Console.WriteLine(tmp.Pop().ToString());

            }

        }

        public static void PrintBot2Head(StackL<T> stk)
        {

            StackL<T> tmp = Clone(stk);
            StackL<T> prnt = new StackL<T>();

            while (!tmp.IsEmpty())
                prnt.Push(tmp.Pop());
            
            while (!prnt.IsEmpty())
                Console.WriteLine(prnt.Pop());


        }

        public static void KeepSmallerThanK(StackL<int> stk, int k)
        {

            do
            {

                int val = stk.Pop();

                if (val < k)
                {

                    stk.Push(val);
                    break;

                }


            } while (true && !stk.IsEmpty());

        }

        public static void KeepBiggerThanK(StackL<int> stk, int k)
        {

            StackL<int> tmp = new StackL<int>();

            while (!stk.IsEmpty())
            {

                int val = stk.Pop();

                if (val > k)
                    tmp.Push(val);


            }

            while (!tmp.IsEmpty())
            {

                stk.Push(tmp.Pop());

            }

        }

        public static void LessThanKm(StackL<Point> stk, Point p)
        {

            if (stk.IsEmpty())
                return;

            Point stk_p = stk.Pop();

            LessThanKm(stk, p);

            int x_dst = Math.Abs(stk_p.GetX() - p.GetX());

            int y_dst = Math.Abs(stk_p.GetY() - p.GetY());

            double dst = Math.Sqrt(x_dst*x_dst + y_dst*y_dst);

            if (dst < 1000)
                stk.Push(stk_p);

        }

        public static bool AreStacksCircular(StackL<int> stk1, StackL<int> stk2)
        {

            int len = GetSizeRec(stk1); ;
            int len2 = GetSizeRec(stk2);

            if (len != len2)
                return false;

            StackL<int> stk1_orig = Clone(stk1);

            StackL<int> stk2_orig = Clone(stk2);

            for (int i = 0; i < len; i++)
            {

                StackL<int> clone = Clone(stk1_orig);
                StackL<int> clone2 = Clone(stk2_orig);

                int count = 0;

                while (!clone.IsEmpty())
                {

                    if (clone.Pop() == clone2.Pop())
                        count++;

                }

                if (count == len)
                    return true;

                MoveTop2Buttom(stk1_orig);

            }

            return false;

        }

        public static int RemoveAllDisturbances(StackL<int> stk, int min, int max, bool first)
        {

            if (stk.IsEmpty())
                return -1;

            int val = stk.Pop();

            int removed = RemoveAllDisturbances(stk, min, max, false);

            if ((val > min && val < max) || removed == -1 || first)
            {
                stk.Push(val);

                if (removed == -1)
                    removed = 0;

                return 0 + removed;
            }

            return 1 + removed;
        }


        public static Node<TwoItems> isRanged(Node<StackL<int>> lst)
        {

            Node<TwoItems> orig_results = new Node<TwoItems>(null, null);
            Node<TwoItems> results = orig_results;

            int serial_num = 1;
            while (lst != null)
            {

                StackL<int> s = lst.GetValue();

                int bot = RemoveButtom(s);
                AddValueToStackButtom(s, bot);

                int top = s.Pop();
                s.Push(top);

                if (bot > top)
                {

                    s.Pop();
                    s.Push(bot);

                    RemoveButtom(s);
                    AddValueToStackButtom(s, top);

                    int tmp = bot;
                    bot = top;
                    top = tmp;

                }

                int removed = RemoveAllDisturbances(s, bot, top, true);

                TwoItems pair = new TwoItems(serial_num, removed);

                results.SetValue(pair);

                Node<TwoItems> new_pair = new Node<TwoItems>(null, null);

                results.SetNext(new_pair);

                results = results.GetNext();

                serial_num++;
                lst = lst.GetNext();

            }

            return orig_results;

        }






    }
}
