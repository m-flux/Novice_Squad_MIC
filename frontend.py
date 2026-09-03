"""
CSR & NGO Collaboration Platform — Streamlit Frontend
=======================================================
Minimalistic, elegant, white-themed UI.
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

# ── CSS: hide Streamlit branding, modern light theme ──────────────────────
hide_st_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Hide Streamlit defaults ─────────────────────────────────── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Base typography ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #1E293B;
}

/* ── App background — soft gradient ──────────────────────────── */
.stApp {
    background: linear-gradient(160deg, #F0F4FF 0%, #FAFBFF 40%, #F5F3FF 70%, #FFF7ED 100%);
    min-height: 100vh;
}

/* ── Streamlit text elements — ensure visibility ─────────────── */
.stMarkdown, .stMarkdown p, .stText, .stCaption,
div[data-testid="stText"], p, span, label,
.stSelectbox label, .stTextInput label, .stNumberInput label,
.stTextArea label, .stCheckbox label {
    color: #334155 !important;
}
.stCaption, small {
    color: #64748B !important;
}

/* ── Headings ─────────────────────────────────────────────────── */
h1 {
    font-weight: 700 !important;
    color: #0F172A !important;
    letter-spacing: -0.5px !important;
}
h2 {
    font-weight: 600 !important;
    color: #1E293B !important;
}
h3 {
    font-weight: 600 !important;
    color: #334155 !important;
}

/* ── Cards — glassmorphism ───────────────────────────────────── */
.card {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    border: 1px solid rgba(148, 163, 184, 0.2);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: all 0.25s ease;
    color: #1E293B;
}
.card:hover {
    box-shadow: 0 8px 30px rgba(99, 102, 241, 0.1);
    border-color: rgba(99, 102, 241, 0.25);
    transform: translateY(-2px);
}
.card h3 {
    color: #0F172A !important;
}
.card p {
    color: #475569 !important;
}

/* ── Buttons — indigo gradient with visible hover ────────────── */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #4F46E5, #6366F1);
    color: #FFFFFF !important;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1.8rem;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.3px;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
}
div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #4338CA, #5558E6);
    color: #FFFFFF !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.35);
}
div.stButton > button:first-child:active {
    transform: translateY(0px);
    box-shadow: 0 2px 6px rgba(79, 70, 229, 0.2);
}

/* ── Form & inputs ───────────────────────────────────────────── */
div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 28px;
    border: 1px solid rgba(148, 163, 184, 0.2);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
input, textarea, select,
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background-color: #F8FAFC !important;
    color: #1E293B !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}
input:focus, textarea:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15) !important;
}

/* ── Selectbox ───────────────────────────────────────────────── */
div[data-baseweb="select"] {
    background-color: #F8FAFC;
    border-radius: 8px;
}

/* ── Checkbox ────────────────────────────────────────────────── */
.stCheckbox span {
    color: #334155 !important;
}

/* ── Tags ─────────────────────────────────────────────────────── */
.tag-priority {
    display: inline-block;
    background: linear-gradient(135deg, #FFF7ED, #FFEDD5);
    color: #C2410C;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 6px;
    border: 1px solid rgba(194, 65, 12, 0.15);
}
.tag-collab {
    display: inline-block;
    background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
    color: #1D4ED8;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 6px;
    border: 1px solid rgba(29, 78, 216, 0.15);
}
.tag-domain {
    display: inline-block;
    background: linear-gradient(135deg, #FAF5FF, #F3E8FF);
    color: #7C3AED;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    border: 1px solid rgba(124, 58, 237, 0.12);
}

/* ── SIS Badge — vibrant gradient ────────────────────────────── */
.sis-badge {
    background: linear-gradient(135deg, #4F46E5, #7C3AED, #A855F7);
    color: #FFFFFF;
    padding: 16px 32px;
    border-radius: 14px;
    font-size: 1.3rem;
    font-weight: 600;
    display: inline-block;
    margin: 12px 0 24px 0;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
}

/* ── Metric row ───────────────────────────────────────────────── */
.metric-row {
    display: flex;
    gap: 16px;
    margin-bottom: 20px;
}
.metric-item {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(8px);
    border-radius: 14px;
    padding: 20px;
    flex: 1;
    text-align: center;
    border: 1px solid rgba(148, 163, 184, 0.2);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    transition: all 0.2s ease;
}
.metric-item:hover {
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.08);
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #4F46E5;
}
.metric-label {
    font-size: 0.78rem;
    color: #64748B;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    font-weight: 500;
}

/* ── Progress bar — gradient ─────────────────────────────────── */
.progress-outer {
    background: #E2E8F0;
    border-radius: 10px;
    height: 10px;
    margin: 8px 0;
    overflow: hidden;
}
.progress-inner {
    background: linear-gradient(90deg, #4F46E5, #7C3AED, #A855F7);
    height: 100%;
    border-radius: 10px;
    transition: width 0.5s ease;
}

/* ── Divider ──────────────────────────────────────────────────── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #CBD5E1, transparent);
    margin: 36px 0;
}

/* ── Landing hero ─────────────────────────────────────────────── */
.hero-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-top: 80px;
    letter-spacing: -1px;
    line-height: 1.15;
}
.hero-sub {
    text-align: center;
    font-size: 1.1rem;
    color: #64748B;
    margin-top: 14px;
    margin-bottom: 48px;
    font-weight: 400;
    line-height: 1.6;
}

/* ── Success message ──────────────────────────────────────────── */
.success-box {
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    border: 1px solid #6EE7B7;
    border-radius: 12px;
    padding: 16px 20px;
    color: #065F46;
    font-weight: 500;
    margin: 12px 0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

/* ── Streamlit info/warning boxes ─────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 12px;
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
    st.markdown('<div class="hero-title">CSR Connect</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Bridging the gap between Corporate Social Responsibility and grassroots impact.</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("I am an NGO", use_container_width=True):
                navigate("ngo_details")
                st.rerun()
        with c2:
            if st.button("I am a Company", use_container_width=True):
                navigate("company_login")
                st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Quick stats
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
                <div class="metric-value">₹1,615L</div>
                <div class="metric-label">Total CSR Pool</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── 2. NGO Details Form ──────────────────────────────────────────────────

def page_ngo_details():
    _back_button("landing")
    st.markdown("## Register Your NGO")
    st.caption("Provide your organisation's details to get started.")

    with st.form("ngo_form"):
        name = st.text_input("NGO Name", placeholder="e.g. Pratham Education Foundation")
        reg_info = st.text_input("Registration Number", placeholder="e.g. MH/2024/001234")
        region = st.text_input("Region (State / District)", placeholder="e.g. Maharashtra")
        years_exp = st.number_input("Years of Experience", min_value=0, max_value=100, value=1)
        submitted = st.form_submit_button("Continue →")

    if submitted:
        if not name or not region:
            st.warning("Please fill in at least the NGO Name and Region.")
            return
        # Register with backend
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
    st.markdown("## Submit Your Project")
    st.caption(f"Logged in as **{st.session_state.ngo_data.get('name', 'NGO')}**")

    with st.form("project_form"):
        domain = st.selectbox("Domain", DOMAINS)
        title = st.text_input("Project Title", placeholder="e.g. Digital Classrooms in Rural Bihar")
        description = st.text_area("Brief Description", placeholder="Describe the impact and objectives…")
        ask_lakhs = st.number_input("Estimated Fund Ask (₹ Lakhs)", min_value=1.0, value=10.0, step=1.0)
        is_collab = st.checkbox("Open to multi-company collaboration")
        submitted = st.form_submit_button("Find Matching Companies →")

    if submitted:
        if not title or not description:
            st.warning("Please fill in the project title and description.")
            return
        # Match companies
        matches = api_get("/companies/match", {"domain": domain, "ask_amount": ask_lakhs})
        st.session_state.matched_companies = matches or []
        st.session_state.proposal_data = {
            "title": title,
            "description": description,
            "domain": domain,
            "ask_lakhs": ask_lakhs,
            "is_collaborative": is_collab,
            "region": st.session_state.ngo_data.get("region", ""),
        }
        navigate("ngo_results")
        st.rerun()


# ── 4. NGO Results — Matched Companies ───────────────────────────────────

def page_ngo_results():
    _back_button("ngo_project")
    st.markdown("## Matched Companies")

    pd = st.session_state.proposal_data
    matches = st.session_state.matched_companies

    st.markdown(
        f"""
        <div class="card">
            <strong>{pd.get('title','')}</strong><br>
            <span class="tag-domain">{pd.get('domain','')}</span>
            &nbsp; Ask: <strong>₹{pd.get('ask_lakhs',0)} Lakhs</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if matches:
        st.markdown(f"**{len(matches)}** companies match your criteria:")
        selected = []
        for m in matches:
            checked = st.checkbox(
                f"{m['Name']}  —  Budget: ₹{m['Budget_Lakhs']}L  |  SIS: {m['SIS_Score']}",
                key=f"sel_{m['Company_ID']}",
            )
            if checked:
                selected.append(m["Company_ID"])

        if st.button("Send Proposals", use_container_width=True):
            if not selected:
                st.warning("Please select at least one company.")
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
                        f'<div class="success-box">✓ {len(result.get("proposals_created",[]))} proposal(s) sent successfully!</div>',
                        unsafe_allow_html=True,
                    )
    else:
        st.info("No companies matched your criteria for solo funding.")
        if pd.get("is_collaborative"):
            st.markdown("Since you opted for collaboration, we'll create a **collaborative funding request** visible to all companies in this domain.")
            if st.button("Create Collaboration Request", use_container_width=True):
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
                        f'<div class="success-box">✓ Collaboration request created! ID: {result["collaboration_created"]}</div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.caption("Tip: Check the collaboration option to open your project to pooled funding from multiple companies.")


