import streamlit as st
import streamlit.components.v1 as stc
import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#selenium
def login_text():
    account = []
    path = 'C:\\work\\jobcan_account.txt'
    with open(path) as f:
        account = f.readlines()
    USER = account[0]
    PASS = account[1]
    return USER,PASS
def brouser_open():
    global browser
    browser = webdriver.Chrome(executable_path='c:\\work\\driver\\chromedriver.exe')
    browser.implicitly_wait(1)
def brouser_headless():#ヘッドレスモードでブラウザを起動
    #webdrier
    global browser
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(executable_path='c:\\work\\driver\\chromedriver.exe', options=options)
    browser.implicitly_wait(1)
def login_jobcan():
    USER , PASS = login_text()
    #access url
    url_login = "https://id.jobcan.jp/users/sign_in"
    browser.get(url_login)
    browser.implicitly_wait(1)
    #user pass    
    element = browser.find_element_by_id('user_email')
    element.clear()
    element.send_keys(USER)
    element = browser.find_element_by_id('user_password')
    element.clear()
    element.send_keys(PASS)
    #crick login
    browser_from = browser.find_element_by_name('commit')
    browser.implicitly_wait(1)
    browser_from.click()
    url = "https://ssl.jobcan.jp/jbcoauth/login"
    time.sleep(1)
    browser.get(url)
def jobcan_dakoku():
    #crick 
    #push_button = browser.find_element_by_id('adit-button-push')
    #push_button.click()
    #print(u"出退勤ボタン押しました。")
    browser.implicitly_wait(2)
def jobcan_syukinbo():
    syukibo_page = browser.find_element_by_xpath('//*[@id="header"]/div[2]/div/ul/li[1]/a')
    syukibo_page.click()
    #print(u"出勤簿")
def jobcan_syusei():
    dakokusyusei_page = browser.find_element_by_xpath('//*[@id="menu_adit_img"]')
    dakokusyusei_page.click()
    syusei_page = browser.find_element_by_xpath('//*[@id="menu_adit"]/table/tbody/tr[1]/td/a')
    syusei_page.click()
    #print(u"打刻修正")
def jobcan_kyuka():
    sinsei_page = browser.find_element_by_xpath('//*[@id="menu_order_img"]')
    sinsei_page.click()
    kyuka_page = browser.find_element_by_xpath('//*[@id="menu_order"]/table/tbody/tr[1]/td/a')
    kyuka_page.click()
    #print(u"休暇申請")
def jobcan_status():
    time.sleep(2)
    updateTime = datetime.datetime.now()
    status = browser.find_element_by_id('working_status')
    dakoku_more = browser.find_element_by_xpath('//*[@id="top_info_area"]/table/tbody/tr[1]/td/a')
    dakoku_error = browser.find_element_by_xpath('//*[@id="top_info_area"]/table/tbody/tr[2]/td/a')
    updateTime = updateTime.strftime('%H:%M:%S')
    status = status.text
    dakoku_more = dakoku_more.text
    dakoku_error = dakoku_error.text
    return updateTime,status,dakoku_more,dakoku_error

#UI
def jobcan_html_ui():
    USER , PASS = login_text()
    dt_now = datetime.datetime.now()
    dt_str = dt_now.strftime('%Y/%m/%d  %A  %H:%M:%S')
    st.write('**' + dt_str + '**')
    #stc.html(#'<p style="font-size: 14px"><strong>' + dt_str + '</strong></p>' +
            #'<p style="font-size: 10px;text-decoration: underline dotted  black">ユーザー名 : </p>' +
            #'<span style="font-size: 16px;color: red;text-decoration: underline solid black"><left><strong>' + USER + '</strong></left></span>'  , height = 45)
    if st.button('|　　  　ステータス確認　 　 　|'):
        brouser_headless()#brouser_open()
        login_jobcan()
        updateTime , status , dakoku_more , dakoku_error = jobcan_status()
        st.write('現在　　　　**' + status + '**　　　　です。')
    if st.button('|　　　　　　打刻　　　　　　|'):
        brouser_headless()
        login_jobcan()
        jobcan_dakoku()
        updateTime , status , dakoku_more , dakoku_error = jobcan_status()
        st.write(updateTime + '　 　 **' + status + '**　　　に変更')
        st.text('|　　　　　 　　打刻漏れ　 :　　' + dakoku_more + '　|')
        st.text('|　　　　　　 　打刻エラー :　　' + dakoku_error + '　|')
    if st.button('ブラウザで開く'):
        brouser_open()
        login_jobcan()
    st.text('---------------------------------')
    if st.button('打刻修正'):
        brouser_open()
        login_jobcan()
        jobcan_syusei()
    if st.button('休暇申請'):
        brouser_open()
        login_jobcan()
        jobcan_kyuka()

jobcan_html_ui()