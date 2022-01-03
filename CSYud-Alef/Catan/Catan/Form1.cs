using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

enum GameAction
{
    House,
    Road,
    Card,
    Robber,
    None
}

enum Housing
{

    TOPLEFT,
    TOP,
    TOPRIGHT,
    BOTTOMLEFT,
    BOTTOM,
    BOTTOMRIGHT,
    NONE
       

}

namespace Catan
{
    public partial class Form1 : Form
    {

        FileSystemWatcher watcher;

        bool is_not_init = false;

        bool host = false;

        bool game_started = false;

        bool waiting_for_players = false;

        int initial_house = 0;
        int initial_road = 0;

        Random rnd = new Random();

        Game game;

        GameAction action = GameAction.None;

        Players player; // Color of player

        Players turn; // whos turn it is
        
        public Form1()
        {
            InitializeComponent();
            FormClosing += Form1_FormClosing;

            watcher = new FileSystemWatcher(AppDomain.CurrentDomain.BaseDirectory, "*.txt");

            watcher.Created += OnCreated;
            watcher.Changed += OnChanged;
            watcher.EnableRaisingEvents = true;

        }

        private void button1_Click(object sender, EventArgs e)
        {

            joingame.Visible = false;
            joingame.Enabled = false;

            if (waiting_for_players)
            {
                startgame.Visible = false;
                startgame.Enabled = false;
                waitingfor.Enabled = false;
                waitingfor.Visible = false;
                File.WriteAllText("data.txt", $"ACTION=INITBOARD:{string.Join(",",game.GetNumbers())}:{string.Join(",", game.GetBiomes())}\nTURN={player}");
                game.DrawBoard();

                wood.Text = "Wood: 0";
                hay.Text = "Hay: 0";
                stone.Text = "Stone: 0";
                sheep.Text = "Sheep: 0";
                brick.Text = "Brick: 0";
                showturn.Text = $"Turn: {player}";
                showturn.BackColor = GetPlayerColor(player);
                game_started = true;
                turn = player;
            }
            else
            {

                player = (Players)rnd.Next(6);
                game = new Game(new Node<Players>(player), gameboard,true);

                show_color.Text = "Color: " + player;
                show_color.BackColor = GetPlayerColor(player);
                if (show_color.BackColor != Color.White)
                    show_color.ForeColor = Color.White;
                else
                    show_color.ForeColor = Color.Black;
                show_color.Font = new Font(show_color.Font, FontStyle.Bold);
                File.WriteAllText("data.txt", $"ACTION=NONE\nTURN={player}");
                File.WriteAllText($"{player}.txt", $"");
                waitingfor.Visible = true;
                playerbox.Text += $"\r\n{player}";
                waiting_for_players = true;
                host = true;
            }
        }

        private void OnCreated(object sender, FileSystemEventArgs e)
        {
            while (IsFileLocked(new FileInfo(e.FullPath)))
                continue;
            if ((waiting_for_players || is_not_init) && !game_started && e.Name != "data.txt")
            {
                if (!playerbox.Text.Contains(e.FullPath.Split('\\').Last().Replace(".txt", "")))
                {
                    playerbox.Text += $"\r\n{e.FullPath.Split('\\').Last().Replace(".txt", "")}";
                    game.AddPlayer(GetPlayer(e.FullPath.Split('\\').Last().Replace(".txt", "")));
                }
            }

        }