# ── 5. Company Login ──────────────────────────────────────────────────────

def page_company_login():
    _back_button("landing")
    st.markdown("## Company Portal")
    st.caption("Enter your Company ID to access your dashboard.")

    companies = api_get("/companies")
    if not companies:
        return

    company_map = {f"{c['Name']} ({c['Company_ID']})": c["Company_ID"] for c in companies}
    selected = st.selectbox("Select your company", list(company_map.keys()))

    if st.button("View Dashboard →", use_container_width=True):
        st.session_state.company_id = company_map[selected]
        navigate("company_dashboard")
        st.rerun()


# ── 6. Company Dashboard ─────────────────────────────────────────────────

def page_company_dashboard():
    _back_button("company_login")

    data = api_get(f"/company/{st.session_state.company_id}/dashboard")
    if not data:
        return

    comp = data["company"]
    feed = data["feed"]

    # Header
    st.markdown(f"## {comp['Name']}")
    st.markdown(f'<div class="sis-badge">🏆 Social Impact Score: {comp["SIS_Score"]}</div>', unsafe_allow_html=True)

    # Metrics
    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-value">₹{comp['Budget_Lakhs']}L</div>
                <div class="metric-label">Available Budget</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{len([f for f in feed if f['type']=='proposal'])}</div>
                <div class="metric-label">Pending Proposals</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{len([f for f in feed if f['type']=='collaboration'])}</div>
                <div class="metric-label">Active Collabs</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not feed:
        st.info("No proposals or collaborations available at this time.")
        return

    st.markdown("### Proposals Feed")

    for item in feed:
        _render_feed_item(item, comp)


