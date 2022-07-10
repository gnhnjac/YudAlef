using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CatanGame
{
    internal class Game
    {

        private Random rnd = new Random();

        Node<Cell> board { get; set; }

        Node<Player> players { get; set; }

        public Game(Node<Players> playing)
        {

            ConstructBoard();

            AddPlayers(playing);

        }

        private void ConstructBoard()
        {

            Console.WriteLine("Setting up board...");

            // First row

            Cell oneone = new Cell();
            Cell onetwo = new Cell();
            Cell onethree = new Cell();

            // Second row

            Cell twoone = new Cell();
            Cell twotwo = new Cell();
            Cell twothree = new Cell();
            Cell twofour = new Cell();

            // Third row

            Cell threeone = new Cell();
            Cell threetwo = new Cell();
            Cell threethree = new Cell();
            Cell threefour = new Cell();
            Cell threefive = new Cell();

            // Fourth row

            Cell fourone = new Cell();
            Cell fourtwo = new Cell();
            Cell fourthree = new Cell();
            Cell fourfour = new Cell();

            // Fifth row

            Cell fiveone = new Cell();
            Cell fivetwo = new Cell();
            Cell fivethree = new Cell();

            // Row:1,Col:1

            oneone.left = new Road(null, oneone);
            oneone.topleft = new Road(null, oneone);
            oneone.topright = new Road(null, oneone);
            oneone.right = new Road(oneone, onetwo);
            oneone.bottomleft = new Road(oneone, twoone);
            oneone.bottomright = new Road(oneone, twotwo);

            // Row:1,Col:2

            onetwo.left = oneone.right;
            onetwo.topleft = new Road(null, onetwo);
            onetwo.topright = new Road(null, onetwo);
            onetwo.right = new Road(onetwo, onethree);
            onetwo.bottomleft = new Road(onetwo, twotwo);
            onetwo.bottomright = new Road(onetwo, twothree);

            // Row:1,Col:3

            onethree.left = onetwo.right;
            onethree.topleft = new Road(null, onethree);
            onethree.topright = new Road(null, onethree);
            onethree.right = new Road(onethree, null);
            onethree.bottomleft = new Road(onethree, twothree);
            onethree.bottomright = new Road(onethree, twofour);

            // Row: 2, Col: 1

            twoone.left = new Road(null, twoone);
            twoone.topleft = new Road(null, twoone);
            twoone.topright = oneone.bottomleft;
            twoone.right = new Road(twoone, twotwo);
            twoone.bottomleft = new Road(twoone, threeone);
            twoone.bottomright = new Road(twoone, threetwo);

            // Row: 2, Col: 2

            twotwo.left = twoone.right;
            twotwo.topleft = oneone.bottomright;
            twotwo.topright = onetwo.bottomleft;
            twotwo.right = new Road(twotwo, twothree);
            twotwo.bottomleft = new Road(twotwo, threetwo);
            twotwo.bottomright = new Road(twotwo, threethree);

            // Row: 2, Col: 3

            twothree.left = twotwo.right;
            twothree.topleft = onetwo.bottomright;
            twothree.topright = onethree.bottomleft;
            twothree.right = new Road(twothree, twofour);
            twothree.bottomleft = new Road(twothree, threethree);
            twothree.bottomright = new Road(twothree, threefour);

            // Row: 2, Col: 4

            twofour.left = twothree.right;
            twofour.topleft = onethree.bottomright;
            twofour.topright = new Road(twofour, null);
            twofour.right = new Road(twofour, null);
            twofour.bottomleft = new Road(twofour, threefour);
            twofour.bottomright = new Road(twofour, threefive);

            // Row: 3: Col: 1

            threeone.left = new Road(null, threeone);
            threeone.topleft = new Road(null, threeone);
            threeone.topright = twoone.bottomleft;
            threeone.right = new Road(threeone, threetwo);
            threeone.bottomleft = new Road(null, threeone);
            threeone.bottomright = new Road(threeone, fourone);

            // Row: 3, Col: 2

            threetwo.left = threeone.right;
            threetwo.topleft = twoone.bottomright;
            threetwo.topright = twotwo.bottomleft;
            threetwo.right = new Road(threetwo, threethree);
            threetwo.bottomleft = new Road(threetwo, fourone);
            threetwo.bottomright = new Road(threetwo, fourtwo);

            // Row: 3, Col: 3

            threethree.left = threetwo.right;
            threethree.topleft = twotwo.bottomright;
            threethree.topright = twothree.bottomleft;
            threethree.right = new Road(threethree, threefour);
            threethree.bottomleft = new Road(threethree, fourtwo);
            threethree.bottomright = new Road(threethree, fourthree);

            // Row: 3, Col: 4

            threefour.left = threethree.right;
            threefour.topleft = twothree.bottomright;
            threefour.topright = twofour.bottomleft;
            threefour.right = new Road(threefour, threefive);
            threefour.bottomleft = new Road(threefour, fourthree);
            threefour.bottomright = new Road(threefour, fourfour);

            // Row: 3, Col: 5

            threefive.left = threefour.right;
            threefive.topleft = twofour.bottomright;
            threefive.topright = new Road(threefive, null);
            threefive.right = new Road(threefive, null);
            threefive.bottomleft = new Road(threefive, fourfour);
            threefive.bottomright = new Road(threefive, null);

            // Row: 4, Col: 1

            fourone.left = new Road(null, fourone);
            fourone.topleft = threeone.bottomright;
            fourone.topright = threetwo.bottomleft;
            fourone.right = new Road(fourone, fourtwo);
            fourone.bottomleft = new Road(null, fourone);
            fourone.bottomright = new Road(fourone, fiveone);

            // Row: 4, Col: 2

            fourtwo.left = fourone.right;
            fourtwo.topleft = threetwo.bottomright;
            fourtwo.topright = threethree.bottomleft;
            fourtwo.right = new Road(fourtwo, fourthree);
            fourtwo.bottomleft = new Road(fourtwo, fiveone);
            fourtwo.bottomright = new Road(fourtwo, fivetwo);


            // Row: 4, Col: 3

            fourthree.left = fourtwo.right;
            fourthree.topleft = threethree.bottomright;
            fourthree.topright = threefour.bottomleft;
            fourthree.right = new Road(fourthree, fourfour);
            fourthree.bottomleft = new Road(fourthree, fivetwo);
            fourthree.bottomright = new Road(fourthree, fivethree);

            // Row: 4, Col: 4

            fourfour.left = fourthree.right;
            fourfour.topleft = threefour.bottomright;
            fourfour.topright = threefive.bottomleft;
            fourfour.right = new Road(fourfour, null);
            fourfour.bottomleft = new Road(fourfour, fivethree);
            fourfour.bottomright = new Road(fourfour, null);

            // Row: 5, Col: 1

            fiveone.left = new Road(null, fiveone);
            fiveone.topleft = fourone.bottomright;
            fiveone.topright = fourtwo.bottomleft;
            fiveone.right = new Road(fiveone, fivetwo);
            fiveone.bottomleft = new Road(null, fiveone);
            fiveone.bottomright = new Road(null, fiveone);

            // Row: 5, Col: 2

            fivetwo.left = fiveone.right;
            fivetwo.topleft = fourtwo.bottomright;
            fivetwo.topright = fourthree.bottomleft;
            fivetwo.right = new Road(fivetwo, fivethree);
            fivetwo.bottomleft = new Road(null, fivetwo);
            fivetwo.bottomright = new Road(null, fivetwo);

            // Row: 5, Col: 3

            fivethree.left = fivetwo.right;
            fivethree.topleft = fourthree.bottomright;
            fivethree.topright = fourfour.bottomleft;
            fivethree.right = new Road(fivethree, null);
            fivethree.bottomleft = new Road(null, fivethree);
            fivethree.bottomright = new Road(null, fivethree);

            board = new Node<Cell>(oneone, new Node<Cell>(onetwo));

            Node<Cell> temp = board;

            board = board.GetNext();
            board.SetNext(new Node<Cell>(onethree));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(twoone));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(twotwo));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(twothree));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(twofour));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(threeone));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(threetwo));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(threethree));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(threefour));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(threefive));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(fourone));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(fourtwo));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(fourthree));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(fourfour));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(fiveone));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(fivetwo));
            board = board.GetNext();
            board.SetNext(new Node<Cell>(fivethree));

            board = temp;

            Console.WriteLine("Finished Setting up board");

            Console.WriteLine("Assigning numbers...");

            // Assign numbers

            AssignNumberToRandomCell(2);
            AssignNumberToRandomCell(3);
            AssignNumberToRandomCell(3);
            AssignNumberToRandomCell(4);
            AssignNumberToRandomCell(4);
            AssignNumberToRandomCell(5);
            AssignNumberToRandomCell(5);
            AssignNumberToRandomCell(6);
            AssignNumberToRandomCell(6);
            AssignNumberToRandomCell(8);
            AssignNumberToRandomCell(8);
            AssignNumberToRandomCell(9);
            AssignNumberToRandomCell(9);
            AssignNumberToRandomCell(10);
            AssignNumberToRandomCell(10);
            AssignNumberToRandomCell(11);
            AssignNumberToRandomCell(11);
            AssignNumberToRandomCell(12);

            Console.WriteLine("Finished assigning numbers");

            Console.WriteLine("Assigning resources...");

            // Assign resources

            while (temp != null)
            {

                if (temp.GetValue().number == 0)
                {

                    temp.GetValue().resource = Resource.Desert;

                }

                temp = temp.GetNext();

            }

            for (int i = 0; i < 4; i++)
                AssignResourceToRandomCell(Resource.Wood);

            for (int i = 0; i < 4; i++)
                AssignResourceToRandomCell(Resource.Hay);

            for (int i = 0; i < 4; i++)
                AssignResourceToRandomCell(Resource.Sheep);

            for (int i = 0; i < 3; i++)
                AssignResourceToRandomCell(Resource.Stone);

            for (int i = 0; i < 3; i++)
                AssignResourceToRandomCell(Resource.Brick);

            Console.WriteLine("Finished assigning resources");

        }

        private void AddPlayers(Node<Players> colors)
        {

            players = new Node<Player>(new Player(colors.GetValue()));
            colors = colors.GetNext();
            Node<Player> temp = players;

            while (colors != null)
            {
                temp.SetNext(new Node<Player>(new Player(colors.GetValue())));
                temp = temp.GetNext();

                colors = colors.GetNext();

            }

        }

        private void AssignNumberToRandomCell(int number)
        {

            while (true)
            {


                Node<Cell> temp = board;

                int index = rnd.Next(20);

                int i = 0;
                while (temp != null)
                {

                    if (index == i)
                    {

                        if (temp.GetValue().number == 0)
                        {

                            temp.GetValue().number = number;
                            return;

                        }
                        break;

                    }

                    temp = temp.GetNext();
                    i++;

                }
            }

        }

        private void AssignResourceToRandomCell(Resource r)
        {

            while (true)
            {


                Node<Cell> temp = board;

                int index = rnd.Next(20);

                int i = 0;
                while (temp != null)
                {

                    if (index == i)
                    {

                        if (temp.GetValue().resource == Resource.None)
                        {

                            temp.GetValue().resource = r;
                            return;

                        }
                        break;

                    }

                    temp = temp.GetNext();
                    i++;

                }
            }

        }

        public override string ToString()
        {
            string s = "Board: \n";

            Node<Cell> temp = board;

            int i = 0;
            while (temp != null)
            {

                s += temp.GetValue().ToString() + "|";
                temp = temp.GetNext();

                if (i == 2 || i == 6 || i == 11 || i == 15)
                    s += "\n";

                i++;
            }

            s += "\nPlayers: \n";

            Node<Player> temp2 = players;

            while (temp2 != null)
            {

                s += temp2.GetValue().ToString() + ", ";
                temp2 = temp2.GetNext();
            }

            return s;
        }

    }
}
