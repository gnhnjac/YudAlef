using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Nodes3
{
    class Smell
    {

        private string name;
        private int strength;
        private int percent;

        public Smell(string name, int strength, int smell_percent)
        {

            this.name = name;

            this.strength = strength;

            this.percent = smell_percent;

        }

        public string GetName()
        {

            return name;

        }

        public int GetStrength()
        {

            return strength;

        }

        public int GetPercent()
        {

            return percent;

        }

        public void SetName(string name)
        {

            this.name = name;

        }

        public void SetStrength(int s)
        {

            this.strength = s;

        }

        public void SetPercent(int p)
        {

            this.percent = p;

        }



    }
}
