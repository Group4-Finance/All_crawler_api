# 匯入相關套件
import pandas as pd  # 用來處理資料表
from fastapi import FastAPI  # 建立 API 用
from sqlalchemy import create_engine, engine  # 用來建立資料庫連線

# 匯入自定義的資料庫連線設定
from api.config import MYSQL_ACCOUNT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT


# 建立連接到 MySQL 資料庫的函式，回傳一個 SQLAlchemy 的連線物件
def get_mysql_data_conn() -> engine.base.Connection:
    # 組成資料庫連線字串，使用 pymysql 作為 driver
    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/crawlerDB"
    engine = create_engine(address)  # 建立 SQLAlchemy 引擎
    connect = engine.connect()  # 建立實際連線
    return connect  # 回傳連線物件


# 建立 FastAPI 應用實例
app = FastAPI()


# 定義根目錄路由（測試用）
@app.get("/")
def read_root():
    return {"Hello": "World"}  # 回傳基本測試訊息


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
    # 根據參數組成 SQL 查詢語句
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




@app.get("/ETF_PremiumDiscoun")
def get_ETF_PremiumDiscoun(
    Stock_id: str = "",  # 股票代號（可透過 URL query string 傳入）
    start_date: str = "",  # 查詢起始日期（格式：YYYY-MM-DD）
    end_date: str = "",  # 查詢結束日期（格式：YYYY-MM-DD）
):
    # 根據參數組成 SQL 查詢語句
    sql = f"""
    select * from ETF_PremiumDiscoun
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
