using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using System.Globalization;

namespace Bulls_and_cows
{
    class Program
    {
        static int[] getHits(string key, string guess)
        {

            int bulls = 0;
            int cows = 0;

            for (int i = 0; i < key.Length; i++)
            {

                if (char.GetNumericValue(key[i]) == char.GetNumericValue(guess[i]))
                {

                    bulls++;

                }
                else
                {

                    for (int j = 0; j < guess.Length; j++)
                    {

                        if (j != i && char.GetNumericValue(key[i]) == char.GetNumericValue(guess[j]))
                        {

                            cows++;

                        }

                    }

                }

            }

            // returns array of bulls and cows
            return new int[2] { bulls, cows };

        }

        static bool isUnique(string guess)
        {

            for (int i = 0; i < guess.Length; i++)
            {

                for (int j = 0; j < guess.Length; j++)
                {

                    if (guess[i] == guess[j] && i != j)
                    {

                        return false;

                    }

                }

            }

            return true;

        }

        static bool isBannedGuess(int[] digits)
        {

            if (digits.Length != digits.Distinct().Count())
            {
                return true;
            }

            return false;

        }

        static int[] validifyDigits(int[] digits)
        {

            if (digits[3] == 10)
            {

                digits[3] = 0;
                digits[2]++;

            }

            if (digits[2] == 10)
            {

                digits[2] = 0;
                digits[1]++;

            }

            if (digits[1] == 10)
            {

                digits[1] = 0;
                digits[0]++;

            }

            return digits;

        }

        static int getValid(Case[] Cases)
        {

            int valid = 0;
            foreach (Case c in Cases)
            {

                if (c.valid)
                {

                    valid++;

                }

            }

            return valid;

        }

        static void Main(string[] args)
        {

            // Bulls = בול , Cows = פגיעה

            // Player guess algorithm

            Console.WriteLine("Game Menu: ");
            Console.WriteLine("1. Player guess");
            Console.WriteLine("2. Computer guess");

            string choice = Console.ReadLine();

            while (choice != "1" && choice != "2")
            {

                Console.WriteLine("Option not in menu.");
                choice = Console.ReadLine();

            }

            Random rnd = new Random();

            int turns = 0;

            Regex rx = new Regex(@"^\d{4}$");

            if (choice == "1")
            {

                string key = $"{rnd.Next(9)}{rnd.Next(9)}{rnd.Next(9)}{rnd.Next(9)}";

                while (!isUnique(key))
                {

                    key = $"{rnd.Next(9)}{rnd.Next(9)}{rnd.Next(9)}{rnd.Next(9)}";

                }

                while (true)
                {

                    Console.Write("Number: ");
                    string guess = Console.ReadLine();

                    while (!rx.IsMatch(guess))
                    {

                        Console.WriteLine("Guess must be 4 digits long and only contain digits.");
                        Console.Write("Number: ");
                        guess = Console.ReadLine();

                    }

                    int[] hits = getHits(key, guess);

                    turns++;

                    if (hits[0] == key.Length)
                    {

                        Console.WriteLine($"You have won in {turns} turns, good job!");
                        break;

                    }

                    Console.WriteLine($"bulls: {hits[0]} , cows: {hits[1]}");

                }

            }
            else
            {

                Console.Write("Enter 4 digit number: ");

                string key = Console.ReadLine();

                while (!rx.IsMatch(key) || !isUnique(key))
                {

                    Console.WriteLine("Key must be 4 digits long and only contain digits. all digits must be different.");
                    Console.Write("Enter 4 digit number: ");
                    key = Console.ReadLine();

                }

                Case[] Cases = new Case[5040];

                int[] digits = { 0, 1, 2, 3 };

                for (int i = 0; i < Cases.Length; i++)
                {

                    Cases[i] = new Case();

                    Cases[i].guess = $"{digits[0]}{digits[1]}{digits[2]}{digits[3]}";

                    digits[3]++;

                    digits = validifyDigits(digits);

                    while (isBannedGuess(digits))
                    {

                        digits[3]++;

                        digits = digits = validifyDigits(digits);

                    }

                }

                int computer_turns = 0;
                while (true)
                {

                    int case_index = rnd.Next(Cases.Length);

                    while (!Cases[case_index].valid)
                    {

                        case_index = rnd.Next(Cases.Length);

                    }

                    string guess = Cases[case_index].guess;

                    int[] hits = getHits(key, guess);

                    computer_turns++;

                    Console.WriteLine(guess);

                    Console.WriteLine($"bulls: {hits[0]} , cows: {hits[1]}");

                    if (hits[0] == 4)
                    {

                        /* If all numbers are bulls ->
                        you won! */

                        Console.WriteLine($"The computer has won in {computer_turns} turns, good job!");
                        break;

                    }

                    /*
                    Remove all cases that don't contain as many numbers from the guess as the sum of bulls and cows
                    or that dont contain as many numbers in the same place as the guess as the number of bulls. 
                    */

                    for (int i = 0; i < Cases.Length; i++)
                    {

                        if (!Cases[i].valid)
                        {
                            continue;
                        }

                        int verified_cows = 0;
                        List<char> verified_bulls = new List<char>();
                        for (int j = 0; j < guess.Length; j++)
                        {

                            if (Cases[i].guess[j] == guess[j])
                            {

                                verified_bulls.Add(guess[j]);

                            }

                        }

                        for (int j = 0; j < guess.Length; j++)
                        {

                            if (Cases[i].guess.Contains(guess[j]) && !verified_bulls.Contains(guess[j]))
                            {

                                verified_cows++;

                            }

                        }

                        if (verified_bulls.Count != hits[0] || verified_cows != hits[1])
                        {

                            Cases[i].valid = false;

                        }

                    }

                    Cases[case_index].valid = false;

                    Console.WriteLine("Cases left: " + getValid(Cases));

                }

            }

            Console.ReadKey();

        }
    }
}
