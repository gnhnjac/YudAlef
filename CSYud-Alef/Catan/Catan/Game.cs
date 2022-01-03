using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

enum Cards
{

    Vp,
    Monopoly,
    TwoRoads,
    YearOfPlenty,
    Knight,
    None

}

enum Roading
{

    LEFT,
    RIGHT,
    TOPLEFT,
    TOPRIGHT,
    BOTTOMLEFT,
    BOTTOMRIGHT,
    NONE

}


namespace Catan
{
    internal class Game
    {
        private Random rnd = new Random();

        Node<Cell> board { get; set; }

        Node<Player> players { get; set; }

        Panel surface { get; set; }

        public int dice { get; set; }

        public int last_placed_index { get; set; }

        public Housing last_placed_position { get; set; }

        public Roading last_placed_road_position { get; set; }

        public int robber_index { get; set; }

        public Game(Node<Players> playing, Panel s, bool isHost)
        {

            ConstructBoard(isHost);

            AddPlayers(playing);

            this.surface = s;

        }

        public void RollDice()
        {

            this.dice = rnd.Next(1, 7) + rnd.Next(1, 7);

        }

        public void SetDice(int num)
        {

            this.dice = num;

        }

        public void GrantDiceResources()
        {

            Node<Cell> brd = board;

            while (brd != null)
            {

                Cell c = brd.GetValue();

                if (c.number == this.dice && c.has_robber == false && c.resource != Resource.Desert)
                {
                    if (c.left.house_bot != Players.None)
                        GrantResource(c.left.house_bot, c.resource);
                    if (c.left.house_top != Players.None)
                        GrantResource(c.left.house_top, c.resource);
                    if (c.right.house_top != Players.None)
                        GrantResource(c.right.house_top, c.resource);
                    if (c.right.house_bot != Players.None)
                        GrantResource(c.right.house_bot, c.resource);
                    if (c.bottomleft.house_top != Players.None)
                        GrantResource(c.bottomleft.house_top, c.resource);
                    if (c.topleft.house_top != Players.None)
                        GrantResource(c.topleft.house_top, c.resource);
                }

                brd = brd.GetNext();

            }

        }

        public void GrantCard(Players color, Cards c)
        {

            Player p = FindPlayer(color);

            p.GrantCard(c);

        }

        public int GetVictoryPoints(Players color)
        {

            Node<Player> tmp = players;

            while (tmp != null)
            {

                if (tmp.GetValue().color == color)
                    return tmp.GetValue().victory_points;

                tmp = tmp.GetNext();

            }

            return 0;

        }

        public void AddVictoryPoints(Players color, int amt)
        {

            Node<Player> tmp = players;

            while (tmp != null)
            {

                if (tmp.GetValue().color == color)
                {
                    tmp.GetValue().victory_points += amt;
                    return;                
                }
                tmp = tmp.GetNext();

            }

        }

        public Players PassTurn(Players p)
        {

            Node<Player> tmp = players;

            while (tmp != null)
            {

                if (tmp.GetValue().color == p)
                {

                    tmp = tmp.GetNext();

                    if (tmp != null)
                    {

                        return tmp.GetValue().color;

                    }
                    else
                    {

                        return players.GetValue().color;

                    }

                }

                tmp = tmp.GetNext();

            }

            return Players.None;

        }

        public bool Buy(Players p, GameAction thing)
        {

            Node<Player> tmp = players;

            while (tmp != null)
            {

                if (tmp.GetValue().color == p)
                {

                    return tmp.GetValue().RemoveResourcesIfAvailable(GetDemand(thing));

                }

            }

            return false;

        }

        private Node<Resource> GetDemand(GameAction Investment)
        {

            Node<Resource> resources = new Node<Resource>(Resource.None);

            if (Investment == GameAction.House)
            {

                resources.SetValue(Resource.Wood);
                resources.SetNext(new Node<Resource>(Resource.Brick, new Node<Resource>(Resource.Hay, new Node<Resource>(Resource.Sheep))));

            }
            else if(Investment == GameAction.Road)
            {

                resources.SetValue(Resource.Wood);
                resources.SetNext(new Node<Resource>(Resource.Brick));

            }
            else if(Investment == GameAction.Card)
            {

                resources.SetValue(Resource.Stone);
                resources.SetNext(new Node<Resource>(Resource.Sheep, new Node<Resource>(Resource.Hay)));

            }
            return resources;

        }

