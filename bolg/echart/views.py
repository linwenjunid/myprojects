from django.shortcuts import render
from django.db import connection
from pyecharts import Scatter3D, Line3D, Grid, Bar, Line, Graph
import random,math
from xadmin.views import BaseAdminView
from django.views.decorators.cache import cache_page

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
    scatter3D = Scatter3D("3D scattering plot demo", width=500, height=500)
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
    line3d = Line3D("3D line plot demo", width=500, height=500)
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


# 需要以下包的支持：matplotlib,jieba,wordcloud
class wordcloudView(BaseAdminView):
    def get(self, request, *args, **kwargs):
        from PIL import Image
        from wordcloud import WordCloud, STOPWORDS
        import jieba
        from io import BytesIO
        from os import path
        from django.conf import settings
        import numpy as np
        from django.http import HttpResponse

        with Image.open(path.join(settings.STATIC_ROOT, '原图.jpg')) as i:
            image_mask = np.array(i)

        with open(path.join(settings.STATIC_ROOT, '数据.txt'), 'rb') as f:
            text = " ".join(jieba.cut(f.read()))

        stopwords = set(STOPWORDS)
        stopwords.add("新闻")
        stopwords.add("百度")
        stopwords.add("公告")
        stopwords.add("关键词")
        # 配置词云
        wc = WordCloud(
            background_color="white",
            max_words=20000,
            stopwords=stopwords,
            font_path="simsun.ttc",
            mask=image_mask)
        # 生成词云
        wc.generate(text)
        # 存储到文件
        # wc.to_file(path.join(d, '结果.png'))
        img = wc.to_image()

        # byte_io = BytesIO()
        # img.save(byte_io, 'PNG')
        # byte_io.seek(0)

        response = HttpResponse(content_type="image/png")
        img.save(response,'PNG')
        return response


@cache_page(60 * 15)
def wordcloud(request):
    # 缓存15分钟
    from PIL import Image
    from wordcloud import WordCloud, STOPWORDS
    import jieba
    from io import BytesIO
    from os import path
    from django.conf import settings
    import numpy as np
    from django.http import HttpResponse

    with Image.open(path.join(settings.STATIC_ROOT, '原图.jpg')) as i:
        image_mask = np.array(i)

    with open(path.join(settings.STATIC_ROOT, '数据.txt'), 'rb') as f:
        text = " ".join(jieba.cut(f.read()))

    stopwords = set(STOPWORDS)
    stopwords.add("新闻")
    stopwords.add("百度")
    stopwords.add("公告")
    stopwords.add("关键词")
    # 配置词云
    wc = WordCloud(
        background_color="white",
        max_words=20000,
        stopwords=stopwords,
        font_path="simsun.ttc",
        mask=image_mask)
    # 生成词云
    wc.generate(text)
    # 存储到文件
    # wc.to_file(path.join(d, '结果.png'))
    img = wc.to_image()

    # byte_io = BytesIO()
    # img.save(byte_io, 'PNG')
    # byte_io.seek(0)

    response = HttpResponse(content_type="image/png")
    img.save(response,'PNG')
    return response


class neo4jView(BaseAdminView):
    def get(self, request, *args, **kwargs):
        from py2neo import Graph as neo4j
        template_name = 'echart/echart.html'
        echart = Graph("关系图谱")
        graph = neo4j('http://192.168.134.4:7474', username='neo4j', password='hadoop')
        data1 = graph.run("match(n1:Actor{name:'沈腾'})-[r1]->(m1:Movie) return n1.name,type(r1),m1.name;").to_table()
        data2 = graph.run("match(n1:Actor{name:'沈腾'})-[r1]->(m1:Movie)<-[r2]-(n2:Actor) return n2.name,type(r2),m1.name;").to_table()
        nodes = [{"name": "沈腾", "symbolSize": 10,"category":1},]
        links = []
        for d in data1:
            nodes.append({"name": d[2], "symbolSize": 20,"category":0})
            links.append({"source": d[0], "target": d[2]})
        for d in data2:
            nodes.append({"name": d[0], "symbolSize": 10,"category":1})
            links.append({"source": d[0], "target": d[2]})
        categories = ["电影","演员"]
        # print(nodes)
        # print(links)
        echart.add("测试",nodes,links,categories=categories,is_label_show=True,is_focusnode=True,is_roam=True,is_rotatelabel=True,graph_repulsion=150)
        context = dict(
            myechart=echart.render_embed(),
            host=REMOTE_HOST,
            script_list=echart.get_js_dependencies()
        )
        return render(request, template_name, context)