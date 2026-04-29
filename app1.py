import streamlit as st

st.set_page_config(
    page_title="Election Assistant",
    page_icon="🗳️",
    layout="centered"
)

election_steps = [
    {"step": 1, "title": "Check Eligibility", "description": "You must be 18+ and a citizen of India.", "documents": ["Age proof", "Address proof"], "next": "Register as Voter"},
    {"step": 2, "title": "Register as Voter", "description": "Fill Form 6 online or offline.", "documents": ["Aadhaar Card", "Passport size photo"], "next": "Get Voter ID"},
    {"step": 3, "title": "Get Voter ID", "description": "After verification, you will receive your Voter ID.", "documents": [], "next": "Find Polling Booth"},
    {"step": 4, "title": "Find Polling Booth", "description": "Check your assigned polling station.", "documents": ["Voter ID"], "next": "Voting Day Process"},
    {"step": 5, "title": "Voting Day Process", "description": "Go to booth, verify identity, cast vote using EVM.", "documents": ["Voter ID"], "next": "Results & Counting"},
    {"step": 6, "title": "Results & Counting", "description": "Votes are counted and results are announced.", "documents": [], "next": "Done"}
]

def get_next_step(age, registered, step, first_time):
    if age < 18:
        return "❌ You are not eligible to vote yet."

    if first_time:
        if registered == "No":
            return "👋 First-time voter guide: Start by registering yourself using Form 6."
        else:
            return "📍 First-time voter guide: Find your polling booth and keep your documents ready."

    if registered == "No":
        return "📝 Please register using Form 6."

    return f"➡️ Your next step is: {election_steps[step]['title']}"

def chatbot_response(question):
    question = question.lower()

    keywords = {
        "register": "Fill Form 6 online or offline to register as a voter.",
        "documents": "You need Aadhaar Card, address proof, and a passport-size photo.",
        "vote": "Visit your polling booth with your voter ID and cast your vote using EVM.",
        "evm": "EVM means Electronic Voting Machine. It is used to record votes securely.",
        "eligibility": "You must be 18+ and an Indian citizen.",
        "first": "If you are a first-time voter, first check eligibility, then register, then find your polling booth."
    }

    for key in keywords:
        if key in question:
            return keywords[key]

    return "Try asking about registration, voting, EVM, eligibility, first-time voter, or documents."

if "step" not in st.session_state:
    st.session_state.step = 0

st.sidebar.header("👤 Your Details")
age = st.sidebar.number_input("Enter your age", min_value=0, max_value=120, value=18)
registered = st.sidebar.selectbox("Are you registered to vote?", ["No", "Yes"])
first_time = st.sidebar.checkbox("Are you a first-time voter?")

st.title("🗳️ Election Assistant")

st.markdown("""
### 🇮🇳 Welcome to the Election Assistant

This app helps you:
- Understand the election process
- Know what to do next
- Ask questions easily

👉 Perfect for first-time voters!
""")

if first_time:
    st.info("👋 Welcome! Since you are a first-time voter, this app will guide you step-by-step.")

progress = (st.session_state.step + 1) / len(election_steps)
st.progress(progress)

if first_time:
    st.success(f"🚀 You're on Step {st.session_state.step + 1} of your voting journey!")

st.subheader("🧭 Election Process Overview")
for step in election_steps:
    if step["step"] == st.session_state.step + 1:
        st.markdown(f"✅ **Step {step['step']}: {step['title']}**")
    else:
        st.markdown(f"Step {step['step']}: {step['title']}")

current = election_steps[st.session_state.step]

st.divider()
st.subheader(f"Step {current['step']}: {current['title']}")
st.write(current["description"])

if current["documents"]:
    st.write("📄 Required Documents:")
    for doc in current["documents"]:
        st.write(f"- {doc}")

col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Previous Step"):
        if st.session_state.step > 0:
            st.session_state.step -= 1
            st.rerun()

with col2:
    if st.button("➡️ Next Step"):
        if st.session_state.step < len(election_steps) - 1:
            st.session_state.step += 1
            st.rerun()

if st.button("🤖 What should I do next?"):
    suggestion = get_next_step(age, registered, st.session_state.step, first_time)
    st.success(suggestion)

if st.session_state.step == len(election_steps) - 1:
    st.success("🎉 You’ve completed the election process guide!")

st.divider()
st.header("💬 Ask Election Assistant")

user_question = st.text_input("Type your question here...", key="chat_input")

if user_question:
    with st.chat_message("user"):
        st.write(user_question)

    with st.chat_message("assistant"):
        answer = chatbot_response(user_question)
        st.write(answer)

st.divider()
st.caption("🔗 Data inspired by the Election Commission of India.")