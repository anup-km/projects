import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from address_book import router

app = FastAPI()
app.include_router(router)   # including all the paths to app
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)   # running the uvicorn
# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
