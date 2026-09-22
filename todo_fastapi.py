from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from todo_model import TodoList,Task

app = FastAPI(title="To-do app")
templates = Jinja2Templates(directory="templates")
DATA_FILE = "todos.json"
todos = TodoList.load(DATA_FILE)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"todos": todos}
    )
@app.post("/add")
def add(title:str=Form(...)):
    todos.add(title.strip())
    todos.save(DATA_FILE)
    return RedirectResponse("/",status_code=303)

@app.get("/toggle/{i}")
def toggole(i:int):
    todos.tasks[i].mark_done()
    todos.save(DATA_FILE)
    return RedirectResponse("/",status_code=303)

@app.get("/delete/{i}")
def delete(i:int):
    del todos.tasks[i]
    todos.save(DATA_FILE)
    return RedirectResponse("/",status_code=303)


@app.get("/save")
def save():
    todos.save(DATA_FILE)
    return RedirectResponse("/",status_code=303)