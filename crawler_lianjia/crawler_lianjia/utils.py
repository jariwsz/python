from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, urlencode 

REGIONS = {
    'pudong':'浦东',
    'minhang':'闵行',
    'baoshan':'宝山',
    'xuhui':'徐汇',
    'putuo':'普陀',
    'yangpu':'杨浦',
    'changning':'长宁',
    'songjiang':'松江',
    'jiading':'嘉定',
    'huangpu':'黄浦',
    'jingan':'静安',
    'hongkou':'虹口',
    'qingpu':'青浦',
    'fengxian':'奉贤',
    'jinshan':'金山',
    'chongming':'崇明',
    'shanghaizhoubian':'上海周边',
}

def cookie_parser():
    cookie_str = 'TY_SESSION_ID=b17da08e-5296-46a9-a9ba-1a0211b63145; lianjia_uuid=b331dfcc-1af1-4dde-962d-5d18685fb564; _smt_uid=5ec333c4.2a945c0e; UM_distinctid=1722a823615465-01bb9e483fe5ce-7a1437-1fa400-1722a823616b8f; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221722a8237e395d-09fc5bb0315c01-7a1437-2073600-1722a8237e5be9%22%2C%22%24device_id%22%3A%221722a8237e395d-09fc5bb0315c01-7a1437-2073600-1722a8237e5be9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.2.2079047963.1589851078; select_city=310000; _jzqckmp=1; _gid=GA1.2.1179144946.1591084755; _qzjc=1; _jzqc=1; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1589935105,1591084752,1591103425,1591149465; CNZZDATA1255604082=1493355695-1589845950-%7C1591149491; CNZZDATA1253492439=1621215475-1589849851-%7C1591153145; CNZZDATA1254525948=164998862-1589850534-%7C1591154148; CNZZDATA1255633284=1073808107-1589845950-%7C1591154143; _jzqa=1.3874763555269256700.1589851076.1591152045.1591154400.12; _jzqx=1.1589868789.1591154400.6.jzqsr=sh%2Elianjia%2Ecom|jzqct=/.jzqsr=sh%2Elianjia%2Ecom|jzqct=/ershoufang/rs%e9%87%91%e5%9c%b0/; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1591154410; _qzja=1.727212561.1589851076190.1591152044607.1591154400009.1591154400009.1591154410319.0.0.0.48.12; _qzjto=20.3.0; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNjYxODViZTI1YTRiZjdkNGE1MTIxYmQ3MTMyNTQ2NTA4NGYyYmY3YTM5NDY4OGIzMTBhZmZiYjViYzk1ZjdkNDMwYmIzMjU2MDYyMzk4OGY5MGVlNDFlOGM4NTk2ZTI1NjcwMDI1ZjEzOTEyODg3ZGJmYjgwMGQ4YjhjODY4MjhkMzRlNmRiMjU1NmZkNDE5ZWVkOTIyNThhODA4YzJmNjg3NWU4NmM3MWZiOWI1ZGEwZjU3YmE4YjM4ZjE3ZTY1ZTMwNzhhYjMzOTM0NjUxM2ViMTJjMTQ1ZjRkMDE5NjkxN2I0MTViNmVhOWQ2ZGUyMzJmMDljZmY1NTZmMjc2ZTQzZGJkZDU1NDBhOTE3MWRiMDJiMjBkZTY5NzA0NTQ5OGI0ZmVlNGY3ODdjN2EwNDVhOTkxMDFlMjczZWRhNTdmN2RjNzkzYWEyNzBiYmZiMmNkYzI4ZWFiZmI1MGVkN1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIwMDExYmU2ZFwifSIsInIiOiJodHRwczovL3NoLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvcnMlRTclQkUlOEUlRTUlQTUlQjMvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; lianjia_ssid=b551da76-5a17-5fc5-0e77-86dc9519d4c4'
    cookie = SimpleCookie()
    cookie.load(cookie_str)

    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    print(cookies)

    return cookies


# cookie_parser()

def parse_url(url):
    url_parsed = urlparse(url)
    print(url_parsed)
    query_string = parse_qs(url_parsed.query)
    print(query_string)