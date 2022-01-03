using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Nodes3
{
    class MrtnRunner
    {

        private string id;
        private int yearB;
        private Node<ItemMrtn> lst;

        public MrtnRunner(string id, int year, Node<ItemMrtn> lst = null)
        {

            this.id = id;
            this.yearB = year;
            this.lst = lst;

        }

        public string GetId()
        {

            return this.id;

        }

        public int GetBirthYear()
        {

            return this.yearB;

        }

        public Node<ItemMrtn> GetPrevMarathons()
        {

            return this.lst;

        }

        public void SetId(string id)
        {

            this.id = id;

        }

        public void SetBirthYear(int year)
        {

            this.yearB = year;

        }

        public void SetPrevMarathons(Node<ItemMrtn> lst)
        {

            this.lst = lst;

        }

    }
}
