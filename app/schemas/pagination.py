from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")

class PaginationParams(BaseModel):
  """
  Pagination parameters for API endpoints.
  """
  page: int = 1
  size: int = 10
  search: Optional[str] = None


class PaginatedResponse(BaseModel, Generic[T]):
  """
  Generic paginated response model that can be used with any data type.
  """
  items: List[T]
  total: int
  page: int
  size: int
  pages: int
  
  class Config:
      from_attributes = True
  