from datetime import date
from typing import Optional
from fastapi import APIRouter
from connection import get_connection
from pydantic import BaseModel

router = APIRouter()
type_map = {
    "expense": "Gasto",
    "income": "Ganho"
}
allowed_order = ["transaction_id", "transaction_description", "category_name", "transaction_type", "status", "amount",
                 "transaction_date"]
allowed_asc_desc = ["ASC", "DESC"]

class Transaction(BaseModel):
    description : str
    category_id : int
    status : str
    amount : float
    type : str
    date : date

class TransactionPatch(BaseModel):
    description : Optional[str] = None
    category_id : Optional[int] = None
    status : Optional[str] = None
    amount : Optional[float] = None
    type : Optional[str] = None
    date : Optional[date] = None

@router.get("/transactions")
def get_transactions(transaction_id : Optional[int] = None, transaction_description : Optional[str] = None,
                     category_name : Optional[str] = None, transaction_type : Optional[str] = None,
                     status : Optional[str] = None, min_amount : Optional[float] = None, max_amount : Optional[float] = None,
                     min_transaction_date : Optional[date] = None, max_transaction_date : Optional[date] = None,
                     order_by : Optional[str] = None, asc_desc : Optional[str] = None,
                     limit: Optional[int] = None, offset: Optional[int] = None):
    conn = get_connection()
    cur = conn.cursor()
    params = []
    query = """
        SELECT t.transaction_id,
               t.transaction_description,
               c.category_name,
               t.transaction_type,
               t.status,
               t.amount,
               t.transaction_date
        FROM transactions t
        JOIN categories c
        ON t.category_id = c.category_id
        WHERE 1 = 1
    """
    if transaction_id is not None:
        query += (" AND t.transaction_id = %s")
        params.append(transaction_id)
    if transaction_description is not None:
        query += (" AND t.transaction_description ILIKE %s")
        params.append(f"%{transaction_description}%")
    if category_name is not None:
        query += (" AND c.category_name ILIKE %s")
        params.append(f"%{category_name}%")
    if transaction_type is not None:
        query += (" AND t.transaction_type ILIKE %s")
        params.append(f"%{transaction_type}%")
    if status is not None:
        query += (" AND t.status ILIKE %s")
        params.append(f"%{status}%")
    if min_amount is not None:
        query += (" AND t.amount >= %s")
        params.append(min_amount)
    if max_amount is not None:
        query += (" AND t.amount <= %s")
        params.append(max_amount)
    if min_transaction_date is not None:
        query += (" AND t.transaction_date >= %s")
        params.append(min_transaction_date)
    if max_transaction_date is not None:
        query += (" AND t.transaction_date <= %s")
        params.append(max_transaction_date)
    if order_by is not None:
        if order_by in allowed_order:
            if asc_desc is not None:
                asc_desc_input = asc_desc.upper()
                if asc_desc_input in allowed_asc_desc:
                    query += (f" ORDER BY {order_by} {asc_desc_input}")
            else:
                query += (f" ORDER BY {order_by} ASC")
    if limit is not None:
        query += (" LIMIT %s")
        params.append(limit)
    if offset is not None:
        query += (" OFFSET %s")
        params.append(offset)
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = []
    for row in rows:
        db_value = row[3]
        display_value = type_map.get(db_value, db_value)
        result.append({
            "id": row[0],
            "description": row[1],
            "category": row[2],
            "type": display_value,
            "status": row[4],
            "amount": row[5],
            "date": row[6].isoformat() if row[6] else None
        })
    return result

@router.post("/transactions")
def post_transaction(transaction : Transaction):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transactions (transaction_description, category_id, status, amount, transaction_type, transaction_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (transaction.description, transaction.category_id, transaction.status, transaction.amount, transaction.type, transaction.date))
    conn.commit()
    cur.close()
    conn.close()
    return {"message" : "Transação criada com sucesso!"}

@router.put("/transactions/{transaction_id}")
def put_transaction(transaction_id : int, transaction : Transaction):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE transactions
        SET transaction_description = %s,
        category_id = %s,
        status = %s,
        amount = %s,
        transaction_type = %s,
        transaction_date = %s
        WHERE transaction_id = %s
    """, (transaction.description, transaction.category_id, transaction.status, transaction.amount, transaction.type, transaction.date, transaction_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message" : "Transação Atualizada com sucesso!"}

@router.patch("/transactions/{transaction_id}")
def patch_transaction(transaction_id : int, transaction : TransactionPatch):
    conn = get_connection()
    cur = conn.cursor()
    fields = []
    values = []

    if transaction.description is not None:
        fields.append("transaction_description = %s")
        values.append(transaction.description)
    if transaction.category_id is not None:
        fields.append("category_id = %s")
        values.append(transaction.category_id)
    if transaction.status is not None:
        fields.append("status = %s")
        values.append(transaction.status)
    if transaction.amount is not None:
        fields.append("amount = %s")
        values.append(transaction.amount)
    if transaction.type is not None:
        fields.append("transaction_type = %s")
        values.append(transaction.type)
    if transaction.date is not None:
        fields.append("transaction_date = %s")
        values.append(transaction.date)
    if not fields:
        return {"message" : "Sem campos para atualizar"}

    query = f"""
        UPDATE transactions
        SET {', '.join(fields)}
        WHERE transaction_id = %s
    """
    values.append(transaction_id)
    cur.execute(query, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
    return {"message" : "Transação atualizada com sucesso!"}

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id : int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM transactions
        WHERE transaction_id = %s
    """, (transaction_id, ))
    conn.commit()
    cur.close()
    conn.close()
    if cur.rowcount == 0:
        return {"message" : "Transação não encontrada"}
    return {"message" : "Transação deletada com sucesso!"}