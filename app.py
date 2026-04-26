from pathlib import Path
import zipfile, textwrap

base = Path("/mnt/data/lyreco_2026_streamlit_app")
base.mkdir(exist_ok=True)

app_py = r'''
import os
from datetime import datetime, timezone

import pandas as pd
import streamlit as st
from supabase import create_client


# =========================
# Basic setup
# =========================

st.set_page_config(
    page_title="Build Your Lyreco 2026",
    page_icon="🔵",
    layout="centered"
)

LYRECO_BLUE = "#00374B"
LYRECO_BLUE_HOVER = "#00506B"
LIGHT_BLUE = "#EAF3F8"
GREEN = "#78BE20"
TEXT = "#1F2933"


# =========================
# Styling
# =========================

st.markdown(f"""
<style>
.stApp {{
    background-color: #FFFFFF;
    color: {TEXT};
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 880px;
}}

.header {{
    background-color: {LYRECO_BLUE};
    padding: 30px;
    border-radius: 22px;
    color: white;
    margin-bottom: 20px;
}}

.header h1 {{
    margin-bottom: 0.3rem;
}}

.green-line {{
    height: 5px;
    width: 100%;
    background-color: {GREEN};
    border-radius: 999px;
    margin: 12px 0 28px 0;
}}

.card {{
    background-color: {LIGHT_BLUE};
    padding: 20px 22px;
    border-radius: 18px;
    margin: 18px 0 8px 0;
    border-left: 6px solid {LYRECO_BLUE};
}}

.result-card {{
    background-color: {LYRECO_BLUE};
    color: white;
    padding: 30px;
    border-radius: 24px;
    margin-top: 28px;
}}

.metric-card {{
    background-color: {LIGHT_BLUE};
    border-radius: 18px;
    padding: 20px;
    border-left: 6px solid {LYRECO_BLUE};
}}

.small-note {{
    color: #52616B;
    font-size: 0.95rem;
}}

.stButton > button {{
    background-color: {LYRECO_BLUE};
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
    border: none;
    font-weight: 700;
}}

.stButton > button:hover {{
    background-color: {LYRECO_BLUE_HOVER};
    color: white;
    border: none;
}}

div[role="radiogroup"] label {{
    background: white;
    padding: 10px 12px;
    border-radius: 12px;
    margin-bottom: 6px;
    border: 1px solid #D9E2EC;
}}

div[role="radiogroup"] label:hover {{
    border-color: {LYRECO_BLUE};
}}
</style>
""", unsafe_allow_html=True)


# =========================
# Supabase connection
# =========================

@st.cache_resource
def get_supabase_client():
    """
    Reads Supabase credentials from Streamlit secrets.

    Required in .streamlit/secrets.toml:
    SUPABASE_URL = "..."
    SUPABASE_KEY = "..."
    """
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")

    if not url or not key:
        return None

    return create_client(url, key)


def save_response(score, persona, answers):
    client = get_supabase_client()
    if client is None:
        st.warning(
            "Database is not configured yet. Your result is shown, but it was not saved to the team dashboard."
        )
        return False

    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "score": int(score),
        "persona": persona,
        "q1": answers[0],
        "q2": answers[1],
        "q3": answers[2],
        "q4": answers[3],
        "q5": answers[4],
    }

    try:
        client.table("lyreco_2026_responses").insert(payload).execute()
        return True
    except Exception as exc:
        st.error(f"Could not save response: {exc}")
        return False


def load_responses():
    client = get_supabase_client()
    if client is None:
        return pd.DataFrame()

    try:
        result = (
            client
            .table("lyreco_2026_responses")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return pd.DataFrame(result.data)
    except Exception as exc:
        st.error(f"Could not load dashboard data: {exc}")
        return pd.DataFrame()


# =========================
# Quiz content
# =========================

QUESTIONS = [
    {
        "question": "1. How should customers find what they need?",
        "options": {
            "Reliable Foundations": 10,
            "Smart Efficiency": 20,
            "Future Growth": 30,
        },
    },
    {
        "question": "2. How should we support customers?",
        "options": {
            "Phone-first and human-led": 10,
            "Chat, FAQ and guided self-service": 20,
            "Proactive digital guidance": 30,
        },
    },
    {
        "question": "3. What matters most in the order journey?",
        "options": {
            "Reliability": 10,
            "Speed and efficiency": 20,
            "Personalization": 30,
        },
    },
    {
        "question": "4. What is the webshop’s role?",
        "options": {
            "Digital catalog": 10,
            "Transaction channel": 20,
            "Growth engine": 30,
        },
    },
    {
        "question": "5. What should Lyreco optimize for in the next 100 years?",
        "options": {
            "Operational excellence": 10,
            "Customer experience": 20,
            "Intelligent, sustainable growth": 30,
        },
    },
]


def calculate_result(answer_values):
    total = sum(answer_values)
    score = round((total / 150) * 100)

    if score <= 50:
        persona = "Legacy Keeper"
        message = (
            "You value reliability, structure and the foundations that helped "
            "Lyreco grow over the last 100 years."
        )
    elif score <= 75:
        persona = "Hybrid Optimizer"
        message = (
            "You combine Lyreco’s operational strength with a clear push toward "
            "smarter, more customer-centric digital commerce."
        )
    else:
        persona = "2026 Growth Driver"
        message = (
            "You are ready to move fast, experiment, personalize and shape the "
            "next chapter of Lyreco eCommerce."
        )

    return score, persona, message


# =========================
# Shared header
# =========================

def render_header():
    st.markdown("""
    <div class="header">
        <h1>Build Your Lyreco 2026</h1>
        <p>100 years behind us. 30 seconds to shape what comes next.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="green-line"></div>', unsafe_allow_html=True)


# =========================
# Participant view
# =========================

def participant_view():
    render_header()

    st.write(
        "Answer 5 quick questions and discover your digital commerce profile. "
        "No names, no login — just your instant result."
    )

    if "submitted_once" not in st.session_state:
        st.session_state.submitted_once = False

    with st.form("lyreco_quiz"):
        answer_values = []
        answer_labels = []

        for item in QUESTIONS:
            st.markdown(f"""
            <div class="card">
                <h4>{item["question"]}</h4>
            </div>
            """, unsafe_allow_html=True)

            label = st.radio(
                label=item["question"],
                options=list(item["options"].keys()),
                label_visibility="collapsed"
            )
            answer_labels.append(label)
            answer_values.append(item["options"][label])

        submitted = st.form_submit_button("Show my result")

    if submitted:
        score, persona, message = calculate_result(answer_values)

        st.markdown(f"""
        <div class="result-card">
            <h2>You are a {persona}</h2>
            <h3>Digital Maturity Score: {score}/100</h3>
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.submitted_once:
            saved = save_response(score, persona, answer_labels)
            st.session_state.submitted_once = True
            if saved:
                st.success("Your result was added to the team snapshot.")
        else:
            st.info("Your result is already counted in the team snapshot.")

        st.markdown(
            '<p class="small-note">Keep your result — we’ll compare profiles together in the discussion.</p>',
            unsafe_allow_html=True
        )


# =========================
# Admin view
# =========================

def admin_view():
    render_header()

    st.subheader("Team snapshot")
    st.caption("Share this view on Teams after people have completed the challenge.")

    if st.button("Refresh dashboard"):
        st.rerun()

    df = load_responses()

    if df.empty:
        st.info("No responses yet. Share the participant link in Teams chat.")
        return

    response_count = len(df)
    avg_score = round(df["score"].mean())
    top_persona = df["persona"].mode().iloc[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{response_count}</h2>
            <p>responses</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{avg_score}/100</h2>
            <p>average score</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{top_persona}</h2>
            <p>team tendency</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Persona distribution")
    persona_counts = (
        df["persona"]
        .value_counts()
        .rename_axis("persona")
        .reset_index(name="count")
    )
    st.bar_chart(persona_counts.set_index("persona"))

    st.subheader("Score distribution")
    st.bar_chart(df[["score"]])

    with st.expander("Raw responses"):
        st.dataframe(df[["created_at", "score", "persona", "q1", "q2", "q3", "q4", "q5"]])


# =========================
# Routing
# =========================

query_params = st.query_params
is_admin = query_params.get("admin", "false").lower() == "true"

if is_admin:
    admin_view()
else:
    participant_view()
'''

