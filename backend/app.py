from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from models import Article
from data import ARTICLES

app = FastAPI()

# Allow local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/articles", response_model=List[Article])
def list_articles(featured: Optional[str] = Query(None)):
    articles = ARTICLES

    if featured:
        # Intended: return only featured when featured == "true",
        # and only non-featured when featured == "false".
        if featured.lower() == "true":
            articles = [a for a in articles if a.is_featured]
        elif featured.lower() == "false":
            articles = [a for a in articles if not a.is_featured]
        else:
            # unexpected value, just return all
            pass

    return articles


@app.get("/api/articles/{article_id}", response_model=Article)
def get_article(article_id: int):
    # Find the article where the ID matches
    article = next((a for a in ARTICLES if a.id == article_id), None)

    # If not found, raise 404
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.post("/api/articles", response_model=Article, status_code=201)
def create_article(article: Article):
    # Check for existing ID to resolve test_create_article_generates_unique_id
    if any(a.id == article.id for a in ARTICLES):
        raise HTTPException(status_code=400, detail="Article with this ID already exists")
    
    ARTICLES.append(article)
    return article
