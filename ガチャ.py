from macro import get_devices_id,Nox_devices,Nox
from time import sleep 
import random
import subprocess
from PIL import Image
import pyocr
import copy
pyocr.tesseract.TESSERACT_CMD = r'C:/Users/yukit/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
tools = pyocr.get_available_tools()
tool = tools[0]  

builder = pyocr.builders.TextBuilder(tesseract_layout=6)
import yaml
#yaml-----------

kue="monbikue.png"
genre="normal.png"
kind="kame"
difficulty="zixyou.png"
#yaml-----------
pre=f"{kind}_p.png"
mid=f"{kind}_m.png"
back=f"{kind}_b.png"
def main():

  #3垢起動~各Noxへのコントローラーの作成
  sub_accounts_controller=[Nox('127.0.0.1:62001'),Nox('127.0.0.1:62025'),Nox('127.0.0.1:62026')]
  sub_multi_controller=Nox_devices(sub_accounts_controller[0],sub_accounts_controller[1],sub_accounts_controller[2])

  for i in range(3,6):#3種類

    for j in range(0,31): #３０回繰り返し
      if( ((i==4)) or (i==3) or((i==5)and(j<=27))):
        pass
      else:
        #サブ垢のアプリデータ入れ替え~ホーム画面まで
        gatixya_multi_controller=copy.copy(sub_accounts_controller)
        sleep(2)
        sub_multi_controller.chage(i-2,j*3)
        sleep(1)
        sub_multi_controller.app_start()
        start2home(sub_multi_controller)
        sleep(3)
        start2home(sub_multi_controller)
        sleep(3)
        sub_multi_controller.touch(340,950)
        sleep(3)
        sub_multi_controller.touch(300,610)
        sleep(2)
        for k in sub_accounts_controller:
          k.img_touch("selecet_get_chara.png",0.90)
          sleep(5)
          k.touch(400,440)
          sleep(8)
          k.touch(510,210)
          sleep(3)
          k.touch(450,200)
          sleep(3)
          k.touch(300,300)
          sleep(2)
          k.touch(300,250)
          sleep(3)
          k.touch(400,850)
          sleep(8)
          if(k.img_touch("no_a-sa-_sita.png",0.95) ): #アーサー
            gatixya_multi_controller.remove(k)
            sleep(3)
            k.touch(300,440) #木
            sleep(8)
            k.touch(100,850)
            sleep(2)
            k.touch(200,440) #水
            sleep(8)
            k.touch(200,440)
            sleep(2)
            k.touch(100,440) #火
            sleep(8)
            k.touch(100,550)
            sleep(2)
            k.touch(500,440) #闇
            sleep(8)
            k.touch(500,440)
            sleep(2)
            k.touch(100,680) #決定
            sleep(8)
            k.swipe(500,570,500,120,2000)
            sleep(3)
            escape=0
            while (k.is_img("selecet_get_chara.png",0.90)):
              k.img_touch("10ren.png",0.90)
              sleep(10)
              k.touch(300,640)
              k.touch(300,670)
              sleep(5)
              while (k.is_img("10ren.png",0.90)==False):
                if(k.is_img("nennrei.png",0.90)):
                  escape=1
                  break
                k.swipe(300,730,300,880,1000)
                k.touch(300,640)
                k.touch(300,670)
                k.touch(400,130)
              if(escape==1):
                break
              sleep(10)
        #アプリを終了
        sub_multi_controller.app_end()
  


def get_monsuto_id(dev,i,j):
  subprocess.call(f"adb -s {dev.id} shell screencap -p /sdcard/screen.png", shell=True)
  subprocess.call(f"adb -s {dev.id} pull /sdcard/screen.png pictures/", shell=True)
  img = Image.open('pictures/screen.png')
  #box=(left, upper, right, lower)でcropの引数に指定
  img=img.crop((249,495,485,534))
  txt_pyocr = tool.image_to_string(img , lang='eng', builder=builder)
  #半角スペースを消す ※読みやすくするため
  txt_pyocr = txt_pyocr.replace(',', '').replace(' ', '').replace('+', '').replace('-', '')
  print(f"{i-2},{j},{txt_pyocr}")


def is_list(a):
  return type(a) is list

def sub_account_start():
  Noxs=get_devices_id(0,1,2) #デバイス番号取得
  Nox0=Nox(Noxs[0])
  Nox1=Nox(Noxs[1])
  Nox2=Nox(Noxs[2])
  return [Nox0,Nox1,Nox2]

def main_account_start(i):
  Noxs=get_devices_id(i) #デバイス番号取得
  return Nox(Noxs[0])

