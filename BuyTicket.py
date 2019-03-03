import time

from click._compat import raw_input
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#地址
URL_Login = 'https://m.damai.cn/damai/minilogin/index.html'#手机登录页面
URL = 'https://m.damai.cn/damai/perform/item.html?projectId=139556&spm=a2o71.search.list.ditem_5'#手机页面
USERNAME = ""
PASSWORD = ""
NAME="蒋晓宇"
TEL="17611242213"
# 预估会出现的日期
dateString = "03.09"
timeString = "19:30"

driver = webdriver.Chrome("C:\chromedriver.exe")
# 设置等待时间
wait = WebDriverWait(driver, 5)
driver.get(URL_Login)


def choose(seletor, by=By.XPATH, type=1):
    try:
        # 控件可点击时才选定
        if type == 1:
            choice = wait.until(EC.element_to_be_clickable((by, seletor)))
        else:
            choice = wait.until(driver.find_elements((by, seletor)))
        return choice
    except TimeoutException as e:
        print("Time out!")
        return None
    except Exception:
        print("Not found!")
        return None


def inputUser():
    global USERNAME
    global PASSWORD
    print("请输入大麦网账号:")
    USERNAMETEMP = raw_input()
    print(USERNAMETEMP)
    if '' != USERNAMETEMP:
        USERNAME = USERNAMETEMP
    print("请输入大麦网账号密码:")
    PASSWORDTEMP = raw_input()
    if '' != PASSWORDTEMP:
        PASSWORD = PASSWORDTEMP
    print(PASSWORDTEMP)


def login():
    print("Login Start!!!")
    driver.switch_to.frame(driver.find_element_by_id('alibaba-login-box'))  # 切入
    # driver.switch_to.frame(choose("alibaba-login-box", By.ID, 2))  # 切入
    zzmmbtn = None
    if None == zzmmbtn:
        zzmmbtn = choose("password-login-link", By.CLASS_NAME)
        zzmmbtn.click()
    zzinput = None
    if None == zzinput:
        zzinput = choose("fm-login-id", By.ID)
        zzinput.send_keys(USERNAME)
    mminput = None
    if None == mminput:
        mminput = choose("fm-login-password", By.ID)
        mminput.send_keys(PASSWORD)
    while True:
        try:
            #定位滑块元素
            source=driver.find_element_by_id("nc_2_n1z")
            #定义鼠标拖放动作
            ActionChains(driver).drag_and_drop_by_offset(source,900,0).perform()
            #等待JS认证运行,如果不等待容易报错
            time.sleep(2)
            # 查看是否认证成功，获取text值
            text = driver.find_element_by_id("nc_2__scale_text")
            # 目前只碰到3种情况：成功（请在在下方输入验证码,请点击图）；无响应（请按住滑块拖动)；失败（哎呀，失败了，请刷新）
            if text.text.startswith(u'请在下方'):
                print('成功滑动')
                break
            if text.text.startswith(u'验证'):
                print('成功滑动')
                break
            if text.text.startswith(u'请按住'):
                continue
        except Exception as e:
            # 这里定位失败后的刷新按钮，重新加载滑块模块
            driver.find_element_by_xpath("//div[@id='havana_nco']/div/span/a").click()
            print(e)
    mminput.send_keys(Keys.RETURN)
    time.sleep(2)
    driver.get(URL)
    print("Login End!!!")


def chooseTicket():
    print("ChooseTicket Start!!!")
    while True:
        # 1 选座购买
        xzgmbtn = None
        if None == xzgmbtn:
            xzgmbtn = choose("button-group__btn1", By.CLASS_NAME)
            xzgmbtn.click()
        # 2 日期选择
        datebtns  = driver.find_elements_by_class_name("buy-body-card__content-button")
        datebtn = None
        for item in datebtns:
            if item.text.find(dateString) > -1:
                print("找到了")
                datebtn = item
                break
        # 判断日期是否存在
        if None == datebtn:
            print("没找到,滚回去重新找")
            driver.refresh()
            continue
        else:
            print("点击")
            time.sleep(0.5)
            datebtn.click()
        # 3 时间选择
        datebtns  = driver.find_elements_by_class_name("buy-body-card__content-button")
        timebtn = None
        for item in datebtns:
            if item.text.find(timeString) > -1:
                print("找到了")
                timebtn = item
                break
        # 判断时间是否存在
        if None == timebtn:
            print("没找到,滚回去重新找")
            driver.refresh()
            continue
        else:
            print("点击")
            time.sleep(0.1)
            timebtn.click()
            break
    # 4 选座购买
    xzgmbtns = driver.find_elements_by_class_name("button-group__btn1")
    xzgmbtns[1].click()
    print("ChooseTicket END!!!")


def chooseLoc():
    pass


def buy():
    print("buy Start!!!")
    while True:
        if driver.current_url.find("trade") > -1:
            # 选择第一个购票人 dm-button
            time.sleep(0.2)
            driver.find_element_by_class_name("dm-button").click()
            # gprbtns = driver.find_element_by_css_selector(".dm-button.ticket-holder__scroller__btn.dm-button__default.dm-button__small")
            # gprbtns[0].click()
            # 填写姓名手机号
            inputs = driver.find_elements_by_class_name("dm-input_left")
            time.sleep(0.1)
            inputs[0].send_keys(NAME)
            time.sleep(0.1)
            inputs[1].send_keys(TEL)
            #去付款 dm-button btn-group__btn dm-button__primary dm-button__large
            print(driver.find_element_by_css_selector(".dm-button.btn-group__btn.dm-button__primary.dm-button__large").text)
            driver.find_element_by_css_selector(".dm-button.btn-group__btn.dm-button__primary.dm-button__large").click()
            break
        else:
            print("等待进入订单页面")

    print("buy End!!!")


if __name__ == '__main__':
    inputUser()
    login()
    chooseTicket()
    chooseLoc()
    buy()


