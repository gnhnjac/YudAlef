using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.Remoting.Metadata;
using System.Text;
using System.Threading.Tasks;

namespace TwentyFourtyEight
{
    class BoardManager
    {

        char block = '█';

        Random rnd = new Random();

        Tile[,] tiles;

        int score = 0;

        public BoardManager()
        {

            tiles = new Tile[4, 4];

            for (int i = 0; i < 4; i++)
            {

                for (int j = 0; j < 4; j++)
                {

                    tiles[i, j] = new Tile();

                }

            }

            drawTileMap();

        }

        public void drawTileMap()
        {

            for (int i = 0; i < 4; i++)
            {

                for (int j = 0; j < 4; j++)
                {

                    for (int k = 0; k < 7; k++)
                    {

                        Console.SetCursorPosition(i * 6 + k, j * 6);
                        Console.Write(block);

                        Console.SetCursorPosition(i * 6 + k, j * 6 + 6);
                        Console.Write(block);

                        Console.SetCursorPosition(i * 6, j * 6 + k);
                        Console.Write(block);

                        Console.SetCursorPosition(i * 6 + 6, j * 6 + k);
                        Console.Write(block);

                    }

                }

            }

        }

        public void Show()
        {

            for (int i = 0; i < 4; i++)
            {

                for (int j = 0; j < 4; j++)
                {

                    Console.ForegroundColor = ConsoleColor.Black;
                    for (int k = 1; k < 6; k++)
                    {

                        Console.SetCursorPosition(i * 6 + k, j * 6 + 3);
                        Console.Write(block);

                    }

                    if (tiles[j, i].Value == 0)
                        continue;

                    Console.ForegroundColor = ConsoleColor.White;

                    if (tiles[j, i].Latest)
                        Console.ForegroundColor = ConsoleColor.Green;

                    Console.SetCursorPosition(i * 6 + 2, j * 6 + 3);
                    Console.Write(tiles[j, i].Value);

                }

            }

            Console.ForegroundColor = ConsoleColor.White;

            Console.SetCursorPosition(25, 12);
            Console.Write("Score: " + score);

        }

        public void Update(ConsoleKey key)
        {

            if (key != ConsoleKey.LeftArrow && key != ConsoleKey.RightArrow && key != ConsoleKey.DownArrow && key != ConsoleKey.UpArrow)
                return;

            for (int i = 0; i < 4; i++)
            {

                for (int j = 0; j < 4; j++)
                {

                    tiles[i, j].Merged = false;

                }

            }

            int dirx = 0;
            int diry = 0;

            switch (key)
            {

                case ConsoleKey.LeftArrow:
                    dirx = -1;
                    break;
                case ConsoleKey.RightArrow:
                    dirx = 1;
                    break;
                case ConsoleKey.UpArrow:
                    diry = -1;
                    break;
                case ConsoleKey.DownArrow:
                    diry = 1;
                    break;

            }

            bool change = false;

            for (int k = 0; k < 3; k++)
            {

                for (int i = 0; i < 4; i++)
                {

                    for (int j = 0; j < 4; j++)
                    {

                        Tile current = tiles[i, j];

                        int x = j + dirx;
                        int y = i + diry;

                        if (current.Value == 0 || y >= 4 || y < 0 || x >= 4 || x < 0)
                            continue;

                        Tile next = tiles[y, x];

                        if (next.Merged)
                            continue;

                        if (next.Value == 0)
                        {

                            next.Value = current.Value;

                            current.Value = 0;

                            change = true;

                        }

                        else if (next.Value == current.Value && !current.Merged)
                        {

                            next.Value = current.Value * 2;

                            current.Value = 0;

                            next.Merged = true;

                            score += next.Value;

                            change = true;

                        }

                        if (current.Merged && next.Value * 2 == current.Value)
                        {

                            current.Value /= 2;

                            next.Value *= 2;

                        }


                    }

                }

            }

            if(change)
                addRandomTile();

        }

        public void addRandomTile()
        {

            if (!spaceAvailable())
                return;

            for(int i = 0; i < 4; i++)
            {

                for(int j = 0; j < 4; j++)
                {

                    if (tiles[i, j].Latest)
                        tiles[i, j].Latest = false;

                }

            }

            int x;
            int y;

            do
            {

                x = rnd.Next(4);
                y = rnd.Next(4);

            } while (tiles[x, y].Value != 0);

            tiles[x, y].Value = (rnd.Next(100) > 5) ? 2 : 4;

            tiles[x, y].Latest = true;

        }

        public bool neighborAvailable()
        {

            for (int i = 0; i < 4; i++)
            {

                for (int j = 0; j < 4; j++)
                {

                    for (int k = -1; k < 2; k++)
                    {

                        for (int o = -1; o < 2; o++)
                        {

                            if (i + k >= 4 || i + k < 0 || j + o >= 4 || j + o < 0 || k == o || k * -1 == o || tiles[i, j].Value == 0)
                                continue;

                            if (tiles[i, j].Value == tiles[i + k, j + o].Value)
                                return true;

                        }

                    }


                }

            }

            return false;

        }

        public bool spaceAvailable()
        {

            for(int i = 0; i < 4; i++)
            {

                for(int j = 0; j < 4; j++)
                {

                    if (tiles[i, j].Value == 0)
                        return true;

                }

            }

            return false;

        }

        public void gameOver()
        {

            Console.SetCursorPosition(0, 25);
            Console.WriteLine("Game Over! Your score was: " + score);

        }

    }
}
