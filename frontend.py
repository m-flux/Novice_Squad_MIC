"""
CSR & NGO Collaboration Platform — Streamlit Frontend
=======================================================
Clean, modern, high-contrast light theme.
Connects to the FastAPI backend at http://localhost:8000.
"""

import streamlit as st
import requests

# ---------------------------------------------------------------------------
# Page Config & Global Styling — MUST be the first Streamlit command
# ---------------------------------------------------------------------------
st.set_page_config(page_title="CSR Connect", layout="centered", page_icon="🤝")

API = "http://localhost:8000"

DOMAINS = [
    "Education", "Health", "Rural Development", "Infrastructure",
    "Technology", "Environment", "Sanitation", "Women Empowerment",
    "Agriculture",
]

# ── Clean, High-Contrast Modern Light Theme ────────────────────────────────
hide_st_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── Hide Streamlit defaults ─────────────────────────────────── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Typography & Background ──────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0F172A;
}

.stApp {
    background-color: #F8FAFC;
}

/* ── Streamlit Text & Labels High-Contrast Override ─────────── */
.stMarkdown, .stMarkdown p, .stText, .stCaption,
div[data-testid="stText"], p, span, label,
.stSelectbox label, .stTextInput label, .stNumberInput label,
.stTextArea label, .stCheckbox label {
    color: #1E293B !important;
}

.stCaption, small {
    color: #64748B !important;
}

/* ── Headings ─────────────────────────────────────────────────── */
h1 {
    font-weight: 700 !important;
    color: #0F172A !important;
    letter-spacing: -0.02em !important;
}
h2 {
    font-weight: 600 !important;
    color: #0F172A !important;
    margin-bottom: 0.5rem !important;
}
h3 {
    font-weight: 600 !important;
    color: #1E293B !important;
}

/* ── Card Containers ─────────────────────────────────────────── */
.card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 22px 24px;
    margin-bottom: 18px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
    transition: all 0.2s ease-in-out;
}
.card:hover {
    border-color: #CBD5E1;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.07);
}
.card h3 {
    color: #0F172A !important;
    margin-top: 0 !important;
}

/* ── Compact Buttons (No forced stretch) & Text Color ───────── */
div.stButton > button,
div.stButton > button:first-child,
div[data-testid="stFormSubmitButton"] > button,
button[data-testid*="BaseButton"],
button[data-testid*="baseButton"] {
    background-color: #0F172A !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: 1px solid #0F172A !important;
    padding: 0.45rem 1.2rem !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05) !important;
}

/* Force all text/span/p elements inside buttons to be white */
div.stButton button *,
div.stButton button:first-child *,
div[data-testid="stFormSubmitButton"] button *,
button[data-testid*="BaseButton"] *,
button[data-testid*="baseButton"] *,
button,
button * {
    color: #FFFFFF !important;
}

div.stButton > button:hover,
div.stButton > button:first-child:hover,
div[data-testid="stFormSubmitButton"] > button:hover,
button[data-testid*="BaseButton"]:hover,
button[data-testid*="baseButton"]:hover {
    background-color: #334155 !important;
    border-color: #334155 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

div.stButton button:hover *,
div.stButton button:first-child:hover *,
div[data-testid="stFormSubmitButton"] button:hover *,
button[data-testid*="BaseButton"]:hover *,
button[data-testid*="baseButton"]:hover * {
    color: #FFFFFF !important;
}

div.stButton > button:active,
div.stButton > button:first-child:active,
div[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0);
}

/* ── Form Inputs ─────────────────────────────────────────────── */
div[data-testid="stForm"] {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
}

input, textarea, select,
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    font-size: 0.92rem !important;
}

input:focus, textarea:focus {
    border-color: #0F172A !important;
    box-shadow: 0 0 0 2px rgba(15, 23, 42, 0.08) !important;
}

/* ── Custom Pill Badges ───────────────────────────────────────── */
.tag-priority {
    display: inline-flex;
    align-items: center;
    background: #FEF3C7;
    color: #B45309;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.76rem;
    font-weight: 600;
    margin-right: 8px;
    border: 1px solid #FDE68A;
}

.tag-collab {
    display: inline-flex;
    align-items: center;
    background: #ECFDF5;
    color: #047857;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.76rem;
    font-weight: 600;
    margin-right: 8px;
    border: 1px solid #A7F3D0;
}

