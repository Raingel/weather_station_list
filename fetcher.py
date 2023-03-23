# %%
import requests
import json
import pandas as pd

def agr_get_sta_list(area_id=0, level_id=0):
    my_headers = {    
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "ja-JP,ja;q=0.9,zh-TW;q=0.8,zh;q=0.7,en-US;q=0.6,en;q=0.5",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest", #required
    }
    #URI = 'https://agr.cwb.gov.tw/NAGR/history/station_day/get_station_name'
    URI = 'https://agr.cwb.gov.tw/NAGR/monitor/get_point_list'
    area = ['', '北', '中', '南', '東'][area_id]
    level = ['自動站', '新農業站'][level_id]
    r1 = requests.post(URI, data={'area':area, 'level':level}, headers = my_headers)
    sta_dict = json.loads(r1.text)
    df = pd.DataFrame(sta_dict['station'])
    extract_df = df[['ID', 'Cname', 'Altitude', 'Latitude', 'Longitude', 'StnBeginTime', 'StnEndTime']]
    extract_df.columns=['站號', '站名', '海拔高度(m)', '緯度', '經度', '資料起始日期', '撤站日期']
    return extract_df
    
def load_weather_station_list():
    #load from CWB
    raw = pd.read_html('https://e-service.cwb.gov.tw/wdps/obs/state.htm')
    weather_station_list = pd.concat([raw[0],raw[1]])
    #load from agri
    """
    Deprecated
    CWB has been providing agricultural weather station data since 2023/03, so there is no need to capture agricultural weather stations separately.
    if include_agr_sta:
        weather_station_list = weather_station_list.append(agr_get_sta_list(level_id=1), ignore_index = True)
    """
    return weather_station_list




# %%
#Load the file containing the English site name, but the code of this data is incomplete, so it can' t be used directly
STMap = requests.get('https://www.cwb.gov.tw/Data/js/Observe/OSM/C/STMap.json').text
STMap_dic = json.loads(STMap)
sta_code_to_en = {}
for sta in STMap_dic:
    sta_code_to_en[sta['ID']] = sta['eSTname']



weather_sta_list = load_weather_station_list()
#Insert the English name of the station
weather_sta_list['英文站名'] = weather_sta_list['站號'].str.slice(0,-1).map(sta_code_to_en)
weather_sta_list.to_csv('./data/weather_sta_list.csv', encoding = 'utf-8-sig')
#back up
weather_sta_list.to_csv('./data/weather_sta_list_'+pd.to_datetime("today").strftime("%Y-%m-%d")+'.csv', encoding = 'utf-8-sig')