        public void SetValues(string[] numbers, string[] biomes)
        {

            Node<Cell> brd = board;

            int i = 0;
            while (brd != null)
            {
                
                brd.GetValue().resource = GetBiome(biomes[i]);
                brd.GetValue().number = int.Parse(numbers[i]);

                if (brd.GetValue().resource == Resource.Desert)
                {
                    brd.GetValue().has_robber = true;
                    robber_index = i;
                }
                brd = brd.GetNext();
                i++;
                
            }

        }

        private Resource GetBiome(string s)
        {

            switch(s)
            {

                case "Brick":
                    return Resource.Brick;
                case "Desert":
                    return Resource.Desert;
                case "Hay":
                    return Resource.Hay;
                case "Sheep":
                    return Resource.Sheep;
                case "Stone":
                    return Resource.Stone;
                case "Wood":
                    return Resource.Wood;

            }

            return Resource.None;

        }

        private void ConstructBoard(bool isHost)
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

            if (!isHost)
                return;

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

            int index = 0;
            while (temp != null)
            {

                if (temp.GetValue().number == 0)
                {

                    temp.GetValue().resource = Resource.Desert;
                    temp.GetValue().has_robber = true;
                    robber_index = index;

                }

                temp = temp.GetNext();
                index++;
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

        public int[] GetNumbers()
        {

            int[] nums = new int[19];

            Node<Cell> tmp = board;

            for (int i = 0; i < nums.Length; i++)
            {

                nums[i] = tmp.GetValue().number;

                tmp = tmp.GetNext();

            }

            return nums;

        }

        public Resource[] GetBiomes()
        {

            Resource[] biomes = new Resource[19];

            Node<Cell> tmp = board;

            for (int i = 0; i < biomes.Length; i++)
            {

                biomes[i] = tmp.GetValue().resource;

                tmp = tmp.GetNext();

            }

            return biomes;

        }

        private void ClearRobber()
        {

            Node<Cell> tmp = board;

            while (tmp != null)
            {

                tmp.GetValue().has_robber = false;
                tmp = tmp.GetNext();

            }

        }

        private Resource RevokeResource(Cell cell)
        {

           if (cell.left.GetPlayer() != Players.None)
            {

                Player p = FindPlayer(cell.left.GetPlayer());
                Resource val = p.GetFirst();
                p.deck = p.RemoveCard(p.deck, 0);
                return val;

            }
            if (cell.topleft.GetPlayer() != Players.None)
            {

                Player p = FindPlayer(cell.topleft.GetPlayer());
                Resource val = p.GetFirst();
                p.deck = p.RemoveCard(p.deck, 0);
                return val;

            }
            if (cell.topright.GetPlayer() != Players.None)
            {

                Player p = FindPlayer(cell.topright.GetPlayer());
                Resource val = p.GetFirst();
                p.deck = p.RemoveCard(p.deck, 0);
                return val;

            }
            if (cell.right.GetPlayer() != Players.None)
            {

                Player p = FindPlayer(cell.right.GetPlayer());
                Resource val = p.GetFirst();
                p.deck = p.RemoveCard(p.deck, 0);
                return val;

            }
            if (cell.bottomright.GetPlayer() != Players.None)
            {

                Player p = FindPlayer(cell.bottomright.GetPlayer());
                Resource val = p.GetFirst();
                p.deck = p.RemoveCard(p.deck, 0);
                return val;

            }
            if (cell.bottomleft.GetPlayer() != Players.None)
            {

                Player p = FindPlayer(cell.bottomleft.GetPlayer());
                Resource val = p.GetFirst();
                p.deck = p.RemoveCard(p.deck, 0);
                return val;

            }

            return Resource.None;

        }

        public Resource PlaceRobber(int mousex, int mousey)
        {

            int r = surface.Width / 10;

            Node<Cell> tmp = board;

            int index = 0;
            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r;

                if (mousex > x-10 && mousex < x+10 && mousey > y-10 && mousey < y+10)
                {
                    ClearRobber();
                    tmp.GetValue().has_robber = true;
                    robber_index = index;
                    return RevokeResource(tmp.GetValue());
                }
                index++;
                tmp = tmp.GetNext();
            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 3 * r - 20;

                if (mousex > x - 10 && mousex < x + 10 && mousey > y - 10 && mousey < y + 10)
                {
                    ClearRobber();
                    tmp.GetValue().has_robber = true;
                    robber_index = index;
                    return RevokeResource(tmp.GetValue());
                }
                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 5; i++)
            {

                int x = (r + 30) * 2 + (r + 30) * i - 2 * r + 10;
                int y = 5 * r - 40;

                if (mousex > x - 10 && mousex < x + 10 && mousey > y - 10 && mousey < y + 10)
                {
                    ClearRobber();
                    tmp.GetValue().has_robber = true;
                    robber_index = index;
                    return RevokeResource(tmp.GetValue());
                }
                tmp = tmp.GetNext();
                index++;

            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 6 * r - 20;

                if (mousex > x - 10 && mousex < x + 10 && mousey > y - 10 && mousey < y + 10)
                {
                    ClearRobber();
                    tmp.GetValue().has_robber = true;
                    robber_index = index;
                    return RevokeResource(tmp.GetValue());
                }
                index++;
                tmp = tmp.GetNext();
            }

            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r * 7;

                if (mousex > x - 10 && mousex < x + 10 && mousey > y - 10 && mousey < y + 10)
                {
                    ClearRobber();
                    tmp.GetValue().has_robber = true;
                    robber_index = index;
                    return RevokeResource(tmp.GetValue());
                }
                tmp = tmp.GetNext();
                index++;
            }

