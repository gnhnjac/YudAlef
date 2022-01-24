using System;
using System.Collections.Generic;
using System.ComponentModel.Design;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace for_exercises2
{
    
    class Program
    {

        static void ex1()
        {

            int negatives, positives;

            negatives = positives = 0;

            for (int i = 0; i < 10; i++)
            {

                Console.WriteLine("Enter whole number: ");

                int num = int.Parse(Console.ReadLine());

                if (num > 0)
                    positives++;

                if (num < 0)
                    negatives++;

            }

            Console.WriteLine("Positive numbers: " + positives);

            Console.WriteLine("Negative numbers: " + negatives);

        }

        static void ex2()
        {

            int nineties = 0;
            int sixties = 0;

            for(int i = 0; i < 10; i++)
            {

                Console.WriteLine("Enter student's grade: ");

                int grade = int.Parse(Console.ReadLine());

                if (grade >= 90 && grade <= 100)
                {

                    nineties++;

                }
                else if (grade >= 60 && grade <= 100)
                {

                    sixties++;

                }

            }

            Console.WriteLine("60+ students: " + sixties);

            Console.WriteLine("90+ students: " + nineties);

        }

        static void ex3()
        {

            int count = 0;

            for(int i = 0; i < 20; i++)
            {

                Console.WriteLine("1st number: ");

                int num1 = int.Parse(Console.ReadLine());

                Console.WriteLine("2nd number: ");

                int num2 = int.Parse(Console.ReadLine());

                if ((num1 > 0 && num2 > 0) && (num1 % 2 == 1 && num2 % 2 == 1))
                    count++;

            }

            Console.WriteLine("Positive uneven pair count: " + count);

        }

        static void ex4()
        {

            Console.WriteLine("Number of tasks: ");
            int tasks = int.Parse(Console.ReadLine());

            int perfect_students = 0;
            int average_students = 0;
            int failures = 0;

            for(int i = 0; i < 30; i++)
            {

                Console.WriteLine("How many tasks did this student finish?");
                int student_tasks = int.Parse(Console.ReadLine());

                if (student_tasks == tasks)
                {

                    perfect_students++;

                }
                else if(student_tasks < tasks && student_tasks > 0)
                {

                    average_students++;

                }
                else
                {

                    failures++; // ;(

                }

            }

            Console.WriteLine(perfect_students + " Perfect Students.");
            Console.WriteLine(average_students + " Average Students.");
            Console.WriteLine(failures + " Failures. Please try harder.");

        }

        static void ex5()
        {

            int all_lovers = 0;
            int comedy_lovers = 0;
            int two_lovers = 0;

            for(int i = 0; i < 10; i++)
            {

                int genres_loved = 0;

                Console.WriteLine("Do you like comedy movies? (Y/N)");
                char ans1 = char.Parse(Console.ReadLine());

                if (ans1 == 'Y')
                {

                    comedy_lovers++;
                    genres_loved++;

                }

                Console.WriteLine("Do you like action movies? (Y/N)");
                char ans2 = char.Parse(Console.ReadLine());

                if (ans2 == 'Y')
                    genres_loved++;

                Console.WriteLine("Do you like drama movies? (Y/N)");
                char ans3 = char.Parse(Console.ReadLine());

                if (ans3 == 'Y')
                    genres_loved++;

                if (genres_loved == 3)
                    all_lovers++;

                if (genres_loved == 2)
                    two_lovers++;

            }

            Console.WriteLine(comedy_lovers + " students like comedy movies.");
            Console.WriteLine(all_lovers + " students like all 3 movie genres.");
            Console.WriteLine(two_lovers + " students only like 2 movie genres.");

        }

        static void ex6()
        {

            Console.WriteLine("Number of test attendants: ");

            int people = int.Parse(Console.ReadLine());

            int failures = 0;

            for(int i = 0; i < people; i++)
            {

                Console.WriteLine("How many wrong sign answers?");

                int signs = int.Parse(Console.ReadLine());

                Console.WriteLine("How many wrong answers from the rest of the answers?");

                int rest_wrong = int.Parse(Console.ReadLine());

                if (signs > 0 || rest_wrong > 3)
                    failures++;

            }

            Console.WriteLine("Number of failures: " + failures);
            Console.WriteLine("Precent of failures: " + failures * 100 / people + "%");

        }

        static void ex7()
        {

            int biggest = 0;
            int smallest = 0;

            for(int i = 0; i < 10; i++)
            {

                Console.WriteLine("Enter a number: ");

                int num = int.Parse(Console.ReadLine());

                if (num > biggest)
                    biggest = num;

                if (num < smallest)
                    smallest = num;

            }

            Console.WriteLine("Biggest number: " + biggest);

            Console.WriteLine("Smallest number: " + smallest);

        }

        static void ex8()
        {

            int betweens = 0;

            for(int i = 0; i < 30; i++)
            {

                Console.WriteLine("Age of attendee: ");

                int age = int.Parse(Console.ReadLine());

                if (age >= 22 && age <= 40)
                    betweens++;

            }

            Console.WriteLine("Number of attendees who's age is between 22 and 40: " + betweens);

        }

        static void ex9()
        {

            int threes = 0;
            int twos = 0;
            int recreation_lovers = 0;
            int trip_over_party = 0;

            for(int i = 0; i < 100; i++)
            {

                int total_recreations = 0;

                Console.WriteLine("Number of trips: ");
                int trips = int.Parse(Console.ReadLine());

                if (trips > 0)
                    total_recreations++;

                Console.WriteLine("Number of parties: ");
                int parties = int.Parse(Console.ReadLine());

                if (parties > 0)
                    total_recreations++;

                Console.WriteLine("Number of movies: ");
                int movies = int.Parse(Console.ReadLine());

                if (movies > 0)
                    total_recreations++;

                if (total_recreations == 3)
                    threes++;

                if (total_recreations == 2)
                    twos++;

                if (movies > 3 || parties > 3 || trips > 3)
                    recreation_lovers++;

                if (trips > parties)
                    trip_over_party++;

            }

            Console.WriteLine(threes + " Students have experienced all 3 experiences.");

            Console.WriteLine(twos + " Students have experienced only 2 experiences.");

            Console.WriteLine(recreation_lovers + " Students have experienced an experienec more than 3 times.");

            Console.WriteLine(trip_over_party + " Students participated in more trips than parties.");

        }

        static void ex10()
        {

            int three_buyers = 0;
            int one_buyers = 0;

            for(int i = 0; i < 2000; i++)
            {

                int total_tickets = 0;

                Console.WriteLine("First show tickets: (0/1)");
                int show = int.Parse(Console.ReadLine());

                if (show == 1)
                    total_tickets++;

                Console.WriteLine("Second show tickets: (0/1)");
                show = int.Parse(Console.ReadLine());

                if (show == 1)
                    total_tickets++;

                Console.WriteLine("Third show tickets: (0/1)");
                show = int.Parse(Console.ReadLine());

                if (show == 1)
                    total_tickets++;

                if (total_tickets == 3)
                    three_buyers++;

                if (total_tickets == 1)
                    one_buyers++;

            }

            Console.WriteLine(three_buyers + " Students bought tickets for all 3 shows.");

            Console.WriteLine(one_buyers + " Students bought tickets for only a single show.");

        }

        static void Main(string[] args)
        {

            // ex1();
            // ex2();
            // ex3();
            // ex4();
            // ex5();
            // ex6();
            // ex7();
            // ex8();
            // ex9();
            // ex10();

        }
    }
}
