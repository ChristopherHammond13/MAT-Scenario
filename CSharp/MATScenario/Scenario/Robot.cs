using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Media;
using System.Windows.Shapes;

namespace MATScenario.Scenario
{
    public class Robot
    {
        
        public CoordinatePair CurrentPosition { get; }
        public List<CoordinatePair> MovementHistory { get; } = new List<CoordinatePair>();
        public Robot(double startX, double startY )
        {
            CurrentPosition = new CoordinatePair(startX, startY)
            {
                X = startX,
                Y = startY
            };
            MovementHistory.Add(new CoordinatePair(CurrentPosition));
        }

        public void Move(double newX, double newY)
        {
            CurrentPosition.X = newX;
            CurrentPosition.Y = newY;
            MovementHistory.Add(new CoordinatePair(CurrentPosition));
        }

        public Ellipse EllipseRepresentation => new Ellipse
        {
            Stroke = Brushes.Red,
            Fill = Brushes.Red,
            StrokeThickness = 0.4,
            HorizontalAlignment = HorizontalAlignment.Center,
            VerticalAlignment = VerticalAlignment.Center
        };

        public Polyline PolylineRepresentation => new Polyline
        {
            Points = new PointCollection
            {
                new Point(CurrentPosition.X, CurrentPosition.Y),
                new Point(CurrentPosition.X + 0.1, CurrentPosition.Y + 0.1)
            },
            Stroke = Brushes.Red,
            Fill = Brushes.Red,
            StrokeThickness = 0.1,
            HorizontalAlignment = HorizontalAlignment.Center,
            VerticalAlignment = VerticalAlignment.Center
        };
    }
}
