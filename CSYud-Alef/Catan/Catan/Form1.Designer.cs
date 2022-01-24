namespace Catan
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.gameboard = new System.Windows.Forms.Panel();
            this.joingame = new System.Windows.Forms.Button();
            this.waitingfor = new System.Windows.Forms.TextBox();
            this.startgame = new System.Windows.Forms.Button();
            this.house = new System.Windows.Forms.Button();
            this.road = new System.Windows.Forms.Button();
            this.card = new System.Windows.Forms.Button();
            this.show_action = new System.Windows.Forms.TextBox();
            this.vp = new System.Windows.Forms.TextBox();
            this.show_color = new System.Windows.Forms.TextBox();
            this.notifier = new System.Windows.Forms.TextBox();
            this.wood = new System.Windows.Forms.TextBox();
            this.stone = new System.Windows.Forms.TextBox();
            this.hay = new System.Windows.Forms.TextBox();
            this.sheep = new System.Windows.Forms.TextBox();
            this.brick = new System.Windows.Forms.TextBox();
            this.dice = new System.Windows.Forms.Button();
            this.show_dice = new System.Windows.Forms.TextBox();
            this.buycard = new System.Windows.Forms.Button();
            this.cards = new System.Windows.Forms.TextBox();
            this.cardquestion = new System.Windows.Forms.TextBox();
            this.typecard = new System.Windows.Forms.TextBox();
            this.contextMenuStrip1 = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.playerbox = new System.Windows.Forms.TextBox();
            this.showturn = new System.Windows.Forms.TextBox();
            this.endturn = new System.Windows.Forms.Button();
            this.gameboard.SuspendLayout();
            this.SuspendLayout();
            // 
            // gameboard
            // 
            this.gameboard.Controls.Add(this.joingame);
            this.gameboard.Controls.Add(this.waitingfor);
            this.gameboard.Controls.Add(this.startgame);
            this.gameboard.Location = new System.Drawing.Point(208, 22);
            this.gameboard.Name = "gameboard";
            this.gameboard.Size = new System.Drawing.Size(400, 400);
            this.gameboard.TabIndex = 0;
            this.gameboard.MouseClick += new System.Windows.Forms.MouseEventHandler(this.gameboard_MouseClick);
            // 
            // joingame
            // 
            this.joingame.Location = new System.Drawing.Point(238, 1);
            this.joingame.Name = "joingame";
            this.joingame.Size = new System.Drawing.Size(75, 23);
            this.joingame.TabIndex = 3;
            this.joingame.Text = "Join Game";
            this.joingame.UseVisualStyleBackColor = true;
            this.joingame.Click += new System.EventHandler(this.joingame_Click);
            // 
            // waitingfor
            // 
            this.waitingfor.Location = new System.Drawing.Point(107, 29);
            this.waitingfor.Name = "waitingfor";
            this.waitingfor.ReadOnly = true;
            this.waitingfor.Size = new System.Drawing.Size(179, 20);
            this.waitingfor.TabIndex = 2;
            this.waitingfor.Text = "Waiting for players...";
            this.waitingfor.Visible = false;
            // 
            // startgame
            // 
            this.startgame.Location = new System.Drawing.Point(157, 0);
            this.startgame.Name = "startgame";
            this.startgame.Size = new System.Drawing.Size(75, 23);
            this.startgame.TabIndex = 1;
            this.startgame.Text = "Start Game";
            this.startgame.UseVisualStyleBackColor = true;
            this.startgame.Click += new System.EventHandler(this.button1_Click);
            // 
            // house
            // 
            this.house.Location = new System.Drawing.Point(249, 428);
            this.house.Name = "house";
            this.house.Size = new System.Drawing.Size(104, 23);
            this.house.TabIndex = 1;
            this.house.Text = "Place House";
            this.house.UseVisualStyleBackColor = true;
            this.house.Click += new System.EventHandler(this.house_Click);
            // 
            // road
            // 
            this.road.Location = new System.Drawing.Point(359, 428);
            this.road.Name = "road";
            this.road.Size = new System.Drawing.Size(104, 23);
            this.road.TabIndex = 2;
            this.road.Text = "Place Road";
            this.road.UseVisualStyleBackColor = true;
            this.road.Click += new System.EventHandler(this.road_Click);
            // 
            // card
            // 
            this.card.Location = new System.Drawing.Point(469, 428);
            this.card.Name = "card";
            this.card.Size = new System.Drawing.Size(104, 23);
            this.card.TabIndex = 3;
            this.card.Text = "Use Card";
            this.card.UseVisualStyleBackColor = true;
            this.card.Click += new System.EventHandler(this.card_Click);
            // 
            // show_action
            // 
            this.show_action.Location = new System.Drawing.Point(12, 74);
            this.show_action.Name = "show_action";
            this.show_action.ReadOnly = true;
            this.show_action.Size = new System.Drawing.Size(189, 20);
            this.show_action.TabIndex = 4;
            this.show_action.Text = "Action Selected: None";
            // 
            // vp
            // 
            this.vp.Location = new System.Drawing.Point(12, 48);
            this.vp.Name = "vp";
            this.vp.ReadOnly = true;
            this.vp.Size = new System.Drawing.Size(100, 20);
            this.vp.TabIndex = 5;
            this.vp.Text = "Victory Points: 0";
            // 
            // show_color
            // 
            this.show_color.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.show_color.Location = new System.Drawing.Point(13, 22);
            this.show_color.Name = "show_color";
            this.show_color.ReadOnly = true;
            this.show_color.Size = new System.Drawing.Size(100, 20);
            this.show_color.TabIndex = 6;
            this.show_color.Text = "Color: ";
            // 
            // notifier
            // 
            this.notifier.Location = new System.Drawing.Point(12, 100);
            this.notifier.Name = "notifier";
            this.notifier.ReadOnly = true;
            this.notifier.Size = new System.Drawing.Size(189, 20);
            this.notifier.TabIndex = 7;
            this.notifier.Text = "Message: ";
            // 
            // wood
            // 
            this.wood.Location = new System.Drawing.Point(12, 127);
            this.wood.Multiline = true;
            this.wood.Name = "wood";
            this.wood.ReadOnly = true;
            this.wood.Size = new System.Drawing.Size(100, 20);
            this.wood.TabIndex = 8;
            this.wood.Text = "Wood: ";
            // 
            // stone
            // 
            this.stone.Location = new System.Drawing.Point(12, 153);
            this.stone.Name = "stone";
            this.stone.ReadOnly = true;
            this.stone.Size = new System.Drawing.Size(100, 20);
            this.stone.TabIndex = 9;
            this.stone.Text = "Stone: ";
            // 
            // hay
            // 
            this.hay.Location = new System.Drawing.Point(12, 179);
            this.hay.Name = "hay";
            this.hay.ReadOnly = true;
            this.hay.Size = new System.Drawing.Size(100, 20);
            this.hay.TabIndex = 10;
            this.hay.Text = "Hay: ";
            // 
            // sheep
            // 
            this.sheep.Location = new System.Drawing.Point(12, 205);
            this.sheep.Name = "sheep";
            this.sheep.ReadOnly = true;
            this.sheep.Size = new System.Drawing.Size(100, 20);
            this.sheep.TabIndex = 11;
            this.sheep.Text = "Sheep: ";
            // 
            // brick
            // 
            this.brick.Location = new System.Drawing.Point(12, 231);
            this.brick.Name = "brick";
            this.brick.ReadOnly = true;
            this.brick.Size = new System.Drawing.Size(100, 20);
            this.brick.TabIndex = 12;
            this.brick.Text = "Brick: ";
            // 
            // dice
            // 
            this.dice.BackColor = System.Drawing.SystemColors.Highlight;
            this.dice.Cursor = System.Windows.Forms.Cursors.Hand;
            this.dice.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.dice.Location = new System.Drawing.Point(12, 257);
            this.dice.Name = "dice";
            this.dice.Size = new System.Drawing.Size(100, 55);
            this.dice.TabIndex = 13;
            this.dice.Text = "Roll Dice";
            this.dice.UseVisualStyleBackColor = false;
            this.dice.Click += new System.EventHandler(this.Dice_Click);
            // 
            // show_dice
            // 
            this.show_dice.Location = new System.Drawing.Point(12, 318);
            this.show_dice.Name = "show_dice";
            this.show_dice.ReadOnly = true;
            this.show_dice.Size = new System.Drawing.Size(100, 20);
            this.show_dice.TabIndex = 14;
            this.show_dice.Text = "Dice: ";
            // 
            // buycard
            // 
            this.buycard.Location = new System.Drawing.Point(12, 344);
            this.buycard.Name = "buycard";
            this.buycard.Size = new System.Drawing.Size(100, 23);
            this.buycard.TabIndex = 15;
            this.buycard.Text = "Buy Card";
            this.buycard.UseVisualStyleBackColor = true;
            this.buycard.Click += new System.EventHandler(this.buycard_Click);
            // 
            // cards
            // 
            this.cards.AcceptsReturn = true;
            this.cards.Location = new System.Drawing.Point(619, 25);
            this.cards.Multiline = true;
            this.cards.Name = "cards";
            this.cards.ReadOnly = true;
            this.cards.Size = new System.Drawing.Size(168, 95);
            this.cards.TabIndex = 16;
            this.cards.Text = "Development Cards: ";
            // 
            // cardquestion
            // 
            this.cardquestion.Location = new System.Drawing.Point(619, 127);
            this.cardquestion.Name = "cardquestion";
            this.cardquestion.ReadOnly = true;
            this.cardquestion.Size = new System.Drawing.Size(100, 20);
            this.cardquestion.TabIndex = 17;
            this.cardquestion.Text = "Which Card?";
            // 
            // typecard
            // 
            this.typecard.Location = new System.Drawing.Point(619, 153);
            this.typecard.Name = "typecard";
            this.typecard.Size = new System.Drawing.Size(100, 20);
            this.typecard.TabIndex = 18;
            // 
            // contextMenuStrip1
            // 
            this.contextMenuStrip1.Name = "contextMenuStrip1";
            this.contextMenuStrip1.Size = new System.Drawing.Size(61, 4);
            // 
            // playerbox
            // 
            this.playerbox.AcceptsReturn = true;
            this.playerbox.Location = new System.Drawing.Point(619, 179);
            this.playerbox.Multiline = true;
            this.playerbox.Name = "playerbox";
            this.playerbox.ReadOnly = true;
            this.playerbox.Size = new System.Drawing.Size(168, 243);
            this.playerbox.TabIndex = 19;
            this.playerbox.Text = "Players:";
            // 
            // showturn
            // 
            this.showturn.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.showturn.Location = new System.Drawing.Point(619, 428);
            this.showturn.Name = "showturn";
            this.showturn.ReadOnly = true;
            this.showturn.Size = new System.Drawing.Size(100, 20);
            this.showturn.TabIndex = 20;
            this.showturn.Text = "Turn: ";
            // 
            // endturn
            // 
            this.endturn.Location = new System.Drawing.Point(13, 374);
            this.endturn.Name = "endturn";
            this.endturn.Size = new System.Drawing.Size(99, 23);
            this.endturn.TabIndex = 21;
            this.endturn.Text = "End Turn";
            this.endturn.UseVisualStyleBackColor = true;
            this.endturn.Click += new System.EventHandler(this.Endturn_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.endturn);
            this.Controls.Add(this.showturn);
            this.Controls.Add(this.playerbox);
            this.Controls.Add(this.typecard);
            this.Controls.Add(this.cardquestion);
            this.Controls.Add(this.cards);
            this.Controls.Add(this.buycard);
            this.Controls.Add(this.show_dice);
            this.Controls.Add(this.dice);
            this.Controls.Add(this.brick);
            this.Controls.Add(this.sheep);
            this.Controls.Add(this.hay);
            this.Controls.Add(this.stone);
            this.Controls.Add(this.wood);
            this.Controls.Add(this.notifier);
            this.Controls.Add(this.show_color);
            this.Controls.Add(this.vp);
            this.Controls.Add(this.show_action);
            this.Controls.Add(this.card);
            this.Controls.Add(this.road);
            this.Controls.Add(this.house);
            this.Controls.Add(this.gameboard);
            this.MinimizeBox = false;
            this.Name = "Form1";
            this.Text = "Form1";
            this.gameboard.ResumeLayout(false);
            this.gameboard.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Panel gameboard;
        private System.Windows.Forms.Button startgame;
        private System.Windows.Forms.Button house;
        private System.Windows.Forms.Button road;
        private System.Windows.Forms.Button card;
        private System.Windows.Forms.TextBox show_action;
        private System.Windows.Forms.TextBox vp;
        private System.Windows.Forms.TextBox show_color;
        private System.Windows.Forms.TextBox notifier;
        private System.Windows.Forms.TextBox wood;
        private System.Windows.Forms.TextBox stone;
        private System.Windows.Forms.TextBox hay;
        private System.Windows.Forms.TextBox sheep;
        private System.Windows.Forms.TextBox brick;
        private System.Windows.Forms.Button dice;
        private System.Windows.Forms.TextBox show_dice;
        private System.Windows.Forms.Button buycard;
        private System.Windows.Forms.TextBox cards;
        private System.Windows.Forms.TextBox cardquestion;
        private System.Windows.Forms.TextBox typecard;
        private System.Windows.Forms.TextBox waitingfor;
        private System.Windows.Forms.ContextMenuStrip contextMenuStrip1;
        private System.Windows.Forms.TextBox playerbox;
        private System.Windows.Forms.Button joingame;
        private System.Windows.Forms.TextBox showturn;
        private System.Windows.Forms.Button endturn;
    }
}

