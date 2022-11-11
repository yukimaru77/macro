from macro import get_devices_id,Nox_devices,Nox
from time import sleep 
import random
import subprocess
import schedule
import yaml
#yaml-----------
with open("config.yml", "r", encoding="utf-8") as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)
kue=data["kue"]
genre=data["genre"]
kind=data["kind"]
difficulty=data["difficulty"]
#yaml-----------
pre=f"{kind}_p.png"
mid=f"{kind}_m.png"
back=f"{kind}_b.png"
def main():
  #設定ファイルの読み込み(クエスト、難易度等)
  """with open('config.yaml', 'r') as file:
      config = yaml.load(file, Loader=yaml.SafeLoader)"""

  #3垢起動~各Noxへのコントローラーの作成
  sub_accounts_controller=sub_account_start()
  sub_multi_controller=Nox_devices(sub_accounts_controller[0],sub_accounts_controller[1],sub_accounts_controller[2])
  

  for i in [3,4,5]:#本アカ3種類
    #本アカのNox起動~コントローラーの作成
    main_accounts_controller=main_account_start(i)

    #本アカのアプリ起動～ホーム画面まで
    main_accounts_controller.app_start()
    all_multi_controller=Nox_devices(sub_accounts_controller[0],sub_accounts_controller[1],sub_accounts_controller[2],main_accounts_controller)
    others_devices_multi_controller=[Nox_devices(sub_accounts_controller[1],sub_accounts_controller[2],main_accounts_controller),Nox_devices(sub_accounts_controller[0],sub_accounts_controller[2],main_accounts_controller),Nox_devices(sub_accounts_controller[0],sub_accounts_controller[1],main_accounts_controller)]
    start2home(main_accounts_controller)

    for j in range(0,31): #３1回繰り返し
      #サブ垢のアプリデータ入れ替え~ホーム画面まで
      #(i==3) or ((i==5) and (j<=20)) or (i==4)
      if(False) :
        pass
      else:
        sleep(2)
        sub_multi_controller.chage(i-2,j*3)
        sleep(1)
        sub_multi_controller.app_start()
        start2home(sub_multi_controller)
        for k in range(4): #クエストを三回繰り返す
          #クエスト選択
          if(k==3):
            k=0
          kue_select(sub_accounts_controller[k])

          #難易度選択~出陣待ち
          wait_go(sub_accounts_controller[k],LINE=True)

          #他3垢の参加
          join(others_devices_multi_controller[k],LINE=True,url=data[f"account{i-2}_{j*3+k}"])

          #出陣~クエスト終了
          while not (sub_accounts_controller[k].is_img("torikesi.png",0.9,x2=200,y1=750,y2=900)):
            sub_accounts_controller[k].touch(sub_accounts_controller[k].x+210) #スタート
          sub_accounts_controller[k].touch(180,650) #"はい"があったと時用
          shot(all_multi_controller) #クエストクリアまで撃つ

          #ホーム画面まで戻る
          clear(all_multi_controller)
        
        #アプリを終了
        sub_multi_controller.pull(i-2,j*3)
        sub_multi_controller.app_end()
        print(f"終了、i={i}、j={j}")
    end(i)

def end(i):
  subprocess.Popen(f"Nox.exe -clone:Nox_{i} -quit", shell=True)
  sleep(10)

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
  if is_list(dev.me):
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
  """if is_list(dev.me):
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

def wait_go(dev,LINE=False):
  while not (dev.is_img("LINE.png",0.9,x1=200,x2=400,y1=370,y2=600)):
    dev.img_touch(difficulty,0.9,x2=280,y1=400,y2=900)
    dev.img_touch("maruti.png",0.9,x1=300,x2=560,y1=350,y2=630)
  while not (dev.is_img("torikesi.png",0.9,x2=200,y1=750,y2=900)):
    if(LINE):
      dev.img_touch("LINE.png",0.9,x1=200,x2=400,y1=370,y2=600)
    else:
      dev.img_touch("tikaku.png",0.9,x2=200,y1=370,y2=600)
    dev.img_touch("sixyutugeki.png",0.9,x1=150,x2=430,y1=500,y2=900)
    dev.img_touch("line_uketuke.png",0.9,x1=210,x2=380,y1=800,y2=870,center=True)


def join(dev,LINE=False,url=""):
  if(LINE):
    dev.clear()
    sleep(2)
    dev.send_url(url)
  if is_list(dev.me):
    while (False in dev.is_img("torikesi.png",0.9,x2=200,y1=750,y2=900)):
      dev.img_touch("marutisanka.png",0.9,x1=360,y1=730,y2=830,sleep_time=0)
      dev.img_touch("saikennsaku.png",0.9,x1=200,y1=720,y2=810,x2=380,sleep_time=0)
      dev.touch(300,350,sleep_time=0)
      dev.touch(300,668,sleep_time=0)
  else:
    while not (dev.is_img("torikesi.png",0.9,x2=200,y1=750,y2=900)):
      dev.img_touch("marutisanka.png",0.9,x1=360,y1=730,y2=830,sleep_time=0)
      dev.img_touch("saikennsaku.png",0.9,x1=200,y1=720,y2=810,x2=380,sleep_time=0)
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
  if is_list(dev.me):
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
  if is_list(dev.me):
    while (False in dev.is_img("home.png",0.9,y1=800)):
      dev.touch(300,450,sleep_time=0)
      dev.img_touch("ok_clear.png",0.9,x1=200,x2=390,y1=810,y2=900)
  else:
    while not (dev.is_img("home.png",0.9,y1=800)):
      dev.touch(300,450,sleep_time=0)
      dev.img_touch("ok_clear.png",0.9,x1=200,x2=390,y1=810,y2=900)


schedule.every().day.at("04:05").do(main)

"""while True:
    schedule.run_pending() #現在時刻が02:22なら一回だけ発火する(2回目以降は無効、実行するとわかるが並列処理ではない)
    sleep(5)"""

main()
