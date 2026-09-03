CSR Bridge: Connecting Companies and NGOs for Greater Impact
Every year, millions in Corporate Social Responsibility (CSR) funds go unused or are heavily concentrated in just a few top-tier cities. Meanwhile, grassroots NGOs doing incredible work struggle to find the right corporate backers.

We built CSR Bridge during this hackathon to fix that.

It is a clean, centralized platform that acts as a matchmaker between companies looking to fund meaningful projects and NGOs seeking financial support. Instead of endless cold emails, NGOs can directly find companies with matching budgets and interests, and companies can pool their resources to fund massive projects together.

How It Works:

The platform is split into two straightforward experiences:

1. The NGO Experience
When an NGO lands on the site, they fill out a quick funding request. They provide their verified details, the project domain (e.g., Women Empowerment, Healthcare, Construction), a brief description, and their estimated budget ask.
The Magic: Once submitted, the platform instantly shows them a curated list of companies interested in their specific domain. Even better, it filters for companies whose available CSR budget exactly matches—or is just slightly short of (by 50k to 1 Lakh)—their asking amount. The NGO can then send targeted proposals in just a few clicks.

2. The Corporate Dashboard
When a company logs in, they are greeted by a minimalistic dashboard showing all the proposals they’ve received.
The Priority Algorithm: We specifically sort these proposals so that under-acknowledged and underdeveloped regions are pushed to the top. Companies that fund these priority projects are rewarded with a higher Social Impact Score (SIS)—a badge of pride displayed next to their name on the platform.

The Collaboration Engine
Sometimes, an NGO needs more money than a single company can provide.
If an NGO checks the "Open to Collaborative Funds" box, their project enters a special pool. If a mid-level company likes the project but doesn't have the full budget, they can pledge a partial amount. This opens a collaboration deal. Once 2, 3, or 4 companies chip in to hit the target budget, the deal is finalized, and the SIS score is shared among them.
Until a collaborative deal reaches 100% funding, any single "whale" company with a massive budget can swoop in, accept the proposal single-handedly, and take the entire deal (and the SIS score) for themselves!

Under the Hood:
To keep the architecture lightning-fast and easy to set up for this hackathon, we built the entire stack in Python.
Backend: Powered by FastAPI to handle all the routing, matching algorithms, and collaboration logic.
Frontend: A clean, elegant, and completely white-labeled web interface. (We kept the UI strictly professional—no default framework watermarks or "powered by" badges).
Database: We bypassed heavy SQL setups and used a lightweight CSV-based database system.

Our Data Structure:
We maintain four core CSV files to act as our relational database:

companies.csv - Stores registered companies, their current CSR budget in lakhs, target domains, and their accumulated Social Impact Score.
ngos.csv - Holds registered NGOs, their verified details, and years of service.
collaborations.csv - The active holding pool for high-budget projects waiting for multiple companies to team up and hit the funding goal.
deals.csv - The ledger of success. Once a proposal is accepted (either solo or fully collaborated), it moves here as a finalized deal.

How to Run Locally...
Clone the repository.

Install the required Python packages:
Bash
pip install fastapi uvicorn pandas streamlit

Start the FastAPI backend server:
Bash
uvicorn backend_app:app --reload

In a new terminal, launch the frontend:
Bash
streamlit run frontend_app.py
