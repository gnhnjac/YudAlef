using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace forPuzzle
{
    class Program
    {

        static void level1()
        {

            int sum = 0;
            for (int i = 2; i < 9; i++)
            {

                if(i != 5)
                {

                    Console.WriteLine(i);

                    sum += i;

                }

            }

            Console.WriteLine("sum=" + sum);

        }

        static void level2()
        {

            for (int a = 30, b = 30; a < 40; a++, b+=a)
            {

                Console.WriteLine(a);

                Console.WriteLine(b);

            }

        }

        static void level3()
        {

            int sum = 0;

            for (int i = -10; i <= 10; i += 2)
            {

                Console.WriteLine(i);

                sum += Math.Abs(i/2);

            }

            Console.WriteLine("sum=" + sum);

        }

        static void level4()
        {

            for(int i = 1; i <= 10; i++)
            {

                Console.WriteLine(i);
                Console.WriteLine($"10{i:00}");
                Console.WriteLine(i / 2);
                Console.WriteLine("--");

            }

        }

        static void level5()
        {

            for(int i = 300; i > -400; i--)
            {

                Console.WriteLine($"i = {i} digit= {i / 10 % 10}");

            }

        }

        static void level6()
        {

            for(char i = 'E'; i <= 'K'; i++)
            {

                Console.Write(i);

                if (i != 'K')
                    Console.Write(',');

            }

            Console.WriteLine();

        }

        static void level7()
        {

            int sum = 0;

            for(int i = 0, t = 1; i < 100; i += 10, t += 1)
            {

                Console.WriteLine("i=" + i);
                Console.WriteLine("t=" + t);
                Console.WriteLine("sum=" + sum);
                Console.WriteLine("--");

                if(sum < 21)
                    sum += t;

            }

        }

        static void level8()
        {

            int n = 1;

            int num;

            int sum = 0;

            do
            {

                Console.WriteLine("Enter Number # " + n);
                num = int.Parse(Console.ReadLine());

                if (num % 2 == 0 && (num % 4 != 0) && num > 0)
                    sum += num;

                n++;

            } while (num >= 0);

            Console.WriteLine("Total sum=" + sum);


        }

        static void Main(string[] args)
        {

            // level1(); 1111
            // level2(); nice
            // level3(); good
            // level4(); well done
            // level5(); go go go
            // level6(); perfect
            // level7(); keep up
            level8(); //smart

        }
    }
}
