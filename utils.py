import requests
import re
import time
import json
import os
import pickle
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from baidu_api import baidu_translate
from mail import Mail
from strings import *
from const import *


def now_time_string(string_format="%Y-%m-%d %H:%M:%S"):
    return stamp_to_string(time.time(), string_format)


def http_get(date="2022-09-16"):
    url = "https://dining.wfu.edu/locations/pit-residential-dining-hall/"
    headers = {
        # 'Content-Type': 'application/x-www-form-urlencoded',
        "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Cookie": "_gcl_au=1.1.1741548063.1660066338; nmstat=14ece206-93c8-ee59-37cd-0880e798531d; _fbp=fb.1.1660066342273.1457629645; _hjSessionUser_882013=eyJpZCI6ImRlZjJmNjg0LTNjOGUtNWU3OC1iMDY0LWFkMzU4NTcxZDdmMyIsImNyZWF0ZWQiOjE2NjAwNjYzNDAyNzQsImV4aXN0aW5nIjp0cnVlfQ==; wordpress_google_apps_login=5a18e34c6885cfe11face49f8ad5a941; __utmc=37972837; __utmz=37972837.1662589783.10.8.utmcsr=cs.wfu.edu|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=37972837.1748346245.1660066338.1662589783.1662675274.11; _ga_JCZH7GR21H=GS1.1.1663025635.8.0.1663025635.0.0.0; _ga=GA1.2.1748346245.1660066338; _gid=GA1.2.1780868067.1663102567",
        "Host": "dining.wfu.edu",
    }
    params = {'date': date}
    data = requests.get(url, params=params, headers=headers)
    return data.text


def translate_one_dish(string):
    baidu_return = baidu_translate(string)
    if len(baidu_return) == 0:
        res = "FAILED TO TRANSLATE"
    elif "dst" in baidu_translate(string)[0]:
        res = baidu_return[0]["dst"]
    else:
        res = "FAILED TO TRANSLATE"
    return "{} ({})".format(string, res)


class MyTranslate:
    def __init__(self):
        self.count = 0

    def translate(self, string):
        self.count += len(string)
        return translate_one_dish(string)


