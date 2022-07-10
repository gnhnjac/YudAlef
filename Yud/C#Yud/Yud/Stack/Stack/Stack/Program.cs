using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Stack
{
    class Program
    {

        static void CheckParenthesis(string s)
        {

            Console.WriteLine("Errors at indices:");

            StackA<char> stack = new StackA<char>(300);

            for (int i = 0; i < s.Length; i++)
            {

                char current = s[i];

                if (current == '[' || current == '{' || current == '(')
                {

                    stack.push(current);

                }
                else if (current == ']' || current == '}' || current == ')')
                {
                    try
                    {

                        char open = stack.pop();

                        switch(current)
                        {

                            case ']':
                                if (open != '[')
                                    Console.WriteLine(i);
                                break;
                            case '}':
                                if (open != '{')
                                    Console.WriteLine(i);
                                break;
                            case ')':
                                if (open != '(')
                                    Console.WriteLine(i);
                                break;

                        }

                    }
                    catch (InvalidOperationException)
                    {

                        Console.WriteLine(i);

                    }

                }


            }

        }

        static void Main(string[] args)
        {

            CheckParenthesis("(([)]");

        }
    }
}
