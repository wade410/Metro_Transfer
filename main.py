#coding:utf-8

import json
from StationManager import StationManager
from Route import Route
from data import get_metro_data_by_city

stations = []
station_index = {}

# 邻接矩阵
v_matrix = []

book = []
dis = []

n = 0  # 顶点数

if __name__ == '__main__':
    # city_name = input("城市\n")
    city_name = "杭州"
    station_manager, line_manager = get_metro_data_by_city(city_name)
    index = 0
    # station_manager站点对应的线路
    for each in station_manager.stations.keys():
        station_index[each] = index
        index += 1
        stations.append(station_manager.stations[each])
    for i in range(0, len(stations)):
        v_matrix.append([])
        for j in range(0, len(stations) - 1):
            same_lines = station_manager.get_same_lines(stations[i], stations[j])
            v_matrix[i].append(line_manager.get_best_route(stations[i].name, stations[j].name, same_lines))

    # start_station = input("起始站\n")
    start_station = '火车东站'
    start_index = station_index[start_station]
    # terminal_station = input("终点站\n")
    terminal_station = '火车南站'
    terminal_index = station_index[terminal_station]

    print("Calculating using Dijkstra")
    # 初始化dis数组
    for i in range(0, len(v_matrix) - 1):
        dis.append((v_matrix[start_index][i].stops, [v_matrix[start_index][i]]))
    # 初始化访问节点
    for i in range(0, len(v_matrix) - 1):
        book.append(0)
    book[0] = 1

    n = len(stations)
    u = 0

    for i in range(0, n - 1):
        min = (9999, [Route()])

        for j in range(0, n - 1):
            if book[j] == 0 and dis[j][0] < min[0]:
                min = (dis[j][0], dis[j][1])
                u = j
        book[u] = 1
        ##  中转损失
        bias = 1

        for v in range(0, n - 1):
            if v_matrix[u][v].stops <= 9999:
                if book[v] == 0 and dis[v][0] > (dis[u][0] + v_matrix[u][v].stops + bias):
                    a = []
                    for each in dis[u][1]:
                        a.append(each)
                    a.append(v_matrix[u][v])

                    dis[v] = (dis[u][0] + v_matrix[u][v].stops, a)

    print("Printing transfer solution")
    solution = dis[terminal_index][1]

    for each_route in solution:
        print("在 " + each_route.from_stop + " 乘坐 " + str(
            each_route.line_number) + "号线 到 " + each_route.to_stop + "(" + str(each_route.stops) + "站)")
        line_manager.print_stops(each_route.line_number, each_route.from_stop, each_route.to_stop)
