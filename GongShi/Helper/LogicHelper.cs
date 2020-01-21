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
    public partial class MainWindow : Window
    {

        private const double lon_of_shanghai = 121.48341;
        private const double lat_of_shanghai = 31.224813;

        //地球半径，单位米
        private const double EARTH_RADIUS = 6378137;

        /// <summary>
        /// 计算两点位置的距离，返回两点的距离，单位：米
        /// 该公式为GOOGLE提供，误差小于0.2米
        /// </summary>
        /// <param name="lng1">第一点经度</param>
        /// <param name="lat1">第一点纬度</param>        
        /// <param name="lng2">第二点经度</param>
        /// <param name="lat2">第二点纬度</param>
        /// <returns></returns>
        public static double GetDistance(double lng1, double lat1)
        {
            double lng2 = lon_of_shanghai;
            double lat2 = lat_of_shanghai;

            double radLat1 = Rad(lat1);
            double radLng1 = Rad(lng1);
            double radLat2 = Rad(lat2);
            double radLng2 = Rad(lng2);
            double a = radLat1 - radLat2;
            double b = radLng1 - radLng2;
            double result = 2 * Math.Asin(Math.Sqrt(Math.Pow(Math.Sin(a / 2), 2) + Math.Cos(radLat1) * Math.Cos(radLat2) * Math.Pow(Math.Sin(b / 2), 2))) * EARTH_RADIUS;
            return result;
        }

        /// <summary>
        /// 经纬度转化成弧度
        /// </summary>
        /// <param name="d"></param>
        /// <returns></returns>
        private static double Rad(double d)
        {
            return (double)d * Math.PI / 180d;
        }


    }
}

