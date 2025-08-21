from fastapi import FastAPI, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from linkedin_agent.db import Base, engine, SessionLocal
from linkedin_agent.models import Post
from linkedin_agent.ai_gen import generate_post
from linkedin_agent.linkedin import post_to_linkedin
from linkedin_agent.settings import Settings

app = FastAPI()
app.mount("/static", StaticFiles(directory="linkedin_agent/static"), name="static")
templates = Jinja2Templates(directory="linkedin_agent/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

# Ensure a settings row exists
def get_or_create_settings(db):
    settings = db.query(Settings).first()
    if not settings:
        settings = Settings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings
@app.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, db: Session = Depends(get_db)):
    settings = get_or_create_settings(db)
    return templates.TemplateResponse("settings.html", {"request": request, "settings": settings})

@app.post("/settings")
def update_settings(request: Request, db: Session = Depends(get_db),
                   title: str = Form(...), handle: str = Form(...), website: str = Form(...),
                   enable_promotion: str = Form(None), enable_auto_comment_own: str = Form(None), enable_comment_other: str = Form(None)):
    settings = get_or_create_settings(db)
    settings.title = title
    settings.handle = handle
    settings.website = website
    settings.enable_promotion = bool(enable_promotion)
    settings.enable_auto_comment_own = bool(enable_auto_comment_own)
    settings.enable_comment_other = bool(enable_comment_other)
    db.commit()
    return RedirectResponse("/settings", status_code=303)


from apscheduler.schedulers.background import BackgroundScheduler
import datetime

# APScheduler setup
def post_scheduled():
    db = SessionLocal()
    now = datetime.datetime.now()
    scheduled_posts = db.query(Post).filter(Post.status == "scheduled", Post.scheduled_time <= now).all()
    for post in scheduled_posts:
        result = post_to_linkedin(post.content)
        post.status = "posted"
        post.linkedin_url = str(result)
        db.commit()
    db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(post_scheduled, 'interval', seconds=60)
scheduler.start()

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).order_by(Post.id.desc()).all()  # Recent first
    return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})
# CSV export endpoint
import csv
from fastapi.responses import StreamingResponse

@app.post("/export_csv")
def export_csv():
    session = SessionLocal()
    posts = session.query(Post).order_by(Post.id.desc()).all()
    session.close()
    def iter_csv():
        header = ["id", "content", "image_url", "status", "scheduled_time", "linkedin_url"]
        yield ",".join(header) + "\n"
        for post in posts:
            row = [
                str(post.id),
                '"' + post.content.replace('"', '""') + '"',
                post.image_url or "",
                post.status,
                str(post.scheduled_time) if post.scheduled_time else "",
                post.linkedin_url or ""
            ]
            yield ",".join(row) + "\n"
    return StreamingResponse(iter_csv(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=posts.csv"})

@app.post("/generate")
def generate(
    db: Session = Depends(get_db),
    topic: str = Form(...),
    image: UploadFile = File(None),
    image_option: str = Form("none"),
    enable_schedule: str = Form(None),
    scheduled_time: str = Form(None)
):
    import datetime
    from linkedin_agent.settings import Settings
    settings = db.query(Settings).first()
    # Personalize and enhance post
    hashtags = "#AI #Agentic #Innovation #LinkedIn #Linky"
    promo = f"\nIf you want your business to be scaled, contact here or DM. {settings.website}" if settings and settings.enable_promotion else ""
    signature = f"\n{settings.title} {settings.handle}" if settings else ""
    prompt = f"Write a short, engaging LinkedIn post about {topic}. Make it sound natural, add some hashtags, and do not mention AI or model."
    content = generate_post(prompt) + f"\n{hashtags}{promo}{signature}"
    image_url = None
    if image_option == "manual" and image and image.filename:
        image_path = f"linkedin_agent/static/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(image.file.read())
        image_url = f"/static/{image.filename}"
    elif image_option == "auto":
        # Placeholder for AI image generation (DALL·E, etc.)
        image_url = "/static/auto_image_placeholder.png"
    scheduled_dt = None
    if enable_schedule and scheduled_time:
        try:
            scheduled_dt = datetime.datetime.fromisoformat(scheduled_time)
        except Exception:
            scheduled_dt = None
    status = "scheduled" if scheduled_dt else "draft"
    post = Post(content=content, status=status, image_url=image_url, scheduled_time=scheduled_dt)
    db.add(post)
    db.commit()
    db.refresh(post)
    return RedirectResponse("/", status_code=303)
@app.post("/approve/{post_id}")
def approve(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if post:
        # If scheduled, check if time has arrived
        import datetime
        if post.scheduled_time and post.scheduled_time > datetime.datetime.now():
            post.status = "scheduled"
            db.commit()
            return RedirectResponse("/", status_code=303)
        # Directly post to LinkedIn on approval or if scheduled time has arrived
        result = post_to_linkedin(post.content)
        post.status = "posted"
        post.linkedin_url = str(result)
        db.commit()
    return RedirectResponse("/", status_code=303)

@app.post("/reject/{post_id}")
def reject(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).get(post_id)
    if post:
        post.status = "rejected"
        db.commit()
    return RedirectResponse("/", status_code=303)

