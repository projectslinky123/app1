def getspan(html, dataproperty):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    if soup is None or len(soup) == 0:
        return "Stock Ticker data cannot be found"
    else:
        n = soup.find('span', dataproperty)
        if n is None or len(n) == 0:
            return "Stock Ticker data cannot be found"
        else:
            return n.get_text()




def getdf(html, tableproperty):
    import pandas as pd
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    if soup is None or len(soup) == 0:
        errorlist = ['table data not found']
        return pd.DataFrame(errorlist, columns=['Error'])
    else:
        tabledata = soup.find('table', tableproperty)
        if tabledata is None or len(tabledata) == 0:
            errorlist = ['table data not found']
            return pd.DataFrame(errorlist, columns=['Error'])
        else:
            return tabledatatodf(pd, tabledata)


def getpagedata(url):
    from selenium import webdriver
    from fake_useragent import UserAgent
    import time

    # initiating the webdriver. Parameter includes the path of the webdriver.
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={UserAgent().random}')
    options.headless = True
    driver = webdriver.Chrome('./app/browsers/chromedriver', options=options)
    driver.implicitly_wait(15)
    driver.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(15)

    html = driver.page_source
    driver.close()  # closing the webdriver
    return html


def cleanupdata(x):
    return str(x).replace('\n', '').replace('$', '').strip()


def tabledatatodf(pd, tabledata):
    list_header = []
    if tabledata.find(["tr"]):
        elements = tabledata.find(["tr"])
    elif tabledata.find(["thead"]).find(["tr"]):
        elements = tabledata.find(["tr"])
    else:
        return pd.DataFrame()

    for items in elements:
        try:
            list_header.append(items.get_text())
        except:
            continue

    # for getting the data
    data = []
    if tabledata.find_all(["tr"])[1:]:
        elements = tabledata.find_all(["tr"])[1:]
    elif tabledata.find(["tbody"]).find_all(["tr"]):
        elements = tabledata.find(["tbody"]).find_all(["tr"])

    for element in elements:
        sub_data = []
        for sub_element in element.find_all(["td", "th"]):
            try:
                sub_data.append(sub_element.get_text("|"))
            except:
                sub_data.append("")
        data.append(sub_data)

    # Storing the data into Pandas
    # DataFrame
    df = pd.DataFrame(data=data, columns=list_header)
    return df



def getpagedata2(url):
    from selenium import webdriver
    from fake_useragent import UserAgent
    import time

    # initiating the webdriver. Parameter includes the path of the webdriver.
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={UserAgent().random}')
    options.headless = True
    driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)
    driver.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(5)

    html = driver.page_source
    driver.close()  # closing the webdriver
    return html
