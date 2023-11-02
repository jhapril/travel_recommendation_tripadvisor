from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

url = 'https://www.tripadvisor.co.kr/Attractions-g4-Activities-c61-Europe.html'

locations = []
countrys = []
addresses = []
reviews = []

df = pd.DataFrame()
df_temp=[]
for j in range(4):      # 한 페이지당 장소 30개, 총 4페이지  -> 장소 총 120개
    if j == 0:
        url = 'https://www.tripadvisor.co.kr/Attractions-g4-Activities-c61-Europe.html'
    else :
        url = 'https://www.tripadvisor.co.kr/Attractions-g4-Activities-c61-oa{}0-Europe.html'.format(j*3)
    driver.get(url)
    time.sleep(0.5)
    for i in range(2, 40):      # section[i]
        # 장소명 누르기 -> 페이지 이동
        driver.find_element('xpath', '//*[@id="lithium-root"]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/section[{}]/div/div/div/div/article/div[2]/header/div/div/div/a[1]/h3/div/span/div'.format(i)).click()
        time.sleep(2)

        #현재 작업 중인 웹 드라이버의 세션을 다른 창 또는 탭으로 전환
        window_handles = driver.window_handles

        # 현재 작업 중인 웹 드라이버의 세션을 다른 창 또는 탭으로 전환
        new_window_handle = window_handles[-1]
        driver.switch_to.window(new_window_handle)

        # 장소
        location = driver.find_element('xpath', '//*[@id="lithium-root"]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1').text
        locations.append(location)
        print(locations)

        # 나라
        country = driver.find_element('xpath', '//*[@id="lithium-root"]/main/div[1]/div[1]/div/div/div[2]/a/span/span').text
        countrys.append(country)
        print(countrys)

        # 링크
        address = driver.current_url
        addresses.append(address)
        print(addresses)

        # 리뷰
        driver.find_element('xpath', '//*[@id="tab-data-qa-reviews-0"]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/button/div/span[1]').click()        # 모든 언어
        time.sleep(2)
        driver.find_element('xpath', '//*[@id="menu-item-ko"]/div/span').click()        # 한국어
        time.sleep(3)

        for l in range(20):     # 총 20페이지
            if l != 0 :
                driver.find_element('xpath','//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[12]/div[1]/div/div[1]/div[2]/div/a').click()

            for k in range(2, 12):      # 한페이지당 10, 총 20 페이지 -> 200개
                try :
                    review1 = driver.find_element('xpath', '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[{}]/div/div/div[3]/a/span/span'.format(k)).text
                    time.sleep(2)
                    review2 = driver.find_element('xpath', '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[{}]/div/div/div[5]/div[1]/div/span/span/span'.format(k)).text
                    time.sleep(2)

                except :
                    review1 = driver.find_element('xpath', '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[{}]/div/div/div[3]/a/span/span'.format(k)).text
                    time.sleep(2)
                    review2 = driver.find_element('xpath', '//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[{}]/div/div/div[4]/div[1]/div/span/span/span'.format(k)).text
                    time.sleep(2)

                finally :
                    review = review1 + ' ' + review2
                    reviews.append(review)
                    print(review)

                df_temp = pd.DataFrame({'location': locations, 'country': countrys, 'address': addresses, 'review': reviews})
            df = df.append(df_temp, ignore_index=True)
            df.to_csv("./crawling_data/crawlingdata_{}.csv".format('activity'), index=False, mode='a')
                    # 다음 페이지 클릭 버튼

            # print('error')
            # reviews=[]
            # driver.find_element('xpath','//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div/div[12]/div[1]/div/div[1]/div[2]/div/a').click()       # 리뷰 다음페이지 클릭
            # time.sleep(3)

        # 리뷰 200개 다 긁어오면 창 종료, 원래 페이지로 돌아가기
        driver.close()
        driver.switch_to.window(window_handles[0])
        time.sleep(1)


    # print(df)


        # 브라우저 닫기

        #현재 작업 중인 웹 드라이버의 세션을 다른 창 또는 탭으로 전환
        # window_handles = driver.window_handles
        #
        # # 현재 작업 중인 웹 드라이버의 세션을 다른 창 또는 탭으로 전환



    # time.sleep(2)











    # 이전 페이지로 돌아가기
    # driver.back()

# if (k % 2499 == 0 and k != 0):
#     df.to_csv('./crawling_data/crawling_introduction_{}_{}.0.csv'.format(z, y), index=False)
#     df_introductions = pd.DataFrame()








# for i in range(5):
#     actions = driver.find_element(By.CSS_SELECTOR, 'body')
#     actions.send_keys(Keys.END)
#     time.sleep(0.5)
#
# driver.find_element('xpath','//*[@id="tab-data-qa-reviews-0"]/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/button/div/span[1]').click()
# driver.find_element('xpath','//*[@id="menu-item-ko"]/div/span').click()



# # 모든 창 핸들을 가져오기
# window_handles = driver.window_handles
#
# # 가장 최근에 열린 창으로 전환
# new_window_handle = window_handles[-1]
# driver.switch_to.window(new_window_handle)
# location = driver.find_element('xpath', '//*[@id="lithium-root"]/main/div[1]/div[2]/div[1]/header/div[3]/div[1]/div/h1').text
# driver.close()

        # locations.append(location)
    # driver.find_element('xpath','//*[@id="lithium-root"]/main/div[1]/div/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/section[40]/div/div[1]/div/div[1]/div[2]/div/a/svg').click()         # 다음페이지 넘어가기
#1