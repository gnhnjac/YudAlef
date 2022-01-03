using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Stack
{
    class TwoItems
    {

        
            private int num1;
            private int num2;

            public TwoItems(int number1, int number2)
            {
                this.num1 = number1;
                this.num2 = number2;
            }
            public int GetNum1()
            {
                return this.num1;
            }
            public int GetNum2()
            {
                return this.num2;
            }
            public void SetNum1(int number1)
            {
                this.num1 = number1;
            }
            public void SetNum2(int number2)
            {
                this.num2 = number2;
            }
            public override string ToString()
            {
                return $"{this.num1},{this.num2}";
            }
        }

    
}
