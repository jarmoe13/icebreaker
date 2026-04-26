import os
from datetime import datetime, timezone
import pandas as pd
import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Build Your Lyreco 2026", page_icon="🔵", layout="centered")

LYRECO_BLUE = "#00374B"
LIGHT_BLUE = "#EAF3F8"
GREEN = "#78BE20"

st.markdown(f"<style>.stApp{{background-color:white;}}</style>", unsafe_allow_html=True)

@st.cache_resource
def get_supabase_client():
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_KEY", "")
    if not url or not key:
        return None
    return create_client(url, key)

def save_response(score, persona):
    client = get_supabase_client()
    if client:
        client.table("lyreco_2026_responses").insert({
            "created_at": datetime.now(timezone.utc).isoformat(),
            "score": score,
            "persona": persona
        }).execute()

questions = [
    ("How should customers find what they need?", {"A":10,"B":20,"C":30}),
    ("How should we support customers?", {"A":10,"B":20,"C":30}),
    ("What matters most?", {"A":10,"B":20,"C":30}),
    ("Role of webshop?", {"A":10,"B":20,"C":30}),
    ("Future focus?", {"A":10,"B":20,"C":30})
]

answers = []
for q, opts in questions:
    answers.append(opts[st.radio(q, list(opts.keys()))])

if st.button("Show result"):
    score = int(sum(answers)/150*100)
    if score<=50: persona="Legacy Keeper"
    elif score<=75: persona="Hybrid Optimizer"
    else: persona="2026 Growth Driver"
    st.write(f"You are {persona}, score {score}")
    save_response(score, persona)
