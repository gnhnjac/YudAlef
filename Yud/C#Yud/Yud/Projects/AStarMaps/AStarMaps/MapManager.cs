using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Shapes;

namespace AStarMaps
{
    class MapManager
    {
        Node[,] Map;

        int cols;
        int rows;

        Node start_node;
        Node end_node;

        List<Node> openSet;
        List<Node> closedSet;

        Canvas canvas;

        Random rnd;

        public MapManager(Canvas c, Node[,] _map, int _cols, int _rows)
        {

            canvas = c;

            rnd = new Random();

            cols = _cols;
            rows = _rows;

            Map = _map;

            openSet = new List<Node>();
            closedSet = new List<Node>();

            start_node = Map[rnd.Next(rows), rnd.Next(cols)];

            start_node.gcost = 0;

            openSet.Add(start_node);

            do
            {

                end_node = Map[rnd.Next(rows), rnd.Next(cols)];

            } while (end_node.x == start_node.x && end_node.y == start_node.y);

            for (int i = 0; i < cols; i++)
            {

                for (int j = 0; j < rows; j++)
                {

                    // Distance formula for hcost
                    Map[i, j].hcost = Math.Sqrt(Math.Pow(i - end_node.y, 2) + Math.Pow(j - end_node.x, 2));

                }

            }

            Ellipse start = new Ellipse
            {


                Width = 10,
                Height = 10,
                Fill = Brushes.Green

            };

            canvas.Children.Add(start);

            Canvas.SetLeft(start, start_node.x);
            Canvas.SetTop(start, start_node.y);

            Ellipse end = new Ellipse
            {


                Width = 10,
                Height = 10,
                Fill = Brushes.Red

            };

            canvas.Children.Add(end);

            Canvas.SetLeft(start, end_node.x);
            Canvas.SetTop(start, end_node.y);


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

                    Node neighbor = Map[current.y + i, current.x + j];

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

                collection.Add(new Point(current.x, current.y));

                current = current.parent;

            }

            collection.Add(new Point(current.x, current.y));

            path.Points = collection;
            path.Stroke = Brushes.Yellow;
            path.StrokeThickness = 4;
            canvas.Children.Add(path);

        }

    }
}
