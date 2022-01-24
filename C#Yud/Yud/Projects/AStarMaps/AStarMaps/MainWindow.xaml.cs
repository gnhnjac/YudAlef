using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Color = System.Drawing.Color;

namespace AStarMaps
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();

            Bitmap img = new Bitmap("..\\..\\Resources\\snazzy-image.png");

            Bitmap paths = new Bitmap(img.Width, img.Height);

            Node[,] map = new Node[img.Width, img.Height];

            for (int i = 0; i < img.Width; i++)
            {
                for (int j = 0; j < img.Height; j++)
                {
                    Color pixel = img.GetPixel(i, j);

                    map[i, j] = new Node(i, j);

                    if (pixel.R == 255 && pixel.G == 255 && pixel.B == 255)
                        paths.SetPixel(i, j, Color.White);

                    else
                    {

                        paths.SetPixel(i, j, Color.Black);
                        map[i, j].isObstacle = true;

                    }

                }
            }

            MapManager mm = new MapManager(PathCanvas, map, img.Width, img.Height);

            int state;

            do
            {

                state = mm.updateBoard();

            } while (state == 0);

            mm.retracePath();

            paths.Save("..\\..\\Resources\\paths.png", ImageFormat.Png);

            MapImage.Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "..\\..\\Resources\\paths.png", UriKind.Absolute));

        }
    }
}
