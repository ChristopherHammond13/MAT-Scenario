using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using MATScenario.Parser;
using MATScenario.Scenario;
using MATScenario.Utils;

namespace MATScenario
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MatParser Parser { get; }
        public static double DefaultScale => 10.0;
        public double CurrentScale { get; private set; } = DefaultScale;

        public double LineThickness
        {
            get { return LineThicknessSlider.Value; }
            set { LineThicknessSlider.Value = value; }
        }

        public MatSolutionParser SolutionParser { get; }

        public MainWindow()
        {
            InitializeComponent();
            Parser = MatParser.FromFilePath("robots.mat");
            SolutionParser = MatSolutionParser.FromFilePath("solution.mat");
            foreach (var s in Parser.Scenarios)
            {
                if (SolutionParser.Solutions.ContainsKey(s.Index))
                {
                    for (var i = 0; i < SolutionParser.Solutions[s.Index].Movements.Count; i++)
                    {
                        SolutionParser.Solutions[s.Index].Movements[i].ForEach(x => s.Robots[i].Move(x.X, x.Y));
                    }
                }
                ScenarioComboBox.Items.Add(s);
            }
                
            ScenarioComboBox.SelectedIndex = 0;
            RefreshCanvas((MatScenario)ScenarioComboBox.SelectedItem);
        }

        private void ScenarioComboBox_OnSelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            var scenario = (MatScenario) ScenarioComboBox.SelectedItem;
            RefreshCanvas(scenario);
        }

        private void RefreshCanvas(MatScenario scenario)
        {
            GraphCanvas.Children.Clear();
            foreach (var o in scenario.Obstacles)
            {
                GraphCanvas.Children.Add(o);
            }

            foreach (var r in scenario.Robots)
            {
                GraphCanvas.Children.Add(r.PolylineRepresentation);
            }
            foreach (var r in scenario.Robots)
            {
                var e = GraphCanvas.Children.Add(r.EllipseRepresentation);
                Canvas.SetLeft(GraphCanvas.Children[e], r.MovementHistory.First().X);
                Canvas.SetTop(GraphCanvas.Children[e], r.MovementHistory.First().Y);
                var brush = RandomBrush.GetRandomBrush();
                if (r.MovementHistory.Count > 1)
                {
                    for (var i = 1; i < r.MovementHistory.Count; i++)
                    {
                        GraphCanvas.Children.Add(new Polyline
                        {
                            Points = new PointCollection
                            {
                                new Point(r.MovementHistory[i].X, r.MovementHistory[i].Y),
                                new Point(r.MovementHistory[i - 1].X, r.MovementHistory[i - 1].Y)
                            },
                            Stroke = brush,
                            Fill = brush,
                            StrokeThickness = LineThickness,
                            HorizontalAlignment = HorizontalAlignment.Center,
                            VerticalAlignment = VerticalAlignment.Center
                        });
                    }
                }
            }
        }

        private void RenderOutputButton_OnClick(object sender, RoutedEventArgs e)
        {
            var rtb = new RenderTargetBitmap((int)MainWindowElement.ActualWidth, (int)MainWindowElement.ActualHeight, 96d, 96d, default(PixelFormat));
            rtb.Render(GraphCanvas);
            var encoder = new PngBitmapEncoder();
            encoder.Frames.Add(BitmapFrame.Create(rtb));
            using (var fs = File.OpenWrite("Render" + ((MatScenario)ScenarioComboBox.SelectedItem).Index + ".png"))
            {
                encoder.Save(fs);
            }
        }

        private void LineThicknessSlider_OnValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            if (!IsInitialized)
                return;

            RefreshCanvas((MatScenario) ScenarioComboBox.SelectedItem);
        }

        private void GraphCanvas_OnMouseDown(object sender, MouseButtonEventArgs e)
        {
            var p = Mouse.GetPosition(GraphCanvas);
            var text = new StringBuilder("Coordinates Under Mouse Click: ");
            text.Append(p.X.ToString(CultureInfo.InvariantCulture));
            text.Append(", ");
            text.Append(p.Y.ToString(CultureInfo.InvariantCulture));
            text.Append(")");

            CurrentCoordinatesLabel.Content = text.ToString();
        }
    }
}