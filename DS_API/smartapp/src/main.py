import uvicorn
from fastapi import FastAPI, Path, Request
from fastapi.responses import JSONResponse

import workflow_runner
from models import Country, Configuration, MyException

app = FastAPI(title='COZY PLACE Data Science Application',
              description='Data Science Application running on FastAPI for scrpaing and data Analysis from COZY PLACE',
              version='0.0.1')

#@app.get("/{index}")
#async def get_result(index: Index = Path(..., title="The name of the Index")
 #                    ):

@app.get("/")
def read_root():
    return {"Data Science app for COZY PLACE": "Choose the country you're looking for"}

@app.get("/{country}")
def get_result(country: str):
    url_scraping = 'http://www.tripadvisor.com'
    config = Configuration(
        country=country #I'm passing this argument from the path that the user use
    )
    try:
        result = workflow_runner.run(config, url_scraping)
        return JSONResponse(status_code=200, content=result)
        print(result)
    except Exception as e:
        #raise MyException(e)
        print(e)

#@app.exception_handler(MyException)
#async def unicorn_exception_handler(request: Request, exc: MyException):
 #   return JSONResponse(
  #      status_code=418,
   #     content={"message": f"Error occurred! Please contact the system admin."},
    #)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)