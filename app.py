import streamlit as st

st.set_page_config(
    page_title="Build Your Lyreco 2026",
    page_icon="🔵",
    layout="centered"
)

LYRECO_BLUE = "#2D2E87"
GREEN = "#9AC31C"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@400;600;700&display=swap');

/* GLOBAL FONT + COLOR */
html, body, [class*="css"] {{
    font-family: 'Jost', sans-serif;
    color: {LYRECO_BLUE};
}}

.stApp {{
    background-color: white;
}}

/* HEADER */
.header {{
    background-color: {LYRECO_BLUE};
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 24px;
}}

/* FORCE WHITE TEXT IN HEADER */
.header *,
.header h1,
.header h1 span,
.header p,
.header p span {{
    color: white !important;
}}

/* QUESTION BLOCK */
.card {{
    background-color: white;
    padding: 16px 0 6px 16px;
    border-left: 6px solid {GREEN};
    margin-top: 24px;
    margin-bottom: 8px;
}}

/* RESULT */
.result-card {{
    background-color: {LYRECO_BLUE};
    padding: 28px;
    border-radius: 22px;
    margin-top: 24px;
}}

/* FORCE WHITE IN RESULT */
.result-card * {{
    color: white !important;
}}

/* GREEN LINE */
.green-line {{
    height: 5px;
    background-color: {GREEN};
    border-radius: 5px;
    margin: 16px 0 24px 0;
}}

/* BUTTON */
.stButton > button {{
    background-color: {LYRECO_BLUE};
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
    border: none;
    font-weight: 600;
}}

.stButton > button:hover {{
    background-color: #1f2065;
    color: white;
}}

/* RADIO COLOR FIX */
input[type="radio"] {{
    accent-color: {LYRECO_BLUE};
}}

[data-testid="stRadio"] input[type="radio"]:checked {{
    accent-color: {LYRECO_BLUE};
}}

/* TYPOGRAPHY */
h1, h2, h3, h4 {{
    font-weight: 600;
}}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>Build Your Lyreco 2026</h1>
    <p>100 years behind us. 30 seconds to shape what comes next.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="green-line"></div>', unsafe_allow_html=True)

st.write("Answer 5 quick questions and discover your digital commerce profile.")

questions = [
    {
        "question": "1. How should customers find what they need?",
        "options": {
            "Reliable Foundations": 10,
            "Smart Efficiency": 20,
            "Future Growth": 30
        }
    },
    {
        "question": "2. How should we support customers?",
        "options": {
            "Phone-first and human-led": 10,
            "Chat, FAQ and guided self-service": 20,
            "Proactive digital guidance": 30
        }
    },
    {
        "question": "3. What matters most in the order journey?",
        "options": {
            "Reliability": 10,
            "Speed and efficiency": 20,
            "Personalization": 30
        }
    },
    {
        "question": "4. What is the webshop’s role?",
        "options": {
            "Digital catalog": 10,
            "Transaction channel": 20,
            "Growth engine": 30
        }
    },
    {
        "question": "5. What should Lyreco optimize for in the next 100 years?",
        "options": {
            "Operational excellence": 10,
            "Customer experience": 20,
            "Intelligent, sustainable growth": 30
        }
    }
]

with st.form("lyreco_quiz"):
    answers = []

    for item in questions:
        st.markdown(f"""
        <div class="card">
            <h4>{item["question"]}</h4>
        </div>
        """, unsafe_allow_html=True)

        answer = st.radio(
            label=item["question"],
            options=list(item["options"].keys()),
            label_visibility="collapsed"
        )
        answers.append(item["options"][answer])

    submitted = st.form_submit_button("Show my result")

if submitted:
    total = sum(answers)
    score = round((total / 150) * 100)

    if score <= 50:
        persona = "Legacy Keeper"
        message = """
        You value reliability, structure and the foundations that helped Lyreco grow over the last 100 years.
        You believe that digital commerce should reinforce trust, not replace it.
        Your strength is stability — you ensure that innovation builds on solid ground.
        """
    elif score <= 75:
        persona = "Hybrid Optimizer"
        message = """
        You balance Lyreco’s operational strength with a clear push toward smarter digital commerce.
        You focus on solutions that are scalable, efficient and meaningful for customers.
        Your strength is integration — connecting today’s business with tomorrow’s opportunities.
        """
    else:
        persona = "2026 Growth Driver"
        message = """
        You are ready to move fast, experiment and shape the future of Lyreco eCommerce.
        You see digital as a strategic growth engine, not just a support channel.
        Your strength is momentum — pushing the organization toward bold, future-ready solutions.
        """

    st.markdown(f"""
    <div class="result-card">
        <h2>You are a {persona}</h2>
        <h3>Digital Maturity Score: {score}/100</h3>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)

    st.success("Keep your result — we’ll compare profiles together in the discussion.")
