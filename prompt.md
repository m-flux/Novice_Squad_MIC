# Hackathon Project Blueprint: CSR & NGO Collaboration Platform

**Target Frameworks:** Python, FastAPI (Backend), Streamlit (Frontend).
**Database:** CSV-based local file storage.
**UI/UX Requirements:** Minimalistic, elegant, white-themed. **CRITICAL:** Hide all Streamlit default branding, menus, footers, and watermarks via custom CSS injection.

---

## 1. File Structure & Database Schema

The backend uses five main CSV files to persist state:

### A. `companies.csv`
Database of eligible companies and their CSR metrics.
- `Company_ID` (String)
- `Name` (String)
- `Budget_Lakhs` (Float) - Current available CSR budget.
- `Interested_Domains` (String) - Comma-separated list (e.g., "Health, Education").
- `SIS_Score` (Integer) - Social Impact Score tracker.

### B. `ngos.csv`
Database of registered NGOs.
- `NGO_ID` (String)
- `Name` (String)
- `Years_Experience` (Integer)
- `Region` (String) - State or district.

### C. `proposals.csv`
Direct funding requests sent from an NGO to specific companies.
- `Proposal_ID` (String)
- `NGO_ID` (String)
- `Target_Company_ID` (String)
- `Title` (String)
- `Description` (Text)
- `Domain` (String)
- `Ask_Lakhs` (Float)
- `Region` (String)
- `Is_Collaborative` (Boolean)
- `Status` (String) - Pending, Accepted, Rejected.

### D. `collaborations.csv`
High-budget requests open to multi-company pooling.
- `Collab_ID` (String)
- `NGO_ID` (String)
- `Title` (String)
- `Description` (Text)
- `Domain` (String)
- `Total_Ask_Lakhs` (Float)
- `Current_Pledged_Lakhs` (Float)
- `Pledged_Companies` (String) - Formatted as `Company_ID:PledgedAmount|Company_ID2:PledgedAmount`
- `Region` (String)
- `Status` (String) - Active, Fulfilled, Cancelled.

### E. `deals.csv`
Finalized successful partnerships (solo or collaborative).
- `Deal_ID` (String)
- `Ref_ID` (String) - ID of the proposal or collab.
- `NGO_ID` (String)
- `Companies_Involved` (String) - Comma-separated company IDs.
- `Total_Amount_Lakhs` (Float)
- `Domain` (String)
- `SIS_Awarded` (Integer)

---

## 2. Frontend Flow (Streamlit) Requirements

### Global Styling (Mandatory snippet for Antigravity IDE):
Inject this HTML at the top of the main script to enforce the white, minimalistic theme and hide Streamlit artifacts:
```python
import streamlit as st

st.set_page_config(page_title="CSR Connect", layout="centered")

hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp {
    background-color: #FFFFFF;
}
.css-1d391kg {  /* Adjusting default text colors if needed */
    background-color: #F8F9FA;
    border-radius: 10px;
}
/* Custom Buttons */
div.stButton > button:first-child {
    background-color: #000000;
    color: #FFFFFF;
    border-radius: 5px;
    border: none;
}
div.stButton > button:first-child:hover {
    background-color: #333333;
    color: #FFFFFF;
}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
```

### Landing Page
Two clean, central buttons/options: **[I am an NGO]** | **[I am a Company]**.

### NGO Portal Flow
1. **Details Form:** Form asking for NGO Name, Registration Info, Region, Years of Experience.
2. **Project Form:** Domain (dropdown), Title, Brief Description, Estimated Fund Ask (Lakhs).
3. **Collaboration Checkbox:** `[ ] Open to multi-company collaboration`
4. **Matching Engine:** 
   - Upon form submission, hit the FastAPI backend.
   - **Filter Logic:** Find companies where `company_domain` intersects with `proposal_domain` AND `company_budget >= (ask - 1.0)`. (Meaning budget is equal, greater, or short by max 1 Lakh).
   - Display list of matched companies.
