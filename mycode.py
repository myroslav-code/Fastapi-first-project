from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.responses import RedirectResponse
from starlette import status
from pathlib import Path
app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

data = {
    "1": "Привет",
    "2": "Как дела?",
    "3": "До свидания"
}

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,  "title": "Мой Сайт", "data": data})

@app.post("/find")
async def find(request: Request, fruit_id: str = Form(...)):
    # Проверка на вшивость: если длина больше 10 символов — разворачиваем сразу
    if len(fruit_id) > 1:
        result = "Слишком долгий запрос, приятель"
    else:  
        result = data.get(fruit_id, "Ничего не найдено")

    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Поиск фруктов", "search_result": result}
    )
    
if __name__ == "__main__":
    uvicorn.run(
        "mycode:app", 
        host="127.0.0.1", 
        port=8001, 
        reload=True
    )