.tag-domain {
    display: inline-flex;
    align-items: center;
    background: #F1F5F9;
    color: #475569;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.76rem;
    font-weight: 500;
    border: 1px solid #E2E8F0;
}

/* ── Header Metrics & Badges ─────────────────────────────────── */
.sis-badge {
    background: #0F172A;
    color: #FFFFFF;
    padding: 12px 24px;
    border-radius: 10px;
    font-size: 1.15rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin: 8px 0 20px 0;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.12);
}

.metric-row {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
}

.metric-item {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 16px;
    flex: 1;
    text-align: center;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #0F172A;
}

.metric-label {
    font-size: 0.75rem;
    color: #64748B;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 600;
}

/* ── Progress Bar ─────────────────────────────────────────────── */
.progress-outer {
    background: #F1F5F9;
    border-radius: 6px;
    height: 8px;
    margin: 8px 0;
    overflow: hidden;
    border: 1px solid #E2E8F0;
}

.progress-inner {
    background: #059669;
    height: 100%;
    border-radius: 6px;
    transition: width 0.4s ease;
}

.divider {
    height: 1px;
    background: #E2E8F0;
    margin: 28px 0;
}

/* ── Success Alert ────────────────────────────────────────────── */
.success-box {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 8px;
    padding: 12px 16px;
    color: #15803D;
    font-weight: 500;
    font-size: 0.9rem;
    margin: 10px 0;
}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session State Defaults
# ---------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "ngo_id" not in st.session_state:
    st.session_state.ngo_id = None
if "ngo_data" not in st.session_state:
    st.session_state.ngo_data = {}
if "company_id" not in st.session_state:
    st.session_state.company_id = None
if "matched_companies" not in st.session_state:
    st.session_state.matched_companies = []
if "proposal_data" not in st.session_state:
    st.session_state.proposal_data = {}


def navigate(page: str):
    st.session_state.page = page


