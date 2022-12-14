import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import pandas as pd
import functions_framework

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def gdrive_gspread_auto(cloud_event):
    SP_CREDENTIAL_FILE = './google_sheets_api_test.json'
    SP_CORP = ['https://www.googleapis.com/auth/drive',
               'https://spreadsheets.google.com/feeds']
    SP_SHEET_KEY = '1trxHvwKXZs6AAMvUVUfqEVDqS-ycf-w7odf1B-S9KME'
    SP_SHEET = 'test'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SP_CREDENTIAL_FILE, SP_CORP)
    gs = gspread.authorize(credentials)
    workbook = gs.open_by_key(SP_SHEET_KEY)
    worksheet = workbook.worksheet(SP_SHEET)

    # 読み込み
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])

    # 処理
    se = pd.Series([6, 'f'], index=df.columns)
    df = df.append(se, ignore_index=True)
    
    # 書き込み
    sheet_name = 'test2'

    # シートが存在しる場合は削除し新規作成
    try:
        workbook.del_worksheet(workbook.worksheet(sheet_name))
        workbook = gs.open_by_key(SP_SHEET_KEY)
    except:
        pass

    workbook.add_worksheet(title=sheet_name, rows=1000, cols=26)
    set_with_dataframe(workbook.worksheet(sheet_name), df, include_index=False)