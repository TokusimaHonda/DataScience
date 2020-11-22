#!/usr/bin/env python
# coding: utf-8

from slackbot.bot import respond_to
from datetime import datetime,timedelta

import pandas as pd
from slackbot.bot import Bot,respond_to
from datetime import datetime

from oauth2client.service_account import ServiceAccountCredentials
import gspread





@respond_to('開始')
def punch_in(message):
    print('トレーニングを開始します')
    timestamp = datetime.now() + timedelta(hours=9)
    date = timestamp.strftime('%Y/%m/%d')
    punch_in = timestamp.strftime('%H:%M')
    message.send(f'開始時刻は、{punch_in}です。')
    worksheet  =auth()
    df = pd.DataFrame(worksheet.get_all_records())
    df = df.append({'日付':date,'開始時刻':punch_in,'終了時刻':'00:00'},ignore_index=True)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print('登録完了しました')
    message.send('活動記録登録完了しました')

    
@respond_to('終了')
def punch_out(message):
    print('トレーニングを終了します')
    timestamp = datetime.now() + timedelta(hours=9)
    punch_out = timestamp.strftime('%H:%M')
    message.send(f'終了時刻は、{punch_out}です。')
    worksheet  =auth()
    df = pd.DataFrame(worksheet.get_all_records())
    df.iloc[-1,2] = punch_out
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print('登録完了しました')
    message.send('活動記録登録完了しました')


# In[5]:


def  auth():
    SP_CREDENTIAL_FILE = 'python-work-be99f-ea5078732ebb.json'
    SP_SCOPE = [
       'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    SP_SHEET_KEY = '1HzOH6qyxYffTZisl3RuPgXBXUyiYBpt-NqAYaR3q13Q'
    SP_SHEET = '活動記録'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE,SP_SCOPE)
    gc = gspread.authorize(credentials)

    worksheet = gc.open_by_key(SP_SHEET_KEY).worksheet(SP_SHEET)
    return worksheet


def main():
    bot = Bot()
    bot.run()
    

if __name__ == "__main__":
    print('star エニタイム出勤Bot')
    main()



