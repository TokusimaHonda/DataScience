import pandas as pd
import datetime as dt
import glob
import openpyxl
import os


#CSVファイルの読み込み
def csv_to_df(data_file_path,data_columns,data_encoding='utf-8'):
    #data_columns=['colA','colB','colC','colD']
    #data_encoding = "shift_jis"
    df = pd.read_csv(data_file_path,header=None,names=data_columns,encoding=data_encoding)
    return df


#固定長ファイルの読み込み
# åglob_file_path = "./dir01/**/*.csv"
# data_colspecs = [(0,1),(1,5),(5,9),(9,20)]
# data_columns=['colA','colB','colC','colD']
def fixed_length_to_df(data_file_path,data_colspecs,data_columns):
    #固定長ファイルの設定 各列の位置を指定する
    #data_colspecs = [(0,1),(1,5),(5,9),(9,20)]
    
    #data_columns=['colA','colB','colC','colD']
    # skiprowsで先頭、skipfooterで末尾の行を読み込まない
    df = pd.read_fwf('input.txt',colspecs=data_colspecs,header=None,skiprows=1,skipfooter=2,names=data_columns)
    return df



# globでファイルパスを取得し、データを連結する。
# glob_file_path = "./dir01/**/*.csv"
# data_colspecs = [(0,1),(1,5),(5,9),(9,20)]
# data_columns=['colA','colB','colC','colD']
def glob_read_file_concat_df(glob_file_path,recursive_flg,data_columns,data_type,data_colspecs=None):
    df_concat = pd.DataFrame()
    for datafile_path in glob.glob(glob_file_path,recursive=recursive_flg):
        if data_type == "fixed_length":
            df_read_data = fixed_length_to_df(datafile_path,data_colspecs,data_columns)
        else:
            df_read_data = csv_to_df(datafile_path,data_columns,"shift_jis")
        df_concat = pd.concat([df_concat,df_read_data],axis=0)
    
    return df_concat

# pandasでよく使う処理を記載
def main():
    # dataframeを外部結合
    df_left,df_right = pd.DataFrame()
    df_merge = pd.merge(df_left,df_right,left_on='left_col_name',right_on='right_col_name')
    print(df_merge)

    

    #datetime型に変換
    df = pd.DataFrame()
    df['date_time']=pd.to_datetime(df['date'].astype(str) + " " + df['time'].astype(str))
    df['yyyy_mm'] = df['date_time'].dt.strftime['%Y%m']

    #読み込んだファイル名を追加
    import_file_path = "./hogehoge.csv"
    df['file_name'] = os.path.split(import_file_path)[1]

    #検索して抽出
    search_key_list = ['seach01','seach02','seach03']
    df_seach_result = df[(df['date_time'] >= dt.datetime(2020,7,1,12,10))
                 & (df['date_time'] <= dt.datetime(2020,12,20,15,30)) 
                 & (df['key_id'].isin(search_key_list))
                ].copy()
    df_seach_result['order'] = df['key_id'].apply(lambda x: search_key_list.index(x) if x in search_key_list else -1)
    df_seach_result_sort = df_seach_result.sort_values('order').reset_index(drop=True).drop(columns='order').copy()
    print(df_seach_result_sort)
    

    
    #excel出力
    df_01,df_02,df_03,df_replace = pd.DataFrame()
    result_excel_file_path = "./excel_out.xlsx"
    df_01.to_excel(result_excel_file_path,sheet_name='sheet_name01',header=True,index=False)
    with pd.ExcelWriter(result_excel_file_path,engine='openpyxl',mode='a') as writer:
        df_02.to_excel(writer,sheet_name='sheet_name02',header=True,index=False)
        df_03.to_excel(writer,sheet_name='sheet_name03',header=True,index=False)

    #データ置換
    df_replace = df.replace({'col01':{'aaa':'aaa_rep','bbb':'bbb_rep','ccc':'ccc_rep'}})
    print(df_replace)


    #ピポットテーブル
    df_pivot_calc = pd.pivot_table(df,index=['row1','row2'],columns=['colA','colB'],values=['value1','value1']
                                    ,aggfunc='sum',fill_value=0).reset_index()
    df_pivot_calc.to_excel(result_excel_file_path,sheet_name='pivot_calc')

    #group_by
    df_groupby_calc = df.groupby(['colA','colB'],as_index=False).agg({'colA':np.sum,'colB':np.sum})
    print(df_groupby_calc)



    
    