def get_menu(date, save_flag=True):
    save_full_time = stamp_to_string(time.time(), "%Y%m%d%H%M%S")
    text = http_get(date)
    soup = BeautifulSoup(text, "lxml")
    period_names = soup.find_all("div", {"class": "c-tabs-nav__link-inner"})
    period_names = [item.text for item in period_names]
    # print(data)
    data_dic = dict()
    data_concerned_dic = dict()
    data_concerned_dic["Lunch"] = dict()
    data_concerned_dic["Dinner"] = dict()

    periods = soup.find_all("div", {"class": "c-tab__content"})
    # assert len(periods) == 4
    word_count = 0
    word_count_need = 0
    for i in range(len(periods)):
        period_dic = dict()
        # print()
        # print(tabs[i])
        blocks = periods[i].find_all("h4", {"class": "toggle-menu-station-data"})
        block_names = [item.text for item in blocks]
        # print(len(blocks))
        # print(blocks)
        block_texts = periods[i].find_all("div", id=re.compile('^menu-station-data-'))
        # print(len(block_texts))
        assert len(blocks) == len(block_texts)

        # print(block_texts)
        # block_names = [item.text for item in blocks]
        # print(periods[i].text)
        for j in range(len(block_texts)):
            dishes = block_texts[j].find_all("a", {"tabindex": "0"})
            dishes = [item.text for item in dishes]
            for item in dishes:
                word_count += len(item)
            if ("LUNCH" in period_names[i] or "LATE BRUNCH" in period_names[i]) and block_names[j].lower() in CONCERNED_STATION_LIST:
                for item in dishes:
                    word_count_need += len(item)
                # if translate_flag:
                #     dishes = ["{}({})".format(item, baidu_translate(item)[0]["dst"]) for item in dishes]
                data_concerned_dic["Lunch"][block_names[j]] = dishes
            elif ("DINNER" in period_names[i]) and block_names[j].lower() in CONCERNED_STATION_LIST:
                for item in dishes:
                    word_count_need += len(item)
                # if translate_flag:
                #     dishes = ["{}({})".format(item, baidu_translate(item)[0]["dst"]) for item in dishes]
                data_concerned_dic["Dinner"][block_names[j]] = dishes
            period_dic[block_names[j]] = {
                "station": block_names[j],
                "dish_num": len(dishes),
                "dishes": list(dishes)
            }
        data_dic[period_names[i]] = {
            "period": period_names[i],
            "station_num": len(blocks),
            "station_menu": period_dic
        }
    dic = {
        "date": date,
        "word_count": word_count,
        "word_count_concerned": word_count_need,
        "data": data_dic,
        "data_concerned": data_concerned_dic
    }
    # print(json.dumps(dic, indent=4, ensure_ascii=False))
    if save_flag and dic["word_count"] > 10:
        folder_path = "saves/{}".format(date)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        target_path = "saves/{}/{}_{}.pkl".format(date, date, save_full_time)
        with open(target_path, "wb") as f:
            pickle.dump(dic, f)
    match_flag = False
    match_reason_list_lunch = []
    match_reason_list_dinner = []
    for period_key in dic["data_concerned"]:
        for station_key in dic["data_concerned"][period_key]:
            for one_dish in dic["data_concerned"][period_key][station_key]:
                for one_word in CONCERNED_DISH_KEYWORD_LIST:
                    if one_word.lower() in one_dish.lower():
                        match_flag = True
                        if period_key == "Lunch":
                            match_reason_list_lunch.append("{}".format(one_dish))
                        elif period_key == "Dinner":
                            match_reason_list_dinner.append("{}".format(one_dish))
    return dic, match_flag, [match_reason_list_lunch, match_reason_list_dinner]


def stamp_to_string(stamp, string_format="%Y-%m-%d %H:%M"):
    return time.strftime(string_format, time.localtime(stamp))


def get_week_day(string, string_format="%Y-%m-%d"):
    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(string, string_format))).isoweekday()


def get_week_day_name(string, string_format="%Y-%m-%d"):
    day = get_week_day(string, string_format="%Y-%m-%d")
    day_name_dic = {
        1: "Mon",
        2: "Tue",
        3: "Wed",
        4: "Thu",
        5: "Fri",
        6: "Sat",
        7: "Sun"
    }
    return day_name_dic[day]


