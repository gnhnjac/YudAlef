using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Queue
{
    public class NumberLog
    {

        int amount;
        int num;

        public NumberLog(int a, int n)
        {

            amount = a;
            num = n;

        }

        public override string ToString()
        {
            return $"{num}: {amount}";
        }

    }
}
