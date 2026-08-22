# Stitch Culture 🧵✨

An AI-powered e-commerce assistant built for **Stitch Culture**, designed to help customers instantly check products, shipping policies, and store details through an interactive chat interface.

* Tech Stack & Architecture
  Frontend: HTML5, CSS3, JavaScript (Vanilla) — Hosted live via **GitHub Pages**.
  Backend: Python, FastAPI, Uvicorn — Deployed as a cloud web service on **Render**.
  AI Engine: Google GenAI SDK (`gemini-3.7-flash`) for real-time natural language responses.
  Data Layer: Pandas for parsing local product data and policies.


* How It Works
1. The User types a question on the frontend interface (e.g., *"What is your return policy?"* or *"Show me hoodies"*).
2. FastAPI Backend  receives the request and searches through local store CSV/text files using basic data retrieval logic.
3. Google Gemini API takes the matched store context, structures a helpful response, and sends it back to the web UI seamlessly.