        private void OnChanged(object sender, FileSystemEventArgs e)
        {
            while (IsFileLocked(new FileInfo(e.FullPath)))
                continue;

            if (is_not_init && !game_started && e.Name == "data.txt")
            {

                string data = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt");
                string action = data.Split('\n')[0].Replace("ACTION=INITBOARD:", "");

                string[] numbers = action.Split(':')[0].Split(',');
                string[] biomes = action.Split(':')[1].Split(',');


                game.SetValues(numbers, biomes);


                game_started = true;
                is_not_init = false;
                game.DrawBoard();

                wood.Text = "Wood: 0";
                hay.Text = "Hay: 0";
                stone.Text = "Stone: 0";
                sheep.Text = "Sheep: 0";
                brick.Text = "Brick: 0";
                string p = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt").Split('\n')[1].Replace("TURN=", "");
                showturn.Text = "Turn: " + p;
                turn = GetPlayer(p);
                showturn.BackColor = GetPlayerColor(GetPlayer(p));
                
            }
            else if (game_started && e.Name == "data.txt")
            {

                string data = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt");
                string current_turn = data.Split('\n')[1].Replace("TURN=", "");
                string action = data.Split('\n')[0].Replace("ACTION=", "");

                if (host)
                {

                    if (action == "PASSTURN")
                    {

                        Players new_turn = game.PassTurn(GetPlayer(current_turn));

                        File.WriteAllText("data.txt", $"ACTION=NONE\nTURN=" + GetPlayerStr(new_turn));

                    }
                }

                turn = GetPlayer(data.Split('\n')[1].Replace("TURN=", ""));
                showturn.Text = "Turn: " + GetPlayerStr(turn);
                showturn.BackColor = GetPlayerColor(turn);

                if (action.Contains("HOUSE")) // ACTION=HOUSE:{game.last_placed_index}:{game.last_placed_position}
                {

                    string[] house_coords = action.Split(':');

                    int index = int.Parse(house_coords[1]);
                    Housing pos = StrToCoords(house_coords[2]);

                    game.PlaceHouseByIndex(turn, index, pos);
                    game.DrawBoard();

                }
                else if (action.Contains("ROAD")) // ACTION=ROAD:{game.last_placed_index}:{game.last_placed_road_position}
                {

                    string[] road_coords = action.Split(':');

                    int index = int.Parse(road_coords[1]);
                    Roading pos = StrToRoadCoords(road_coords[2]);

                    game.PlaceRoadByIndex(turn, index, pos);
                    game.DrawBoard();

                }
                else if (action.Contains("DICE") && player != turn) // ACTION=DICE:num
                {
                    Console.WriteLine(action);
                    int num = int.Parse(action.Split(':')[1]);

                    game.SetDice(num);

                    show_dice.Text = "Dice: " + game.dice.ToString();

                    game.GrantDiceResources();

                    Update_Resources();

                }
                else if(action.Contains("ROBBER") && player != turn)
                {

                    int robber_ind = int.Parse(action.Replace("ROBBER:",""));
                    game.robber_index = robber_ind;
                    Resource r = game.PlaceRobberByIndex(robber_ind);

                    game.DrawBoard();
                    Update_Resources();

                }
            }

        }

        private Housing StrToCoords(string pos)
        {
            /*
            enum Housing
        {

            TOPLEFT,
            TOP,
            TOPRIGHT,
            BOTTOMLEFT,
            BOTTOM,
            BOTTOMRIGHT


        }
        */

            switch(pos)
            {

                case "TOPLEFT":
                    return Housing.TOPLEFT;
                case "TOP":
                    return Housing.TOP;
                case "TOPRIGHT":
                    return Housing.TOPRIGHT;
                case "BOTTOMLEFT":
                    return Housing.BOTTOMLEFT;
                case "BOTTOM":
                    return Housing.BOTTOM;
                case "BOTTOMRIGHT":
                    return Housing.BOTTOMRIGHT;

            }

            return Housing.NONE;

        }

        private Roading StrToRoadCoords(string pos)
        {


            switch (pos)
            {

                case "TOPLEFT":
                    return Roading.TOPLEFT;
                case "LEFT":
                    return Roading.LEFT;
                case "TOPRIGHT":
                    return Roading.TOPRIGHT;
                case "BOTTOMLEFT":
                    return Roading.BOTTOMLEFT;
                case "RIGHT":
                    return Roading.RIGHT;
                case "BOTTOMRIGHT":
                    return Roading.BOTTOMRIGHT;

            }

            return Roading.NONE;

        }

