"""Dynamic SQL query builder"""
from typing import Any, Dict, List, Optional

class QueryBuilder:
    def __init__(self, table: str):
        self.table = table
        self._select = ["*"]
        self._where = []
        self._order_by = []
        self._limit = None
    
    def select(self, *cols: str):
        self._select = list(cols) if cols else ["*"]
        return self
    
    def where(self, condition: str):
        self._where.append(condition)
        return self
    
    def order_by(self, col: str, direction: str = "ASC"):
        self._order_by.append(f"{col} {direction}")
        return self
    
    def limit(self, n: int):
        self._limit = n
        return self
    
    def build(self) -> str:
        query = f"SELECT {', '.join(self._select)} FROM {self.table}"
        if self._where:
            query += " WHERE " + " AND ".join(self._where)
        if self._order_by:
            query += " ORDER BY " + ", ".join(self._order_by)
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query

def test():
    qb = QueryBuilder("users")
    query = qb.select("id", "name", "email").where("age > 18").order_by("name").limit(10).build()
    print(query)

if __name__ == "__main__":
    test()
