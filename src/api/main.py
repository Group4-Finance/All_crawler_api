# 匯入相關套件
import pandas as pd  # 用來處理資料表
from fastapi import FastAPI  # 建立 API 用
from sqlalchemy import create_engine, engine  # 用來建立資料庫連線
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status
import numpy as np


# 匯入自定義的資料庫連線設定
from api.config import MYSQL_ACCOUNT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT






# 建立連接到 MySQL 資料庫的函式，回傳一個 SQLAlchemy 的連線物件
def get_mysql_data_conn() -> engine.base.Connection:
    # 組成資料庫連線字串，使用 pymysql 作為 driver
    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/crawlerDB"
    engine = create_engine(address)  # 建立 SQLAlchemy 引擎
    connect = engine.connect()  # 建立實際連線
    return connect  # 回傳連線物件


# 建立連接到 MySQL 資料庫的函式，回傳一個 SQLAlchemy 的連線物件
def get_mysql_data_conn_signal() -> engine.base.Connection:
    # 組成資料庫連線字串，使用 pymysql 作為 driver
    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/ETF_signal"
    engine = create_engine(address)  # 建立 SQLAlchemy 引擎
    connect = engine.connect()  # 建立實際連線
    return connect  # 回傳連線物件

# 建立 FastAPI 應用實例
app = FastAPI()

