from bs4 import BeautifulSoup
import requests
import random

# Lotto Function 樂透爬蟲(大樂透、今彩539、威力彩)
def Lotto(LottoName):
    # 解析網頁、抓取資料
    Url = "https://www.taiwanlottery.com.tw/index_new.aspx" # 樂透url
    Html = requests.get(Url) # 抓取網頁html內容
    ObjHtml = BeautifulSoup(Html.text, 'html.parser') # 傳入url指定html型態建立其物件，回傳html結構字串
    DivTag2 = ObjHtml.select('div.contents_box02') # 樂透開獎號碼div區塊

    # 大樂透
    if LottoName == "Big": 
        BigTitle = DivTag2[2].find_all('span')[0].text # 從第2個DivTag找到 大樂透 日期與期數
        BigNumber = DivTag2[2].find_all('div', {'class':'ball_tx ball_yellow'}) # 從第2個DivTag找到 大樂透 號碼
        BigString = "" # 大樂透號碼
        for i in range(6,12): 
            BigString += BigNumber[i].text
        BigSpecialNumber = DivTag2[2].find_all('div', {'class':'ball_red'}) # 從第2個DivTag找到 大樂透 特別號
        BigResult = '大樂透： {0} \n  {1} 特別號：{2}'.format(BigTitle, BigString, BigSpecialNumber[0].text)
        return BigResult
    # 威力彩
    elif LottoName == "Power": 
        PowerTitle = DivTag2[0].find_all('span')[0].text # 從第0個DivTag找到 威力彩 日期與期數
        PowerNumber = DivTag2[0].find_all('div', {'class':'ball_tx ball_green'}) # 從第0個DivTag找到 威力彩 號碼
        PowerString = "" # 威力彩號碼
        for j in range(6, 12): 
            PowerString += PowerNumber[j].text
        PowerSpecialNumber = DivTag2[0].find_all('div', {'class':'ball_red'}) # 從第0個DivTag找到 威力彩 特別號
        PowerResult = '威力彩： {0} \n  {1} 特別號：{2}'.format(PowerTitle, PowerString, PowerSpecialNumber[0].text)
        return PowerResult
    # 今彩539
    elif LottoName == "Aya": 
        DivTag3 = ObjHtml.select('div.contents_box03') # 樂透開獎號碼div區塊
        AyaNumber = DivTag3[0].find_all('div', {'class':'ball_tx ball_lemon'}) # 從第0個DivTag找到 今彩539 號碼
        AyaTitle = DivTag3[0].find_all('span')[0].text # 從第0個DivTag找到 威力彩 日期與期數
        AyaString = "" # 今彩539
        for k in range(5, 10): # 今彩539
            AyaString += AyaNumber[k].text
        AyaResult = '今彩539 {0} \n  {1} '.format(AyaTitle, AyaString)
        return AyaResult
    else:
        return "error"


# RandomLotto Function 樂透電腦選號(大樂透、今彩539、威力彩)
def RandomLotto(LottoName):
    if LottoName == "Big": # 大樂透電腦選號
        Number = random.sample(range(1, 50), 6)
        Number.append(random.sample(range(1, 50), 1)) # 特別號
        Result = IntChangeString(Number)
        # Result = [str(x) for x in Number]
    elif LottoName == "Power": # 威力彩電腦選號
        Number = random.sample(range(1,39), 6)
        Number.append(random.sample(range(1,9), 1)) # 特別號
        Result = IntChangeString(Number)
        # Result = [str(x) for x in Number]
    elif LottoName == "Aya": # 今彩539電腦選號
        Number = random.sample(range(1, 40), 5)
        Result = IntChangeString(Number)
        # Result = [str(x) for x in Number]
    else:
        Result = "error"
    return Result


# list int 轉 list string
def IntChangeString(List1):
    List = [str(x) for x in List1]
    ListString = " , ".join(List)
    return ListString

