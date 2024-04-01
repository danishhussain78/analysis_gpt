from pydantic import BaseModel

class get_summery_schema(BaseModel):
    question:str="who get the highest sales in the data"

class sales_data_by_employee(BaseModel):
    employee_id:str

class sales_data_by_time(BaseModel):
    start_date:str="2022-07-26"
    end_date:str="2023-07-26"
