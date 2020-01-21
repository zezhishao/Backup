using GMap.NET;
using GMap.NET.MapProviders;
using GMap.NET.WindowsPresentation;
using Microsoft.Maps.MapControl.WPF;
using System;
using System.Collections.Generic;
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
        public static Dictionary<string, object> Analysis(string Url)
        {
            return Newtonsoft.Json.JsonConvert.DeserializeObject<Dictionary<string, object>>(GetResponse(Url));
        }

        private static string GetResponse(string url)
        {
            HttpWebRequest request = WebRequest.Create(url) as HttpWebRequest;
            HttpWebResponse response = request.GetResponse() as HttpWebResponse;//发送请求并获取相应回应数据   //断点查看url和foldpath
            //字符串化返回数据
            StreamReader streamReader = new StreamReader(response.GetResponseStream());
            return streamReader.ReadToEnd();
        }
    }
}