def _render_feed_item(item, comp):
    """Render a single proposal or collaboration card with action buttons."""
    is_priority = item.get("is_priority_region", False)
    is_collab = item["type"] == "collaboration"

    # Tags
    tags_html = ""
    if is_priority:
        tags_html += '<span class="tag-priority">⚡ High Priority Region — 2.5× SIS</span>'
    if is_collab:
        tags_html += '<span class="tag-collab">🤝 Collab</span>'
    tags_html += f'<span class="tag-domain">{item.get("Domain","")}</span>'

    # Title & description
    title = item.get("Title", "Untitled")
    desc = item.get("Description", "")
    region = item.get("Region", "")
    ask = float(item.get("Ask_Lakhs", 0) or item.get("Total_Ask_Lakhs", 0))

    card_inner = f"""
        {tags_html}
        <h3 style="margin: 10px 0 4px 0; font-size: 1.15rem; color: #0F172A;">{title}</h3>
        <p style="color: #334155; font-size: 0.92rem; margin: 0 0 8px 0; line-height: 1.5;">{desc}</p>
        <p style="color: #475569; font-size: 0.85rem; margin: 0; font-weight: 500;">
            📍 {region} &nbsp;|&nbsp; 💰 ₹{ask} Lakhs
        </p>
    """

    # Progress bar for collabs
    if is_collab:
        pledged = float(item.get("Current_Pledged_Lakhs", 0))
        total = float(item.get("Total_Ask_Lakhs", 1))
        pct = min(100, int((pledged / total) * 100)) if total > 0 else 0
        card_inner += f"""
        <div style="margin-top:10px;">
            <span style="font-size:0.85rem; color:#475569; font-weight: 500;">Pledged: ₹{pledged}L / ₹{total}L ({pct}%)</span>
            <div class="progress-outer">
                <div class="progress-inner" style="width:{pct}%;"></div>
            </div>
        </div>
        """

    st.markdown(f'<div class="card">{card_inner}</div>', unsafe_allow_html=True)

    # ── Action Buttons ────────────────────────────────────────────
    if is_collab:
        collab_id = item.get("Collab_ID", "")
        c1, c2 = st.columns(2)
        with c1:
            pledge_amt = st.number_input(
                "Pledge Amount (₹ Lakhs)",
                min_value=1.0,
                max_value=float(comp["Budget_Lakhs"]),
                value=min(10.0, float(comp["Budget_Lakhs"])),
                step=1.0,
                key=f"pledge_{collab_id}",
            )
            if st.button("Pledge", key=f"btn_pledge_{collab_id}", use_container_width=True):
                result = api_post("/company/action/pledge", {
                    "collab_id": collab_id,
                    "company_id": comp["Company_ID"],
                    "pledge_amount": pledge_amt,
                })
                if result:
                    msg = "✓ Pledge recorded!"
                    if result.get("fulfilled"):
                        msg = "✓ Collaboration fully funded! Deal created."
                    st.markdown(f'<div class="success-box">{msg}</div>', unsafe_allow_html=True)
                    st.rerun()
        with c2:
            total_ask_val = float(item.get("Total_Ask_Lakhs", 0))
            if float(comp["Budget_Lakhs"]) >= total_ask_val:
                if st.button("⚡ Solo Takeover", key=f"btn_solo_{collab_id}", use_container_width=True):
                    result = api_post("/company/action/solo_takeover", {
                        "collab_id": collab_id,
                        "company_id": comp["Company_ID"],
                    })
                    if result:
                        st.markdown(
                            f'<div class="success-box">✓ Solo takeover complete! SIS awarded: {result.get("sis_awarded",0)}</div>',
                            unsafe_allow_html=True,
                        )
                        st.rerun()
            else:
                st.caption("Budget insufficient for solo takeover.")
    else:
        # Solo proposal
        proposal_id = item.get("Proposal_ID", "")
        if st.button("Accept Proposal", key=f"btn_accept_{proposal_id}", use_container_width=True):
            result = api_post("/company/action/accept", {
                "proposal_id": proposal_id,
                "company_id": comp["Company_ID"],
            })
            if result:
                st.markdown(
                    f'<div class="success-box">✓ Proposal accepted! Deal created. SIS awarded: {result.get("sis_awarded",0)}</div>',
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
