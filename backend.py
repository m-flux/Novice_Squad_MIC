"""
CSR & NGO Collaboration Platform — FastAPI Backend
====================================================
Handles all data operations on CSV files and exposes REST endpoints
for the Streamlit frontend.
"""

import os
import uuid
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from filelock import FileLock
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# App & Config
# ---------------------------------------------------------------------------
app = FastAPI(title="CSR Connect API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

CSV_SCHEMAS = {
    "companies": ["Company_ID", "Name", "Budget_Lakhs", "Interested_Domains", "SIS_Score"],
    "ngos": ["NGO_ID", "Name", "Years_Experience", "Region"],
    "proposals": [
        "Proposal_ID", "NGO_ID", "Target_Company_ID", "Title",
        "Description", "Domain", "Ask_Lakhs", "Region",
        "Is_Collaborative", "Status",
    ],
    "collaborations": [
        "Collab_ID", "NGO_ID", "Title", "Description", "Domain",
        "Total_Ask_Lakhs", "Current_Pledged_Lakhs", "Pledged_Companies",
        "Region", "Status",
    ],
    "deals": [
        "Deal_ID", "Ref_ID", "NGO_ID", "Companies_Involved",
        "Total_Amount_Lakhs", "Domain", "SIS_Awarded",
    ],
}

# Regions that receive the 2.5× SIS multiplier
UNDERDEVELOPED_REGIONS = {
    "Bihar", "Odisha", "Jharkhand", "Chhattisgarh",
    "Assam", "Manipur", "Meghalaya", "Mizoram",
    "Nagaland", "Tripura", "Arunachal Pradesh", "Sikkim",
}

# ---------------------------------------------------------------------------
# CSV Helpers (thread-safe via FileLock)
# ---------------------------------------------------------------------------

def _csv_path(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.csv")


def _lock_path(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.csv.lock")


import math

def sanitize_val(v):
    if isinstance(v, float) and math.isnan(v):
        return 0.0
    if str(v) == "nan":
        return ""
    return v

def sanitize_dict(d: dict) -> dict:
    return {k: sanitize_val(v) for k, v in d.items()}

def sanitize_records(records: list) -> list:
    return [sanitize_dict(r) if isinstance(r, dict) else r for r in records]

def read_csv(name: str) -> pd.DataFrame:
    """Read a CSV file, initialising it with headers if it doesn't exist."""
    path = _csv_path(name)
    lock = FileLock(_lock_path(name), timeout=5)
    with lock:
        if not os.path.exists(path):
            df = pd.DataFrame(columns=CSV_SCHEMAS[name])
            df.to_csv(path, index=False)
            return df
        df = pd.read_csv(path, dtype=str).fillna("")
        # Ensure numeric columns are cast properly
        float_cols = [c for c in df.columns if "Lakhs" in c or "Score" in c or "Experience" in c or "Awarded" in c]
        for c in float_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
        return df


def write_csv(name: str, df: pd.DataFrame) -> None:
    """Overwrite a CSV file with the given DataFrame."""
    path = _csv_path(name)
    lock = FileLock(_lock_path(name), timeout=5)
    with lock:
        df.to_csv(path, index=False)


def _new_id(prefix: str) -> str:
    return f"{prefix}{uuid.uuid4().hex[:8].upper()}"


# ---------------------------------------------------------------------------
# SIS Calculation
# ---------------------------------------------------------------------------

def calculate_sis(amount_lakhs: float, region: str, is_collab: bool) -> int:
    """
    1 Lakh = 10 base points.
    Underdeveloped region → ×2.5
    Collaboration → ×1.2
    """
    base = amount_lakhs * 10
    if region.strip().title() in UNDERDEVELOPED_REGIONS:
        base *= 2.5
    if is_collab:
        base *= 1.2
    return int(round(base))


def is_priority_region(region: str) -> bool:
    return region.strip().title() in UNDERDEVELOPED_REGIONS


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class NGORegister(BaseModel):
    name: str
    years_experience: int
    region: str


class ProposalSend(BaseModel):
    ngo_id: str
    title: str
    description: str
    domain: str
    ask_lakhs: float
    region: str
    is_collaborative: bool
    target_company_ids: List[str]  # empty list → collab-only


class AcceptRequest(BaseModel):
    proposal_id: str
    company_id: str


class PledgeRequest(BaseModel):
    collab_id: str
    company_id: str
    pledge_amount: float


class SoloTakeoverRequest(BaseModel):
    collab_id: str
    company_id: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

# ── NGO Registration ──────────────────────────────────────────────────────

@app.post("/ngos/register")
def register_ngo(body: NGORegister):
    df = read_csv("ngos")
    ngo_id = _new_id("NGO")
    new_row = {
        "NGO_ID": ngo_id,
        "Name": body.name,
        "Years_Experience": body.years_experience,
        "Region": body.region,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    write_csv("ngos", df)
    return {"ngo_id": ngo_id, "message": "NGO registered successfully."}


# ── Company Matching ──────────────────────────────────────────────────────

@app.get("/companies/match")
def match_companies(domain: str = Query(...), ask_amount: float = Query(...)):
    """
    Returns companies where:
      - `domain` intersects with their `Interested_Domains`, AND
      - `Budget_Lakhs >= (ask_amount - 1.0)`
    """
    df = read_csv("companies")
    results = []
    for _, row in df.iterrows():
        company_domains = [d.strip() for d in str(row["Interested_Domains"]).split(",")]
        if domain.strip() in company_domains and float(row["Budget_Lakhs"]) >= (ask_amount - 1.0):
            results.append({
                "Company_ID": row["Company_ID"],
                "Name": row["Name"],
                "Budget_Lakhs": float(row["Budget_Lakhs"]),
                "Interested_Domains": row["Interested_Domains"],
                "SIS_Score": int(float(row["SIS_Score"])),
            })
    return results


# ── Get all companies (for login dropdown) ────────────────────────────────

@app.get("/companies")
def list_companies():
    df = read_csv("companies")
    return df.to_dict(orient="records")


# ── Send Proposals / Create Collab ────────────────────────────────────────

@app.post("/proposals/send")
def send_proposals(body: ProposalSend):
    """
    If target_company_ids is non-empty, create individual proposals.
    If is_collaborative is True, ALWAYS create a collaboration entry in collaborations.csv
    so all companies in the domain can discover and pledge to it.
    """
    created_proposals = []
    created_collab = None

    # Case 1: Direct proposals to specific target companies
    if body.target_company_ids:
        df_prop = read_csv("proposals")
        for cid in body.target_company_ids:
            pid = _new_id("P")
            new_row = {
                "Proposal_ID": pid,
                "NGO_ID": body.ngo_id,
                "Target_Company_ID": cid,
                "Title": body.title,
                "Description": body.description,
                "Domain": body.domain,
                "Ask_Lakhs": body.ask_lakhs,
                "Region": body.region,
                "Is_Collaborative": str(body.is_collaborative),
                "Status": "Pending",
            }
            df_prop = pd.concat([df_prop, pd.DataFrame([new_row])], ignore_index=True)
            created_proposals.append(pid)
        write_csv("proposals", df_prop)

    # Case 2: Collaboration flag is True → create entry in collaborations.csv
    if body.is_collaborative:
        df_collab = read_csv("collaborations")
        # Check if an active collab with same title and NGO already exists
        exists = df_collab[
            (df_collab["NGO_ID"] == body.ngo_id) &
            (df_collab["Title"] == body.title) &
            (df_collab["Status"] == "Active")
        ]
        if exists.empty:
            cid = _new_id("CLB")
            new_row = {
                "Collab_ID": cid,
                "NGO_ID": body.ngo_id,
                "Title": body.title,
                "Description": body.description,
                "Domain": body.domain,
                "Total_Ask_Lakhs": body.ask_lakhs,
                "Current_Pledged_Lakhs": 0.0,
                "Pledged_Companies": "",
                "Region": body.region,
                "Status": "Active",
            }
            df_collab = pd.concat([df_collab, pd.DataFrame([new_row])], ignore_index=True)
            write_csv("collaborations", df_collab)
            created_collab = cid
        else:
            created_collab = exists.iloc[0]["Collab_ID"]

    return {
        "proposals_created": created_proposals,
        "collaboration_created": created_collab,
        "message": "Submissions processed successfully.",
    }


def sync_collaborations_from_proposals():
    """
    Ensure any collaborative proposals in proposals.csv have a corresponding
    Active entry in collaborations.csv so all companies in that domain can participate.
    """
    df_prop = read_csv("proposals")
    df_collab = read_csv("collaborations")

    collab_props = df_prop[
        (df_prop["Is_Collaborative"].astype(str).str.lower() == "true") &
        (df_prop["Status"] == "Pending")
    ]

    new_rows = []
    for _, prop in collab_props.iterrows():
        title = prop["Title"]
        ngo_id = prop["NGO_ID"]

        # Check if already in collaborations.csv
        exists = df_collab[
            (df_collab["NGO_ID"] == ngo_id) &
            (df_collab["Title"] == title) &
            (df_collab["Status"] != "Cancelled")
        ]
        if exists.empty:
            cid = _new_id("CLB")
            new_rows.append({
                "Collab_ID": cid,
                "NGO_ID": ngo_id,
                "Title": title,
                "Description": prop["Description"],
                "Domain": prop["Domain"],
                "Total_Ask_Lakhs": float(prop["Ask_Lakhs"]),
                "Current_Pledged_Lakhs": 0.0,
                "Pledged_Companies": "",
                "Region": prop["Region"],
                "Status": "Active",
            })

    if new_rows:
        df_collab = pd.concat([df_collab, pd.DataFrame(new_rows)], ignore_index=True)
        write_csv("collaborations", df_collab)


# ── Company Dashboard ────────────────────────────────────────────────────

@app.get("/company/{company_id}/dashboard")
def company_dashboard(company_id: str):
    """
    Returns:
      - company info
      - direct proposals targeted at this company
      - active collaborations in this company's domains
    Sorted with underdeveloped/priority regions at the TOP.
    """
    # Auto-sync collaborative proposals into collaborations.csv
    sync_collaborations_from_proposals()

    # Company info
    df_comp = read_csv("companies")
    comp_row = df_comp[df_comp["Company_ID"] == company_id]
    if comp_row.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    comp = comp_row.iloc[0]
    company_domains = [d.strip() for d in str(comp["Interested_Domains"]).split(",")]

    # Direct proposals
    df_prop = read_csv("proposals")
    direct = df_prop[
        (df_prop["Target_Company_ID"] == company_id) & (df_prop["Status"] == "Pending")
    ].copy()
    direct["_priority"] = direct["Region"].apply(lambda r: 0 if is_priority_region(str(r)) else 1)
    direct = direct.sort_values("_priority").drop(columns=["_priority"])
    direct_list = []
    for _, row in direct.iterrows():
        d = sanitize_dict(row.to_dict())
        d["is_priority_region"] = is_priority_region(str(row["Region"]))
        d["type"] = "proposal"
        direct_list.append(d)

    # Active collaborations in company's domain
    df_collab = read_csv("collaborations")
    collab_list = []
    for _, row in df_collab[df_collab["Status"] == "Active"].iterrows():
        if str(row["Domain"]).strip() in company_domains:
            d = sanitize_dict(row.to_dict())
            d["is_priority_region"] = is_priority_region(str(row["Region"]))
            d["type"] = "collaboration"
            collab_list.append(d)

    # Sort collabs by priority region
    collab_list.sort(key=lambda x: (0 if x["is_priority_region"] else 1))

    # Merge and sort globally
    all_items = direct_list + collab_list
    all_items.sort(key=lambda x: (0 if x["is_priority_region"] else 1))

    return {
        "company": {
            "Company_ID": comp["Company_ID"],
            "Name": comp["Name"],
            "Budget_Lakhs": float(comp["Budget_Lakhs"]),
            "Interested_Domains": comp["Interested_Domains"],
            "SIS_Score": int(float(comp["SIS_Score"])),
        },
        "feed": all_items,
        "direct_proposals": direct_list,
        "active_collaborations": collab_list,
    }


# ── Accept Proposal (Solo) ───────────────────────────────────────────────

@app.post("/company/action/accept")
def accept_proposal(body: AcceptRequest):
    df_prop = read_csv("proposals")
    idx = df_prop.index[df_prop["Proposal_ID"] == body.proposal_id]
    if idx.empty:
        raise HTTPException(status_code=404, detail="Proposal not found")
    i = idx[0]
    proposal = df_prop.loc[i]

    if proposal["Status"] != "Pending":
        raise HTTPException(status_code=400, detail="Proposal is not Pending")

    ask = float(proposal["Ask_Lakhs"])
    region = str(proposal["Region"])
    domain = str(proposal["Domain"])
    ngo_id = str(proposal["NGO_ID"])
    is_collab = str(proposal["Is_Collaborative"]).lower() == "true"

    # Deduct budget
    df_comp = read_csv("companies")
    cidx = df_comp.index[df_comp["Company_ID"] == body.company_id]
    if cidx.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    ci = cidx[0]
    budget = float(df_comp.loc[ci, "Budget_Lakhs"])
    if budget < ask:
        raise HTTPException(status_code=400, detail="Insufficient budget")
    df_comp.loc[ci, "Budget_Lakhs"] = budget - ask

    # SIS
    sis = calculate_sis(ask, region, is_collab)
    df_comp.loc[ci, "SIS_Score"] = int(float(df_comp.loc[ci, "SIS_Score"])) + sis

    # Update proposal
    df_prop.loc[i, "Status"] = "Accepted"

    # Create deal
    df_deals = read_csv("deals")
    deal_id = _new_id("D")
    new_deal = {
        "Deal_ID": deal_id,
        "Ref_ID": body.proposal_id,
        "NGO_ID": ngo_id,
        "Companies_Involved": body.company_id,
        "Total_Amount_Lakhs": ask,
        "Domain": domain,
        "SIS_Awarded": sis,
    }
    df_deals = pd.concat([df_deals, pd.DataFrame([new_deal])], ignore_index=True)

    # Persist
    write_csv("proposals", df_prop)
    write_csv("companies", df_comp)
    write_csv("deals", df_deals)

    return {"deal_id": deal_id, "sis_awarded": sis, "message": "Proposal accepted."}


# ── Pledge to Collaboration ──────────────────────────────────────────────

@app.post("/company/action/pledge")
def pledge_to_collab(body: PledgeRequest):
    df_collab = read_csv("collaborations")
    idx = df_collab.index[df_collab["Collab_ID"] == body.collab_id]
    if idx.empty:
        raise HTTPException(status_code=404, detail="Collaboration not found")
    i = idx[0]
    collab = df_collab.loc[i]

    if collab["Status"] != "Active":
        raise HTTPException(status_code=400, detail="Collaboration is not Active")

    # Deduct company budget
    df_comp = read_csv("companies")
    cidx = df_comp.index[df_comp["Company_ID"] == body.company_id]
    if cidx.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    ci = cidx[0]
    budget = float(df_comp.loc[ci, "Budget_Lakhs"])
    if budget < body.pledge_amount:
        raise HTTPException(status_code=400, detail="Insufficient budget")
    df_comp.loc[ci, "Budget_Lakhs"] = budget - body.pledge_amount

    # Update pledged info
    current_pledged = float(collab["Current_Pledged_Lakhs"])
    new_pledged = current_pledged + body.pledge_amount
    df_collab.loc[i, "Current_Pledged_Lakhs"] = new_pledged

    existing_pledges = str(collab["Pledged_Companies"]).strip()
    if existing_pledges and existing_pledges != "nan":
        new_pledge_str = f"{existing_pledges}|{body.company_id}:{body.pledge_amount}"
    else:
        new_pledge_str = f"{body.company_id}:{body.pledge_amount}"
    df_collab.loc[i, "Pledged_Companies"] = new_pledge_str

    deal_id = None
    total_sis = 0
    total_ask = float(collab["Total_Ask_Lakhs"])

    # Completion check
    if new_pledged >= total_ask:
        df_collab.loc[i, "Status"] = "Fulfilled"
        region = str(collab["Region"])
        domain = str(collab["Domain"])
        ngo_id = str(collab["NGO_ID"])

        # Distribute SIS proportionally
        pledge_entries = new_pledge_str.split("|")
        all_companies = []
        for entry in pledge_entries:
            parts = entry.split(":")
            if len(parts) == 2:
                all_companies.append((parts[0], float(parts[1])))

        for comp_id, amount in all_companies:
            sis = calculate_sis(amount, region, True)
            total_sis += sis
            # Add SIS to company
            comp_idx = df_comp.index[df_comp["Company_ID"] == comp_id]
            if not comp_idx.empty:
                df_comp.loc[comp_idx[0], "SIS_Score"] = int(float(df_comp.loc[comp_idx[0], "SIS_Score"])) + sis

        # Create deal
        df_deals = read_csv("deals")
        deal_id = _new_id("D")
        companies_str = ",".join([c[0] for c in all_companies])
        new_deal = {
            "Deal_ID": deal_id,
            "Ref_ID": body.collab_id,
            "NGO_ID": ngo_id,
            "Companies_Involved": companies_str,
            "Total_Amount_Lakhs": total_ask,
            "Domain": domain,
            "SIS_Awarded": total_sis,
        }
        df_deals = pd.concat([df_deals, pd.DataFrame([new_deal])], ignore_index=True)
        write_csv("deals", df_deals)

    write_csv("collaborations", df_collab)
    write_csv("companies", df_comp)

    return {
        "message": "Pledge recorded.",
        "new_pledged_total": new_pledged,
        "deal_id": deal_id,
        "fulfilled": new_pledged >= total_ask,
    }


# ── Solo Takeover of a Collaboration ─────────────────────────────────────

@app.post("/company/action/solo_takeover")
def solo_takeover(body: SoloTakeoverRequest):
    df_collab = read_csv("collaborations")
    idx = df_collab.index[df_collab["Collab_ID"] == body.collab_id]
    if idx.empty:
        raise HTTPException(status_code=404, detail="Collaboration not found")
    i = idx[0]
    collab = df_collab.loc[i]

    if collab["Status"] != "Active":
        raise HTTPException(status_code=400, detail="Collaboration is not Active")

    total_ask = float(collab["Total_Ask_Lakhs"])
    region = str(collab["Region"])
    domain = str(collab["Domain"])
    ngo_id = str(collab["NGO_ID"])

    df_comp = read_csv("companies")

    # Check invoking company has enough budget
    cidx = df_comp.index[df_comp["Company_ID"] == body.company_id]
    if cidx.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    ci = cidx[0]
    budget = float(df_comp.loc[ci, "Budget_Lakhs"])
    if budget < total_ask:
        raise HTTPException(status_code=400, detail="Insufficient budget for full takeover")

    # Refund existing pledgers
    existing_pledges = str(collab["Pledged_Companies"]).strip()
    if existing_pledges and existing_pledges != "nan":
        for entry in existing_pledges.split("|"):
            parts = entry.split(":")
            if len(parts) == 2:
                refund_cid, refund_amt = parts[0], float(parts[1])
                ridx = df_comp.index[df_comp["Company_ID"] == refund_cid]
                if not ridx.empty:
                    df_comp.loc[ridx[0], "Budget_Lakhs"] = float(df_comp.loc[ridx[0], "Budget_Lakhs"]) + refund_amt

    # Deduct full amount from takeover company
    df_comp.loc[ci, "Budget_Lakhs"] = float(df_comp.loc[ci, "Budget_Lakhs"]) - total_ask

    # SIS (solo, not collab multiplier)
    sis = calculate_sis(total_ask, region, False)
    df_comp.loc[ci, "SIS_Score"] = int(float(df_comp.loc[ci, "SIS_Score"])) + sis

    # Mark collab as Cancelled
    df_collab.loc[i, "Status"] = "Cancelled"

    # Create deal
    df_deals = read_csv("deals")
    deal_id = _new_id("D")
    new_deal = {
        "Deal_ID": deal_id,
        "Ref_ID": body.collab_id,
        "NGO_ID": ngo_id,
        "Companies_Involved": body.company_id,
        "Total_Amount_Lakhs": total_ask,
        "Domain": domain,
        "SIS_Awarded": sis,
    }
    df_deals = pd.concat([df_deals, pd.DataFrame([new_deal])], ignore_index=True)

    write_csv("collaborations", df_collab)
    write_csv("companies", df_comp)
    write_csv("deals", df_deals)

    return {"deal_id": deal_id, "sis_awarded": sis, "message": "Solo takeover complete."}


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
