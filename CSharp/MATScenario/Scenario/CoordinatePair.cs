using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MATScenario.Scenario
{
    public class CoordinatePair
    {
        public double X;
        public double Y;

        public CoordinatePair(double x, double y)
        {
            X = x;
            Y = y;
        }

        public CoordinatePair(CoordinatePair other)
        {
            X = other.X;
            Y = other.Y;
        }
    }
}
