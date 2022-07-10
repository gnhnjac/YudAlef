using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
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
using System.Windows.Threading;

namespace AStar
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        static int ROWS = 50;
        static int COLS = 50;

        static Random rnd = new Random();

        DispatcherTimer timer = new DispatcherTimer();

        BoardManager bm;

        bool done = false;

        public MainWindow()
        {
            InitializeComponent();

            bm = new BoardManager(gameCanvas, COLS, ROWS);

            //int i = bm.updateBoard();

            //while (i == 0)
            //{

            //    i = bm.updateBoard();
            //    Dispatcher.Invoke(new Action(() => { }), DispatcherPriority.ContextIdle);
            //    Thread.Sleep(200);

            //}

            //if (i == -1)
            //    Console.WriteLine("No Path");

            //else
            //    bm.retracePath();

        }

        void updateBoard(object sender, EventArgs e)
        {

            int i = bm.updateBoard();

            if (i == -1)
                timer.Stop();

            else if (i == 1)
            {

                bm.retracePath();
                timer.Stop();
                done = true;

            }

            else
                bm.retracePath();

        }

        private void LeftClick(object sender, MouseEventArgs e)
        {

            if (done)
                return;

            if (!timer.IsEnabled && e.LeftButton == MouseButtonState.Pressed)
                bm.addObstacle(e.GetPosition(gameCanvas).X, e.GetPosition(gameCanvas).Y);

            e.Handled = true;

        }

        private void startPathFinding(object sender, RoutedEventArgs e)
        {

            if (done)
                return;

            timer.Interval = TimeSpan.FromSeconds(0.01);
            timer.Tick += updateBoard;
            timer.Start();

        }

        private void toggleNodes(object sender, RoutedEventArgs e)
        {
            bm.toggleNodes();

            e.Handled = true;
        }

        private void toggleClosed(object sender, RoutedEventArgs e)
        {

            bm.toggleClosed();

            e.Handled = true;

        }
    }
}
