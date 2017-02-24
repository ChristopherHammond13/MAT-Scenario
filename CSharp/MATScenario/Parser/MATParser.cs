using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;
using System.Windows.Shapes;
using MATScenario.Annotations;
using MATScenario.Scenario;
using MATScenario.Utils;

namespace MATScenario.Parser
{
    public class MatParser
    {
        private readonly string _inputData;
        public List<MatScenario> Scenarios = new List<MatScenario>();
        
        public MatParser(string inputText)
        {
            _inputData = inputText.Trim();
            Parse();
        }

        public static MatParser FromFilePath(string path)
        {
            var text = File.ReadAllText(path);
            return new MatParser(text);
        }

        private void Parse()
        {
            foreach (var s in Regex.Split(_inputData, "\\n"))
            {
                var line = s.Trim().Replace(" ", string.Empty);
                var colon = line.IndexOf(':');
                var index = int.Parse(line.Substring(0, colon));
                
                var scenario = new MatScenario(index);

                var hasObstacles = line.Contains("#");

                var endOfRobots = hasObstacles ? line.IndexOf('#') : line.Length - 1;
                var robotsText = line.Substring(colon + 1, endOfRobots - colon - 1);
                var robotsCoordinates = robotsText.Split(',');
                for (var i = 0; i < robotsCoordinates.Length - 1; i += 2)
                {
                    robotsCoordinates[i] = robotsCoordinates[i].Replace("(", "").Replace(")", "");
                    robotsCoordinates[i+1] = robotsCoordinates[i + 1].Replace("(", "").Replace(")", "");
                    var x = double.Parse(robotsCoordinates[i]);
                    var y = double.Parse(robotsCoordinates[i + 1]);

                    scenario.Robots.Add(new Robot(x, y));
                }

                if (hasObstacles)
                {
                    var obstacleString = line.Substring(endOfRobots + 1, line.Length - endOfRobots - 1);
                    var obstacles = obstacleString.Split(';');
                    foreach (var obstacle in obstacles)
                    {
                        var coords = obstacle.Split(',');
                        var corners = new List<CoordinatePair>();

                        for (var i = 0; i < coords.Length - 1; i += 2)
                        {
                            coords[i] = coords[i].Replace("(", "").Replace(")", "");
                            coords[i + 1] = coords[i + 1].Replace("(", "").Replace(")", "");
                            var x = double.Parse(coords[i]);
                            var y = double.Parse(coords[i + 1]);

                            corners.Add(new CoordinatePair(x, y));
                        }

                        var obstaclePolygon = new Polygon
                        {
                            Points = new PointCollection(),
                            Stroke = null,
                            Fill = RandomBrush.GetRandomBrush(),
                            StrokeThickness = 0,
                            HorizontalAlignment = HorizontalAlignment.Center,
                            VerticalAlignment = VerticalAlignment.Center
                        };
                        foreach (var corner in corners)
                        {
                            obstaclePolygon.Points.Add(new Point(corner.X, corner.Y));
                        }

                        scenario.Obstacles.Add(obstaclePolygon);
                    }
                }

                Scenarios.Add(scenario);
            }
        }
        
    }
}
