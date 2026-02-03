from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.responses import RedirectResponse
from starlette import status
app = FastAPI()
count_archive = {"result": 0}
# Указываем, где лежат наши чертежи
templates = Jinja2Templates(directory="templates")
# Подключаем статику (стили, скрипты)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,  "title": "Мой Нуарный Сайт", "result": count_archive["result"]})

@app.post("/increment")
async def add_one():
    result = count_archive["result"]
    # Нажали кнопку — прибавили единицу в словаре
    count_archive["result"] += 1
    
    # Возвращаем юзера на главную, чтобы он увидел обновленную цифру
    return RedirectResponse(url="/", headers={"X-Result": str(result)}, status_code=status.HTTP_303_SEE_OTHER)

if __name__ == "__main__":
    import uvicorn
    # Запускаем мотор
    uvicorn.run(
        "mycode:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True  # Перезагрузка при каждом изменении, чтобы не терять время
    )

