from macro import get_devices_id,Nox_devices,Nox
from time import sleep 
import random
import yaml
#yaml-----------
kue="ibekue.png"
genre="ibe.png"
kind="ibe"
difficulty="kixyuukixyoku.png"
#yaml-----------
pre=f"{kind}_p.png"
mid=f"{kind}_m.png"
back=f"{kind}_b.png"
def main():
    sub_multi_controller=Nox_devices(Nox('127.0.0.1:62001'),Nox('127.0.0.1:62025'))
    s=Nox('127.0.0.1:62001')
    print("aaaaa")
    clear(sub_multi_controller)




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

  if is_list(dev.is_img("home.png",0.9)):
    while (False in dev.is_img("home.png",0.9)):
      dev.img_touch("consent.png",0.9)
      dev.img_touch("ok0.png",0.9)
      dev.img_touch("ok1.png",0.9)
      dev.img_touch("ok2.png",0.9)
      dev.img_touch("ok3.png",0.9)
      dev.touch(300,400)
  else:
    while not (dev.is_img("home.png",0.9)):
      dev.img_touch("consent.png",0.9)
      dev.img_touch("ok0.png",0.9)
      dev.img_touch("ok1.png",0.9)
      dev.img_touch("ok2.png",0.9)
      dev.img_touch("ok3.png",0.9)
      dev.touch(300,400)    
  sleep(3)
  dev.touch(50,950)
  
def kue_select(dev):
  """if is_list(dev.is_img("home.png",0.9)):
    while (False in dev.is_img("asobikata.png",0.9)):
      dev.img_touch("ok1kai.png",0.9)
      dev.img_touch("kueok.png",0.9)
      dev.img_touch(genre,0.9)
      dev.img_touch(pre,0.9)
      dev.img_touch(mid,0.9)
      dev.img_touch(back,0.9)
      for i,flag in enumerate(dev.is_img("marutisanka.png",0.9)):
        if flag:
          dev.devices[i].touch(dev.devices[i].x-120,dev.devices[i].y)
    while (False in dev.img_touch(kue,0.9)):
      dev.img_touch("ok1kai.png",0.9)
      dev.img_touch("kueok.png",0.9)
      for i,flag in enumerate(dev.is_img("sixyousai.png",0.9)):
        if flag:
          dev.devices[i].touch(dev.devices[i].x-120,dev.devices[i].y-110)
      for i,flag in enumerate(dev.is_img("bar.png",0.95)): #下にスライド
        if flag:
          dev.devices[i].swipe(dev.devices[i].x,dev.devices[i].y,dev.devices[i].x,dev.devices[i].y+50,750)
  else:"""
  while not (dev.is_img("asobikata.png",0.9)):
    dev.img_touch("ok1kai.png",0.9)
    dev.img_touch("kueok.png",0.9)
    dev.img_touch(genre,0.9)
    dev.img_touch(pre,0.9)
    dev.img_touch(mid,0.9)
    dev.img_touch(back,0.9)
    if dev.is_img("marutisanka.png",0.9):
      dev.touch(dev.x-120,dev.y)
  while not (dev.is_img(kue,0.9)):
    dev.img_touch("ok1kai.png",0.9)
    dev.img_touch("kueok.png",0.9)
    if dev.is_img("sixyousai.png",0.9):
      dev.touch(dev.x-120,dev.y-110)
    if dev.is_img("bar.png",0.9):
      dev.swipe(dev.x,dev.y,dev.x,dev.y+50,750)
  dev.touch()

def wait_go(dev):
  dev.img_touch(difficulty,0.9)
  sleep(0.5)
  dev.img_touch("maruti.png",0.9)
  sleep(0.5)
  dev.img_touch("tikaku.png",0.9)
  while not (dev.is_img("sixyutugeki.png",0.9)):
    pass
  dev.touch()
  
def join(dev):
  if is_list(dev.is_img("torikesi.png",0.9)):
    while (False in dev.is_img("torikesi.png",0.9)):
      dev.img_touch("marutisanka.png",0.9)
      dev.touch(300,350)
      dev.touch(300,668)
  else:
    while not (dev.is_img("torikesi.png",0.9)):
      dev.img_touch("marutisanka.png",0.9)
      dev.touch(300,350)
      dev.touch(300,668)

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
  if is_list(dev.is_img("torikesi.png",0.9)):
    judge=[False]
    while (False in judge):
      print(judge)
      judge=[]
      for i in dev.devices:
        j=i.is_img("ok_fin.png",0.9)
        if not (j):
          x=decide()
          i.swipe(x[0],x[1],x[2],x[3],500+random.randint(0,500))
        judge.append(j)
  else:
    j=True
    while j:
        j=dev.is_img("ok_fin.png",0.9)
        if not (j):
          x=decide()
          dev.swipe(x[0],x[1],x[2],x[3],500+random.randint(0,500))
  dev.touch()

def clear(dev):
  if is_list(dev.is_img("home.png",0.9)):
    while (False in dev.is_img("home.png",0.9)):
      dev.touch(300,450)
      dev.img_touch("ok_clear.png",0.9)
  else:
    while not (dev.is_img("home.png",0.9)):
      dev.touch(300,450)
      dev.img_touch("ok_clear.png",0.9)
main()



