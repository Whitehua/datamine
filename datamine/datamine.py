import re

import MySQLdb
import MySQLdb.cursors
import numpy as np
import matplotlib.pyplot as plt

def get_info():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="anjuke", charset="utf8")
    cs = conn.cursor()

    SHOW_TABLE_SQL = """SHOW TABLES"""
    cs.execute(SHOW_TABLE_SQL)
    tables = [cs.fetchall()]

    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]

    city_list = []
    for i in range(1,len(table_list)):
        city_list.append(table_list[i])

    #print(city_list)
    conn.commit()
    return city_list

def get_mean_price(tablename,opt):
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="anjuke", charset="utf8")
    cs = conn.cursor()
    all_district = []
    city_mean_price = []
    SQL1 = """ 
                select `unitprice` from """ + tablename + """ 
        """

    cs.execute(SQL1)
    cache1 = cs.fetchall()
    for s in cache1:
        city_mean_price.append(s[0])
    conn.commit()
    SQL2 = """ 
                    select `district` as district from `"""+tablename+"""` group by `district` having count(district)>1
            """

    cs.execute(SQL2)
    cache2 = cs.fetchall()
    for s in cache2:
        all_district.append(s[0])
    conn.commit()
    #print(all_district)
    all_district_mean = {}
    for a in range(len(list(all_district))):
        single_district_mean = []
        SQL3 = """ 
                        select `unitprice` from `""" + tablename + """` WHERE district = '"""+str(all_district[a])+"""'
                """
        cs.execute(SQL3)
        cache3 = cs.fetchall()
        b=0
        for aa in cache3:
            single_district_mean.append(str(aa[0]).split('元')[0])
            b=b+1
        cc = list(map(int, single_district_mean))
        mean = np.mean(cc)
        min = np.min(list(map(int, single_district_mean)))
        max = np.max(list(map(int, single_district_mean)))

        #print(all_district[a],mean)
        ss = str(''.join(list(all_district[a])))
        if opt == 'mean':
            all_district_mean.setdefault(ss,int(mean))
        else:
            all_district_mean.setdefault(ss,int(b))
        #all_district_mean[a].append(int(mean))
        #all_district_mean[a].append(int(min))
        #all_district_mean[a].append(int(max))
    conn.commit()
    #print(all_district_mean)
    return all_district_mean

def get_year_price(tablename,opt):
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="anjuke", charset="utf8")
    cs = conn.cursor()
    all_district = []
    city_mean_price = []
    SQL1 = """ 
                select `unitprice` from """ + tablename + """ 
        """

    cs.execute(SQL1)
    cache1 = cs.fetchall()
    for s in cache1:
        city_mean_price.append(s[0])
    conn.commit()
    SQL2 = """ 
                    select `buildtime` as buildtime from `"""+tablename+"""` group by `buildtime` having count(buildtime)>1
            """

    cs.execute(SQL2)
    cache2 = cs.fetchall()
    for s in cache2:
        all_district.append(s[0])
    conn.commit()
    #print(all_district)
    all_district_mean = {}
    for a in range(len(list(all_district))):
        single_district_mean = []
        SQL3 = """ 
                        select `unitprice` from `""" + tablename + """` WHERE buildtime = '"""+str(all_district[a])+"""'
                """
        cs.execute(SQL3)
        cache3 = cs.fetchall()
        b=0
        for aa in cache3:
            single_district_mean.append(str(aa[0]).split('元')[0])
            b=b+1
        cc = list(map(int, single_district_mean))
        mean = np.mean(cc)

        #print(all_district[a],mean)
        ss = str(''.join(list(all_district[a])))
        year_price = str(''.join(ss.split('年')[0]))
        if opt == 'mean':
            all_district_mean.setdefault(year_price,int(mean))
        else:
            all_district_mean.setdefault(year_price,int(b))
        #all_district_mean[a].append(int(mean))
        #all_district_mean[a].append(int(min))
        #all_district_mean[a].append(int(max))
    conn.commit()
    print(all_district_mean)
    return all_district_mean

def data_draw(list,p):
    all = {}
    for i in range(len(list)):
        all.setdefault(list[i],list[i][p])
    #print(len(list))
    return all

def draw_bash(y):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    group_data = list(y.values())
    group_names = list(y.keys())
    group_mean = np.mean(group_data)
    min = np.min(group_data)
    max = np.max(group_data)
    fig, ax = plt.subplots()
    ax.barh(group_names, group_data)

    ax.axvline(group_mean, ls='--', color='r')

    ax.title.set(y=1.05)


    for group in range(len(group_names)):
        ax.text(y.get(str(group_names[group]))+100, group, y.get(str(group_names[group])) , fontsize=12,
                verticalalignment="center",color='green')

    ax.set(xlim=[0, 10000], xlabel='各地区房价均值', ylabel='区域',
           title='房价均价区域统计')
    c = int((max / 10000) + 1) * 10e3
    ax.set_xticks([0,int(c/10), int((c/10)*2), int((c/10)*3), int((c/10)*4), int((c/10)*5), int((c/10)*6) , int((c/10)*7) ,int((c/10)*8), int((c/10)*9),c])


    plt.show()

def draw_pie(y):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    group_data = list(y.values())
    group_names = list(y.keys())


    fig, ax = plt.subplots()
    ax.pie(group_data)

    ax.title.set(y=1.05)
    explode = (0,)*len(group_names)

    ax.pie(group_data,explode)

    plt.pie(group_data,explode=explode,labels=group_names,autopct="%1.2f%%",shadow=False,startangle=90)
    plt.legend(loc='upper right', bbox_to_anchor=(1.35, 0.9),ncol=1)
    plt.title('各地区房屋出售比例')
    plt.show()

def draw_scatter(y):

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.figure(figsize=(19.2, 10.8))

    group_data = list(y.values())
    group_names = list(y.keys())

    plt.scatter(group_names,group_data,c="red",s=20, marker='o')

    plt.title("建造年份与房价图")  # title：设置子图的标题。

    #plt.savefig('quxiantu.png', dpi=120, bbox_inches='tight')
    plt.show()

def draw_pre(y):

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.figure(figsize=(19.2, 10.8))

    group_data = list(y.values())
    group_names = list(y.keys())

    data = []
    year = []
    for group in range(len(group_names)):
        data.append(str(group_data[group]))
        year.append(str(group_names[group]))
    dd = list(map(float, data))
    yy = list(map(float,year))
    # 用3次多项式拟合
    f1 = np.polyfit(yy, dd, 5)
    p1 = np.poly1d(f1)
    print(p1)  # 打印出拟合函数
    yvals1 = p1(yy)  # 拟合y值



    plt.plot(yy, yvals1, 'r', label='拟合值')

    plt.title("建造年份与房价预测图")  # title：设置子图的标题。

    #plt.savefig('quxiantu.png', dpi=120, bbox_inches='tight')
    plt.show()


def aaaa():
    for i in range(len(get_info())):
        draw_bash(get_mean_price(get_info()[i], 'mean'))
        draw_pie(get_mean_price(get_info()[i], 'percent'))
        draw_pie(get_year_price(get_info()[i], 'mean'))
        draw_scatter(get_year_price(get_info()[i], 'mean'))
        draw_pre(get_year_price(get_info()[i],'mean'))






if __name__ == '__main__':
    aaaa()