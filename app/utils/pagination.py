from typing import Type, List, Tuple
from sqlalchemy.orm import Query
from sqlalchemy import or_
import math

def paginate_query(query: Query, model: Type, params, search_fields: List[str]) -> Tuple:
    if params.search and search_fields:
        filters = [getattr(model, field).ilike(f"%{params.search}%") for field in search_fields]
        query = query.filter(or_(*filters))
    total_items = query.order_by(None).count()
    total_pages = math.ceil(total_items / params.size) if params.size else 1
    items = query.order_by(model.id).offset((params.page - 1) * params.size).limit(params.size).all()
    return total_items, total_pages, params.page, items