requirements = '''streamlit
supabase
pandas
'''

sql = '''
-- Run this in Supabase SQL Editor

create table if not exists lyreco_2026_responses (
    id bigint generated by default as identity primary key,
    created_at timestamptz not null default now(),
    score int not null,
    persona text not null,
    q1 text,
    q2 text,
    q3 text,
    q4 text,
    q5 text
);

-- Simple policy setup for this internal event app.
-- Use the anon public key in Streamlit secrets.
-- For a one-off internal icebreaker this is intentionally simple.

alter table lyreco_2026_responses enable row level security;

drop policy if exists "Allow inserts for event app" on lyreco_2026_responses;
create policy "Allow inserts for event app"
on lyreco_2026_responses
for insert
to anon
with check (true);

drop policy if exists "Allow reads for event dashboard" on lyreco_2026_responses;
create policy "Allow reads for event dashboard"
on lyreco_2026_responses
for select
to anon
using (true);
'''

secrets_template = '''
# Add this in Streamlit Community Cloud:
# App settings → Secrets

SUPABASE_URL = "https://YOUR-PROJECT.supabase.co"
SUPABASE_KEY = "YOUR-SUPABASE-ANON-PUBLIC-KEY"
'''

readme = '''
# Build Your Lyreco 2026

A tiny Streamlit icebreaker app for a Lyreco eCommerce team event.

## Views

Participant view:

```text
https://your-app.streamlit.app
