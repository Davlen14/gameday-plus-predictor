# 🤖 n8n Workflow - Gameday+ Architecture (Step-by-Step)

## PART 1: USER TO FLASK API (Frontend Flow)

**Create these nodes in order:**

1. **Start Node** - "User Browser"
   - Type: Manual trigger
   - Label: "User selects teams"

2. **Node** - "React Frontend"
   - Type: HTTP Request
   - Method: POST
   - URL: http://localhost:5173
   - Description: "App.tsx sends prediction request"

3. **Node** - "Flask API Endpoint" 
   - Type: Webhook
   - URL: http://localhost:5002/predict
   - Method: POST
   - Data: `{home_team, away_team}`

**Connect:** Start → React → Flask

---

## PART 2: FLASK SPLITS INTO 3 BRANCHES

**Create split node:**

4. **Split Node** - "Prediction Processing Hub"
   - Type: Switch/Router
   - Branches: 3 parallel paths

**Branch 1 - Core Engine:**
5. **Node** - "LightningPredictor"
   - File: graphqlpredictor.py
   - Action: Fetch GraphQL data

**Branch 2 - Betting Data:**
6. **Node** - "BettingLinesManager"  
   - File: betting_lines_manager.py
   - Action: Get sportsbook lines

**Branch 3 - Static Data:**
7. **Node** - "Load JSON Files"
   - Files: fbs.json, Coaches.json
   - Action: Read team/coach data

**Connect:** Flask → Split → All 3 branches

---

## PART 3: GRAPHQL API CALLS (10-15 parallel)

**Inside Branch 1, add these parallel nodes:**

8. **HTTP Node** - "Team Stats Query"
9. **HTTP Node** - "Player Stats Query"
10. **HTTP Node** - "Game Lines Query"
11. **HTTP Node** - "Rankings Query"
12. **HTTP Node** - "Weather Query"
13. **HTTP Node** - "Coaching Query"

**All point to:** https://graphql.collegefootballdata.com

**Merge Node:**
14. **Merge** - "Combine GraphQL Results"

---

## PART 4: DATA AGGREGATION

15. **Node** - "Data Aggregation"
    - Type: Code/Function
    - Action: Combine all 3 branches
    - Output: 18 UI component sections

16. **Node** - "Format JSON Response"
    - Creates: ui_components object
    - Includes: betting_analysis with individual_books

---

## PART 5: RETURN TO FRONTEND

17. **Node** - "Flask Returns JSON"
    - HTTP Response
    - Time: 20-35 seconds

18. **Node** - "React Updates State"
    - Action: setPredictionData()

19. **Node** - "Render 24 Components"
    - Components: MarketComparison, PredictionCards, etc.

20. **End Node** - "User Views Analysis"

---

## VISUAL SETTINGS

**Colors:**
- Blue: Frontend nodes
- Green: Backend nodes  
- Orange: External API nodes
- Purple: Data merge nodes

**Shapes:**
- Rectangles: User/Frontend
- Hexagons: Processing
- Clouds: API calls
- Cylinders: Data storage

**Arrows:**
- Solid: Main flow
- Dashed: Parallel branches
- Thick: Critical path (GraphQL queries)
