import os
import mysql.connector
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# 1) FastAPI 인스턴스 먼저 생성
app = FastAPI()

# 2) 정적 파일 마운트 (폴더가 있으면 활용)
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 3) 환경변수 로딩 (GitHub Secrets → .env → 컨테이너 env)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# 4) 루트: 정적 index.html 있으면 반환, 없으면 간단 안내
@app.get("/")
def read_index():
    index_path = "static/index.html"
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {"message": "FastAPI running. Visit /db-check to verify DB connection."}

# 5) DB 연결 확인: SELECT 1
@app.get("/db-check")
def db_check():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)},
        )