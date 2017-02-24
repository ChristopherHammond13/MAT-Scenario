using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;

namespace MATScenario.Utils
{
    public static class RandomBrush
    {
        public static Brush GetRandomBrush()
        {
            var rnd = new Random((int)DateTime.Now.Ticks);

            var brushesType = typeof(Brushes);

            var properties = brushesType.GetProperties();

            var random = rnd.Next(properties.Length);
            var result = (Brush)properties[random].GetValue(null, null);

            return result;
        }
    }
}
