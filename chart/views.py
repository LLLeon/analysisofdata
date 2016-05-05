from django.shortcuts import render
from chart.models import ItemInfo
from django.core.paginator import Paginator


# 主界面main.html的view
def index(request):
    limit = 8
    arti_info = ItemInfo.objects()
    paginator = Paginator(arti_info, limit)
    page = request.GET.get('page', 1)
    loaded = paginator.page(page)
    context = {
        'ItemInfo': loaded,
        'counts': arti_info.count(),
        'last_time': arti_info.order_by('-pub_date').limit(1)
    }
    return render(request, 'index_data.html', context)


# -------------------------------------------------------------------
# 北京各城区二手物品交易量Top5图表数据--生成函数
def get_top5(date1, date2, area, limit):  # 注意area需要放在list中
    pipeline = [
    {'$match': {'$and': [{'pub_date': {'$gte': date1, '$lte': date2}}, {'area': {'$all': area}}]}},  # $all为包含的意思
    {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
    {'$sort': {'counts': -1}},
    {'$limit': limit}
]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'data': [i['counts']],
            'type': 'column'
        }
        yield data


# 各地区series
top5_CY = [i for i in get_top5('2015.12.01', '2015.12.25', ['朝阳'], 5)]
top5_HD = [i for i in get_top5('2015.12.01', '2015.12.25', ['海淀'], 5)]
top5_FT = [i for i in get_top5('2015.12.01', '2015.12.25', ['丰台'], 5)]


# chart.html的view,内容为各地区发帖量Top5
def chart(request):
    context = {
        'top5_CY': top5_CY,
        'top5_HD': top5_HD,
        'top5_FT': top5_FT
    }
    return render(request, 'chart.html', context)


# ---------------------------------------------------------------------------
# 各类别发帖量数据--生成函数
def get_post_times(types):
    #统计类别
    pipeline =[
    {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
    {'$sort': {'counts': -1}}
]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'data': [i['counts']],
            'type': types
        }
        yield data


# 各类别发帖量统计的series
post_time = [data for data in get_post_times('column')]


# post_times.html的view,内容为各类别发帖量统计
def post_times(request):
    context = {
        'post_times': post_time
    }
    return render(request, 'post_times.html', context)


# -----------------------------------------------------------------------------
# 一天内交易物品种类、地区分布数据--生成函数
def get_deal_type(date, time):  # 获取一天内交易物品种类数据
    pipeline = [
        {'$match': {'$and': [{'pub_date': date}, {'time': time}]}},
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        yield [i['_id'][0], i['counts']]


def get_deal_area(date, time):  # 获取一天内交易物品地区数据
    pipeline = [
        {'$match': {'$and': [{'pub_date': date}, {'time': time}]}},
        {'$group': {'_id': {'$slice': ['$area', 0, 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        yield [i['_id'][0], i['counts']]


# 一天内交易物品种类数据的series
deal_types = [{
        'type': 'pie',
        'name': 'pie chart',
        'data': [i for i in get_deal_type('2016.01.10', 1)]
    }]


# 一天内交易物品地区数据的series
deal_areas = [{
    'type': 'pie',
    'name': 'pie chart',
    'data': [i for i in get_deal_area('2016.01.10', 1)]
}]


# deal_type.html的view，内容为一天内交易物品类别及地区统计
def deal_type(request):
    context = {
        'deal_type': deal_types,  # context 的key连接到html文件中jQuery的series
        'deal_area': deal_areas
    }
    return render(request, 'deal_type.html',context)
