using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Nodes3
{
    class ItemMrtn
    {

        static int year;
        static int score;

        public ItemMrtn(int y, int s)
        {

            year = y;
            score = s;

        }

        public int GetYear()
        {

            return year;

        }

        public int GetScore()
        {

            return score;

        }

        public void SetYear(int y)
        {

            year = y;

        }

        public void SetScore(int s)
        {

            score = s;

        }

    }
}
