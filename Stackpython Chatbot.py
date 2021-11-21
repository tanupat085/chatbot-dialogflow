#code by Stackpython
#Import Library
import json
import os
from gspread.client import Client
from numpy.lib.function_base import select
import pandas as pd
from flask import Flask
from flask import request
from flask import make_response
import csv
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
spd_key = '1GofRw5an6OcKXhTmHVx2g7wX0uGuWoePOW3Daw-V5_M'
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cerds = ServiceAccountCredentials.from_json_keyfile_name("cerds.json", scope)
client = gspread.authorize(cerds)
sheet = client.open("Chatbot").worksheet('Sheet1')
sheet2 = client.open("Chatbot").worksheet('Sheet2')
sheet3 = client.open("Chatbot").worksheet('Sheet3')
data2 = sheet2.get_all_records()
data3 = sheet3.get_all_records()
listdata3 = pd.DataFrame(data3)
listdata2 = pd.DataFrame(data2)
# อ่านจากหน้า sheet2
# print(listdata2)
data3 = sheet3.get_all_records()
listdata3 = pd.DataFrame(data3)
index3 = int(len(listdata3) + 2)



#----------------------------------- notion----------------------------------- 
from random import randint
# import firebase_admin 
# from firebase_admin import credentials
# from firebase_admin import firestore
# cred = credentials.Certificate("codelabtext-adea3-firebase-adminsdk-dxibt-249123249d.json")
# firebase_admin.initialize_app(cred)

filedatabase = open('db.json')
notion_db = json.load(filedatabase)
print(len(notion_db['results']))
testnotion = notion_db['results'][0]['properties']['status']['rich_text'][0]['plain_text']
data = sheet.get_all_records()
listdata = pd.DataFrame(data)
index = int(len(listdata) + 2)

# อ่านจากหน้า sheet1
# print("data: ",data)
# print("index: ",index)
sheet.insert_row([testnotion,'notion testing4'],index)

#----------------------------------- notion----------------------------------- 

#notion to table
#notion file
filenotion = open('db.json')
datanotion = json.load(filenotion)
def get_projects_titles(data):

    return list(data["results"][0]["properties"].keys())


def Notion_to_table():
    titlenotion = get_projects_titles(datanotion)
    lendat = len(datanotion['results'])
    print("lensdat :" , lendat)
    print("titlenotion :" ,titlenotion)
    b = {}
    for x in reversed(titlenotion):
        if x == 'Name':
             b[x] = [datanotion['results'][i]['properties'][x]['title'][0]['plain_text'] for i in range(0,lendat) ]
        elif x == 'Column':
            b[x] = [datanotion['results'][i]['properties'][x]['select']['name'] for i in range(0,lendat) ]
        elif x == 'person':
            b[x] = [datanotion['results'][i]['properties'][x]['people'][0]['name'] for i in range(0,lendat) ]
        else :
            b[x] = [datanotion['results'][i]['properties'][x]['rich_text'][0]['plain_text'] for i in range(0,lendat) ]
        
    # print(b)
    df = pd.DataFrame.from_dict(b)
    print("df :" , df)
    df= df[::-1]
    
    client.open_by_key(spd_key).values_clear("Sheet3")
    set_with_dataframe(sheet3,df)
    # df = df.to_dict('list')
    print(df)
    
    return df
    


def Exportdata_to_sheet():
    data_to_sheet = Notion_to_table()
    
Exportdata_to_sheet()




# Flask
app = Flask(__name__)
@app.route('/', methods=['POST']) 

def MainFunction(): 

    #รับ intent จาก Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)

    #เรียกใช้ฟังก์ชัน generate_answer เพื่อแยกส่วนของคำถาม
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    
    #ตอบกลับไปที่ Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #การตั้งค่าประเภทของข้อมูลที่จะตอบกลับไป

    return r

def generating_answer(question_from_dailogflow_dict):

    #Print intent ที่รับมาจาก Dailogflow
    print(json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))

    #เก็บต่า ชื่อของ intent ที่รับมาจาก Dailogflow
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"] 

    #ลูปตัวเลือกของฟังก์ชั่นสำหรับตอบคำถามกลับ
    if intent_group_question_str == 'หิวจัง':
        answer_str = menu_recormentation()
    elif intent_group_question_str == 'คำนวนน้ำหนัก': 
        answer_str = BMI(question_from_dailogflow_dict)
    else: answer_str = "ผมไม่เข้าใจ คุณต้องการอะไร"

    #สร้างการแสดงของ dict 
    answer_from_bot = {"fulfillmentText": answer_str}
    
    #แปลงจาก dict ให้เป็น JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
    
    return answer_from_bot

def menu_recormentation(): #ฟังก์ชั่นสำหรับเมนูแนะนำ
#-----------------------------------
    # database_ref = firestore.client().document('Food/Menu_List')
    # database_dict = database_ref.get().to_dict()
    # database_list = list(database_dict.values())
    # ran_menu = randint(0,len(database_list)-1)
    # menu_name = database_list[ran_menu]
#-----------------------------------
    menu_name = 'ข้าวขาหมู'
    answer_function = menu_name + ' มั้ย '
    return answer_function

def BMI(respond_dict): #ฟังก์ชั่นสำหรับคำนวนน้ำหนัก

    #เก็บค่าของ Weight กับ Height
    weight1 = float(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Weight.original"])
    height1 = float(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Height.original"])

    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    index = int(len(listdata) + 2)
    print("data: ",data)
    print("index: ",index)
    sheet.insert_row([weight1,height1],index)
    

    #คำนวนน้ำหนัก
    BMI = weight1/(height1/100)**2
    if BMI < 18.5 :
        answer_function = "ผอมจัง"
    elif 18.5 <= BMI < 23.0:
        answer_function = "สมส่วน"
    elif 23.0 <= BMI < 25.0:
        answer_function = "ค่อนข้างอ้วน"
    elif 25.0 <= BMI < 30:
        answer_function = "อ้วนล่ะนะ"
    else :
        answer_function = "อ้วนมากจ้าา"
    return answer_function

#Flask
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
