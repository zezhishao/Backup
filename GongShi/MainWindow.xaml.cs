using GMap.NET;
using GMap.NET.MapProviders;
using GMap.NET.WindowsPresentation;
using MaterialDesignThemes.Wpf;
using Microsoft.Maps.MapControl.WPF;
using Newtonsoft.Json;
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
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        int Mode = 0;   //0 = 初始化；1 = 地图模式, 2 = 列表模式
        int[] showRecord = new int[2] { -1, -1 };   //用以显示列表选择Flag
        Location center = new Location(36.688075, 117.065558);  //地图中心
        double zoomLevel = 14;  //地图缩放等级
        public static JArray Data = new JArray(); //列表数据源

        public MainWindow()
        {
            InitializeComponent();
            SwithPage(1);
            RenewMode(0);
            center = myMap.Center;
            zoomLevel = myMap.ZoomLevel;
        }
        /*
         * 山大洪家楼 36.688075, 117.065558
         * 山大中心校 36.673107, 117.-059290
         * 
         * ListBox数据源格式
         * List<JObject>
         * JObject:
         *  Properties{
         *      com_name: 工厂名
         *      厂家名称：工厂名（和上一个重复了）
         *      
         *      产能指标-月：
         *      
         *      SKU个数：
         *      好评率
         *      重复购买率
         *      正面舆情占比
         *      
         *      商品成本-斤
         *      运输成本
         *      
         *      tel
         *      web_site
         *      location
         *      case
         *      
         *      zzdf：最终得分（100分满）
         *      cnpf：产能评分
         *      jgys：价格优势
         *      sczl：生产质量
         *      
         *      
         *      lon：经度，竖着的
         *      lat：维度，横着的
         *  }
         */

        private void 工食一下Btn_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                //TODO: set url request
                string productName = this.查找产品TBX.Text;
                string region = this.地区选择TBX.Text;

                if (productName != "薯片" || region != "上海")
                {
                    MessageBox.Show("该种类或地区尚未支持，搜一下\"薯片\"、 \"上海\"试试吧~", "感谢您的使用");
                    return;
                }

                string url = "http://58.87.66.15:8000/getData?keyword=" + System.Web.HttpUtility.UrlEncode(productName) + "&region=" + System.Web.HttpUtility.UrlEncode(region);

                //TODO: get url response
                Dictionary<string, object> response = Analysis(url);
                bool result = (bool)response["result"];
                string msg = response["msg"].ToString();
                object aaa = System.Web.HttpUtility.UrlDecode(response["object"].ToString());
                Data = JsonConvert.DeserializeObject<JArray>(response["object"].ToString());

                int a = 1;
                //TODO：刷新界面并传递数据
                if (result)
                {
                    SwithPage(2);
                    //JObject Data = response["data"];
                    // 伪造Data
                    this.列表.ItemsSource = Data;
                    this.列表.SelectedIndex = 0;
                    this.Fac_Num.Text = Data.Count.ToString();
                }
                else
                {
                    //获取数据失败
                    //TODO 提示获取失败
                    throw new Exception("提示获取失败");
                }
            }
            catch(Exception ee)
            {
                MessageBox.Show(ee.Message, "错误");
            }
            
        }

        private void 地图模式Btn_Click(object sender, RoutedEventArgs e)
        {
            RenewMode(1);
        }

        private void 列表模式Btn_Click(object sender, RoutedEventArgs e)
        {
            RenewMode(2);
        }

        /// <summary>
        /// 查看第三个页面
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void 查看详情_Click(object sender, RoutedEventArgs e)
        {
            Button btn = (Button)sender;
            JObject data =(JObject) btn.Tag;
            Set_详情页面(data);
        }

        private void Set_详情页面(JObject data)
        {
            详情_最终评分.Text = Math.Round(float.Parse(data["zzdf"].ToString()),2).ToString();
            详情_cnpg.Value = Convert.ToInt32(float.Parse(data["cnpg"].ToString()));
            详情_jgys.Value = Convert.ToInt32(float.Parse(data["jgys"].ToString()));
            详情_sczl.Value = Convert.ToInt32(float.Parse(data["sczl"].ToString()));

            case_三级.Text = data["case"].ToString();
            详情_工厂名称.Text = data["厂家名称"].ToString();
            详情_position.Text = data["location"].ToString();
            详情_site.Text = data["web_site"].ToString();
            详情_sku.Text = data["SKU个数"].ToString();
            详情_tel.Text = data["tel"].ToString();
            详情_case.Text = data["case"].ToString();
            详情_经销商地址.Text = data["location"].ToString();

            详情_推测月产量.Text = Math.Round(double.Parse(data["产能指标-月"].ToString()),2).ToString() + "件（7.5kg 标准包装）";
            详情_舆情评价.Text = "正面舆情占比" + float.Parse(data["正面舆情占比"].ToString()) * 100 + "%";
            详情_重复购买.Text = "重复购买率" + float.Parse(data["重复购买率"].ToString()) * 100 + "%";
            详情_客户评价.Text = "好评率" + data["好评率"].ToString();
            详情_是否需要冷链.Text = "不需要";
            详情_商品价格.Text = data["商品成本-斤"].ToString() + " 元 / 斤";
            详情_与目的地距离.Text = Math.Round(GetDistance(double.Parse(data["lon"].ToString()), double.Parse(data["lat"].ToString())) / 1000.0, 2).ToString() + "km";
            详情_预估运输成本.Text = "预计" + data["运输成本"].ToString() + "吨 / kg";
            详情_月产量.Text = data["产能指标-月"].ToString() + "件（7.5kg 标准包装）";

            详情_与工厂距离.Text = "未知";

            详情_舆情关键词.Text = "安全、美味、绿色";
            double a = double.Parse(data["产能指标-月"].ToString()) * 7.5 * double.Parse(data["商品成本-斤"].ToString()) / 10000;
            详情_营业额.Text = (Math.Round(a*2,3)).ToString() + " 万元";

            SwithPage(3);
        }



        private void 返回次级页面_Click(object sender, RoutedEventArgs e)
        {
            SwithPage(2);
        }

        private void 加入对比_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("功能尚未开通！", "提示");
        }
    }
}
