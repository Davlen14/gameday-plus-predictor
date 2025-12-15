"""
Multi-coach API server backed by instance/coaches_master.db
Usage:
    python serve_coaches_api.py

Endpoints:
    GET /api/coaches               -> list coach names
    GET /api/coach/<name>          -> coach summary (record, stints, signature wins, close games, avg margin)
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pathlib import Path
from datetime import datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
CORS(app)

instance_dir = Path(__file__).parent / "instance"
db_path = instance_dir / "coaches_master.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


class Coach(db.Model):
    __tablename__ = "coaches"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    current_school: Mapped[str] = mapped_column(String(100))
    headshot_url: Mapped[str] = mapped_column(Text, nullable=True)
    career_record: Mapped[str] = mapped_column(String(20))
    career_win_pct: Mapped[float] = mapped_column(Float)
    total_games: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    games = relationship("Game", back_populates="coach")
    stints = relationship("Stint", back_populates="coach")


class Stint(db.Model):
    __tablename__ = "stints"
    id: Mapped[int] = mapped_column(primary_key=True)
    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id"))
    school: Mapped[str] = mapped_column(String(100))
    start_year: Mapped[int] = mapped_column(Integer)
    end_year: Mapped[int] = mapped_column(Integer)
    record: Mapped[str] = mapped_column(String(20))
    win_pct: Mapped[float] = mapped_column(Float, nullable=True)
    games_coached: Mapped[int] = mapped_column(Integer, nullable=True)

    coach = relationship("Coach", back_populates="stints")


class Game(db.Model):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id"))
    cfbd_id: Mapped[int] = mapped_column(Integer, nullable=True)
    season: Mapped[int] = mapped_column(Integer, nullable=False)
    week: Mapped[int] = mapped_column(Integer, nullable=False)
    season_type: Mapped[str] = mapped_column(String(20), nullable=True)
    school: Mapped[str] = mapped_column(String(100), nullable=False)
    opponent: Mapped[str] = mapped_column(String(100), nullable=False)
    opponent_logo: Mapped[str] = mapped_column(Text, nullable=True)
    result: Mapped[str] = mapped_column(String(1), nullable=False)
    coach_score: Mapped[int] = mapped_column(Integer, nullable=False)
    opponent_score: Mapped[int] = mapped_column(Integer, nullable=False)
    opponent_sp_overall: Mapped[float] = mapped_column(Float, nullable=True)
    opponent_sp_offense: Mapped[float] = mapped_column(Float, nullable=True)
    opponent_sp_defense: Mapped[float] = mapped_column(Float, nullable=True)
    opponent_fpi: Mapped[float] = mapped_column(Float, nullable=True)
    opponent_srs: Mapped[float] = mapped_column(Float, nullable=True)
    excitement_index: Mapped[float] = mapped_column(Float, nullable=True)
    is_home: Mapped[bool] = mapped_column(Boolean, default=False)
    is_neutral: Mapped[bool] = mapped_column(Boolean, default=False)
    is_conference: Mapped[bool] = mapped_column(Boolean, default=False)
    is_signature: Mapped[bool] = mapped_column(Boolean, default=False)

    coach = relationship("Coach", back_populates="games")


def compute_signature_wins(coach_id: int):
    # Signature if flagged OR opponent SP+ >=15 with a win
    wins = db.session.query(Game).filter(
        Game.coach_id == coach_id,
        Game.result == "W",
        (Game.is_signature == True) | (Game.opponent_sp_overall >= 15)
    ).order_by(Game.opponent_sp_overall.desc().nullslast()).all()
    output = []
    for g in wins:
        output.append({
            "season": g.season,
            "week": g.week,
            "opponent": g.opponent,
            "score": f"{g.coach_score}-{g.opponent_score}",
            "stage": "postseason" if g.season_type == "postseason" else "regular",
            "opp_sp": g.opponent_sp_overall
        })
    return output


def compute_close_record(coach_id: int, margin: int = 7):
    games = db.session.query(Game).filter(Game.coach_id == coach_id).all()
    wins = losses = 0
    for g in games:
        if abs(g.coach_score - g.opponent_score) <= margin:
            if g.result == "W":
                wins += 1
            else:
                losses += 1
    return wins, losses


def average_margin(coach_id: int):
    res = db.session.query(
        func.avg(Game.coach_score - Game.opponent_score)
    ).filter(Game.coach_id == coach_id).scalar()
    return round(res, 1) if res is not None else None


@app.route("/api/coaches", methods=["GET"])
def list_coaches():
    with app.app_context():
        coaches = db.session.query(Coach).order_by(Coach.name).all()
        return jsonify([c.name for c in coaches])


@app.route("/api/coach/<name>", methods=["GET"])
def get_coach(name: str):
    with app.app_context():
        coach = db.session.query(Coach).filter(func.lower(Coach.name) == name.lower()).first()
        if not coach:
            return jsonify({"error": "not found"}), 404

        sig_wins = compute_signature_wins(coach.id)
        close_w, close_l = compute_close_record(coach.id)
        avg_margin = average_margin(coach.id)

        resp = {
            "metadata": {
                "coach": coach.name,
                "headshot": coach.headshot_url,
                "schools": [s.school for s in coach.stints],
                "generated": coach.created_at.isoformat() if coach.created_at else None
            },
            "career_summary": {
                "record": coach.career_record,
                "win_pct": coach.career_win_pct,
                "games": coach.total_games
            },
            "stints": [
                {
                    "school": s.school,
                    "start_year": s.start_year,
                    "end_year": s.end_year,
                    "record": s.record,
                    "win_pct": s.win_pct,
                    "games": s.games_coached
                } for s in coach.stints
            ],
            "analytics": {
                "signature_wins": sig_wins,
                "close_games": {"wins": close_w, "losses": close_l},
                "avg_margin": avg_margin
            }
        }
        return jsonify(resp)


@app.route("/api/health", methods=["GET"])
def health():
    ok = db_path.exists()
    return jsonify({"status": "ok" if ok else "missing_db", "db": str(db_path)})


if __name__ == "__main__":
    print("=" * 80)
    print("MULTI-COACH API SERVER")
    print("=" * 80)
    print(f"DB: {db_path}")
    print("Endpoints:")
    print("  GET /api/coaches")
    print("  GET /api/coach/<name>")
    print("  GET /api/health")
    print("=" * 80)
    app.run(debug=True, port=5002)
