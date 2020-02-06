import datetime

from bs4 import BeautifulSoup
import requests
from datetime import datetime
import MySQLdb
import MySQLdb.cursors

def getHouseList(url):
    house = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'}
    # get从网页获取信息
    res = requests.get(url, headers=headers)
    # 解析内容
    soup = BeautifulSoup(res.content, 'html.parser')
    # 房源title
    housename_divs = soup.find_all('div', class_='city_panel')
    for housename_div in housename_divs:
        housename_as = housename_div.find_all('a')
        for housename_a in housename_as:
            housename = []
            # 标题
            housename.append(SplitString(housename_a.get_text()))
            # 超链接
            housename.append(housename_a.get('href'))
            house.append(housename)
    return house

def SplitString(str):
    str = "-".join(str.split())
    str.replace('\r', '').replace('\t', '').replace('\n','')
    return str

# profile_directory=r'--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data'
# 主函数
def RunSpider():
    url = 'https://shenzhen.anjuke.com/sale/?from=navigation'
    houses = getHouseList(url)
    return WriteMySQL(houses)

def WriteMySQL(houses):
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="anjuke", charset="utf8")
    cursor = conn.cursor()

    #######第一次运行注释此段##########
    #清空表
    cursor.execute('truncate table spider_city_data;')
    conn.commit()
    #######第一次运行注释此段##########

    #######非第一次运行注释此段##########
    #SQL = """ Create table spider_city_data (`id` int(11) NOT NULL AUTO_INCREMENT, `title` varchar(255) DEFAULT NULL,`url` varchar(255) DEFAULT NULL,`city` varchar(100) DEFAULT NULL,`datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='MySQL Foreign Servers table';flush privileges;"""
    #cursor.execute(SQL)
    #######非第一次运行注释此段##########


    now = datetime.now().replace(microsecond=0).isoformat(' ')
    SQL = """
                   insert IGNORE into spider_city_data (
                   title,url,city,datetime)
                   value (%s,%s,%s,%s)"""
    #print(houses)
    for i in range(len(houses)-1):
        cahce = str(houses[i][1]).split('//')
        cache = str(cahce[1]).split('.')

        print(str(houses[i][0]),str(houses[i][1]),str(cache[0]),now)
        na=(str(houses[i][0]),str(houses[i][1]),str(cache[0]),now)
        cursor.execute(SQL,na)
        conn.commit()
    return 0


if __name__ == '__main__':
    RunSpider()
