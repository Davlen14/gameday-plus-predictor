"""
Flask API to serve Matt Campbell data from SQLite database to Matt.html
=========================================================================
This creates a local API endpoint that Matt.html can fetch from instead of
using hardcoded JSON data.

Usage:
    python3 serve_campbell_api.py
    Then open Matt.html in browser (it will fetch from http://localhost:5001/api/campbell)
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, Boolean, Text, DateTime
from datetime import datetime

# =============================================================================
# DATABASE SETUP (Same schema as ingestion script)
# =============================================================================

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
CORS(app)  # Enable CORS for local development

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campbell_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# =============================================================================
# MODELS (Same as ingest script)
# =============================================================================

class Coach(db.Model):
    __tablename__ = 'coaches'
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
    draft_picks = relationship("DraftPick", back_populates="coach")
    rankings = relationship("Ranking", back_populates="coach")


class Stint(db.Model):
    __tablename__ = 'stints'
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
    __tablename__ = 'games'
    id: Mapped[int] = mapped_column(primary_key=True)
    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id"))
    season: Mapped[int] = mapped_column(Integer)
    week: Mapped[int] = mapped_column(Integer)
    season_type: Mapped[str] = mapped_column(String(20), nullable=True)
    school: Mapped[str] = mapped_column(String(100))
    opponent: Mapped[str] = mapped_column(String(100))
    opponent_logo: Mapped[str] = mapped_column(Text, nullable=True)
    result: Mapped[str] = mapped_column(String(1))
    coach_score: Mapped[int] = mapped_column(Integer)
    opponent_score: Mapped[int] = mapped_column(Integer)
    opponent_sp_overall: Mapped[float] = mapped_column(Float, nullable=True)
    opponent_sp_offense: Mapped[float] = mapped_column(Float, nullable=True)
    opponent_sp_defense: Mapped[float] = mapped_column(Float, nullable=True)
    opponent_fpi: Mapped[float] = mapped_column(Float, nullable=True)
    opponent_srs: Mapped[float] = mapped_column(Float, nullable=True)
    excitement_index: Mapped[float] = mapped_column(Float, nullable=True)
    is_home: Mapped[bool] = mapped_column(Boolean)
    is_neutral: Mapped[bool] = mapped_column(Boolean)
    is_conference: Mapped[bool] = mapped_column(Boolean)
    is_signature: Mapped[bool] = mapped_column(Boolean)

    coach = relationship("Coach", back_populates="games")


class DraftPick(db.Model):
    __tablename__ = 'draft_picks'
    id: Mapped[int] = mapped_column(primary_key=True)
    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id"))
    player_name: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)
    round: Mapped[int] = mapped_column(Integer)
    pick: Mapped[int] = mapped_column(Integer, nullable=True)
    nfl_team: Mapped[str] = mapped_column(String(100))
    college_school: Mapped[str] = mapped_column(String(100), nullable=True)
    position: Mapped[str] = mapped_column(String(10), nullable=True)

    coach = relationship("Coach", back_populates="draft_picks")


class Ranking(db.Model):
    __tablename__ = 'rankings'
    id: Mapped[int] = mapped_column(primary_key=True)
    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id"))
    season: Mapped[int] = mapped_column(Integer)
    week: Mapped[int] = mapped_column(Integer)
    rank: Mapped[int] = mapped_column(Integer)
    school: Mapped[str] = mapped_column(String(100))

    coach = relationship("Coach", back_populates="rankings")


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route('/api/campbell', methods=['GET'])
def get_campbell_data():
    """
    Returns Matt Campbell data in the EXACT format that Matt.html expects.
    This matches the fullData structure in the HTML file.
    """
    with app.app_context():
        coach = db.session.query(Coach).filter_by(name="Matt Campbell").first()

        if not coach:
            return jsonify({"error": "Matt Campbell not found in database"}), 404

        # Build games array
        games = []
        for g in coach.games:
            # Reconstruct homeTeam/awayTeam from stored data
            if g.is_home:
                home_team = g.school
                away_team = g.opponent
                home_points = g.coach_score
                away_points = g.opponent_score
                away_logo = g.opponent_logo
                home_logo = None  # Could store this if needed
                away_sp = g.opponent_sp_overall
                home_sp = None
            else:
                home_team = g.opponent
                away_team = g.school
                home_points = g.opponent_score
                away_points = g.coach_score
                home_logo = g.opponent_logo
                away_logo = None
                home_sp = g.opponent_sp_overall
                away_sp = None

            game_obj = {
                "id": g.id,
                "season": g.season,
                "week": g.week,
                "seasonType": g.season_type or "regular",
                "homeTeam": home_team,
                "awayTeam": away_team,
                "homePoints": home_points,
                "awayPoints": away_points,
                "homeLogo": [home_logo] if home_logo else [],
                "awayLogo": [away_logo] if away_logo else [],
                "homeSPOverall": home_sp,
                "awaySPOverall": away_sp,
                "excitement": g.excitement_index
            }
            games.append(game_obj)

        # Build signature wins
        signature_wins = []
        sig_games = db.session.query(Game).filter_by(
            coach_id=coach.id,
            is_signature=True
        ).order_by(Game.opponent_sp_overall.desc()).all()

        for sg in sig_games:
            signature_wins.append({
                "season": sg.season,
                "week": sg.week,
                "opponent": sg.opponent,
                "score": f"{sg.coach_score}-{sg.opponent_score}",
                "opp_sp": sg.opponent_sp_overall
            })

        # Build team mappings for logos
        team_mappings = {}
        unique_opponents = db.session.query(Game.opponent, Game.opponent_logo).filter_by(
            coach_id=coach.id
        ).distinct().all()

        for opp, logo in unique_opponents:
            if opp and logo:
                team_mappings[opp] = {
                    "logo": logo,
                    "colors": ["#000000", "#FFFFFF"]  # Default colors
                }

        # Build response matching Matt.html structure
        response = {
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
                }
                for s in coach.stints
            ],
            "games": games,
            "analytics": {
                "signature_wins": signature_wins,
                "team_mappings": team_mappings
            }
        }

        return jsonify(response)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "database": "connected"})


# =============================================================================
# RUN SERVER
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("MATT CAMPBELL API SERVER")
    print("=" * 80)
    print(f"🚀 Server starting on http://localhost:5001")
    print(f"📊 API endpoint: http://localhost:5001/api/campbell")
    print(f"🏥 Health check: http://localhost:5001/api/health")
    print()
    print("To test:")
    print("  curl http://localhost:5001/api/campbell | jq")
    print()
    print("Next: Update Matt.html to fetch from this endpoint instead of hardcoded data")
    print("=" * 80)

    app.run(debug=True, port=5001)
