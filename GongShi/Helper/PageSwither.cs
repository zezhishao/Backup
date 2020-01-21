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
    /// 页面切换及其简单逻辑
    /// </summary>
    public partial class MainWindow : Window
    {        
        /// <summary>
        /// 切换页面
        /// </summary>
        /// <param name="Page">1: 主页；2：次级页面；3：详情页</param>
        public void SwithPage(int Page)
        {
            switch (Page)
            {
                case 1:
                    this.主页.Visibility = Visibility.Visible;
                    this.次级.Visibility = Visibility.Collapsed;
                    this.详情.Visibility = Visibility.Collapsed;
                    break;
                case 2:
                    this.主页.Visibility = Visibility.Collapsed;
                    this.次级.Visibility = Visibility.Visible;
                    this.详情.Visibility = Visibility.Collapsed;
                    break;
                case 3:

                    this.主页.Visibility = Visibility.Collapsed;
                    this.次级.Visibility = Visibility.Collapsed;
                    this.详情.Visibility = Visibility.Visible;
                    break;
                default: throw new Exception("页面切换出错");
            }
        }

        /// <summary>
        /// 切换模式
        /// </summary>
        /// <param name="mode">0:初始化; 1:地图模式; 2:列表模式</param>
        private void RenewMode(int mode)
        {
            if (Mode == mode)
            {
                return;
            }
            else
            {
                Mode = mode;
                switch (Mode)
                {
                    case 0:
                        this.列表层.Visibility = Visibility.Collapsed;
                        break;
                    case 1:
                        this.myMap.Width += 列表层.Width;
                        this.列表层.Visibility = Visibility.Collapsed;
                        break;
                    case 2:
                        this.myMap.Width -= 列表层.Width;
                        this.列表层.Visibility = Visibility.Visible;
                        break;
                }
            }
        }

        /// <summary>
        /// 列表选中改变
        /// 需要更换地图选点和背景框
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void 列表_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            //更改指示标志
            int index = this.列表.SelectedIndex;
            Data[index]["isShow"] = true;
            showRecord[1] = showRecord[0];
            showRecord[0] = index;
            if (showRecord[1] != -1)
            {
                Data[showRecord[1]]["isShow"] = false;
            }
            else if (index != 0)
            {
                Data[0]["isShow"] = false;
            }
            this.列表.ItemsSource = Data;

            //更新地图显示
            double lon = Double.Parse(Data[index]["lon"].ToString());
            double lat = Double.Parse(Data[index]["lat"].ToString());
            center = new Location(lat, lon);
            this.myMap.Center = center;
            MapLayer.SetPosition(this.myPin, this.myMap.Center);
        }

        /// <summary>
        /// 点击坐标显示列表
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void MyPin_MouseUp(object sender, MouseButtonEventArgs e)
        {
            RenewMode(2);
        }
    }
}
