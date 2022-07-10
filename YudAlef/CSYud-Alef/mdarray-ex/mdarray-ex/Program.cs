using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace mdarray_ex
{

    class Program
    {


        static int func(int [,] data)
        {
            int max_sum = 0;
            for (int i = 0; i < data.Length; i++)
            {
                int sum = 0;
                for (int j = 0; j <  data[0, i]; j++)
                {

                    sum += data[i, j % 4 + 1];

                }

                if (sum > max_sum)
                    max_sum = sum;

            }

            return max_sum;


        }


        static bool is_golden(int [,] data, int i, int j)
        {
            if (i > 0 && i < data.Length - 1)
            {

                if (data[i - 1, j] + data[i + 1, j] == data[i, j])
                    return true;


            } else if(j > 0 && j < data.GetLength(1))
            {


                if (data[i, j - 1] + data[i, j + 1] == data[i, j])
                    return true;

            }

            return false;

        }

        static bool is_surrounded(int [,] data, int i, int j)
        {

            if (data[i, j] != 1)
                return false;

            int i_seq = 0;
            bool seq_started = false;
            for (int k = 0; k < data.Length; k++)
            {

                if (seq_started && data[k, j] == 0)
                    break;

                if (data[k, j] == 1)
                {
                    seq_started = true;
                }

                if (seq_started)
                    i_seq++;

            }

            int j_seq = 0;
            seq_started = false;
            for (int k = 0; k < data.GetLength(1); k++) { 

                if (seq_started && data[i, k] == 0)
                    break;

                if (data[i, k] == 1)
                {
                    seq_started = true;
                }

                if (seq_started)
                    j_seq++;

            }

            if (i_seq == j_seq)
                return true;

            return false;

        }

        static int get_surrounded(int[,] data)
        {
            int count = 0;
            for (int i = 0; i < data.Length; i++)
            {

                for (int j = 0; j < data.GetLength(1); j++)
                {

                    if (is_surrounded(data, i, j))
                        count++;

                }

            }
            return count;

        }


        static void Main(string[] args)
        {
        }
    }
}