origins = [
    "http://localhost:3000",  # React 開發預設網址
    "http://127.0.0.1:3000",
    "http://35.206.205.183:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定義根目錄路由（測試用）
@app.get("/")
def read_root():
    return {"Hello": "World"}  # 回傳基本測試訊息


# def nan_to_none(x):
#     if pd.isna(x):
#         return None
#     else:
#         return x

@app.get("/ETF_signal")
def get_ETF_signal(
    Stock_id: str = "",
    start_date: str = "",
    end_date: str = "",
):
    sql = f"""
    SELECT * FROM ETF_signal_result_{Stock_id}
    WHERE Date >= '{start_date}' AND Date <= '{end_date}'
    """
    mysql_conn = get_mysql_data_conn_signal()
    data_df = pd.read_sql(sql, con=mysql_conn)

    data_df["市價"] = data_df["市價"].astype(object)
    data_df["市價"] = data_df["市價"].where(data_df["市價"].notna(), None)
    data_df["premium_discount_rate"] = data_df["premium_discount_rate"].astype(object)
    data_df["premium_discount_rate"] = data_df["premium_discount_rate"].where(data_df["premium_discount_rate"].notna(), None)
    data_df["折溢價分數"] = data_df["折溢價分數"].astype(object)
    data_df["折溢價分數"] = data_df["折溢價分數"].where(data_df["折溢價分數"].notna(), None)
    data_df["VIX"] = data_df["VIX"].astype(object)
    data_df["VIX"] = data_df["VIX"].where(data_df["VIX"].notna(), None)
    data_df["指數綜合分數"] = data_df["指數綜合分數"].astype(object)
    data_df["指數綜合分數"] = data_df["指數綜合分數"].where(data_df["指數綜合分數"].notna(), None)
    data_df["總分"] = data_df["總分"].astype(object)
    data_df["總分"] = data_df["總分"].where(data_df["總分"].notna(), None)
    data_df["燈號"] = data_df["燈號"].astype(object)
    data_df["燈號"] = data_df["燈號"].where(data_df["燈號"].notna(), None)


    print("-----------------------------轉換成None-----------------------------")
    print(data_df)

    data_dict = data_df.to_dict("records")
    return {"data": data_dict}

    # mysql_conn = get_mysql_data_conn_signal()
    # params = {
    #         "start_date": start_date,
    #         "end_date": end_date
    #     }
    # data_df = pd.read_sql(sql, con=mysql_conn, params= params)
    # data_dict = data_df.to_dict("records")
    # return {"data": data_dict}

# 定義取得台灣股價的 API 路由
@app.get("/cnyes_headlines")
def get_cnyes_headlines(
    start_date: str = "",  # 查詢起始日期（格式：YYYY-MM-DD）
    end_date: str = "",  # 查詢結束日期（格式：YYYY-MM-DD）
):
    # 根據參數組成 SQL 查詢語句
    sql = f"""
    select * from cnyes_headlines
    where  pub_time >= '{start_date}'
    and pub_time <= '{end_date}'
    """
    # 建立資料庫連線
    mysql_conn = get_mysql_data_conn()
    # 使用 Pandas 執行 SQL 查詢並取得資料
    data_df = pd.read_sql(sql, con=mysql_conn)
    # 將資料轉為 List of Dict 格式，方便 FastAPI 回傳 JSON
    data_dict = data_df.to_dict("records")
    return {"data": data_dict}  # 回傳資料結果




@app.get("/ETF_historyprice")
def get_ETF_historyprice(
    Stock_id: str = "",  # 股票代號（可透過 URL query string 傳入）
    start_date: str = "",  # 查詢起始日期（格式：YYYY-MM-DD）
    end_date: str = "",  # 查詢結束日期（格式：YYYY-MM-DD）
):
    try: # 根據參數組成 SQL 查詢語句
        sql = f"""
        select * from ETF_historyprice
        where Stock_id = '{Stock_id}'
        and Date>= '{start_date}'
        and Date<= '{end_date}'
        """
        # 建立資料庫連線
        mysql_conn = get_mysql_data_conn()
        # 使用 Pandas 執行 SQL 查詢並取得資料
        data_df = pd.read_sql(sql, con=mysql_conn)
        # 將資料轉為 List of Dict 格式，方便 FastAPI 回傳 JSON
        data_dict = data_df.to_dict("records")
        return {"data": data_dict}  # 回傳資料結果
    except Exception as e:
        return {"error": str(e)}




@app.get("/ETF_PremiumDiscount")
def get_ETF_PremiumDiscoun(
    Stock_id: str = "",  # 股票代號（可透過 URL query string 傳入）
    start_date: str = "",  # 查詢起始日期（格式：YYYY-MM-DD）
    end_date: str = "",  # 查詢結束日期（格式：YYYY-MM-DD）
):
    # 根據參數組成 SQL 查詢語句
    sql = f"""
    select * from ETF_PremiumDiscount
    where Stock_id = '{Stock_id}'
    and Date>= '{start_date}'
    and Date<= '{end_date}'
    """
    # 建立資料庫連線
    mysql_conn = get_mysql_data_conn()
    # 使用 Pandas 執行 SQL 查詢並取得資料
    data_df = pd.read_sql(sql, con=mysql_conn)
    # 將資料轉為 List of Dict 格式，方便 FastAPI 回傳 JSON
    data_dict = data_df.to_dict("records")
    return {"data": data_dict}  # 回傳資料結果




@app.get("/MagaBank_NEWS")
def get_MagaBank_NEWS(
    start_date: str = "",  # 查詢起始日期（格式：YYYY-MM-DD）
    end_date: str = "",  # 查詢結束日期（格式：YYYY-MM-DD）
):
    # 根據參數組成 SQL 查詢語句
    sql = f"""
    select * from MagaBank_NEWS
    where Date>= '{start_date}'
    and Date<= '{end_date}'
    """
    # 建立資料庫連線
    mysql_conn = get_mysql_data_conn()
    # 使用 Pandas 執行 SQL 查詢並取得資料
    data_df = pd.read_sql(sql, con=mysql_conn)
    # 將資料轉為 List of Dict 格式，方便 FastAPI 回傳 JSON
    data_dict = data_df.to_dict("records")
    return {"data": data_dict}  # 回傳資料結果




@app.get("/ptt")
def get_ptt(
    start_date: str = "",  # 查詢起始日期（格式：YYYY-MM-DD）
    end_date: str = "",  # 查詢結束日期（格式：YYYY-MM-DD）
):
    # 根據參數組成 SQL 查詢語句
    sql = f"""
    select * from ptt
    where  Date>= '{start_date}'
    and Date<= '{end_date}'
    """
    # 建立資料庫連線
    mysql_conn = get_mysql_data_conn()
    # 使用 Pandas 執行 SQL 查詢並取得資料
    data_df = pd.read_sql(sql, con=mysql_conn)
    # 將資料轉為 List of Dict 格式，方便 FastAPI 回傳 JSON
    data_dict = data_df.to_dict("records")
    return {"data": data_dict}  # 回傳資料結果



@app.get("/vix")
def get_vix(
    start_date: str = "",  # 查詢起始日期（格式：YYYY-MM-DD）
    end_date: str = "",  # 查詢結束日期（格式：YYYY-MM-DD）
):
    # 根據參數組成 SQL 查詢語句
    sql = f"""
    select * from vix
    where  Date>= '{start_date}'
    and Date<= '{end_date}'
    """
    # 建立資料庫連線
    mysql_conn = get_mysql_data_conn()
    # 使用 Pandas 執行 SQL 查詢並取得資料
    data_df = pd.read_sql(sql, con=mysql_conn)
    # 將資料轉為 List of Dict 格式，方便 FastAPI 回傳 JSON
    data_dict = data_df.to_dict("records")
    return {"data": data_dict}  # 回傳資料結果
