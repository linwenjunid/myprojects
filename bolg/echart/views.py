from django.shortcuts import render
from django.db import connection
from pyecharts import Scatter3D, Line3D, Grid, Bar, Line
import random,math
from xadmin.views import BaseAdminView

REMOTE_HOST = "https://pyecharts.github.io/assets/js"


def exc_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def scatter3D():
    # select    province, difi_re_num    from REPORT_REG
    # ret = """select city, difi_re_num  from REPORT_REG a, province_to_city b where a.province=b.province"""
    # data_list = exc_sql(ret)
    # attr = [i[0] for i in data_list]
    # value = [i[1] for i in data_list]
    # geo = Geo("全国各地用户注册图", width=1200, height=600)
    # geo.add("各省注册量", attr, value, type="effectScatter", border_color="#ffffff", symbol_size=2,
    #         is_label_show=True, label_text_color="#00FF00", label_pos="inside", symbol_color="yellow",
    #         geo_normal_color="#006edd", geo_emphasis_color="#0000ff")
    # data = {'data': scatter3D.render_embed()}
    # return render(request, 'guo_report.html', data)
    data = [[random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)] for _ in range(80)]
    range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
                   '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D = Scatter3D("3D scattering plot demo", width=500, height=250)
    scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
    return scatter3D


def line3d():
    _data = []
    for t in range(0, 25000):
        _t = t / 1000
        x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
        y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
        z = _t + 2.0 * math.sin(75 * _t)
        _data.append([x, y, z])
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    line3d = Line3D("3D line plot demo", width=500, height=250)
    line3d.add("", _data, is_visualmap=True,
               visual_range_color=range_color, visual_range=[0, 30],
               is_grid3D_rotate=True, grid3D_rotate_speed=180)
    return line3d


class scatter3DView(BaseAdminView):

    def get(self, request, *args, **kwargs):
        template_name = 'echart/echart.html'
        echart = scatter3D()
        context = dict(
            myechart=echart.render_embed(),
            host=REMOTE_HOST,
            script_list=echart.get_js_dependencies()
        )
        return render(request, template_name, context)


class line3dView(BaseAdminView):

    def get(self, request, *args, **kwargs):
        template_name = 'echart/echart.html'
        echart = line3d()
        context = dict(
            myechart=echart.render_embed(),
            host=REMOTE_HOST,
            script_list=echart.get_js_dependencies()
        )
        return render(request, template_name, context)


class gridView(BaseAdminView):
    def get(self, request, *args, **kwargs):
        template_name = 'echart/echart.html'
        bar = Bar()
        bar.add('服装', ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
        line = Line()
        line.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
        echart = Grid(page_title='组合图',width=1200,height=250)
        echart.add(bar,grid_left='50%')
        echart.add(line,grid_right='55%')
        context = dict(
            myechart=echart.render_embed(),
            host=REMOTE_HOST,
            script_list=echart.get_js_dependencies()
        )
        return render(request, template_name, context)
