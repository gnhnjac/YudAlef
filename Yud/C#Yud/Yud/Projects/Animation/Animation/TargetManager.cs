using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Animation
{
    class TargetManager
    {

        static char block = '█';

        int create_interval;

        List<Target> t_list = new List<Target>();

        public TargetManager(int interval)
        {

            create_interval = interval;

            var target_create = new Timer((e) =>
            {
                createTarget();
            }, null, TimeSpan.Zero, TimeSpan.FromSeconds(create_interval));

        }
        void createTarget()
        {

            t_list.Add(new Target());

        }

        public void showTargets()
        {

            for (int i = 0; i < t_list.Count; i++)
            {

                t_list[i].Show();

            }

        }

        public int updateTargets(Person player)
        {

            int return_code = 0;

            for (int i = 0; i < t_list.Count; i++)
            {

                Target t = t_list[i];

                bool isManEating = player.isEating(t.X, (int)t.Y);

                if (player.isEating(t.X, (int)t.Y))
                {

                    t.Clear();
                    t_list.RemoveAt(i);
                    return_code = 1;
                    continue;

                }

                if (!t.InBounds() || player.isBumping(t.X, (int)t.Y))
                {

                    t.Clear();
                    t_list.RemoveAt(i);
                    return_code = -1;
                    continue;

                }

                t.Update();

            }

            return return_code;

        }

    }
}
