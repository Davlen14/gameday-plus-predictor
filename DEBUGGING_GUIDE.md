# Gameday+ Project: The Permanent Debugging Guide

This guide explains the single root cause of the most common and frustrating errors in this project. Follow the checklist to ensure a smooth startup every time.

---

## 🤯 The Core Problem: Data Dependency

The entire application, from the Python backend to the React frontend, is **completely dependent on one thing: having the correct data file for the correct week.**

When this one condition isn't met, the system doesn't just fail; it fails in a series of confusing and misleading ways:

1.  **Backend Crash (`TypeError`):** The server crashes when trying to format betting lines that don't exist (`None` values).
2.  **Frontend Shows Fake Data:** The UI is designed to be resilient. When it doesn't receive real sportsbook data, it falls back to displaying a **hardcoded, fake list of sportsbooks** (Bovada, ESPN Bet, DraftKings) with "N/A" values. This is the most confusing part, as it makes it seem like the API is working but the data is just empty.
3.  **Misleading Logs:** The backend log often shows a `"POST /predict HTTP/1.1" 200 -` (OK) status, hiding the fact that the data formatting part of the request failed.

You get stuck in a loop of fixing one symptom, only for another to appear, because the root cause—the data file—wasn't correct.

---

## ✅ The Permanent Solution: Your Pre-Launch Checklist

To prevent this from ever happening again, follow this checklist **every single time** you work on the project.

### **The Golden Rule: Data First.**
*The application code is fine. The problem is almost always the data.* Before you run `./start-fullstack.sh`, you must ensure the data is correct.

### **Pre-Flight Checklist:**

**1. What is the current week?**
   - Example: It's **Week 15**.

**2. Does the betting lines file exist?**
   - Check your project directory for `week15.json`.
   - If it doesn't exist, you **must** create it.

**3. Does the file contain betting lines?**
   - Open `week15.json`. It **must** contain the `"lines"` array with data from sportsbooks.
   - If it's missing, the UI will show "N/A".
   - **Action:** Use this `curl` command to fetch the lines and create the file. (Change the week number as needed).
     ```bash
     curl -s "https://api.collegefootballdata.com/lines?year=2025&week=15&seasonType=regular" \
       -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
       -o week15.json
     
     echo "✅ Created week15.json with real betting lines."
     ```

   - **GraphQL Alternative:** If you prefer GraphQL, use this command. It is more complex but allows you to select specific fields.
     ```bash
     curl -X POST https://graphql.collegefootballdata.com/v1/graphql \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p" \
       -d '{"query":"query { game(where: {season: {_eq: 2025}, week: {_eq: 15}}) { id homeTeam awayTeam lines { provider { name } spread overUnder } } }"}' \
       -o week15_graphql.json
     
     echo "✅ Created week15_graphql.json with real betting lines."
     ```

**4. Is the code pointing to the right file?**
   - Open `betting_lines_manager.py`.
   - Look at this line (around line 14):
     ```python
     def __init__(self, lines_file: str = "week15.json", ...):
     ```
   - Make sure the `lines_file` default value matches the current week (e.g., `"week15.json"`).

---

### **Troubleshooting Guide**

If you see an error, use this guide to find the *real* problem instantly.

| If you see this error... | The *actual* problem is... | How to fix it... |
| :--- | :--- | :--- |
| **`TypeError: unsupported format string`** in logs | The JSON file is missing the `"lines"` array for a game. | Run the `curl` command from the checklist to get a new file with lines. |
| **`FileNotFoundError: week<N>.json`** in logs | The `betting_lines_manager.py` is pointing to a file that doesn't exist. | 1. Create the missing file. <br> 2. Or, update the `lines_file` in `betting_lines_manager.py` to a file you have. |
| **"N/A" for spreads in the UI** | The API worked, but the JSON file has no betting lines for that specific game. | Your data file is incomplete. Run the `curl` command to get fresh data. |
| **Server crashes on startup** | Almost certainly a data file issue. | Check `logs/backend.log` for a `FileNotFoundError` or `TypeError` and follow the steps above. |
