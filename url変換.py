import csv
import re
csvfile = open("id_re.csv", 'r')
reader = csv.reader(csvfile)
for row in reader:
    num=1
    url="https://static.monster-strike.com/line/?pass_code="
    row[2] = re.sub('[^0-9]',"",str(row[2]))
    
    for i in row[2]:
        i=int(i)
        if(num%3==1):
            if(i==0):
                a="MD"
            elif(i==1):
                a="MT"
            elif(i==2):
                a="Mj"
            elif(i==3):
                a="Mz"
            elif(i==4):
                a="ND"
            elif(i==5):
                a="NT"
            elif(i==6):
                a="Nj"
            elif(i==7):
                a="Nz"
            elif(i==8):
                a="OD"
            elif(i==9):
                a="OT"
        elif(num%3==2):
            if(i==0):
                a="A"
            elif(i==1):
                a="E"
            elif(i==2):
                a="I"
            elif(i==3):
                a="M"
            elif(i==4):
                a="Q"
            elif(i==5):
                a="U"
            elif(i==6):
                a="Y"
            elif(i==7):
                a="c"
            elif(i==8):
                a="g"
            elif(i==9):
                a="k"
        else:
            if(i==0):
                a="w"
            elif(i==1):
                a="x"
            elif(i==2):
                a="y"
            elif(i==3):
                a="z"
            elif(i==4):
                a="0"
            elif(i==5):
                a="1"
            elif(i==6):
                a="2"
            elif(i==7):
                a="3"
            elif(i==8):
                a="4"
            elif(i==9):
                a="5"
        num=num+1
        url=url+a
    print(f'account{row[0]}_{row[1]} : "{url}"')
