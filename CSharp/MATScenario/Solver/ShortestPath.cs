using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;
using System.Windows.Shapes;
using MATScenario.Scenario;

namespace MATScenario.Solver
{
    class ShortestPath
    {
        private List<List<Polyline>> _options = new List<List<Polyline>>();
        //public ShortestPath(List<Polygon> obstacles, Point robot1, Point robot2)
        //{
        //    var attempted = new List<Point>();
        //    var points = new List<Point>();
        //    obstacles.ForEach(x => points.AddRange(x.Points.ToList()));
        //    foreach (var point in points)
        //    {
        //        var line = new Polyline
        //        {
        //            Points = new PointCollection
        //            {
        //                robot1,
        //                point
        //            }
        //        };
                
        //    }
        //}

        //public ShortestPath(List<Polygon> obstacles, Point robot1, Point robot2)
        //{
        //    var vertices = new List<Point>();
        //    var edges = new List<Point>();
        //    obstacles.ForEach(x => vertices.AddRange(x.Points));
        //    foreach (var v in vertices)
        //    {
               
        //    }
        //}

        public ShortestPath(List<Polygon> obstacles, Point robot1, Point robot2)
        {
            var vertices = new List<Point>();
            obstacles.ForEach(x => vertices.AddRange(x.Points));
            var path = new List<Point>();

            var edges = new List<Polyline>();
            foreach (var obstacle in obstacles)
            {
                for (var i = 0; i < obstacle.Points.Count; i++)
                {
                    var join = i == obstacle.Points.Count ? 0 : i + 1;
                    var line = new Polyline();
                    line.Points.Add(new Point(obstacle.Points[i].X, obstacle.Points[i].Y));
                    line.Points.Add(new Point(obstacle.Points[join].X, obstacle.Points[join].Y));
                }
            }
            foreach (var v in vertices)
            {
                foreach (var w in vertices)
                {
                    foreach (var e in edges)
                    {
                        
                    }
                }
            }
        }
    }
}
