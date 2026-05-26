import routes
from fastapi import FastAPI
from connection import get_connection
from pydantic import BaseModel
from typing import Optional
from api.routes import transactions

app = FastAPI()
type_map = {
    "expense": "Gasto",
    "income": "Ganho"
}

app.include_router(transactions.router)


class Category(BaseModel):
    name: str
    description: str
    type: str
    active: bool

class CategoryPatch(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    active: Optional[bool] = None

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/categories")
def get_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT category_id, category_name, category_description, category_type, is_active 
        FROM categories
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = []
    for row in rows:
        db_value = row[3]
        display_value = type_map.get(db_value, db_value)
        result.append({
            "id" : row[0],
            "nome" : row[1],
            "descrição": row[2],
            "tipo": display_value,
            "ativo" : row[4]
        })

    return result

@app.post("/categories")
def post_category(category: Category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO categories (category_name, category_description, category_type, is_active)
        values (%s, %s, %s, %s)
    """,(category.name, category.description, category.type, category.active))
    conn.commit()
    conn.close()
    cur.close()
    return {"message": "Categoria criado com sucesso"}

@app.put("/categories/{category_id}")
def put_category(category_id: int, category: Category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE categories
        SET category_name = %s,
        category_description = %s,
        category_type = %s,
        is_active = %s
        WHERE category_id = %s
    """, (category.name, category.description, category.type, category.active, category_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Categoria atualizada com sucesso"}

@app.patch("/categories/{category_id}")
def patch_category(category_id: int, category: CategoryPatch):
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []

    if category.name is not None:
        fields.append("category_name = %s")
        values.append(category.name)

    if category.description is not None:
        fields.append("category_description = %s")
        values.append(category.description)

    if category.type is not None:
        fields.append("category_type = %s")
        values.append(category.type)

    if category.active is not None:
        fields.append("is_active = %s")
        values.append(category.active)

    if not fields:
        return {"message": "Sem campos para atualizar!"}

    query = f"""
        UPDATE categories
        SET {', '.join(fields)}
        WHERE category_id = %s
    """

    values.append(category_id)
    cur.execute(query, tuple(values))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Categoria atualizada com sucesso"}

@app.delete("/categories/{category_id}")
def delete_category(category_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM categories
        WHERE category_id = %s
    """, (category_id, ))
    conn.commit()
    cur.close()
    conn.close()
    if cur.rowcount == 0:
        return {"message": "Categoria não encontrada!"}
    return {"messsage": "Categoria deletada com sucesso"}