def start2home(dev):
  if is_list(dev.is_img("home.png",0.9,y1=800)):
    while (False in dev.is_img("home.png",0.9,y1=800)):
      dev.img_touch("consent.png",0.9,y1=500,sleep_time=0)
      dev.img_touch("ok0.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
      dev.img_touch("ok1.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
      dev.img_touch("ok2.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
      dev.img_touch("ok3.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
      dev.touch(300,400,sleep_time=0)
  else:
    while not (dev.is_img("home.png",0.9,y1=800)):
      dev.img_touch("consent.png",0.9,y1=500)
      dev.img_touch("ok0.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
      dev.img_touch("ok1.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
      dev.img_touch("ok2.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
      dev.img_touch("ok3.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
      dev.touch(300,400,sleep_time=0)    
  sleep(3)
  dev.touch(50,950)

def kue_select(dev):
  """if is_list(dev.is_img("home.png",0.9,y1=800)):
    while (False in dev.is_img("asobikata.png",0.9,x1=250,y1=150,x2=350,y2=250)):
      dev.img_touch("ok1kai.png",0.9,y1=500,x1=100,x2=500)
      dev.img_touch("kueok.png",0.9,y1=500,x1=100,x2=500)
      dev.img_touch(genre,0.9,x1=80,y1=520,x2=520,y2=710)
      dev.img_touch(pre,0.9,y1=160,y2=520)
      dev.img_touch(mid,0.9,y1=160,y2=520)
      dev.img_touch(back,0.9,y1=160,y2=520)
      for i,flag in enumerate(dev.is_img("marutisanka.png",0.9,x1=360,y1=730,y2=830)):
        if flag:
          dev.devices[i].touch(dev.devices[i].x-120,dev.devices[i].y)
    while (False in dev.is_img(kue,0.9,x2=440,y1=250,y2=890)):
      dev.img_touch("ok1kai.png",0.9,y1=500,x1=100,x2=500)
      dev.img_touch("kueok.png",0.9,y1=500,x1=100,x2=500)
      for i,flag in enumerate(dev.is_img("sixyousai.png",0.9,x1=420,y1=400,x2=550,y2=540)):
        if flag:
          dev.devices[i].touch(dev.devices[i].x-120,dev.devices[i].y-110)
      for i,flag in enumerate(dev.is_img("bar.png",0.9,x1=550,y1=150,y2=9305)): #下にスライド
        if flag:
          dev.devices[i].swipe(dev.devices[i].x,dev.devices[i].y,dev.devices[i].x,dev.devices[i].y+50,750)
  else:"""
  while not (dev.is_img("asobikata.png",0.9,x1=250,y1=150,x2=350,y2=250)):
    dev.img_touch("ok1kai.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
    dev.img_touch("kueok.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
    dev.img_touch(genre,0.9,x1=80,y1=520,x2=520,y2=710,sleep_time=0)
    dev.img_touch(pre,0.9,y1=160,y2=520,sleep_time=0)
    dev.img_touch(mid,0.9,y1=160,y2=520,sleep_time=0)
    dev.img_touch(back,0.9,y1=160,y2=520,sleep_time=0)
    if dev.is_img("marutisanka.png",0.9,x1=360,y1=730,y2=830):
      dev.touch(dev.x-120,dev.y)
  while not (dev.is_img(kue,0.9,x2=440,y1=250,y2=890)):
    dev.img_touch("ok1kai.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
    dev.img_touch("kueok.png",0.9,y1=500,x1=100,x2=500,sleep_time=0)
    if dev.is_img("sixyousai.png",0.9,x1=420,y1=400,x2=550,y2=540):
      dev.touch(dev.x-120,dev.y-110)
    if dev.is_img("bar.png",0.9,x1=550,y1=150,y2=930):
      dev.swipe(dev.x,dev.y,dev.x,dev.y+50,750)
  dev.touch()

def wait_go(dev):
  dev.img_touch(difficulty,0.9,x2=280,y1=400,y2=900)
  sleep(0.5)
  dev.img_touch("maruti.png",0.9,x1=300,x2=560,y1=350,y2=630)
  sleep(0.5)
  dev.img_touch("tikaku.png",0.9,x2=200,y1=370,y2=600)
  while not (dev.is_img("sixyutugeki.png",0.9,x1=150,x2=430,y1=500,y2=900)):
    pass
  dev.touch()

def join(dev):
  if is_list(dev.is_img("torikesi.png",0.9,x2=200,y1=750,y2=900)):
    while (False in dev.is_img("torikesi.png",0.9,x2=200,y1=750,y2=900)):
      dev.img_touch("marutisanka.png",0.9,x1=360,y1=730,y2=830,sleep_time=0)
      dev.touch(300,350,sleep_time=0)
      dev.touch(300,668,sleep_time=0)
  else:
    while not (dev.is_img("torikesi.png",0.9,x2=200,y1=750,y2=900)):
      dev.img_touch("marutisanka.png",0.9,x1=360,y1=730,y2=830,sleep_time=0)
      dev.touch(300,350,sleep_time=0)
      dev.touch(300,668,sleep_time=0)

def decide():
    x2=random.randint(260,320)
    y2=random.randint(290,460)
    x=random.randint(50,150)
    y=random.randint(50,150)
    sign=random.randint(1,4)
    if sign==1:
      return([x2+x,y2+y,x2,y2])
    if sign==2:
      return([x2+x,y2-y,x2,y2])
    if sign==3:
      return([x2-x,y2+y,x2,y2])
    if sign==4:
      return([x2-x,y2-y,x2,y2])

def shot(dev):
  if is_list(dev.is_img("torikesi.png",0.9,x2=200,y1=750,y2=900)):
    judge=[False]
    while (False in judge):
      judge=[]
      for i in dev.devices:
        j=i.is_img("ok_fin.png",0.9,x1=150,x2=450,y1=500,y2=750)
        if not (j):
          x=decide()
          i.swipe(x[0],x[1],x[2],x[3],500+random.randint(0,500))
        judge.append(j)
  else:
    j=True
    while j:
        j=dev.is_img("ok_fin.png",0.9,x1=150,x2=450,y1=500,y2=750)
        if not (j):
          x=decide()
          dev.swipe(x[0],x[1],x[2],x[3],500+random.randint(0,500))
  dev.touch()

def clear(dev):
  if is_list(dev.is_img("home.png",0.9,y1=800)):
    while (False in dev.is_img("home.png",0.9,y1=800)):
      dev.touch(300,450,sleep_time=0)
      dev.img_touch("ok_clear.png",0.9,x1=200,x2=390,y1=810,y2=900)
  else:
    while not (dev.is_img("home.png",0.9,y1=800)):
      dev.touch(300,450,sleep_time=0)
      dev.img_touch("ok_clear.png",0.9,x1=200,x2=390,y1=810,y2=900)

main()




    


