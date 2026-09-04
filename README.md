# CSR Bridge: Connecting Companies and NGOs for Greater Impact

Every year, millions in Corporate Social Responsibility (CSR) funds go unused or remain heavily concentrated in top-tier cities, while grassroots NGOs struggle to find corporate backers. CSR Bridge is a centralized matchmaker built to bridge this gap. Instead of cold emails, NGOs find companies with matching budgets and interests, and companies can pool resources to fund large-scale projects.

## Core Features

### 1. The NGO Experience

NGOs submit a funding request detailing their verified credentials, project domain (e.g., Women Empowerment, Healthcare), and budget.

* **Smart Matching:** The platform instantly curates a list of companies interested in that specific domain.
* **Budget Alignment:** Filters prioritize companies whose available CSR budget exactly matches or is within 50k–1 Lakh of the requested amount, allowing NGOs to send targeted proposals instantly.

### 2. The Corporate Dashboard

Companies access a minimalistic dashboard displaying incoming proposals.

* **Priority Algorithm:** Proposals from under-acknowledged and underdeveloped regions are automatically sorted to the top.
* **Social Impact Score (SIS):** Companies funding priority projects are rewarded with a higher SIS, displayed prominently as a badge on the platform.

### 3. The Collaboration Engine

For projects exceeding a single company's budget, NGOs can opt into "Collaborative Funds."

* **Partial Pledges:** Mid-level companies can pledge partial amounts to open a collaboration deal.
* **Goal Reached:** Once multiple companies hit the target budget, the deal finalizes and the SIS is shared among them.
* **Whale Buyouts:** Until a collaborative deal is 100% funded, a single high-budget company can swoop in, fully fund the proposal, and claim the entire deal and SIS.

## Tech Stack & Architecture

Built entirely in Python for a lightweight, hackathon-friendly architecture.

* **Backend:** FastAPI handles routing, matching algorithms, and collaboration logic.
* **Frontend:** Streamlit provides a clean, white-labeled web interface.
* **Database:** A lightweight, relational CSV-based system bypassing heavy SQL setups.

### Data Structure

* `companies.csv`: Registered companies, available CSR budget (in lakhs), target domains, and accumulated SIS.
* `ngos.csv`: Registered NGOs, verified details, and years of service.
* `collaborations.csv`: Active holding pool for high-budget projects awaiting joint funding.
* `deals.csv`: Finalized ledger of accepted proposals (solo or collaborative).


### VISIT OUR REPO

* [Check it out](https://github.com/Bhavesh07-jain/Novice_Squad_MIC/edit/main/README.md)


## Local Setup Instructions

1. **Clone the repository and navigate to the directory:**
```bash
git clone https://github.com/Bhavesh07-jain/Novice_Squad_MIC/edit/main/README.md
cd <repo-folder-name>
```


2. **Install the required dependencies:**
```bash
pip install fastapi uvicorn pandas streamlit
```


3. **Start the FastAPI backend server:**
```bash
uvicorn backend_app:app --reload
```


4. **Launch the frontend in a new terminal:**
```bash
streamlit run frontend_app.py
```
