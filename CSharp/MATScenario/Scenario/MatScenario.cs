using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Shapes;

namespace MATScenario.Scenario
{
    public class MatScenario
    {
        public int Index { get; }
        public List<Polygon> Obstacles { get; private set; } = new List<Polygon>();
        public List<Robot> Robots { get; private set; } = new List<Robot>();

        public MatScenario(int index)
        {
            Index = index;
        }

        public override string ToString()
        {
            return Index.ToString();
        }
    }
}