        private void joingame_Click(object sender, EventArgs e)
        {
            if (waiting_for_players)
                return;

            bool initiated = false;
            foreach (string fileName in Directory.GetFiles(AppDomain.CurrentDomain.BaseDirectory))
            {

                if (fileName.Contains("data.txt"))
                    initiated = true;

            }

            if (!initiated)
                return;

            startgame.Visible = false;
            startgame.Enabled = false;

            joingame.Visible = false;
            joingame.Enabled = false;
            Node<Players> playing = new Node<Players>(Players.None);
            foreach (string fileName in Directory.GetFiles(AppDomain.CurrentDomain.BaseDirectory))
            {

                if (fileName.Contains(".txt") && !fileName.Contains("data.txt"))
                {
                    playerbox.Text += "\r\n" + fileName.Split('\\').Last().Replace(".txt", "");
                    if (playing.GetValue() == Players.None)
                        playing.SetValue(GetPlayer(fileName.Split('\\').Last().Replace(".txt", "")));
                    else
                    {

                        playing = new Node<Players>(GetPlayer(fileName.Split('\\').Last().Replace(".txt", "")), playing);

                    }
                }
            }

            do
            {

                player = (Players)rnd.Next(6);

            } while (playerbox.Text.Contains(player.ToString()));

            game = new Game(new Node<Players>(player, playing), gameboard, false);

            show_color.Text = "Color: " + player;
            show_color.BackColor = GetPlayerColor(player);
            if (show_color.BackColor != Color.White)
                show_color.ForeColor = Color.White;
            else
                show_color.ForeColor = Color.Black;
            show_color.Font = new Font(show_color.Font, FontStyle.Bold);

            File.WriteAllText($"{player}.txt", "");
            playerbox.Text += $"\r\n{player}";
            is_not_init = true;
        }

        private Players GetPlayer(string s)
        {

            switch (s)
            {

                case "Blue":
                    return Players.Blue;
                case "Orange":
                    return Players.Orange;
                case "Green":
                    return Players.Green;
                case "White":
                    return Players.White;
                case "Red":
                    return Players.Red;
                case "Brown":
                    return Players.Brown;

            }
            return Players.None;

        }

        private string GetPlayerStr(Players p)
        {

            switch (p)
            {

                case Players.Blue:
                    return "Blue";
                case Players.Orange:
                    return "Orange";
                case Players.Green:
                    return "Green";
                case Players.White:
                    return "White";
                case Players.Red:
                    return "Red";
                case Players.Brown:
                    return "Brown";

            }
            return "";

        }

        private Color GetPlayerColor(Players p)
        {

            switch(p)
            {

                case Players.White:
                    return Color.White;
                case Players.Blue:
                    return Color.Blue;
                case Players.Green:
                    return Color.Green;
                case Players.Brown:
                    return Color.Brown;
                case Players.Orange:
                    return Color.Orange;
                case Players.Red:
                    return Color.Red;

            }

            return Color.Black;

        }

