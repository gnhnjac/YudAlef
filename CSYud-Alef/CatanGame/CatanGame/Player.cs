using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CatanGame
{
    internal class Player
    {
        public Players color { get; set; }

        public int victory_points { get; set; }

        public Player(Players c)
        {

            this.color = c;

            this.victory_points = 0;

        }

        public override string ToString()
        {
            return this.color.ToString();
        }

    }
}
