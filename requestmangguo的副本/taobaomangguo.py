#coding:utf-8
import requests
from lxml import etree
import jsonpath
import re
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



headers = {
    'cookie':'miid=851480781739738881; thw=cn; UM_distinctid=15e07df76ba71d-0dbdbe441986b-31667c01-1fa400-15e07df76bb3ff; hng=CN%7Czh-CN%7CCNY%7C156; tracknick=liuchanghuangs; _cc_=W5iHLLyFfA%3D%3D; tg=0; cna=RJg2Ed2o3FcCATEFAILnjUr9; t=e16326cc993d9381bac027228bcd8947; enc=CTFKqEqBUPzc6rBivb3yjOZy%2FIV4L8BdB7KtSI3M1yUXwSB52MFnquj3dKoqcTZejsMuoAms3z6l9vBgpSmqnQ%3D%3D; JSESSIONID=C7359215FF4CD7DEB749589B7A313C1C; isg=AubmTZ5vgCPwDldAMbR1vhqVN1qobyFmVdVwYtCP0onkU4ZtOFd6kcyh33mk',
    'referer': 'https://s.taobao.com/search?q=%E8%8B%B9%E6%9E%9C&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s=88',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
}



def url_frist(url):

    response = requests.get(url, headers=headers)
    try:
        info = re.findall('{"pageName.*false}}', response.content)[0].encode('utf-8')
    except:
        print response.status_code
        with open('1.html', 'w') as f:
            f.write(response.content)
        print "未抓取url:" + url
        url_frist(url)
        return
        # print info
        # with open("1.html","w") as f:
        # f.write(str(url_list))
    info_json = json.loads(info)
    url_list = jsonpath.jsonpath(info_json, '$..detail_url')
    i = 0
    for url in url_list:
        #print url
        item = {}
        item["price"] = jsonpath.jsonpath(info_json, '$..view_price')[i] + '\t'
        #print item['price']

        item["province"] = jsonpath.jsonpath(info_json, '$..item_loc')[i] + '\t'

        if url.startswith('https'):
            # print url
            content(url,item)
        else:
            url = "https:" + url
            # print url
            content(url,item)


def content(url,item):
    #print 1
    response = requests.get(url,headers = headers)
    html =etree.HTML(response.content)
    title_list1 = html.xpath('//ul[@id="J_AttrUL"]/li/text()')
    title_list2 = html.xpath('//ul[@class="attributes-list"]/li/text()')
    if len(title_list1) != 0:

        #print 1111111
        title_list1 = ",".join(title_list1).encode('utf-8')
        #print title_list1
        title = re.findall('\xe6\xb0\xb4\xe6\x9e\x9c\xe7\xa7\x8d\xe7\xb1\xbb.*?,', title_list1)
        # print title
        if len(title) != 0:
            title = title[0]
            item["name"] = title[title.find(':') + 1:-1] + "\t"
            weight = re.findall('\xe5\x87\x80\xe5\x90\xab\xe9\x87\x8f:\xc2\xa0\d*g', title_list1)
            #print weight
            item["weight"] = weight[0][weight[0].find(':') + 1:] + "\t"
            # if a in title:
            # print title.encode('utf-8')
            # item = response.meta["item"]
            # item["name"] = title[title.find(':')+1:]+"\t"
            # print item["name"]
            # yield item
            with open(item["name"] + ".txt", "a") as f:
                f.write(item["name"] + item["price"] + item["province"] + item["weight"] + "\n")
    elif len(title_list2) != 0:
        # for title in title_list2:
        #print 2222222
        title_list2 = ",".join(title_list2).encode('utf-8')
        # print title_list2
        title = re.findall('\xe6\xb0\xb4\xe6\x9e\x9c\xe7\xa7\x8d\xe7\xb1\xbb.*?,', title_list2)
        # print title
        if len(title) != 0:
            title = title[0]
            item["name"] = title[title.find(':') + 1:-1] + "\t"
            weight = re.findall('\xe5\x87\x80\xe5\x90\xab\xe9\x87\x8f:\xc2\xa0\d*g', title_list2)
            # print weight
            item["weight"] = weight[0][weight[0].find(':') + 1:] + "\t"
            with open(item["name"] + ".txt", "a") as f:
                f.write(item["name"] + item["price"] + item["province"] + item["weight"] + "\n")
if __name__ == "__main__":
    #url_list = []
    for i in range(100):
        print i
        page = i*44
        url = "https://s.taobao.com/search?q=%E8%8A%92%E6%9E%9C&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48&s="+str(page)
        #url_list.append(url)
        print url
        url_frist(url)
    #pool = ThreadPool(10)
    #pool.map(h_request, url_list)
    #pool.close()
    #pool.join()