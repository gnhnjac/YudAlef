using System;

namespace ExtraEx
{
    class Program
    {

        static Random rand = new Random();

        static int[] shuffle(int N)
        {

            int[] arr = new int[N];

            for (int i = 0; i < arr.Length; i++)
            {

                arr[i] = i+1;

            }

            for (int i = N-1; i >= 0; i--)
            {
                int ind = rand.Next(N);
                int temp = arr[i];
                arr[i] = arr[ind];
                arr[ind] = temp;

            }

            return arr;

        }


        static bool ticket_counter(int tickets, int profit)
        {

            /* 
             
               Returns true if found a result
               Find how many tickets there are of each 3, 10, and 15 dollar variants given the parameters
             
            */


            for (int i = 0; i < tickets; i++)
            {
                for (int j = 0; j < tickets; j++)
                {

                    if ((7 * i + 12 * j) == profit - 3 * tickets)
                    {
                        Console.WriteLine($"The amount of 3 dollar tickets bought: {tickets-i-j} \n" +
                                          $"The amount of 10 dollar tickets bought: {i} \n" +
                                          $"The amount of 15 dollar tickets bought: {j} ");

                        return true;
                    }
                }
            }

            return false;

        }

        static void Main(string[] args)
        {

            /* Ex 1 */

            int[] ex1arr = shuffle(10);

            for (int i = 0; i < ex1arr.Length; i++)
            {

                Console.WriteLine(ex1arr[i]);

            }

            Console.WriteLine("_________________________");

            /* Ex 2 */

            int[] ex2arr = shuffle(10);

            int dupnum = rand.Next(ex2arr.Length)+1;

            int replaceindex = rand.Next(ex2arr.Length);

            ex2arr[replaceindex] = dupnum;

            for (int i = 0; i < ex2arr.Length; i++)
            {

                Console.WriteLine(ex2arr[i]);

            }

            for (int i = 0; i < ex2arr.Length; i++)
            {

                if (ex2arr[Math.Abs(ex2arr[i]) - 1] >= 0)
                    ex2arr[Math.Abs(ex2arr[i]) - 1] = -ex2arr[Math.Abs(ex2arr[i]) - 1];
                else
                    Console.WriteLine("The duplicate number is " + Math.Abs(ex2arr[i]));

            }

            for (int i = 0; i < ex2arr.Length; i++)
            {

                if (ex2arr[i] >= 0)
                {
                    Console.WriteLine("The missing number is " + (i + 1));
                    break;
                }
            }

            Console.WriteLine("_________________________");

            /* Ex 3 */

            ticket_counter(100, 400);

        }
    }
}
