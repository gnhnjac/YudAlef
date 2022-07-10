using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Nodes3
{
    class Card
    {

        private int num;
        private string color;

        public Card(int num, string color)
        {

            this.num = num;
            this.color = color;

        }

        public int GetNum()
        {

            return num;

        }

        public string GetColor()
        {

            return color;

        }

        public void SetNum(int n)
        {

            num = n;

        }

        public void SetColor(string color)
        {

            this.color = color;

        }


    }
}
