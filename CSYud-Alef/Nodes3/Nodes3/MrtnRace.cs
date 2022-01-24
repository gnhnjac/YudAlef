using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Nodes3
{
    class MrtnRace
    {
        public string countrey { get; set; }
        public int yearMrtn { get; set; }
        public Node<MrtnRunner> lstM { get; set; }

        public MrtnRace(string c, int y, Node<MrtnRunner> lst = null)
        {


            countrey = c;
            yearMrtn = y;
            lstM = lst;

        }

        public void AddMrtnToRunner(string id, int score)
        {
            Node<MrtnRunner> head = lstM;
            while (head != null)
            {

                if (head.GetValue().GetId() == id)
                {

                    Node<ItemMrtn> run_head = head.GetValue().GetPrevMarathons();

                    if (run_head == null)
                    {

                        head.GetValue().SetPrevMarathons(new Node<ItemMrtn>(new ItemMrtn(yearMrtn, score), null));

                    }
                    else
                    {

                        while (run_head.HasNext())
                        {

                            run_head = run_head.GetNext();

                        }

                        run_head.SetNext(new Node<ItemMrtn>(new ItemMrtn(yearMrtn, score), null));

                    }
                    
                    break;

                }

                head = head.GetNext();

            }

        }



    }
}
