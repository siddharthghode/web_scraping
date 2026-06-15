from flask import Flask, render_template, jsonify
from database.mongo import MongoDBClient
from collections import defaultdict

app = Flask(__name__)


def get_grouped_books():
    db = MongoDBClient()
    books = list(db.collection.find({}, {"_id": 0})) if db.client else []
    db.close()
    grouped = defaultdict(list)
    for book in books:
        grouped[book.get("source", "Unknown")].append(book)
    return books, grouped


@app.route("/")
def index():
    books, grouped = get_grouped_books()
    return render_template("index.html", books=books, grouped=grouped)


@app.route("/api/stats")
def stats():
    books, grouped = get_grouped_books()
    return jsonify({
        "total": len(books),
        "sources": len(grouped),
        "in_stock": sum(1 for b in books if b.get("availability") is True),
        "by_source": {
            src: {"count": len(bks), "in_stock": sum(1 for b in bks if b.get("availability") is True)}
            for src, bks in grouped.items()
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
