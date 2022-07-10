using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace AnalogClock
{
    class Program
    {

        static int RADIUS = 20;

        static void Main(string[] args)
        {

            Clock analog = new Clock(0, 0, RADIUS);

            DateTime now = DateTime.Now;

            double minute_degree = (270 + now.Minute * 360 / 60)%360;

            double hour_degree = (270 + (now.Hour*60+now.Minute) * 360 / (12*60)) % 360;

            double m_hand_len = RADIUS*2.8/4;

            double h_hand_len = RADIUS*2.3/4;

            analog.DrawHand(minute_degree, false, m_hand_len);
            analog.DrawHand(hour_degree, false, h_hand_len);


            while (true)
            {

                now = DateTime.Now;

                double new_m_degree = (270 + now.Minute * 360 / 60) % 360;

                if (new_m_degree != minute_degree)
                {

                    analog.DrawHand(minute_degree, true, m_hand_len);
                    analog.DrawHand(new_m_degree, false, m_hand_len);
                    minute_degree = new_m_degree;
                }

                double new_h_degree = (270 + (now.Hour * 60 + now.Minute) * 360 / (12 * 60)) % 360;
                if (new_h_degree != hour_degree)
                {

                    analog.DrawHand(hour_degree, true, h_hand_len);
                    analog.DrawHand(new_h_degree, false, h_hand_len);
                    hour_degree = new_h_degree;
                }

            }

        }
    }
}
