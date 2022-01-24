using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace findMe
{
    class Program
    {

        static Random rnd = new Random();

        static void Main(string[] args)
        {

            int min;
            int max;

            do
            {

                Console.WriteLine("Number range must be at least 100.");

                Console.WriteLine("Min number: ");

                min = int.Parse(Console.ReadLine());

                Console.WriteLine("Max number: ");

                max = int.Parse(Console.ReadLine());

            } while (max+1 - min < 100);

            Console.WriteLine("How many games do you wanna play? ");

            int games = int.Parse(Console.ReadLine());
            int games_won = 0;
            int games_lost = 0;
            int turn_sum = 0;

            for (int i = 0; i < games; i++)
            {

                Console.WriteLine("Game #" + (i + 1));

                int num = rnd.Next(min, max + 1);

                int guess;

                int guess_index = 1;

                do
                {

                    Console.WriteLine($"guess #{guess_index}: Please guess a number 0-100");

                    guess = int.Parse(Console.ReadLine());

                    if (guess > num)
                    {
                        Console.WriteLine("The number is smaller");
                    }

                    else if (guess < num)
                    {
                        Console.WriteLine("The number is bigger");
                    }
                    else
                    {
                        Console.WriteLine($"Well Done! You have guessed the number after {guess_index} attempts.");
                        games_won++;
                        turn_sum += guess_index;
                        break;
                    }

                    guess_index++;

                    if (guess_index == 11)
                    {
                        Console.WriteLine($"sorry, you have reached maximum attempts - the number was {num}");
                        games_lost++;

                    }

                } while (guess != num && guess_index <= 10);

                Console.WriteLine("Games won: " + games_won);
                Console.WriteLine("Games lost: " + games_lost);
                Console.WriteLine("Average turns: " + (turn_sum / games_won));

            }

        }
    }
}
