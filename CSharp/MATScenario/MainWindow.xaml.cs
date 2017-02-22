using System;
using System.Collections.Generic;
using System.ComponentModel;
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

        public MainWindow()
        {
            InitializeComponent();
            Parser = MatParser.FromFilePath("robots.mat");
            foreach (var s in Parser.Scenarios)
                ScenarioComboBox.Items.Add(s);
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
                Canvas.SetLeft(GraphCanvas.Children[e], r.CurrentPosition.X);
                Canvas.SetTop(GraphCanvas.Children[e], r.CurrentPosition.Y);
            }
        }
    }
}
