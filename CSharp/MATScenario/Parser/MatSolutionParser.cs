using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using MATScenario.Scenario;
using MATScenario.Solution;

namespace MATScenario.Parser
{
    public class MatSolutionParser
    {
        private readonly string _inputData;
        public Dictionary<int, MatSolution> Solutions = new Dictionary<int, MatSolution>();
        public MatSolutionParser(string inputData)
        {
            _inputData = inputData.Trim();
            Parse();
        }
        public static MatSolutionParser FromFilePath(string path)
        {
            var text = File.ReadAllText(path);
            return new MatSolutionParser(text);
        }

        private void Parse()
        {
            foreach (var s in Regex.Split(_inputData, "\\n"))
            {
                // Ignore the team name and password lines
                if (!s.Contains(":"))
                    continue;

                var line = s.Trim().Replace(" ", string.Empty);
                var colon = line.IndexOf(':');
                var index = int.Parse(line.Substring(0, colon));

                var solution = new MatSolution(index);

                var positions = line.Substring(colon + 1);
                foreach (var robot in positions.Split(';'))
                {
                    var movements = new List<CoordinatePair>();
                    var cleanRobot = robot.Replace(")", "").Replace("(", "");
                    var coords = cleanRobot.Split(',');
                    for (var i = 0; i < coords.Length - 1; i+=2)
                    {
                        movements.Add(new CoordinatePair(double.Parse(coords[i]), double.Parse(coords[i + 1])));
                    }
                    solution.Movements.Add(movements);
                }
                Solutions.Add(index, solution);
            }
        }
    }
}
