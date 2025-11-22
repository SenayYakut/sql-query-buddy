from fastapi import FastAPI
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
from backend.rag.router import router as rag_router

DB_PATH = "backend/db/retail.db"

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include RAG router
app.include_router(rag_router, prefix="/rag")

# Standard REST endpoints
@app.get("/customers")
def get_customers():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers;")
    rows = cursor.fetchall()
    conn.close()
    return {"customers": rows}

@app.get("/orders")
def get_orders():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders;")
    rows = cursor.fetchall()
    conn.close()
    return {"orders": rows}

@app.get("/products")
def get_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products;")
    rows = cursor.fetchall()
    conn.close()
    return {"products": rows}