            return Resource.None;


        }

        public Resource PlaceRobberByIndex(int ind)
        {

            int r = surface.Width / 10;

            Node<Cell> tmp = board;

            int index = 0;
            for (int i = 0; i < 3; i++)
            {

                if (index == ind)
                {
                    ClearRobber();
                    tmp.GetValue().has_robber = true;
                    return RevokeResource(tmp.GetValue());
                }
                index++;
                tmp = tmp.GetNext();
            }

            for (int i = 0; i < 4; i++)
            {

                if (index == ind)
                {
                    ClearRobber();
                    tmp.GetValue().has_robber = true;
                    return RevokeResource(tmp.GetValue());
                }
                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 5; i++)
            {

                if (index == ind)
                {
                    ClearRobber();
                    tmp.GetValue().has_robber = true;
                    return RevokeResource(tmp.GetValue());
                }
                tmp = tmp.GetNext();
                index++;

            }

            for (int i = 0; i < 4; i++)
            {

                if (index == ind)
                {
                    ClearRobber();
                    tmp.GetValue().has_robber = true;
                    return RevokeResource(tmp.GetValue());
                }
                index++;
                tmp = tmp.GetNext();
            }

            for (int i = 0; i < 3; i++)
            {

                if (index == ind)
                {
                    ClearRobber();
                    tmp.GetValue().has_robber = true;
                    return RevokeResource(tmp.GetValue());
                }
                tmp = tmp.GetNext();
                index++;
            }

            return Resource.None;


        }



        internal bool UseCardIfAvailable(string card, Players p)
        {

            Player player = FindPlayer(p);
            if (card == "Knight")
            {

                if (player.UseDevelopmentCard(Cards.Knight))
                    return true;
                return false;

            }
            else if (card == "YearOfPlenty")
            {

                if (player.UseDevelopmentCard(Cards.YearOfPlenty))
                    return true;
                return false;

            }
            else if (card == "TwoRoads")
            {

                if (player.UseDevelopmentCard(Cards.TwoRoads))
                    return true;
                return false;

            }
            else if (card == "Monopoly")
            {

                if (player.UseDevelopmentCard(Cards.Monopoly))
                    return true;
                return false;

            }
            else if (card == "Vp")
            {

                if (player.UseDevelopmentCard(Cards.Vp))
                    return true;
                return false;

            }

            return false;

        }

        public void AddPlayer(Players p)
        {

            players = new Node<Player>(new Player(p), players);

        }

        public void GrantInitialResources(Players player)
        {
            Node<Player> tmp = players;

            while(tmp != null)
            {

                if (tmp.GetValue().color == player)
                {

                    Node<Cell> tmp2 = this.board;

                    while (tmp2 != null)
                    {

                        if (tmp2.GetValue().left.Contains(player) || tmp2.GetValue().right.Contains(player) || tmp2.GetValue().topleft.Contains(player) || tmp2.GetValue().topright.Contains(player) || tmp2.GetValue().bottomleft.Contains(player) || tmp2.GetValue().bottomright.Contains(player))
                        {
                            if (tmp2.GetValue().resource != Resource.Desert && tmp2.GetValue().has_robber == false)
                                tmp.GetValue().GrantResource(tmp2.GetValue().resource);

                        }
                        tmp2 = tmp2.GetNext();
                    }

                }

                tmp = tmp.GetNext();

            }
        }

        private Player FindPlayer(Players color)
        {

            Node<Player> tmp = players;

            while (tmp != null)
            {

                if (tmp.GetValue().color == color)
                    return tmp.GetValue();

            }

            return null;

        }