        private void gameboard_MouseClick(object sender, MouseEventArgs e)
        {
           

            if (!game_started || turn != player)
                return;

            if (action == GameAction.House)
            {

                if (initial_house < 2)
                {

                    if (game.PutHouse(e.X, e.Y, player))
                    {
                        initial_house++;
                        if(initial_house == 1)
                            game.GrantInitialResources(player);
                        game.DrawBoard();
                        game.AddVictoryPoints(player, 1);
                        vp.Text = "Victory Points: " + game.GetVictoryPoints(player);
                        Update_Resources();
                        while (IsFileLocked(new FileInfo(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt")))
                            continue;
                        string data = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt");
                        string rest_of_data = string.Join("\n", data.Split('\n').Skip(1).ToArray());
                        File.WriteAllText("data.txt", $"ACTION=HOUSE:{game.last_placed_index}:{game.last_placed_position}\n" + rest_of_data);
                    }
                    show_action.Text = "Action Selected: None";
                    action = GameAction.None;
                    return;

                }

                 if (!game.Buy(player, GameAction.House))
                 {
                        notifier.Text = "Message: Not Enough Resources";
                        return;
                 }

                if (!game.PutHouse(e.X, e.Y, player))
                {
                    notifier.Text = "Message: Couldn't Place House";
                    game.GrantResource(player, Resource.Wood);
                    game.GrantResource(player, Resource.Brick);
                    game.GrantResource(player, Resource.Hay);
                    game.GrantResource(player, Resource.Sheep);
                }
                else
                {
                    game.AddVictoryPoints(player, 1);
                    game.DrawBoard();
                    vp.Text = "Victory Points: " + game.GetVictoryPoints(player);
                    while (IsFileLocked(new FileInfo(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt")))
                        continue;
                    string data = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt");
                    string rest_of_data = string.Join("\n", data.Split('\n').Skip(1).ToArray());
                    File.WriteAllText("data.txt", $"ACTION=HOUSE:{game.last_placed_index}:{game.last_placed_position}\n" + rest_of_data);

                }
                show_action.Text = "Action Selected: None";
                action = GameAction.None;
            }
            else if (action == GameAction.Road)
            {

                if (initial_road < 2)
                {

                    if (game.PutRoad(e.X, e.Y, player))
                    {
                        initial_road++;
                        while (IsFileLocked(new FileInfo(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt")))
                            continue;
                        string data = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt");
                        string rest_of_data = string.Join("\n", data.Split('\n').Skip(1).ToArray());
                        File.WriteAllText("data.txt", $"ACTION=ROAD:{game.last_placed_index}:{game.last_placed_road_position}\n" + rest_of_data);
                        game.DrawBoard();
                    }
                    show_action.Text = "Action Selected: None";
                    action = GameAction.None;

                    return;

                }

                 if (!game.Buy(player, GameAction.Road))
                 {
                        notifier.Text = "Message: Not Enough Resources";
                        return;
                 }
                
                if (!game.PutRoad(e.X, e.Y, player))
                {
                    notifier.Text = "Message: Couldn't Place Road";

                    game.GrantResource(player, Resource.Wood);
                    game.GrantResource(player, Resource.Brick);

                }
                else
                {
                    while (IsFileLocked(new FileInfo(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt")))
                        continue;
                    string data = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt");
                    string rest_of_data = string.Join("\n", data.Split('\n').Skip(1).ToArray());
                    File.WriteAllText("data.txt", $"ACTION=ROAD:{game.last_placed_index}:{game.last_placed_road_position}\n" + rest_of_data);
                    game.DrawBoard();
                }

                show_action.Text = "Action Selected: None";
                action = GameAction.None;

            }
            else if (action == GameAction.Robber)
            {
                int prev_ind = game.robber_index;
                Resource r = game.PlaceRobber(e.X, e.Y);
                game.DrawBoard();

                if (prev_ind != game.robber_index)
                {
                    if (r != Resource.None)
                        game.GrantResource(player, r);

                    while (IsFileLocked(new FileInfo(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt")))
                        continue;
                    string data = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt");
                    string rest_of_data = string.Join("\n", data.Split('\n').Skip(1).ToArray());
                    File.WriteAllText("data.txt", $"ACTION=ROBBER:{game.robber_index}\n" + rest_of_data);

                    show_action.Text = "Action Selected: None";
                    action = GameAction.None;

                }


            }

            Update_Resources();

        }
        protected virtual bool IsFileLocked(FileInfo file)
        {
            try
            {
                using (FileStream stream = file.Open(FileMode.Open, FileAccess.Read, FileShare.None))
                {
                    stream.Close();
                }
            }
            catch (IOException)
            {
                //the file is unavailable because it is:
                //still being written to
                //or being processed by another thread
                //or does not exist (has already been processed)
                Thread.Sleep(500);

                return true;
            }

            //file is not locked
            return false;
        }


        private void Update_Resources()
        {

            int[] resources = game.GetResources(player);

            wood.Text = $"Wood: {resources[(int)Resource.Wood]}";
            hay.Text = $"Hay: {resources[(int)Resource.Hay]}";
            stone.Text = $"Stone: {resources[(int)Resource.Stone]}";
            sheep.Text = $"Sheep: {resources[(int)Resource.Sheep]}";
            brick.Text = $"Brick: {resources[(int)Resource.Brick]}";

        }

        private void house_Click(object sender, EventArgs e)
        {

            if (game_started && turn == player)
            {

                action = GameAction.House;
                show_action.Text = "Action Selected: Place House";

            }

        }

        private void road_Click(object sender, EventArgs e)
        {
            if (game_started && turn == player)
            {

                action = GameAction.Road;
                show_action.Text = "Action Selected: Place Road";

            }
        }

        private void Dice_Click(object sender, EventArgs e)
        {

            if (game_started && turn == player)
            {

                game.RollDice();

                show_dice.Text = "Dice: " + game.dice.ToString();

                game.GrantDiceResources();

                Update_Resources();

                if (game.dice == 7)
                {

                    action = GameAction.Robber;
                    show_action.Text = "Action Selected: Place Robber";

                }

                while (IsFileLocked(new FileInfo(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt")))
                    continue;
                string data = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt");
                string rest_of_data = string.Join("\n", data.Split('\n').Skip(1).ToArray());
                File.WriteAllText("data.txt", $"ACTION=DICE:{game.dice}\n" + rest_of_data);

            }

        }

        private T RandomEnumValue<T>()
        {
            var v = Enum.GetValues(typeof(T));
            return (T)v.GetValue(rnd.Next(v.Length-1));
        }

        private void buycard_Click(object sender, EventArgs e)
        {

            if (game_started && turn == player)
            {

                if (!game.Buy(player, GameAction.Card))
                {
                    notifier.Text = "Message: Not Enough Resources";
                    return;
                }
                Cards card = RandomEnumValue<Cards>();
                game.GrantCard(player, card);

                cards.Text += $", {card}";

                Update_Resources();

            }

        }

        private void card_Click(object sender, EventArgs e)
        {

            if (game_started && turn == player)
            {

                if (!game.UseCardIfAvailable(typecard.Text, player))
                    notifier.Text = "Message: Couldn't find card";
                else
                {

                    cards.Text = cards.Text.Remove(cards.Text.IndexOf(", " + typecard.Text), (", " + typecard.Text).Length);

                    if (typecard.Text == "Vp")
                        game.AddVictoryPoints(player, 1);
                    else if (typecard.Text == "TwoRoads")
                        initial_road = 0;
                    else if (typecard.Text == "YearOfPlenty")
                    {

                        game.GrantResource(player, RandomEnumValue<Resource>());
                        game.GrantResource(player, RandomEnumValue<Resource>());
                        Update_Resources();
                    }
                }

            }

        }

        private void Endturn_Click(object sender, EventArgs e)
        {
            if (game_started && turn == player)
            {
                while (IsFileLocked(new FileInfo(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt")))
                    continue;
                string data = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "\\data.txt");
                string rest_of_data = string.Join("\n", data.Split('\n').Skip(1).ToArray());
                File.WriteAllText("data.txt", $"ACTION=PASSTURN\n" + rest_of_data);

            }
        }

        void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {

            if (!host)
                return;

            string[] filePaths = Directory.GetFiles(AppDomain.CurrentDomain.BaseDirectory, "*.txt");
            foreach (string filePath in filePaths)
                File.Delete(filePath);
        }

        void OnProcessExit(object sender, EventArgs e)
        {
            if (!host)
                return;

            string[] filePaths = Directory.GetFiles(AppDomain.CurrentDomain.BaseDirectory, "*.txt");
            foreach (string filePath in filePaths)
                File.Delete(filePath);
        }

    }
}
