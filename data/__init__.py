# -*- coding: utf-8 -*-
import json
from collections import OrderedDict
import requests
from lxml import etree
import requests
import json
from StationManager import StationManager
from LineManager import LineManager
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36 2345Explorer/10.11.0.20694'}


def get_metro_line_map():
    url = 'http://map.amap.com/subway/index.html?&1100'
    res = requests.get(url=url, headers=headers)
    res.raise_for_status()
    res.encoding = res.apparent_encoding
    html = res.text
    Html = etree.HTML(html)
    # print(etree.tostring(Html, encoding="unicode"))
    # div中取城市列表
    res1 = Html.xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/a')
    res2 = Html.xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/a')
    for i in res1:
        # 城市ID值
        ID = ''.join(i.xpath('.//@id'))  # 属性需要加上双斜杠
        # 城市拼音名
        cityNamePinYin = ''.join(i.xpath('.//@cityname'))  # ./表示在当层目录下使用
        # 城市名
        cityName = ''.join(i.xpath('./text()'))
        get_message(ID, cityNamePinYin, cityName)
    for i in res2:
        # 城市ID值
        ID = ''.join(i.xpath('.//@id'))
        # 城市拼音名
        cityNamePinYin = ''.join(i.xpath('.//@cityname'))
        # 城市名
        cityName = ''.join(i.xpath('./text()'))
        get_message(ID, cityNamePinYin, cityName)


def get_message(ID, cityNamePinYin, cityName):  # 用于得到城市的具体线路信息
    """
    地铁线路信息获取
    """
    url = 'http://map.amap.com/service/subway?_1555502190153&srhdata=' + ID + '_drw_' + cityNamePinYin + '.json'
    global stations
    response = requests.get(url=url, headers=headers)
    html = response.text
    result = json.loads(html)
    data_list = []
    for i in result['l']:
        for j in i['st']:
            data_json = {"key": i['ln'],
                         "value": j['n']}

            # 判断是否含有地铁分线
            if len(i['la']) > 0:
                data_json["key"] = data_json.get("key") + '(' + i[
                    'la'] + ')'
                data_list.append(data_json)
            else:
                data_list.append(data_json)
    f = open("data/" + cityName + '.json', "a+")
    # 去重
    json.dump(list(OrderedDict((tuple(d.items()), d) for d in data_list).values()), f, ensure_ascii=False)
    print(cityName + '地铁站点爬取结束')
    f.close()


def get_metro_data_by_city(city_name):
    station_manager = StationManager()
    line_manager = LineManager()
    offline_file_exist = os.path.isfile("data/" + city_name + ".json")
    if not offline_file_exist:
        get_metro_line_map()
    f = open("data/" + city_name + ".json")
    content = f.read()
    data = json.loads(content, encoding="utf-8")
    for each in data:
        line_number = each["key"]
        station_name = str(each["value"])
        station_manager.add_station(station_name, line_number)
        line_manager.add_line(line_number, station_name)
    return station_manager, line_manager