# ---------------------------------------------------------------------------
# Helper: API Calls
# ---------------------------------------------------------------------------
def api_get(path, params=None):
    try:
        r = requests.get(f"{API}{path}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def api_post(path, json_data=None):
    try:
        r = requests.post(f"{API}{path}", json=json_data, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════════════════════════

# ── 1. Landing Page ───────────────────────────────────────────────────────

def page_landing():
    st.markdown("<h1 style='text-align: center; margin-top: 40px;'>CSR Connect</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #64748B; font-size: 1.05rem; margin-bottom: 36px;'>"
        "Empowering impactful corporate-NGO partnerships through intelligent CSR matching."
        "</p>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="card" style="text-align: center;">
                <h3 style="margin-bottom: 8px;">For NGOs</h3>
                <p style="font-size: 0.88rem; color: #64748B;">Register your cause, request CSR funds, or start multi-company collaborative projects.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Enter NGO Portal →", key="btn_ngo_portal"):
            navigate("ngo_details")
            st.rerun()

    with c2:
        st.markdown(
            """
            <div class="card" style="text-align: center;">
                <h3 style="margin-bottom: 8px;">For Companies</h3>
                <p style="font-size: 0.88rem; color: #64748B;">Access your CSR dashboard, fund verified proposals, and earn Social Impact Score (SIS).</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Enter Company Portal →", key="btn_company_portal"):
            navigate("company_login")
            st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Platform overview stats
    st.markdown(
        """
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-value">8</div>
                <div class="metric-label">Partner Companies</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">9</div>
                <div class="metric-label">CSR Domains</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">2.5×</div>
                <div class="metric-label">Priority Region SIS Multiplier</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── 2. NGO Details Form ──────────────────────────────────────────────────

def page_ngo_details():
    _back_button("landing")
    st.markdown("## Register Your NGO")
    st.caption("Provide your organisation's background to start submitting funding proposals.")

    with st.form("ngo_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("NGO Name", placeholder="e.g. Shiksha Foundation")
            region = st.text_input("Region (State / District)", placeholder="e.g. Bihar")
        with col2:
            reg_info = st.text_input("Registration Info", placeholder="e.g. Reg #12345/2024")
            years_exp = st.number_input("Years of Experience", min_value=0, max_value=100, value=3)

        submitted = st.form_submit_button("Proceed to Project Submission →")

    if submitted:
        if not name or not region:
            st.warning("Please provide your NGO Name and Region.")
            return
        result = api_post("/ngos/register", {
            "name": name,
            "years_experience": int(years_exp),
            "region": region,
        })
        if result:
            st.session_state.ngo_id = result["ngo_id"]
            st.session_state.ngo_data = {
                "name": name,
                "reg_info": reg_info,
                "region": region,
                "years_experience": years_exp,
            }
            navigate("ngo_project")
            st.rerun()


# ── 3. NGO Project Form ──────────────────────────────────────────────────

def page_ngo_project():
    _back_button("ngo_details")
    st.markdown("## Submit CSR Project Proposal")
    st.caption(f"NGO: **{st.session_state.ngo_data.get('name', 'Registered NGO')}** | Region: **{st.session_state.ngo_data.get('region', 'N/A')}**")

    with st.form("project_form"):
        c1, c2 = st.columns(2)
        with c1:
            domain = st.selectbox("CSR Domain", DOMAINS)
        with c2:
            ask_lakhs = st.number_input("Required Funding (₹ Lakhs)", min_value=1.0, value=25.0, step=5.0)

        title = st.text_input("Project Title", placeholder="e.g. Rural Healthcare Mobile Clinic")
        description = st.text_area("Project Description", placeholder="Detail the scope, target beneficiaries, and expected outcomes…")

        is_collab = st.checkbox("Open to multi-company pooled collaboration (recommended for high budgets)", value=True)

        submitted = st.form_submit_button("Search Matching Companies & Submit →")

    if submitted:
        if not title or not description:
            st.warning("Please complete the project title and description.")
            return

        matches = api_get("/companies/match", {"domain": domain, "ask_amount": ask_lakhs})
        st.session_state.matched_companies = matches or []
        st.session_state.proposal_data = {
            "title": title,
            "description": description,
            "domain": domain,
            "ask_lakhs": ask_lakhs,
            "is_collaborative": is_collab,
            "region": st.session_state.ngo_data.get("region", "India"),
        }
        navigate("ngo_results")
        st.rerun()


# ── 4. NGO Results — Matched Companies ───────────────────────────────────

def page_ngo_results():
    _back_button("ngo_project")
    st.markdown("## Matched CSR Partner Options")

    pd = st.session_state.proposal_data
    matches = st.session_state.matched_companies

    st.markdown(
        f"""
        <div class="card">
            <span class="tag-domain">{pd.get('domain','')}</span>
            <h3 style="margin: 8px 0 4px 0;">{pd.get('title','')}</h3>
            <p style="font-size: 0.88rem; color: #475569; margin: 0;">
                Funding Request: <strong>₹{pd.get('ask_lakhs',0)} Lakhs</strong> &nbsp;|&nbsp;
                Region: <strong>{pd.get('region','')}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if matches:
        st.markdown(f"**{len(matches)}** companies have sufficient CSR budget and domain interest:")
        selected = []
        for m in matches:
            checked = st.checkbox(
                f"**{m['Name']}**  •  Available Budget: ₹{m['Budget_Lakhs']}L  •  Current SIS: {m['SIS_Score']}",
                key=f"sel_{m['Company_ID']}",
                value=True,
            )
            if checked:
                selected.append(m["Company_ID"])

        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Send Direct Proposal(s)", key="btn_send_direct"):
                if not selected:
                    st.warning("Please select at least one target company.")
                else:
                    result = api_post("/proposals/send", {
                        "ngo_id": st.session_state.ngo_id,
                        "title": pd["title"],
                        "description": pd["description"],
                        "domain": pd["domain"],
                        "ask_lakhs": pd["ask_lakhs"],
                        "region": pd["region"],
                        "is_collaborative": pd["is_collaborative"],
                        "target_company_ids": selected,
                    })
                    if result:
                        st.markdown(
                            f'<div class="success-box">✓ Direct proposal(s) sent to {len(selected)} company(ies)!</div>',
                            unsafe_allow_html=True,
                        )
    else:
        st.info("No single company currently has enough available budget to fund this proposal alone.")

    if pd.get("is_collaborative"):
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### Open Multi-Company Collaboration")
        st.write("Publishing as a collaborative request allows **multiple companies with lower or partial budgets** to pool funds together.")
        if st.button("Publish as Open Collaboration Request", key="btn_pub_collab"):
            result = api_post("/proposals/send", {
                "ngo_id": st.session_state.ngo_id,
                "title": pd["title"],
                "description": pd["description"],
                "domain": pd["domain"],
                "ask_lakhs": pd["ask_lakhs"],
                "region": pd["region"],
                "is_collaborative": True,
                "target_company_ids": [],
            })
            if result and result.get("collaboration_created"):
                st.markdown(
                    f'<div class="success-box">✓ Collaboration request published! Open for multi-company pledges.</div>',
                    unsafe_allow_html=True,
                )


# ── 5. Company Login ──────────────────────────────────────────────────────

def page_company_login():
    _back_button("landing")
    st.markdown("## Corporate CSR Login")
    st.caption("Select your registered company profile to view incoming proposals and open collaboration opportunities.")

    companies = api_get("/companies")
    if not companies:
        return

    company_map = {f"{c['Name']}  (Available: ₹{c['Budget_Lakhs']}L)": c["Company_ID"] for c in companies}
    selected_label = st.selectbox("Company Profile", list(company_map.keys()))

    if st.button("Access Dashboard →", key="btn_access_dash"):
        st.session_state.company_id = company_map[selected_label]
        navigate("company_dashboard")
        st.rerun()


# ── 6. Company Dashboard ─────────────────────────────────────────────────

def page_company_dashboard():
    _back_button("company_login")

    data = api_get(f"/company/{st.session_state.company_id}/dashboard")
    if not data:
        return

    comp = data["company"]
    direct_props = data.get("direct_proposals", [])
    active_collabs = data.get("active_collaborations", [])

    # Header
    st.markdown(f"## {comp['Name']}")
    st.markdown(f'<div class="sis-badge">🏆 Social Impact Score: {comp["SIS_Score"]} SIS</div>', unsafe_allow_html=True)

    # Key Metrics
    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-value">₹{comp['Budget_Lakhs']}L</div>
                <div class="metric-label">Available CSR Budget</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{len(direct_props)}</div>
                <div class="metric-label">Direct Proposals</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{len(active_collabs)}</div>
                <div class="metric-label">Active Collaborations</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Tabbed Interface
    tab_direct, tab_collab = st.tabs([
        f"📩 Direct Proposals ({len(direct_props)})",
        f"🤝 Multi-Company Collaborations ({len(active_collabs)})"
    ])

    # ── Tab 1: Direct Proposals
    with tab_direct:
        if not direct_props:
            st.info("No direct proposals pending for your company at this time.")
        else:
            for item in direct_props:
                _render_direct_proposal_card(item, comp)

    # ── Tab 2: Multi-Company Collaborations
    with tab_collab:
        st.caption("Active multi-company pooled funding requests in your interested domains. Companies with any budget size can participate by pledging funds!")
        if not active_collabs:
            st.info("No active collaboration requests open in your interested domains.")
        else:
            for item in active_collabs:
                _render_collaboration_card(item, comp)


def _render_direct_proposal_card(item, comp):
    """Render direct proposal targeted at this company."""
    is_priority = item.get("is_priority_region", False)
    title = item.get("Title", "Untitled")
    desc = item.get("Description", "")
    region = item.get("Region", "")
    ask = float(item.get("Ask_Lakhs", 0))
    proposal_id = item.get("Proposal_ID", "")

    priority_tag = '<span class="tag-priority">⚡ High Priority Region (2.5× SIS)</span>' if is_priority else ''
    domain_tag = f'<span class="tag-domain">{item.get("Domain","")}</span>'

    st.markdown(
        f"""
        <div class="card">
            <div>{priority_tag}{domain_tag}</div>
            <h3 style="margin: 10px 0 6px 0;">{title}</h3>
            <p style="color: #334155; font-size: 0.9rem; margin-bottom: 10px; line-height: 1.5;">{desc}</p>
            <p style="font-size: 0.85rem; color: #475569; font-weight: 500; margin: 0;">
                📍 Region: <strong>{region}</strong> &nbsp;|&nbsp; 💰 Required: <strong>₹{ask} Lakhs</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([2, 3])
    with c1:
        if float(comp["Budget_Lakhs"]) >= ask:
            if st.button(f"Accept & Fund Full ₹{ask}L", key=f"btn_acc_{proposal_id}"):
                result = api_post("/company/action/accept", {
                    "proposal_id": proposal_id,
                    "company_id": comp["Company_ID"],
                })
                if result:
                    st.markdown(
                        f'<div class="success-box">✓ Proposal Accepted! Deal finalized. +{result.get("sis_awarded",0)} SIS awarded!</div>',
                        unsafe_allow_html=True,
                    )
                    st.rerun()
        else:
            st.caption("Insufficient budget to accept solo.")


def _render_collaboration_card(item, comp):
    """Render multi-company collaboration card with pledge controls."""
    is_priority = item.get("is_priority_region", False)
    title = item.get("Title", "Untitled")
    desc = item.get("Description", "")
    region = item.get("Region", "")
    total_ask = float(item.get("Total_Ask_Lakhs", 0))
    current_pledged = float(item.get("Current_Pledged_Lakhs", 0))
    collab_id = item.get("Collab_ID", "")

    pct = min(100, int((current_pledged / total_ask) * 100)) if total_ask > 0 else 0
    priority_tag = '<span class="tag-priority">⚡ High Priority Region (2.5× SIS)</span>' if is_priority else ''
    collab_tag = '<span class="tag-collab">🤝 Open Collaboration</span>'
    domain_tag = f'<span class="tag-domain">{item.get("Domain","")}</span>'

    st.markdown(
        f"""
        <div class="card">
            <div>{priority_tag}{collab_tag}{domain_tag}</div>
            <h3 style="margin: 10px 0 6px 0;">{title}</h3>
            <p style="color: #334155; font-size: 0.9rem; margin-bottom: 10px; line-height: 1.5;">{desc}</p>
            <p style="font-size: 0.85rem; color: #475569; font-weight: 500; margin-bottom: 8px;">
                📍 Region: <strong>{region}</strong> &nbsp;|&nbsp; 🎯 Total Ask: <strong>₹{total_ask} Lakhs</strong>
            </p>
            <div style="font-size: 0.82rem; color: #047857; font-weight: 600;">
                Current Pledged: ₹{current_pledged}L of ₹{total_ask}L ({pct}% funded)
            </div>
            <div class="progress-outer">
                <div class="progress-inner" style="width: {pct}%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    remaining_needed = max(1.0, total_ask - current_pledged)
    max_pledgeable = min(float(comp["Budget_Lakhs"]), remaining_needed)

    if max_pledgeable > 0:
        c1, c2 = st.columns([2, 1])
        with c1:
            pledge_val = st.number_input(
                "Contribution Amount (₹ Lakhs)",
                min_value=1.0,
                max_value=max_pledgeable,
                value=min(10.0, max_pledgeable),
                step=1.0,
                key=f"in_pledge_{collab_id}",
            )
        with c2:
            st.write("") # spacing
            st.write("")
            if st.button("Pledge Amount", key=f"btn_plg_{collab_id}"):
                result = api_post("/company/action/pledge", {
                    "collab_id": collab_id,
                    "company_id": comp["Company_ID"],
                    "pledge_amount": pledge_val,
                })
                if result:
                    msg = f"✓ Pledged ₹{pledge_val}L towards this collaboration!"
                    if result.get("fulfilled"):
                        msg = "🎉 Collaboration fully funded! Deal finalized."
                    st.markdown(f'<div class="success-box">{msg}</div>', unsafe_allow_html=True)
                    st.rerun()

    # Solo takeover option if company budget covers full total ask
    if float(comp["Budget_Lakhs"]) >= total_ask:
        if st.button(f"⚡ Single-Handedly Takeover Entire Project (₹{total_ask}L)", key=f"btn_so_{collab_id}"):
            result = api_post("/company/action/solo_takeover", {
                "collab_id": collab_id,
                "company_id": comp["Company_ID"],
            })
            if result:
                st.markdown(
                    f'<div class="success-box">✓ Solo Takeover Complete! Previous pledges refunded, full deal awarded to {comp["Name"]}.</div>',
                    unsafe_allow_html=True,
                )
                st.rerun()


# ---------------------------------------------------------------------------
# Navigation Helper
# ---------------------------------------------------------------------------
def _back_button(target: str):
    if st.button("← Back", key=f"back_to_{target}"):
        navigate(target)
        st.rerun()


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
PAGES = {
    "landing": page_landing,
    "ngo_details": page_ngo_details,
    "ngo_project": page_ngo_project,
    "ngo_results": page_ngo_results,
    "company_login": page_company_login,
    "company_dashboard": page_company_dashboard,
}

PAGES.get(st.session_state.page, page_landing)()