        public void GrantResource(Players color, Resource r)
        {

            Player p = FindPlayer(color);

            if (p == null)
                return;

            p.GrantResource(r);

        }

        public int[] GetResources(Players player)
        {

            int[] resources = new int[6];
            for (int i = 0; i < resources.Length; i++)
            {
                resources[i] = 0;
            }

            Node<Player> tmp = players;

            while (tmp != null)
            {

                if (tmp.GetValue().color == player)
                {

                    Node<Resource> tmp2 = tmp.GetValue().deck;

                    while (tmp2 != null)
                    {

                        if (tmp2.GetValue() == Resource.None)
                            return resources;

                        resources[(int)tmp2.GetValue()]++;

                        tmp2 = tmp2.GetNext();

                    }

                }

                tmp = tmp.GetNext();

            }

            return resources;

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

        public void DrawBoard()
        {
            
            Graphics graphics = surface.CreateGraphics();

            int r = surface.Width / 10;

            Node<Cell> tmp = board;

            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r;

                drawCell(graphics, r, x, y, tmp.GetValue());
                tmp = tmp.GetNext();
            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 3 * r - 20;

                drawCell(graphics, r, x, y, tmp.GetValue());
                tmp = tmp.GetNext();
            }

            for (int i = 0; i < 5; i++)
            {

                int x = (r + 30) * 2 + (r + 30) * i - 2 * r + 10;
                int y = 5 * r - 40;

                drawCell(graphics, r, x, y, tmp.GetValue());
                tmp = tmp.GetNext();

            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 6 * r - 20;

                drawCell(graphics, r, x, y, tmp.GetValue());
                tmp = tmp.GetNext();
            }

            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r * 7;

                drawCell(graphics, r, x, y, tmp.GetValue());
                tmp = tmp.GetNext();
            }

            tmp = board;

            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r;
                drawRoads(graphics, x, y, tmp.GetValue());
                drawHouses(graphics, x, y, tmp.GetValue());
                
