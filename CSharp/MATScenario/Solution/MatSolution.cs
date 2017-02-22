using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MATScenario.Scenario;

namespace MATScenario.Solution
{
    public class MatSolution
    {
        public int Index { get; private set; }
        public List<List<CoordinatePair>> Movements = new List<List<CoordinatePair>>();
        public MatSolution(int index)
        {
            Index = index;
        }
    }
}