5. **Action:** NGO can multi-select from these companies and click "Send Proposals". 
6. **Collab Trigger:** If the ask is very high, no solo companies match, AND the collab box is checked -> directly create an entry in `collaborations.csv` via backend API.

### Company Portal Flow
1. **Simple Login:** Enter Company Name/ID to view dashboard.
2. **Dashboard Header:** Display Company Name and an achievement badge: `🏆 Social Impact Score (SIS): {score}`.
3. **Proposals Feed:** 
   - Fetches from both `proposals.csv` (targeted at them) and `collaborations.csv` (open collabs in their domain).
   - **Crucial Sorting Logic:** Sort proposals so that underdeveloped/under-acknowledged regions (e.g., rural tags, specific states like Bihar, Odisha, North East) appear at the **TOP**. Explain via a small tag `[High Priority Region - 2x SIS points]`.
   - Show a clear visual marker `[🤝 Collab]` for collaborative proposals.
4. **Actions on Proposals:**
   - **Solo Accept (Regular):** Deducts company budget, moves proposal to `deals.csv`, awards SIS based on region priority.
   - **Pledge (Collab):** Pledges partial amount. Adds company to `Pledged_Companies` in `collaborations.csv`. 
   - **Solo Takeover (Collab):** If an active collab is ongoing (partially funded by others), but THIS company has enough budget to fund it entirely and chooses to do so single-handedly: It cancels the collab, voids other companies' pledges (refunds their virtual budget), and awards the full deal and SIS to the solo company.

---

## 3. Backend Logic (FastAPI) & Algorithms

The backend must expose endpoints to support the frontend while handling data consistency across CSVs.

### Core Endpoints
1. `GET /companies/match`
   - Accepts: `domain`, `ask_amount`
   - Logic: Returns list of companies where `domain` is in `Interested_Domains` AND `Budget_Lakhs >= (ask_amount - 1.0)`.

2. `POST /proposals/send`
   - Appends to `proposals.csv` or `collaborations.csv` depending on the collaborative flag.

3. `GET /company/{company_id}/dashboard`
   - Returns matched direct proposals and active collaborations in their domain.
   - Handles the regional sorting algorithm before returning JSON.

4. `POST /company/action/accept`
   - Accepts: `proposal_id`, `company_id`
   - Logic: 
     - Read `proposals.csv`, change status.
     - Deduct `ask` from `companies.csv` budget.
     - Calculate SIS (e.g., Base = ask amount. Multiplier = x2 if region in underdeveloped list). Add to company SIS.
     - Write to `deals.csv`.

5. `POST /company/action/pledge`
   - Accepts: `collab_id`, `company_id`, `pledge_amount`
   - Logic:
     - Update `Current_Pledged_Lakhs` in `collaborations.csv`.
     - Update `Pledged_Companies` string.
     - **Completion Check:** If `Current_Pledged_Lakhs >= Total_Ask_Lakhs`, finalize the deal. Move to `deals.csv`. Distribute SIS proportionally among pledged companies based on their contribution.

6. `POST /company/action/solo_takeover`
   - Logic: Read `collaborations.csv`. Remove existing pledges (add back budget to those companies). Grant full deal to the invoking company. Move to `deals.csv`.

### Social Impact Score (SIS) Algorithm Rule
- 1 Lakh INR funded = 10 SIS base points.
- Underdeveloped Region Modifier = 2.5x multiplier.
- Collaboration Modifier = 1.2x multiplier (encourages teamwork).
- Backend strictly calculates this during the transfer of a proposal to a deal.

---

## 4. Implementation Steps for IDE
1. Initialize FastAPI app in `backend.py`.
2. Implement CSV helper functions (pandas read/write wrappers to avoid file locks).
3. Create Pydantic models for request validation.
4. Implement the API routes as specified above.
5. Initialize Streamlit app in `frontend.py`.
6. Apply the CSS reset snippet first.
7. Build routing logic using `st.session_state` to toggle between NGO and Company views.
8. Connect Streamlit `requests` calls to the FastAPI local server (default `http://localhost:8000`).
