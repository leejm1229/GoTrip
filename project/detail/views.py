from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .models import Board, Img, Kakao
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import requests
import json
from search.models import Search
import time
import re
# from konlpy.tag import Mecab
# from collections import Counter

# def analysis(title):
#     mecab = Mecab()
#     title = Search.objects.get(title=title)
#     boards = Board.objects.filter(destination=title)

#     lines = []
#     hangul = re.compile('[^ ㄱ-ㅣ 가-힣]')

#     for board in boards:
#         result = hangul.sub('', board.contents)
#         lines.append(result)
#     line = ",".join(lines)
#     nouns = mecab.nouns(line)
#     # print(nouns)
#     nouns = [x for x in nouns if len(x) > 1]
#     counter = Counter(nouns)
#     print(counter.most_common(10))

def detail(request):
    title = request.GET.get('title')
    img_crawl(title)
    review_crawl(title)
    kakao(title)
    # analysis(title)
    return redirect('./detail/?title=%s' % title) # 넘겨주기


def detail_list(request):
    title = request.GET.get('title')
    title = Search.objects.get(title=title)
    images = Img.objects.filter(destination=title)
    kakao = Kakao.objects.filter(destination=title)
    boards = Board.objects.filter(destination=title).order_by('id')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(boards, 5) 
    boards = paginator.get_page(page)

    x = kakao[0].x
    y = kakao[0].y
    return render(request, 'detail/detail.html', {'boards':boards ,'images' : images, 'y':y, 'x' : x, 'title':title})


# 이미지 크롤링 --------------------------------------------------------------------------------------------------------------
def img_crawl(title):
    title = Search.objects.get(title=title)
    img = Img.objects.filter(destination=title)

    img.delete()
    link = Search.objects.get(title = title) 
    
    page = 1
    option = Options()
    option.add_argument('no-sandbox')
    option.add_argument('--headless')
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome('./chromedriver', options=option) # Mac
    # browser = webdriver.Chrome('./chromedriver.exe', options=option) # Window
    browser.get(link.url)
    print(browser)
    while page < 7:                                                                                       
        try:                                                                                              
            item = WebDriverWait(browser,3).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.yMdQy.w > ul > li.CyFNY._A.MBoCH > div")))
            image = item.get_attribute('style').replace('background-image: url("', '').replace('");', '')
            
            img = Img(
                destination = title,
                address = image,
            )
            img.save()
        except:
            print('에러1')

        try:                                                                                                    
            WebDriverWait(browser, 3).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div > div.AWPqO.Z1._S.nlmjL > button'))).click()
        except:
            print('에러2')

        page += 1


# 카카오 지도(위도, 경도) ------------------------------------------------------------------------------------------------------------------------
def kakao(title):
    title = Search.objects.get(title=title)
    kakao = Kakao.objects.filter(destination=title)
    kakao.delete()

    item = Search.objects.get(title = title)
    address = item.address

    
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+address
    headers = {"Authorization": "KakaoAK 2b6d2255a3c62ca88e47dc43bac4ee37"}
    result = json.loads(str(requests.get(url,headers=headers).text))
    match_first = result['documents'][0]['address']
    y, x = float(match_first['y']),float(match_first['x'])


    kakao = Kakao(
        destination = title,
        x = x,
        y = y
    )

    kakao.save()


# 댓글 크롤링 -------------------------------------------------------------------------------------------------------------------
def review_crawl(title):
    title = Search.objects.get(title=title)
    board = Board.objects.filter(destination=title)

    board.delete()
    link = Search.objects.get(title = title) 
    

    option = Options()
    option.add_argument('no-sandbox')
    option.add_argument('--headless')
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    option.add_argument("disable-features=NetworkService")
    browser = webdriver.Chrome('./chromedriver', options=option) # Mac
    # browser = webdriver.Chrome('./chromedriver.exe', options=option) # Window

    link = Search.objects.get(title = title)
    browser.get(link.url)
    page = 1

    
    while page < 4:
        items = WebDriverWait(browser, 3).until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.LbPSX > div')))
        items = items[:-1]

        for key, item in enumerate(items):
            scope = item.find_element(By.CSS_SELECTOR, '#tab-data-qa-reviews-0 > div > div.LbPSX > div:nth-child({}) >  span > div > div:nth-child(2) > svg'.format(key+1))
            scope = scope.get_attribute('aria-label').replace('풍선 5개 중 ', '')

            date = item.find_element(By.CSS_SELECTOR, '#tab-data-qa-reviews-0 > div > div.LbPSX > div:nth-child({}) > span > div > div.RpeCd'.format(key+1)).text
                                       
            text = item.find_element(By.CSS_SELECTOR, '#tab-data-qa-reviews-0 > div > div.LbPSX > div:nth-child({}) > span > div > div.biGQs._P.fiohW.qWPrE.ncFvv.fOtGX > a > span'.format(key+1)).text
                                            
            content = item.find_element(By.CSS_SELECTOR, '#tab-data-qa-reviews-0 > div > div.LbPSX > div:nth-child({}) > span > div > div._T.FKffI > div.fIrGe._T.bgMZj > div > span'.format(key+1)).text
     
            board = Board(
            destination = title,
            scope = scope,
            register_dttm = date,
            title = text,
            contents = content
            )

            board.save()
            
        
        page += 1

        try:                                                                                                   
            WebDriverWait(browser, 2).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '#tab-data-qa-reviews-0 > div > div.LbPSX > div:nth-child(11) > div:nth-child(2) > div > div.OvVFl.j > div.xkSty > div > a'))).click()
            time.sleep(3)
        except:
            print('다음버튼 오류')
            pass
