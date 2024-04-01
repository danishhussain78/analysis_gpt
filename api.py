from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import JSONResponse
import os
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from schema import get_summery_schema,sales_data_by_employee,sales_data_by_time

app = FastAPI()


os.environ["OPENAI_API_KEY"]="write your api key"

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
engine=create_engine("sqlite:///sales_analysis.db")
db = SQLDatabase(engine=engine)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)


@app.get("/get_summery")
async def get_summery():
    response=agent_executor.invoke({"input": "make summery of prodvided sale data", "context": "sales_analysis"})
    return JSONResponse(content=response)


@app.post("/chat_with_data/")
async def chat_with_data(question:get_summery_schema):
    response=agent_executor.invoke({"input": question.question, "context": "sales_analysis"})
    return JSONResponse(content=response)


@app.post("/sales_data_by_employee")
async def get_sales_data_by_employee(data:sales_data_by_employee):
    response=agent_executor.invoke({"input": f"generate employee progress summery from sale_analysis, employee id is {data.employee_id}", "context": "sales_analysis"})
    return JSONResponse(content=response)

@app.post("/sales_data_by_time")
async def get_sales_data_by_time(data:sales_data_by_time):
    response=agent_executor.invoke({"input": f"generate sales analysis summery from {data.start_date} to {data.end_date}", "context": "sales_analysis"})
    return JSONResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8080)