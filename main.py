from quora import text_process
import multiprocessing as mp
import requests
import time
import re
import csv
import codecs
import sys

base_url = 'https://www.quora.com'
cookies = {
    'm-b':"7zg1z_8aPEgJMXsdHQKL6Q\\075\\075",
    'm-s':"smfVU6E2rDASsnQddhD5BQ\\075\\075",
    'm-early_v':'29d000462444051c',
    'm-tz':'-480',
    '_ga':'GA1.2.1731073594.1531826895',
    'm-css_v':'6e3532559a13f2c6',
    'm-wf-loaded':'q-icons-q_serif',
    '_gid':'GA1.2.1158350481.1531999442',
    'm-sa':'1',
    'm-lat':"NWHHYZiXMByEHCmqR10u5Q\\075\\075",
    'm-login':'1',
}
headers = {
    'Host' : 'www.quora.com',
    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
}
session = requests.session()
session.headers = headers
requests.utils.add_dict_to_cookiejar(session.cookies, cookies)

ff = open('question_link.txt', 'r', encoding = 'utf-8').read()
href_list = re.findall(r'href=\"(.*?)\"', ff, re.I)
sources = [base_url+href for href in href_list]
sources = sources[500:1000]




def crawl(source):
    response =  session.get(source, allow_redirects = False)
    print(response)
    time.sleep(1)
    return response.text



def multicore():
     global htmls
     pool = mp.Pool()
     multi_res = [pool.apply_async(crawl, (source,)) for source in sources]
     htmls = [res.get() for res in multi_res]


if __name__ == '__main__':

    multicore()
    csvfile = open('data.csv', 'wb')
    csvfile.write(codecs.BOM_UTF8) #防止乱码
    csvfile.close()
    with open('data.csv', 'a', encoding = 'utf-8', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['订阅数','问题','话题一','话题二','话题三','话题四','话题五','话题六','回答内容','浏览量','赞同数','作者被订阅数','作者回答数','图片数','外链数'])
        text_process(htmls, session, writer)
