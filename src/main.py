from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models import Base, engine, NameEntry, SessionLocal

app = FastAPI()

# Set up the template directory
templates = Jinja2Templates(directory="website/templates")

# Mount the static files directory
app.mount("/static", StaticFiles(directory="website"), name="static")


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to render the form and show last entered name
@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request, db: Session = Depends(get_db)):
    last_entry = db.query(NameEntry).order_by(NameEntry.id.desc()).first()
    last_name = last_entry.name if last_entry else ""
    return templates.TemplateResponse(
        "main.html", {"request": request, "last_name": last_name}
    )


# Endpoint to handle form submission and store name in the database
@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request, name: str = Form(...), db: Session = Depends(get_db)
):
    # Add new name to the database
    new_name = NameEntry(name=name)
    db.add(new_name)
    db.commit()

    # Display the last submitted name
    return templates.TemplateResponse(
        "main.html", {"request": request, "last_name": name}
    )
