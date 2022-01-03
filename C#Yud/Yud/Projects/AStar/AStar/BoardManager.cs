using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Shapes;

namespace AStar
{
    class BoardManager
    {

        Node[,] Board;

        int cols;
        int rows;

        int cell_width;
        int cell_height;

        bool showNodes = false;
        bool showClosed = false;

        Node start_node;
        Node end_node;

        List<Node> openSet;
        List<Node> closedSet;

        Canvas canvas;

        Random rnd;

        public BoardManager(Canvas c, int _cols, int _rows)
        {

            canvas = c;

            rnd = new Random();

            cols = _cols;
            rows = _rows;

            cell_width = (int)canvas.Width / rows;
            cell_height = (int)canvas.Height / cols;

            Board = new Node[cols, rows];

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    Board[i, j] = new Node(j, i);

                }

            }

            openSet = new List<Node>();
            closedSet = new List<Node>();

            start_node = Board[rnd.Next(rows), rnd.Next(cols)];

            start_node.gcost = 0;

            openSet.Add(start_node);

            do
            {

                end_node = Board[rnd.Next(rows), rnd.Next(cols)];

            } while (end_node.x == start_node.x && end_node.y == start_node.y);

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    // Internal

                    // Distance formula for hcost
                    Board[i, j].hcost = Math.Sqrt(Math.Pow(i - end_node.y, 2) + Math.Pow(j - end_node.x, 2));

                    // Graphics
                    Ellipse rect = new Ellipse()
                    {

                        Width = cell_width * 7 / 8,
                        Height = cell_height * 7 / 8,
                        Stroke = Brushes.Black,
                        StrokeThickness = 0,
                        Fill = Brushes.White,

                    };

                    if (i == start_node.y && j == start_node.x)
                        rect.Fill = Brushes.Blue;

                    else if (i == end_node.y && j == end_node.x)
                        rect.Fill = Brushes.Red;

                    else if (Board[i, j].isObstacle)
                        rect.Fill = Brushes.Black;

                    canvas.Children.Add(rect);

                    Canvas.SetLeft(rect, j * cell_width);
                    Canvas.SetTop(rect, i * cell_height);

                }

            }

        }

        public void addObstacle(double mx, double my)
        {

            int brushWidth = 5;
            brushWidth /= 2;

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    if (i * cell_height - brushWidth <= my && i * cell_height + cell_height + brushWidth >= my && j * cell_width - brushWidth <= mx && j * cell_width + cell_width + brushWidth >= mx)
                    {

                        if ((i == start_node.y && j == start_node.x) || (i == end_node.y && j == end_node.x))
                            return;

                        Board[i, j].isObstacle = true;

                        Ellipse rect = (Ellipse)canvas.Children[i * cols + j];

                        rect.Fill = Brushes.Black;

                    }

                }

            }

        }

        public void toggleNodes()
        {

            showNodes = !showNodes;

            if (showNodes)
            {

                var ellipses = canvas.Children.OfType<Ellipse>().ToList();
                foreach (var e in ellipses)
                {
                    e.StrokeThickness = 1;
                }

            }
            else
            {

                var ellipses = canvas.Children.OfType<Ellipse>().ToList();
                foreach (var e in ellipses)
                {
                    e.StrokeThickness = 0;
                }

            }

        }

        public void toggleClosed()
        {

            showClosed = !showClosed;

            if (!showClosed)
            {

                for(int i = 0; i < cols; i++)
                {

                    for(int j = 0; j < rows; j++)
                    {

                        if (closedSet.Contains(Board[i, j]) && !(i == start_node.y && j == start_node.x) && !(i == end_node.y && j == end_node.x))
                        {

                            Ellipse e = (Ellipse)canvas.Children[i * cols + j];
                            e.Fill = Brushes.White;

                        }

                    }

                }

            }

        }

        public int updateBoard()
        {

            if (openSet.Count == 0)
                return -1;

            Node best = openSet.First();

            foreach (Node candidate in openSet)
            {

                if (candidate.fcost < best.fcost)
                    best = candidate;

            }

            Node current = best;

            openSet.Remove(current);
            closedSet.Add(current);

            if (current == end_node)
                return 1;

            for (int i = -1; i < 2; i++)
            {

                for (int j = -1; j < 2; j++)
                {

                    if (current.y + i < 0 || current.y + i >= cols || current.x + j < 0 || current.x + j >= rows || (i == 0 && j == 0))
                        continue;

                    Node neighbor = Board[current.y + i, current.x + j];

                    if (closedSet.Contains(neighbor))
                        continue;

                    double new_gcost = current.gcost + Math.Sqrt(i * i + j * j);

                    if (new_gcost < neighbor.gcost)
                    {

                        neighbor.parent = current;
                        neighbor.gcost = new_gcost;

                    }

                    if (!openSet.Contains(neighbor) && !neighbor.isObstacle)
                        openSet.Add(neighbor);

                }

            }

            if (!showClosed)
                return 0;

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    Ellipse rect = (Ellipse)canvas.Children[i * cols + j];

                    if (closedSet.Contains(Board[i, j]) && !(i == start_node.y && j == start_node.x))
                        rect.Fill = Brushes.Gray;

                }

            }

            return 0;

        }

        public void retracePath()
        {

            var lines = canvas.Children.OfType<Polyline>().ToList();
            foreach (var line in lines)
            {
                canvas.Children.Remove(line);
            }

            Node current = closedSet.Last();

            Polyline path = new Polyline();
            PointCollection collection = new PointCollection();

            while (current != start_node)
            {

                collection.Add(new Point(current.x * cell_width + cell_width / 2 - 2, current.y * cell_height + cell_height / 2 - 2));

                current = current.parent;

            }

            collection.Add(new Point(current.x * cell_width + cell_width / 2 - 2, current.y * cell_height + cell_height / 2 - 2));

            path.Points = collection;
            path.Stroke = Brushes.Yellow;
            path.StrokeThickness = 4;
            canvas.Children.Add(path);

        }

    }
}
