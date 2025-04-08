from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Optional, Annotated

class PaginationParams(BaseModel):
    page: Annotated[Optional[int], Query(1, description="Номер страницы", gt=0)]
    per_page: Annotated[Optional[int], Query(3, description="Число отелей на странице", gt=0, lt=21)]

PaginationDep = Annotated[PaginationParams, Depends()]