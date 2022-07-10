using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Controls.Primitives;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace MineSweeper
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        static int ROWS = 16;

        static int COLS = 16;

        static int MINES = 40;

        BoardManager bm;

        bool failed = false;
        
        public MainWindow()
        {

            InitializeComponent();

            bm = new BoardManager(GameCanvas);

            bm.Initialize(ROWS, COLS, MINES);

            bm.initializeVisuals();

            Mines.Text = "Mines Left: " + bm.mines_left.ToString();

        }

        private void LeftClick(object sender, MouseButtonEventArgs e)
        {

            if (failed)
                return;

            if (bm.exposeCell(e.GetPosition(GameCanvas).X, e.GetPosition(GameCanvas).Y))
            {

                failed = true;
                return;

            }

            bm.Draw();

            e.Handled = true;

        }

        private void RightClick(object sender, MouseButtonEventArgs e)
        {

            if (failed)
                return;

            bm.flagCell(e.GetPosition(GameCanvas).X, e.GetPosition(GameCanvas).Y);

            bm.Draw();

            Mines.Text = "Mines Left: " + bm.mines_left.ToString();

            e.Handled = true;

        }

        private void Reset(object sender, RoutedEventArgs e)
        {

            bm.Initialize(ROWS, COLS, MINES);

            bm.Draw();

            Mines.Text = "Mines Left: " + bm.mines_left.ToString();

            failed = false;

            e.Handled = true;

        }

        private void ScrollClick(object sender, MouseButtonEventArgs e)
        {

            if (failed)
                return;

            if (e.ChangedButton == MouseButton.Middle && e.ButtonState == MouseButtonState.Pressed)
            {

                if (bm.quickExpose(e.GetPosition(GameCanvas).X, e.GetPosition(GameCanvas).Y))
                {

                    failed = true;
                    return;

                }

            }

            bm.Draw();

            e.Handled = true;

        }
    }
}
