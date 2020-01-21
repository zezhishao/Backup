using GMap.NET;
using GMap.NET.MapProviders;
using GMap.NET.WindowsPresentation;
using MaterialDesignThemes.Wpf;
using Microsoft.Maps.MapControl.WPF;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Net;
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
namespace GongShi
{
    /// <summary>
    /// 无需再看的UI助手
    /// </summary>
    public partial class MainWindow : Window
    {

      
        private void Map_ViewChangeEnd(object sender, MapEventArgs e)
        {
            if (myMap.ZoomLevel != zoomLevel)
            {
                myMap.ZoomLevel = zoomLevel;
            }

            if (!myMap.Center.Equals(center))
            {
                myMap.Center = center;
            }
        }



        private void MyGotFocus(object sender, RoutedEventArgs e)
        {
            TextBox txb = ((TextBox)sender);
            ((TextBox)sender).SelectAll();
            ((TextBox)sender).PreviewMouseDown -= new MouseButtonEventHandler(MyPreviewMouseDown);
        }
        private void MyPreviewMouseDown(object sender, MouseButtonEventArgs e)
        {
            ((TextBox)sender).Focus();
            e.Handled = true;
        }

        private void MyLostFocus1(object sender, RoutedEventArgs e)
        {
            ((TextBox)sender).PreviewMouseDown += new MouseButtonEventHandler(MyPreviewMouseDown);
            ((TextBox)sender).IsEnabled = true;
        }
    }
}
