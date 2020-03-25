import time
from selenium import webdriver

# 输入公司查询页面的url
url = 'https://angel.co/companies?company_types[]=Mobile+App&stage=Seed&locations[]=1681-Silicon+Valley'
# more按钮的css selector
selector_new = '#root > div.page.unmodified.dl85.layouts.fhr17.header._a._jm > div.companies.dc59.fix36._a._jm > div > div.content > div.dc59.frs86._a._jm > div.results > div.more'
# 公司的css selector
selector_com = '#root > div.page.unmodified.dl85.layouts.fhr17.header._a._jm > div.companies.dc59.fix36._a._jm > div > div.content > div.dc59.frs86._a._jm > div.results > div > div > div.company.column > div > div.text > div.name > a'
# 存储公司的url的list
company_list = []
# 存储个人页面url的list
profile_list = []
# 存储领英url的list
linkedin_list = []
# 存储页面数
count = 0


# 获取公司url
def get_company(driver):
    global company_list, selector_com,count

    for i in range(1, count):
        if i == 1:
            company = driver.find_elements_by_css_selector(selector_com)
            for com in company:
                company_list.append(com.get_attribute('href'))
        else:
            selector_com = selector_com[
                           :-62] + 'div.dc59.frs86._a._jm > div > div > div > div.company.column > div > div.text > div.name > a'
            company = driver.find_elements_by_css_selector(selector_com)
            for com in company:
                company_list.append(com.get_attribute('href'))


# 加载出所有公司
def click_update(driver):
    global selector_new, count
    count_raw = driver.find_element_by_css_selector(
        "#root > div.page.unmodified.dl85.layouts.fhr17.header._a._jm > div.companies.dc59.fix36._a._jm > div > div.content > div.dc59.frs86._a._jm > div.top > div.count")
    count = (int(count_raw[:-10]))/20
    for i in range(1, count):
        if i == 1:
            print(selector_new)
            driver.find_element_by_css_selector(selector_new).click()
            time.sleep(3)
        else:
            print(selector_new)
            selector_new = selector_new[:-8] + 'div.dc59.frs86._a._jm > div > div.more'
            driver.find_element_by_css_selector(selector_new).click()
            time.sleep(3)


# 获取创始人url
def get_profile(driver):
    global company_list
    for url in company_list:
        new_window = 'window.open("%s");' % url
        print(new_window)
        driver.execute_script(new_window)
        # 移动句柄，对新打开页面进行操作
        driver.switch_to.window(driver.window_handles[2])
        time.sleep(2)
        profiles = driver.find_elements_by_css_selector(
            '#main > div.component_70709 > div.wrapper_06a53 > div > div > div.profile_89ad5 > div > section > div:nth-child(2) > div.component_11e1f.twoColumn_7aa41 > div > div > div > div.identity_675c7 > div > h4 > a')
        for person in profiles:
            profile_list.append(person.get_attribute('href'))
            print(person.get_attribute('href'))
        driver.close()
        driver.switch_to.window(driver.window_handles[1])


# 获取领英url
def get_linkin(driver):
    global profile_list
    for url in profile_list:
        new_window = 'window.open("%s");' % url
        print(new_window)
        driver.execute_script(new_window)
        # 移动句柄，对新打开页面进行操作
        driver.switch_to.window(driver.window_handles[2])
        time.sleep(2)
        try:
            linkin_url = driver.find_element_by_css_selector(
                '#root > div.page.flush_bottom.dl85.layouts.fhr17.header._a._jm > div > div.prefix.u-bgWhite > div > div > div.dps64.profiles-show.fsr47.subheader._a._jm > div > div > div > div.text.profile-text.u-textAlignCenterSmOnly > div.u-colorGray9 > div:nth-child(1) > div:nth-child(2) > div > span:nth-child(1) > a')
            if linkin_url.get_attribute('href').find('linkedin') != -1:
                linkedin_list.append(linkin_url.get_attribute('href'))
                print(linkin_url.get_attribute('href'))
            else:
                print('linkedin no found')
        except Exception as e:
            pass
        driver.close()
        driver.switch_to.window(driver.window_handles[1])


# 登陆网页，不然无法获取创始人具体信息
def log_in(driver):
    driver.get('https://angel.co/login')
    usrname = driver.find_element_by_css_selector('#user_email')
    usrname.send_keys('xuhang.shi@outlook.com')
    usrpsw = driver.find_element_by_css_selector('#user_password')
    usrpsw.send_keys('200831sxh')
    login = driver.find_element_by_css_selector('#new_user > div:nth-child(6) > input')
    login.click()
    new_window = 'window.open("%s");' % url
    print(new_window)
    driver.execute_script(new_window)
    # 移动句柄，对新打开页面进行操作
    driver.switch_to.window(driver.window_handles[1])


# opts = Options()
# opts.add_argument('--headless')
# driver = webdriver.Chrome(options=opts)


# 上方注释用于切换有头/无头模式
driver = webdriver.Chrome()
log_in(driver)
time.sleep(5)
click_update(driver)
get_company(driver)
print(company_list)
get_profile(driver)
print(profile_list)
get_linkin(driver)
for link in linkedin_list:
    print(link)