def daily_job():
    time_stamp = time.time()
    today_date = stamp_to_string(time_stamp, "%Y-%m-%d")

    df_date = []
    df_day = []
    df_match = []
    df_match_reason_lunch = []
    df_match_reason_dinner = []
    mt = MyTranslate()
    dic_list = []
    while True:
        new_date = stamp_to_string(time_stamp, "%Y-%m-%d")
        menu_dic, match_flag, match_reason = get_menu(new_date)
        # print("{}: \"{}\", \"{}\"".format(new_date, match_flag, match_reason))
        dic_list.append(menu_dic)
        if menu_dic["word_count"] <= 10:
            break
        df_date = df_date + [new_date]
        df_day = df_day + [get_week_day_name(new_date)]
        df_match = df_match + (["Yes"] if match_flag else ["No"])
        new_lunch = match_reason[0]
        new_lunch = [mt.translate(item) for item in new_lunch]
        new_dinner = match_reason[1]
        new_dinner = [mt.translate(item) for item in new_dinner]
        df_match_reason_lunch = df_match_reason_lunch + (["[br]".join(new_lunch)] if len(match_reason[0]) > 0 else [""])
        df_match_reason_dinner = df_match_reason_dinner + (["[br]".join(new_dinner)] if len(match_reason[1]) > 0 else [""])
        time_stamp += 86400
    # print(df_date)
    # print(df_match)
    # print(df_match_reason_lunch)
    # print(df_match_reason_dinner)
    df = pd.DataFrame()
    df["Date"] = df_date
    df["Day"] = df_day
    df["Match"] = df_match
    df["Lunch"] = df_match_reason_lunch
    df["Dinner"] = df_match_reason_dinner
    df.reset_index(drop=True, inplace=True)
    df.index += 1

    df_today_lunch = pd.DataFrame()
    lunch_list_dic = dict()
    for station_key in dic_list[0]["data_concerned"]["Lunch"]:
        station_dishes = dic_list[0]["data_concerned"]["Lunch"][station_key]
        station_dishes = [mt.translate(item) for item in station_dishes]
        lunch_list_dic[station_key] = station_dishes
    lunch_list_max = max([len(lunch_list_dic[one_key]) for one_key in lunch_list_dic])
    # print("lunch_list_max:", lunch_list_max)
    # print(lunch_list_dic)
    for one_key in lunch_list_dic:
        df_today_lunch[one_key] = lunch_list_dic[one_key] + [""] * (lunch_list_max - len(lunch_list_dic[one_key]))
    df_today_lunch.reset_index(drop=True, inplace=True)
    df_today_lunch.index += 1

    df_today_dinner = pd.DataFrame()
    dinner_list_dic = dict()
    for station_key in dic_list[0]["data_concerned"]["Dinner"]:
        station_dishes = dic_list[0]["data_concerned"]["Dinner"][station_key]
        station_dishes = [mt.translate(item) for item in station_dishes]
        dinner_list_dic[station_key] = station_dishes
    dinner_list_max = max([len(dinner_list_dic[one_key]) for one_key in dinner_list_dic])
    # print("dinner_list_max:", lunch_list_max)
    # print(dinner_list_dic)
    for one_key in dinner_list_dic:
        df_today_dinner[one_key] = dinner_list_dic[one_key] + [""] * (dinner_list_max - len(dinner_list_dic[one_key]))
    df_today_dinner.reset_index(drop=True, inplace=True)
    df_today_dinner.index += 1

    mail = Mail()
    to_receivers = ["xue20@wfu.edu", "zhanj318@wfu.edu"]  # ["zhanj318@wfu.edu"]
    mail.set_receivers(to_receivers, [], [])
    content_html = STRING_MAIL_TEXT_HEAD + STRING_MAIL_TEXT_TITLE.format(today_date)
    content_html += STRING_MAIL_TEXT_PART_NONE_BLUE.format(
        "Calendar",
        df.to_html().replace(" style=\"text-align: right;\"", "")
    ).replace("[br]", "<br>")
    content_html += STRING_MAIL_TEXT_README.format(
        "Keywords: {}".format(str(CONCERNED_DISH_KEYWORD_LIST)),
        "Station Interest: {}".format(str(CONCERNED_STATION_LIST)),
        "Translation Cost: {} characters".format(mt.count),
    )
    content_html += STRING_MAIL_TEXT_PART_NONE_RED.format(
        "Today Menu - Lunch",
        df_today_lunch.to_html().replace(" style=\"text-align: right;\"", "")
    )
    content_html += STRING_MAIL_TEXT_PART_NONE_RED.format(
        "Today Menu - Dinner",
        df_today_dinner.to_html().replace(" style=\"text-align: right;\"", "")
    )

    content_html += STRING_MAIL_TEXT_TAIL
    # print(content_html)
    mail.send(content_html, [], "PIT Daily [{}] - Today [{}]".format(today_date, df_match[0]), "html")
    print(now_time_string(), "[ ok ] Finished")


if __name__ == "__main__":
    # print(stamp_to_string(time.time()))
    # print(stamp_to_string(time.time() + 86400))
    # date = "2022-10-20"
    # menu = get_menu(date)
    # print(json.dumps(menu, indent=4, ensure_ascii=False))
    # res = http_get("2022-09-20")
    # print(res)
    # menu = get_menu("2022-09-16")
    # print(json.dumps(menu, indent=4, ensure_ascii=False))
    print(get_week_day_name("2022-10-08"))
    # daily_job()
    pass
