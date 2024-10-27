import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def update_weather_info():
    # 현재 시간에서 30분 전의 시간을 계산
    t = datetime.now() - timedelta(minutes=30)
    r = datetime.now()
    h = datetime.now() + timedelta(minutes=30)
    h_time = h.strftime('%H%M')
    real_time = r.strftime('%H%M')
    base_date = t.strftime('%Y%m%d')
    base_time = t.strftime('%H%M')

    # 좌표값
    x = 76
    y = 90

    # API Key
    api_key = "u4xDoGDjs6KKdP82wJI6KfIm1UQCD0Fp86HOjnJ7xBfpPFhDm2I6JcK9WzoJhkT52sBAf4aItv6sq3bVouQEmQ=="

    # API 호출 URL 생성
    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst?ServiceKey={api_key}&numOfRows=60&base_date={base_date}&base_time={base_time}&nx=90&ny=76"

    # HTTP 연결 생성
    response = requests.get(url)

    # tree 구조로 변경
    tree = ET.fromstring(response.content)

    # 날씨정보가 들어갈 배열 생성
    weather_info = [""] * 5

    # XML 데이터 파싱
    ok = False
    for header in tree.iter('header'):
        if header.find('resultCode').text == "00":
            ok = True
        else:
            print(header.find('resultMsg').text)

    if ok:
        for item in tree.iter('item'):
            category = item.find('category').text
            fcstValue = item.find('fcstValue').text
            fcstTime = item.find('fcstTime').text
            fcstTime = fcstTime[:-2]
            a = h_time[:-2]
            if a == fcstTime:
                # 기상
                # PTY(1 : 맑음, 3 : 구름 많음, 4 : 흐림)
                if category == "PTY":
                    weather_info[2] = fcstValue
                elif category == "SKY":
                    weather_info[2] = fcstValue
                # 온도
                elif category == "T1H":
                    weather_info[3] = fcstValue
                # 습도
                elif category == "REH":
                    weather_info[4] = fcstValue

        # 날짜
        weather_info[0] = base_date
        # 시간
        weather_info[1] = real_time

        print("날짜 : " + weather_info[0])
        print("시간 : " + weather_info[1])
        print("강수 : " + weather_info[2])
        print("온도 : " + weather_info[3])
        print("습도 : " + weather_info[4])

        # UI 텍스트 업데이트
        canvas.itemconfig(date_text, text=datetime.strptime(base_date, "%Y%m%d").strftime("안녕하세요! 오늘은 %Y년 %m월 %d일"))
        canvas.itemconfig(time_text, text=datetime.strptime(real_time, "%H%M").strftime("%H시 %M분 입니다."))
        canvas.itemconfig(temp_text, text=weather_info[3] + "º")
        canvas.itemconfig(info_text, text="어제보다 0.4º 상승 / 구름많음")
        canvas.itemconfig(rain_text, text="강수량 " + weather_info[2])
        canvas.itemconfig(humidity_text, text="습도 " + weather_info[4] + "%")
        canvas.itemconfig(wind_text, text="남풍 2.5m/s")

        # 비에 대한 경고 메시지 업데이트
        if int(weather_info[2]) > 80:
            canvas.itemconfig(umbrella_message, text="비가 올 확률이 높아요! 우산을 챙기세요")
        else:
            canvas.itemconfig(umbrella_message, text="비 걱정 없는 맑은 하루 되세요!")


# UI 창 생성
root = tk.Tk()
root.geometry("600x300")

# 캔버스를 사용하여 배경 이미지 추가
canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(row=0, column=0, rowspan=5, columnspan=5)

# 배경 이미지 경로 설정
background_path = "C:/weathericon/rainyday_99.png"  # 배경 이미지 경로를 실제 이미지 경로로 설정
background_image = Image.open(background_path)
background_image = background_image.resize((600, 300))  # 창 크기에 맞게 이미지 크기 조정
background_photo = ImageTk.PhotoImage(background_image)

# 배경 이미지 캔버스에 추가
canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

# 날짜와 시간, 기타 데이터를 캔버스 위에 텍스트로 추가
date_text = canvas.create_text(120, 40, text="", font=("맑은 고딕", 10, "bold"), fill="white", anchor=tk.W)
time_text = canvas.create_text(355, 40, text="", font=("맑은 고딕", 10, "bold"), fill="white", anchor=tk.W)
umbrella_message = canvas.create_text(180, 60, text="", font=("맑은 고딕", 10, "bold"), fill="white", anchor=tk.W)
temp_text = canvas.create_text(250, 100, text="00º", font=("맑은 고딕", 50, "bold"), fill="white", anchor=tk.W)
info_text = canvas.create_text(110, 160, text="어제보다 0.4º 상승 / 구름많음", font=("맑은 고딕", 20), fill="white", anchor=tk.W)
rain_text = canvas.create_text(120, 190, text="강수량 ", font=("맑은 고딕", 10, "bold"), fill="white", anchor=tk.W)
humidity_text = canvas.create_text(270, 190, text="습도 ", font=("맑은 고딕", 10, "bold"), fill="white", anchor=tk.W)
wind_text = canvas.create_text(400, 190, text="남풍 2.5m/s", font=("맑은 고딕", 10, "bold"), fill="white", anchor=tk.W)

# 기존 Label_06부터 Label_09까지는 배경색을 유지
box_text_01 = "미세먼지\n 좋음"
Label_06 = tk.Label(canvas,
                    text=box_text_01,
                    font=("맑은 고딕", 10),
                    background="lightskyblue1",
                    width=10,
                    anchor="center",
                    padx=10, pady=5)
Label_06.place(x=100, y=200)

box_text_02 = "초미세먼지\n 보통"
Label_07 = tk.Label(canvas,
                    text=box_text_02,
                    font=("맑은 고딕", 10),
                    background="lightskyblue2",
                    width=10,
                    anchor="center",
                    padx=10, pady=5)
Label_07.place(x=200, y=200)

box_text_03 = "자외선\n 높음"
Label_08 = tk.Label(canvas,
                    text=box_text_03,
                    font=("맑은 고딕", 10),
                    background="lightskyblue3",
                    width=10,
                    anchor="center",
                    padx=10, pady=5)
Label_08.place(x=300, y=200)

box_text_04 = " 일몰\n19:22"
Label_09 = tk.Label(canvas,
                    text=box_text_04,
                    font=("맑은 고딕", 10),
                    background="lightskyblue4",
                    width=10,
                    anchor="center",
                    padx=10, pady=5)
Label_09.place(x=400, y=200)

Update_Button = tk.Button(canvas, text="초기화", command=update_weather_info)
Update_Button.place(x=275, y=260)

# 초기 텍스트 설정
current_date = datetime.now().strftime('%Y%m%d')
current_time = datetime.now().strftime('%H%M')
canvas.itemconfig(date_text, text=datetime.strptime(current_date, "%Y%m%d").strftime("안녕하세요! 오늘은 %Y년 %m월 %d일"))
canvas.itemconfig(time_text, text=datetime.strptime(current_time, "%H%M").strftime("%H시 %M분 입니다."))

# 창 계속 실행
root.mainloop()
