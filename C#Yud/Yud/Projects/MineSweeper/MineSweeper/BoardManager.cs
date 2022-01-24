using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace MineSweeper
{
    class BoardManager
    {

        Random rnd = new Random();

        Cell[,] Board;

        int mines;
        public int mines_left;

        int rows;
        int cols;

        int width;
        int height;

        Canvas canvas;

        bool minesGenerated;

        public BoardManager(Canvas _canvas)
        {

            canvas = _canvas;

        }

        public void Initialize(int x, int y, int mine_amount)
        {

            rows = x;
            cols = y;

            Board = new Cell[y, x];

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    Board[i, j] = new Cell();

                }

            }

            mines = mine_amount;

            mines_left = mines;

            minesGenerated = false;

            height = (int)(canvas.Height) / cols;
            width = (int)(canvas.Width) / rows;

            for (int i = canvas.Children.Count - 1; i >= 0; i --)
            {
                UIElement Child = canvas.Children[i];
                if (Child is Line)
                    canvas.Children.Remove(Child);
            }

        }

        public void initializeVisuals()
        {

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    // Top left
                    Border cell_tl = new Border
                    {

                        Height = height,
                        Width = width,
                        BorderThickness = new Thickness(3, 3, 0, 0),
                        BorderBrush = Brushes.White,
                        Background = Brushes.LightGray

                    };

                    // Bottom right
                    Border cell_br = new Border
                    {

                        Height = height,
                        Width = width,
                        BorderThickness = new Thickness(0, 0, 3, 3),
                        BorderBrush = Brushes.Gray,

                    };

                    cell_br.Child = cell_tl;

                    canvas.Children.Add(cell_br);

                    Canvas.SetTop(cell_br, i * height);
                    Canvas.SetLeft(cell_br, j * width);

                }

            }

        }

        void generateMines(int mx, int my)
        {

            if (minesGenerated)
                return;

            for (int i = 0; i < mines; i++)
            {

                int rx = rnd.Next(rows);
                int ry = rnd.Next(cols);

                while (Board[ry, rx].isBomb || (rx == mx && ry == my))
                {

                    rx = rnd.Next(rows);
                    ry = rnd.Next(cols);

                }

                Board[ry, rx].isBomb = true;

            }

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    Board[i, j].value = getNeighboringBombs(i, j);

                }

            }

            minesGenerated = true;

        }

        public void Draw()
        {

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    drawCell(i, j);

                }

            }

        }

        void drawCell(int i, int j)
        {

            Border parent = (Border)canvas.Children[i * cols + j];

            Border main = (Border)parent.Child;

            if (Board[i, j].state == State.Revealed)
            {

                TextBlock value = new TextBlock
                {

                    Text = Board[i, j].value.ToString(),
                    FontSize = 20,
                    VerticalAlignment = VerticalAlignment.Center

                };


                if(Board[i, j].value != 0)
                    main.Child = value;

                main.BorderThickness = new Thickness(0);

                parent.BorderThickness = new Thickness(1);

            }
            else if (Board[i, j].state == State.Flagged)
            {

                Image flag = new Image()
                {

                    Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "..\\..\\Images\\Flag2.png", UriKind.Absolute)),
                    Stretch = Stretch.Uniform,
                    HorizontalAlignment = HorizontalAlignment.Center,
                    VerticalAlignment = VerticalAlignment.Center

                };

                main.Child = flag;

            }
            else
            {

                main.BorderThickness = new Thickness(3, 3, 0, 0);

                parent.BorderThickness = new Thickness(0, 0, 3, 3);

                main.Child = null;

                main.Background = Brushes.LightGray;

            }

            return;

        }

        int getNeighboringBombs(int i, int j)
        {

            if (Board[i, j].isBomb)
                return -1;

            int bombs = 0;

            for (int k = -1; k < 2; k++)
            {

                for (int l = -1; l < 2; l++)
                {

                    if (i + k < 0 || i + k >= cols || j + l < 0 || j + l >= rows || (k == 0 && l == 0))
                        continue;

                    if (Board[i + k, j + l].isBomb)
                        bombs++;

                }

            }

            return bombs;

        }

        public bool exposeCell(double x, double y)
        {

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    if (i * height <= y && i * height + height >= y && j * width <= x && j * width + width >= x)
                    {

                        if (Board[i, j].state == State.Flagged)
                            return false;

                        generateMines(j, i);

                        if (Board[i, j].value == 0)
                        {

                            exposeNeighbors(i, j);

                        }
                        else if (Board[i, j].value > 0)
                        {

                            Board[i, j].state = State.Revealed;

                        }
                        else
                        {

                            endGame(i, j);
                            return true;

                        }

                        if (checkWin())
                        {
                            Draw();
                            endGame(i, j);
                            return true;

                        }

                        return false;

                    }

                }

            }

            return false;

        }

        void exposeNeighbors(int i, int j)
        {

            Board[i, j].state = State.Revealed;

            for (int k = -1; k < 2; k++)
            {

                for (int l = -1; l < 2; l++)
                {

                    if (i + k < 0 || i + k >= cols || j + l < 0 || j + l >= rows || (k == 0 && l == 0))
                        continue;

                    if (Board[i + k, j + l].state == State.Revealed || Board[i + k, j + l].state == State.Flagged)
                        continue;

                    if (Board[i + k, j + l].value == 0)
                        exposeNeighbors(i + k, j + l);

                    if (Board[i + k, j + l].value > 0)
                        Board[i + k, j + l].state = State.Revealed;

                }

            }

        }

        public void flagCell(double x, double y)
        {

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    if (i * height <= y && i * height + height >= y && j * width <= x && j * width + width >= x)
                    {

                        if (Board[i, j].state == State.Revealed)
                            return;

                        if (Board[i, j].state == State.Flagged)
                        {

                            mines_left++;
                            Board[i, j].state = State.Closed;
                            return;

                        }

                        Board[i, j].state = State.Flagged;
                        mines_left--;
                        return;

                    }

                }

            }

        }

        public bool quickExpose(double x, double y)
        {

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    if (i * height <= y && i * height + height >= y && j * width <= x && j * width + width >= x)
                    {

                        if (Board[i, j].state == State.Flagged || Board[i, j].state == State.Closed)
                            return false;

                        int neighboring_flags = 0;

                        for (int k = -1; k < 2; k++)
                        {

                            for (int l = -1; l < 2; l++)
                            {

                                if (i + k < 0 || i + k >= cols || j + l < 0 || j + l >= rows)
                                    continue;

                                if (Board[i + k, j + l].state == State.Revealed)
                                    continue;

                                if (Board[i + k, j + l].state == State.Flagged)
                                    neighboring_flags++;

                            }

                        }

                        if (neighboring_flags != Board[i, j].value)
                            return false;

                        for(int k = -1; k < 2; k++)
                        {

                            for (int l = -1; l < 2; l++)
                            {

                                if (i + k < 0 || i + k >= cols || j + l < 0 || j + l >= rows)
                                    continue;

                                if (Board[i + k, j + l].state == State.Revealed || Board[i + k, j + l].state == State.Flagged)
                                    continue;

                                if (Board[i + k, j + l].value == 0)
                                {

                                    exposeNeighbors(i + k, j + l);

                                }

                                else if (Board[i + k, j + l].value > 0)
                                {

                                    Board[i + k, j + l].state = State.Revealed;

                                }
                                else
                                {

                                    endGame(i + k, j + l);
                                    return true;

                                }

                            }

                        }

                        if (checkWin())
                        {
                            Draw();
                            endGame(i, j);
                            return true;

                        }

                        return false;


                    }

                }

            }

            return false;

        }

        public void endGame(int i, int j)
        {

            for(int y = 0; y < cols; y++)
            {

                for(int x = 0; x < rows; x++)
                {

                    if (Board[y, x].isBomb && Board[y, x].state != State.Flagged)
                    {

                        Border parent = (Border)canvas.Children[y * cols + x];

                        Border main = (Border)parent.Child;

                        main.BorderThickness = new Thickness(0);

                        parent.BorderThickness = new Thickness(1);

                        Image bomb = new Image()
                        {

                            Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "..\\..\\Images\\bomb.png", UriKind.Absolute)),
                            Stretch = Stretch.Uniform,
                            HorizontalAlignment = HorizontalAlignment.Center,
                            VerticalAlignment = VerticalAlignment.Center

                        };

                        if (y == i && x == j)
                            main.Background = Brushes.Red;

                        main.Child = bomb;

                    }
                    else if(!Board[y, x].isBomb && Board[y, x].state == State.Flagged)
                    {

                        Border parent = (Border)canvas.Children[y * cols + x];

                        Border main = (Border)parent.Child;

                        main.BorderThickness = new Thickness(0);

                        parent.BorderThickness = new Thickness(1);

                        Image bomb = new Image()
                        {

                            Source = new BitmapImage(new Uri(AppDomain.CurrentDomain.BaseDirectory + "..\\..\\Images\\bomb.png", UriKind.Absolute)),
                            Stretch = Stretch.Uniform,
                            HorizontalAlignment = HorizontalAlignment.Center,
                            VerticalAlignment = VerticalAlignment.Center

                        };

                        main.Child = bomb;

                        Line x1 = new Line
                        {

                            X1 = x * width,
                            Y1 = y * height,
                            X2 = x * width + width,
                            Y2 = y * height + height,
                            Stroke = Brushes.Red,
                            StrokeThickness = 4

                        };

                        Line x2 = new Line
                        {

                            X1 = x * width + width,
                            Y1 = y * height,
                            X2 = x * width,
                            Y2 = y * height + height,
                            Stroke = Brushes.Red,
                            StrokeThickness = 4

                        };

                        canvas.Children.Add(x1);
                        canvas.Children.Add(x2);

                    }


                }

            }

        }

        bool checkWin()
        {

            int revealed = 0;

            for(int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    if (Board[i, j].state == State.Revealed)
                        revealed++;

                }

            }

            if (revealed == rows * cols - mines)
                return true;

            return false;

        }

    }
}
