using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Nodes3
{
    class Program
    {

        static Node<Smell> SmellsInCommon(Node<Smell> p1, Node<Smell> p2)
        {

            Node<Smell> head = null;

            while (p1 != null && p2 != null)
            {

                if (p1.GetValue().GetName() == p2.GetValue().GetName() && p1.GetValue().GetStrength() == p2.GetValue().GetStrength())
                    head = new Node<Smell>(p1.GetValue(), head);

                p1 = p1.GetNext();
                p2 = p2.GetNext();

            }

            return head;

        }

        static Node<Card> SortAndCountUnique(Node<Card> lst)
        {

            Node<Card> head = new Node<Card>(null, lst);
            Node<Card> original_head = head;
            while (head.GetNext().HasNext())
            {

                if (head.GetNext().GetValue().GetNum() != head.GetNext().GetNext().GetValue().GetNum())
                {

                    Card saved = head.GetNext().GetValue();

                    head.SetNext(head.GetNext().GetNext());

                    Node<Card> temp = original_head;

                    bool found = false;

                    while (temp.HasNext())
                    {

                        if (saved.GetNum() == temp.GetNext().GetValue().GetNum())
                        {

                            Node<Card> n = new Node<Card>(saved, temp.GetNext());

                            temp.SetNext(n);

                            found = true;
                            
                            break;

                        }

                        temp = temp.GetNext();

                    }

                    if (!found)
                    {

                        Node<Card> n = new Node<Card>(saved, original_head.GetNext());
                        original_head.SetNext(n);

                    }

                }

                head = head.GetNext();

            }

            head = original_head.GetNext();

            int unique = 1;
            while (head.HasNext())
            {

                if (head.GetValue().GetNum() != head.GetNext().GetValue().GetNum())
                    unique++;

                head = head.GetNext();

            }

            head.SetNext(new Node<Card>(new Card(unique, "white"), null));


            return original_head.GetNext();

        }

        static Node<Card> CreateListFromArray2(Card[] a)
        {

            Node<Card> head, tail = null;

            head = new Node<Card>(a[0]);

            tail = head;

            for (int i = 1; i < a.Length; i++)
            {

                tail.SetNext(new Node<Card>(a[i]));

                tail = tail.GetNext();


            }

            return head;


        }

        static Node<int> CreateListFromArray(int[] a)
        {

            Node<int> head, tail = null;

            head = new Node<int>(a[0]);

            tail = head;

            for (int i = 1; i < a.Length; i++)
            {

                tail.SetNext(new Node<int>(a[i]));

                tail = tail.GetNext();


            }

            return head;


        }

        static void PrintList2(Node<int> head)
        {

            while (head != null)
            {

                Console.Write(head.GetValue());
                head = head.GetNext();

            }

        }

        static void PrintList(Node<Card> head)
        {

            while (head != null)
            {

                Console.WriteLine(head.GetValue().GetNum() + " " + head.GetValue().GetColor());
                head = head.GetNext();

            }

        }

        public int CountPersistentRunners(MrtnRace race)
        {

            int persistent = 0;

            Node<MrtnRunner> runners = race.lstM;

            while (runners != null)
            {

                Node<ItemMrtn> head = runners.GetValue().GetPrevMarathons();

                int sequence = 1;

                while (head.HasNext())
                {

                    if (head.GetValue().GetYear() + 1 == head.GetNext().GetValue().GetYear())
                    {

                        sequence++;

                        if (sequence == 3)
                        {

                            persistent++;
                            break;

                        }

                    }
                    else
                    {

                        sequence = 1;

                    }

                    head = head.GetNext();

                }

                runners = runners.GetNext();


            }


            return persistent;

        }

        static int RecursiveQ(Node<int> lst)
        {

            if (!lst.GetNext().HasNext())
                return Math.Abs(lst.GetValue() - lst.GetNext().GetValue());

            Node<int> next_lst = new Node<int>(0, null);

            Node<int> head_ptr = next_lst;

            while (lst.HasNext())
            {

                int diff = Math.Abs(lst.GetValue() - lst.GetNext().GetValue());

                Node<int> diff_node = new Node<int>(diff, null);

                next_lst.SetNext(diff_node);

                next_lst = diff_node;

                lst = lst.GetNext();

            }

            PrintList2(head_ptr.GetNext());
            Console.WriteLine();

            return RecursiveQ(head_ptr.GetNext());


        }

        static void Main(string[] args)
        {
            /*
            Node<Card> lst = CreateListFromArray2(new Card[]{new Card(3,"red"), new Card(4, "red"),new Card(2, "red"),new Card(7, "red"),new Card(4, "red"),new Card(7, "red"), new Card(3, "red"), new Card(3, "red") });

            lst = SortAndCountUnique(lst);

            PrintList(lst);

            lst = CreateListFromArray2(new Card[] { new Card(3, "red")});

            lst = SortAndCountUnique(lst);

            PrintList(lst);
            */


            Node<int> lst = CreateListFromArray(new int[]{1,2,3,4,6,7,9,3,7,3});

            Console.WriteLine(RecursiveQ(lst));

        }
    }
}