                tmp = tmp.GetNext();
            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 3 * r - 20;
                drawRoads(graphics, x, y, tmp.GetValue());
                drawHouses(graphics, x, y, tmp.GetValue());
                tmp = tmp.GetNext();
            }

            for (int i = 0; i < 5; i++)
            {

                int x = (r + 30) * 2 + (r + 30) * i - 2 * r + 10;
                int y = 5 * r - 40;
                drawRoads(graphics, x, y, tmp.GetValue());
                drawHouses(graphics, x, y, tmp.GetValue());
                tmp = tmp.GetNext();

            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 6 * r - 20;
                drawRoads(graphics, x, y, tmp.GetValue());
                drawHouses(graphics, x, y, tmp.GetValue());
                tmp = tmp.GetNext();
            }

            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r * 7;
                drawRoads(graphics, x, y, tmp.GetValue());
                drawHouses(graphics, x, y, tmp.GetValue());
                tmp = tmp.GetNext();
            }

        }

        private void drawCell(Graphics g, int r, int x, int y, Cell c)
        {

            var shape = new PointF[6];


            //Create 6 points
            for (int a = 0; a < 6; a++)
            {
                shape[a] = new PointF(
                    x + r * (float)Math.Cos((a * 60 + 90) * Math.PI / 180f),
                    y + r * (float)Math.Sin((a * 60 + 90) * Math.PI / 180f));
            }

            Brush color = Brushes.Black;

            switch (c.resource)
            {

                case Resource.Desert:
                    color = Brushes.LightYellow;
                    break;
                case Resource.Wood:
                    color = Brushes.ForestGreen;
                    break;
                case Resource.Hay:
                    color = Brushes.Yellow;
                    break;
                case Resource.Sheep:
                    color = Brushes.LightGreen;
                    break;
                case Resource.Brick:
                    color = Brushes.DarkRed;
                    break;
                case Resource.Stone:
                    color = Brushes.DarkGray;
                    break;

            }
            
            g.FillPolygon(color, shape);
            g.DrawPolygon(Pens.Black, shape);

            Brush num_color = Brushes.Black;

            if (c.number == 6 || c.number == 8)
                num_color = Brushes.Red;

            if (c.number.ToString().Length > 1)
                g.DrawString(c.number.ToString(), new Font("Arial", 16), num_color, new Point(x-15,y-10));
            else
                g.DrawString(c.number.ToString(), new Font("Arial", 16), num_color, new Point(x - 10, y - 10));

            if (c.has_robber)
            {

                g.FillEllipse(Brushes.Black, new Rectangle(x - 10, y - 10, 15, 15));

            }

        }

        private void drawRoads(Graphics g, int x, int y, Cell c)
        {
            int r = surface.Width / 10;
            if (c.bottomleft.occupant != Players.None)
            {

                // Create points that define line.   
                Point point1 = new Point((int)(x + r * (float)Math.Cos((0 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin((1 * 60 + 90) * Math.PI / 180f))+r/2);
                Point point2 = new Point((int)(x + r * (float)Math.Cos((1 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin(((2) * 60 + 90) * Math.PI / 180f))+r);

                // Draw line to screen.   
                g.DrawLine(GetPen(c.bottomleft.occupant), point1, point2);
            }
            if (c.left.occupant != Players.None)
            {

                // Create points that define line.   
                Point point1 = new Point((int)(x + r * (float)Math.Cos((1 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin((1 * 60 + 90) * Math.PI / 180f)));
                Point point2 = new Point((int)(x + r * (float)Math.Cos((2 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin(((2) * 60 + 90) * Math.PI / 180f)));

                // Draw line to screen.   
                g.DrawLine(GetPen(c.left.occupant), point1, point2);
            }
            if (c.topleft.occupant != Players.None)
            {

                // Create points that define line.   
                Point point1 = new Point((int)(x + r * (float)Math.Cos((2 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin((1 * 60 + 90) * Math.PI / 180f))-r);
                Point point2 = new Point((int)(x + r * (float)Math.Cos((3 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin(((2) * 60 + 90) * Math.PI / 180f))-r/2);

                // Draw line to screen.   
                g.DrawLine(GetPen(c.topleft.occupant), point1, point2);
            }
            if (c.topright.occupant != Players.None)
            {

                // Create points that define line.   
                Point point1 = new Point((int)(x + r * (float)Math.Cos((3 * 60 + 90) * Math.PI / 180f)), (int)((int)(y + r * (float)Math.Sin((1 * 60 + 90) * Math.PI / 180f)) - (int)r*1.5));
                Point point2 = new Point((int)(x + r * (float)Math.Cos((4 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin(((2) * 60 + 90) * Math.PI / 180f)));

                // Draw line to screen.   
                g.DrawLine(GetPen(c.topright.occupant), point1, point2);
            }
            if (c.right.occupant != Players.None)
            {

                // Create points that define line.   
                Point point1 = new Point((int)(x + r * (float)Math.Cos((4 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin((1 * 60 + 90) * Math.PI / 180f)));
                Point point2 = new Point((int)(x + r * (float)Math.Cos((5 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin(((2) * 60 + 90) * Math.PI / 180f)));

                // Draw line to screen.   
                g.DrawLine(GetPen(c.right.occupant), point1, point2);
            }
            if (c.bottomright.occupant != Players.None)
            {

                // Create points that define line.   
                Point point1 = new Point((int)(x + r * (float)Math.Cos((5 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin((1 * 60 + 90) * Math.PI / 180f)));
                Point point2 = new Point((int)(x + r * (float)Math.Cos((6 * 60 + 90) * Math.PI / 180f)), (int)(y + r * (float)Math.Sin(((2) * 60 + 90) * Math.PI / 180f))+r+r/2);

                // Draw line to screen.   
                g.DrawLine(GetPen(c.bottomright.occupant), point1, point2);
            }

        }

        private void drawHouses(Graphics g, int x, int y, Cell c)
        {

            if (c.bottomleft.house_top != Players.None)
                g.FillEllipse(GetColor(c.bottomleft.house_top), new Rectangle(x - 7, y + 32, 15, 15));
            if (c.left.house_bot != Players.None)
                g.FillEllipse(GetColor(c.left.house_bot), new Rectangle(x-42, y+16, 15, 15));
            if (c.left.house_top != Players.None)
                g.FillEllipse(GetColor(c.left.house_top), new Rectangle(x - 42, y - 28, 15, 15));
            if (c.topleft.house_top != Players.None)
                g.FillEllipse(GetColor(c.topleft.house_top), new Rectangle(x - 7, y - 44, 15, 15));
            if (c.topright.house_top != Players.None)
                g.FillEllipse(GetColor(c.topright.house_top), new Rectangle(x +28, y-28 , 15, 15));
            if (c.right.house_bot != Players.None)
                g.FillEllipse(GetColor(c.right.house_bot), new Rectangle(x + 28, y+16, 15, 15));

        }

        private Brush GetColor(Players p)
        {

            switch(p)
            {

                case Players.White:
                    return Brushes.White;
                case Players.Red:
                    return Brushes.Red;
                case Players.Green:
                    return Brushes.Green;
                case Players.Blue:
                    return Brushes.Blue;
                case Players.Brown:
                    return Brushes.Brown;
                case Players.Orange:
                    return Brushes.Orange;

            }

            return Brushes.Black;

        }

        private Pen GetPen(Players p)
        {

            return new Pen(GetColor(p), 5);

        }

        public bool PutHouse(int mousex, int mousey, Players color)
        {

            // Road structure

            // HouseBot------HouseTop

            // House Bot
            // \
            //  \
            //   \ 
            // House Top

            // House Top
            //   /
            //  /
            // /
            // House Bot

            int r = surface.Width / 10;

            Node<Cell> tmp = board;

            int index = 0;
            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r;

                if (PutHouseInHex(mousex, mousey, x, y, color, tmp.GetValue()))
                {
                    last_placed_index = index;
                    return true;
                }

                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 3 * r - 20;

                if (PutHouseInHex(mousex, mousey, x, y, color, tmp.GetValue()))
                {
                    last_placed_index = index;
                    return true;
                }

                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 5; i++)
            {

                int x = (r + 30) * 2 + (r + 30) * i - 2 * r + 10;
                int y = 5 * r - 40;

                if (PutHouseInHex(mousex, mousey, x, y, color, tmp.GetValue()))
                {
                    last_placed_index = index;
                    return true;
                }

                tmp = tmp.GetNext();
                index++;

            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 6 * r - 20;

                if (PutHouseInHex(mousex, mousey, x, y, color, tmp.GetValue()))
                {
                    last_placed_index = index;
                    return true;
                }
                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r * 7;

                if (PutHouseInHex(mousex, mousey, x, y, color, tmp.GetValue()))
                {
                    last_placed_index = index;
                    return true;
                }

                tmp = tmp.GetNext();
                index++;
            }

            return false;

        }

        private bool PutHouseInHex(int mousex,int mousey,int x, int y, Players color, Cell c)
        {

            int r = surface.Width / 10;

            for (int a = 0; a < 6; a++)
            {

                int tmpx = (int)(x + r * (float)Math.Cos((a * 60 + 90) * Math.PI / 180f));
                int tmpy = (int)(y + r * (float)Math.Sin((a * 60 + 90) * Math.PI / 180f));

                if (tmpx - 10 < mousex && tmpx + 10 > mousex && tmpy + 10 > mousey && tmpy - 10 < mousey)
                {

                    switch (a)
                    {

                        case 0:

                            if (c.bottomleft.house_top != Players.None || c.bottomright.house_bot != Players.None)
                                return false;

                            c.bottomleft.house_top = color;
                            c.bottomright.house_bot = color;
                            last_placed_position = Housing.BOTTOM;
                            return true;
                        case 1:

                            if (c.left.house_bot != Players.None || c.bottomleft.house_bot != Players.None)
                                return false;

                            c.bottomleft.house_bot = color;
                            c.left.house_bot = color;
                            last_placed_position = Housing.BOTTOMLEFT;
                            return true;
                        case 2:

                            if (c.left.house_top != Players.None || c.topleft.house_bot != Players.None)
                                return false;

                            c.left.house_top = color;
                            c.topleft.house_bot = color;
                            last_placed_position = Housing.TOPLEFT;
                            return true;
                        case 3:

                            if (c.topleft.house_top != Players.None || c.topright.house_bot != Players.None)
                                return false;

                            c.topleft.house_top = color;
                            c.topright.house_bot = color;
                            last_placed_position = Housing.TOP;
                            return true;
                        case 4:

                            if (c.topright.house_top != Players.None || c.right.house_top!= Players.None)
                                return false;

                            c.topright.house_top = color;
                            c.right.house_top = color;
                            last_placed_position = Housing.TOPRIGHT;
                            return true;
                        case 5:

                            if (c.right.house_bot != Players.None || c.bottomright.house_top != Players.None)
                                return false;

                            c.bottomright.house_top = color;
                            c.right.house_bot = color;
                            last_placed_position = Housing.BOTTOMRIGHT;
                            return true;
                    }

                }

            }
            return false;
        }

        public void PlaceHouseByIndex(Players color, int wanted_index, Housing pos)
        {

            int r = surface.Width / 10;

            Node<Cell> tmp = board;

            int index = 0;
            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r;

                if (index == wanted_index)
                {
                    PutHouseByPos(x, y, color, pos, tmp.GetValue());
                    return;
                }

                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 3 * r - 20;

                if (index == wanted_index)
                {
                    PutHouseByPos(x, y, color, pos, tmp.GetValue());
                    return;
                }

                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 5; i++)
            {

                int x = (r + 30) * 2 + (r + 30) * i - 2 * r + 10;
                int y = 5 * r - 40;

                if (index == wanted_index)
                {
                    PutHouseByPos(x, y, color, pos, tmp.GetValue());
                    return;
                }

                tmp = tmp.GetNext();
                index++;

            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 6 * r - 20;

                if (index == wanted_index)
                {
                    PutHouseByPos(x, y, color, pos, tmp.GetValue());
                    return;
                }
                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r * 7;

                if (index == wanted_index)
                {
                    PutHouseByPos(x, y, color, pos, tmp.GetValue());
                    return;
                }
                tmp = tmp.GetNext();
                index++;
            }

        }

        private void PutHouseByPos(int x, int y, Players color, Housing pos, Cell c)
        {

            int r = surface.Width / 10;

            for (int a = 0; a < 6; a++)
            {

                if (a == GetRotation(pos))
                {

                    switch (a)
                    {

                        case 0:

                            c.bottomleft.house_top = color;
                            c.bottomright.house_bot = color;
                            last_placed_position = Housing.BOTTOM;
                            return;
                        case 1:

                            c.bottomleft.house_bot = color;
                            c.left.house_bot = color;
                            last_placed_position = Housing.BOTTOMLEFT;
                            return;
                        case 2:

                            c.left.house_top = color;
                            c.topleft.house_bot = color;
                            last_placed_position = Housing.TOPLEFT;
                            return;
                        case 3:

                            c.topleft.house_top = color;
                            c.topright.house_bot = color;
                            last_placed_position = Housing.TOP;
                            return;
                        case 4:

                            c.topright.house_top = color;
                            c.right.house_top = color;
                            last_placed_position = Housing.TOPRIGHT;
                            return;
                        case 5:

                            c.bottomright.house_top = color;
                            c.right.house_bot = color;
                            last_placed_position = Housing.BOTTOMRIGHT;
                            return;
                    }

                }

            }

        }

        public void PlaceRoadByIndex(Players color, int wanted_index, Roading pos)
        {

            int r = surface.Width / 10;

            Node<Cell> tmp = board;

            int index = 0;
            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r;

                if (index == wanted_index)
                {
                    PutRoadByPos(x, y, color, pos, tmp.GetValue());
                    return;
                }

                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 3 * r - 20;

                if (index == wanted_index)
                {
                    PutRoadByPos(x, y, color, pos, tmp.GetValue());
                    return;
                }

                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 5; i++)
            {

                int x = (r + 30) * 2 + (r + 30) * i - 2 * r + 10;
                int y = 5 * r - 40;

                if (index == wanted_index)
                {
                    PutRoadByPos(x, y, color, pos, tmp.GetValue());
                    return;
                }

                tmp = tmp.GetNext();
                index++;

            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 6 * r - 20;

                if (index == wanted_index)
                {
                    PutRoadByPos(x, y, color, pos, tmp.GetValue());
                    return;
                }
                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r * 7;

                if (index == wanted_index)
                {
                    PutRoadByPos(x, y, color, pos, tmp.GetValue());
                    return;
                }
                tmp = tmp.GetNext();
                index++;
            }

        }

        private void PutRoadByPos(int x, int y, Players color, Roading pos, Cell c)
        {

            int r = surface.Width / 10;

            for (int a = 0; a < 6; a++)
            {

                if (a == GetRoadRotation(pos))
                {

                    switch (a)
                    {

                        case 0:
                            last_placed_road_position = Roading.BOTTOMLEFT;
                            c.bottomleft.occupant = color;
                            break;
                        case 1:
                            last_placed_road_position = Roading.LEFT;
                            c.left.occupant = color;
                            break;
                        case 2:
                            last_placed_road_position = Roading.TOPLEFT;
                            c.topleft.occupant = color;
                            break;
                        case 3:
                            last_placed_road_position = Roading.TOPRIGHT;
                            c.topright.occupant = color;
                            break;
                        case 4:
                            last_placed_road_position = Roading.RIGHT;
                            c.right.occupant = color;
                            break;
                        case 5:
                            last_placed_road_position = Roading.BOTTOMRIGHT;
                            c.bottomright.occupant = color;
                            break;
                    }

                }

            }

        }

        private int GetRotation(Housing pos)
        {

            switch(pos)
            {

                case Housing.BOTTOM:
                    return 0;
                case Housing.BOTTOMLEFT:
                    return 1;
                case Housing.TOPLEFT:
                    return 2;
                case Housing.TOP:
                    return 3;
                case Housing.TOPRIGHT:
                    return 4;
                case Housing.BOTTOMRIGHT:
                    return 5;

            }

            return 0;

        }

        private int GetRoadRotation(Roading pos)
        {

            switch (pos)
            {

                case Roading.BOTTOMLEFT:
                    return 0;
                case Roading.LEFT:
                    return 1;
                case Roading.TOPLEFT:
                    return 2;
                case Roading.TOPRIGHT:
                    return 3;
                case Roading.RIGHT:
                    return 4;
                case Roading.BOTTOMRIGHT:
                    return 5;

            }

            return 0;

        }


        public bool PutRoad(int mousex, int mousey, Players color)
        {

            int r = surface.Width / 10;

            Node<Cell> tmp = board;

            int index = 0;
            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r;

                if (PutRoadInHex(mousex, mousey, x, y, color, tmp.GetValue()))
                {
                    last_placed_index = index;
                    return true;
                }
                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 3 * r - 20;

                if (PutRoadInHex(mousex, mousey, x, y, color, tmp.GetValue()))
                {
                    last_placed_index = index;
                    return true;
                }

                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 5; i++)
            {

                int x = (r + 30) * 2 + (r + 30) * i - 2 * r + 10;
                int y = 5 * r - 40;

                if (PutRoadInHex(mousex, mousey, x, y, color, tmp.GetValue()))
                {
                    last_placed_index = index;
                    return true;
                }

                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 4; i++)
            {


                int x = (r + 30) + (r + 30) * i + r - 5;
                int y = 6 * r - 20;

                if (PutRoadInHex(mousex, mousey, x, y, color, tmp.GetValue()))
                {
                    last_placed_index = index;
                    return true;
                }

                tmp = tmp.GetNext();
                index++;
            }

            for (int i = 0; i < 3; i++)
            {


                int x = (r + 30) * 2 + (r + 30) * i;
                int y = r * 7;

                if (PutRoadInHex(mousex, mousey, x, y, color, tmp.GetValue()))
                {
                    last_placed_index = index;
                    return true;
                }

                tmp = tmp.GetNext();
                index++;
            }

            return false;

        }

        private bool PutRoadInHex(int mousex, int mousey, int x, int y, Players color, Cell c)
        {

            int r = surface.Width / 10;

            for (int a = 0; a < 6; a++)
            {

                int tmpx = (int)(x + r * (float)Math.Cos((a * 60 + 90) * Math.PI / 180f));
                int tmpy = (int)(y + r * (float)Math.Sin((a * 60 + 90) * Math.PI / 180f));

                int tmpx2 = (int)(x + r * (float)Math.Cos(((a+1) * 60 + 90) * Math.PI / 180f));
                int tmpy2 = (int)(y + r * (float)Math.Sin(((a+1) * 60 + 90) * Math.PI / 180f));

                bool found_cell = false;

                if ((a == 1 || a == 4) && (tmpx - 5 < mousex && tmpx + 5 > mousex) && ((tmpy < mousey && tmpy2 > mousey) || (tmpy > mousey && tmpy2 < mousey)))
                    found_cell = true;
                else if (((tmpx < mousex && tmpx2 > mousex) || (tmpx > mousex && tmpx2 < mousex)) && ((tmpy < mousey && tmpy2 > mousey) || (tmpy > mousey && tmpy2 < mousey)))
                    found_cell = true;

                if (found_cell)
                {

                    switch (a)
                    {

                        case 0:

                            if (c.bottomleft.occupant != Players.None)
                                return false;

                            c.bottomleft.occupant = color;
                            last_placed_road_position = Roading.BOTTOMLEFT;
                            return true;
                        case 1:

                            if (c.left.occupant != Players.None)
                                return false;

                            c.left.occupant = color;
                            last_placed_road_position = Roading.LEFT;
                            return true;
                        case 2:

                            if (c.topleft.occupant != Players.None)
                                return false;

                            c.topleft.occupant = color;
                            last_placed_road_position = Roading.TOPLEFT;
                            return true;
                        case 3:

                            if (c.topright.occupant != Players.None)
                                return false;

                            c.topright.occupant = color;
                            last_placed_road_position = Roading.TOPRIGHT;
                            return true;
                        case 4:

                            if (c.right.occupant != Players.None)
                                return false;

                            c.right.occupant = color;
                            last_placed_road_position = Roading.RIGHT;
                            return true;
                        case 5:

                            if (c.bottomright.occupant != Players.None)
                                return false;

                            c.bottomright.occupant = color;
                            last_placed_road_position = Roading.BOTTOMRIGHT;
                            return true;
                    }

                }

            }
            return false;
        }

    }
}
