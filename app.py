# pylint: disable = invalid-name
import os
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import streamlit as st
from dotenv import load_dotenv

from agents.agent import Agent

# Load environment variables
load_dotenv()


def send_email(receiver_email: str, subject: str, body: str):
    """
    Sends an email using Gmail SMTP with credentials from .env
    """
    try:
        gmail_user = os.environ.get("GMAIL_USER")
        gmail_pass = os.environ.get("GMAIL_PASS")

        if not gmail_user or not gmail_pass:
            st.error("❌ Gmail credentials not found in environment variables.")
            return

        # Compose email
        msg = MIMEMultipart()
        msg["From"] = gmail_user
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send email via Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, receiver_email, msg.as_string())

        st.success("✅ Email sent successfully!")

    except Exception as e:
        st.error(f"❌ Error sending email: {e}")


def initialize_agent():
    if "agent" not in st.session_state:
        st.session_state.agent = Agent()
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())


def render_custom_css():
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-bottom: 2rem;
        }
        body {
            background-color: #f5f7fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-title {
            font-size: 3em;
            color: #0f4c81;
            text-align: center;
            margin-bottom: 0.2em;
            font-weight: 700;
        }
        .sub-title {
            font-size: 1.2em;
            color: #333;
            text-align: left;
            margin-bottom: 1em;
        }
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            width: 100%;
            padding: 0;
        }
        .query-container:hover, .query-box:hover {
            box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        }
        textarea[placeholder] {
            border-radius: 8px !important;
            border: 1px solid #ccc !important;
            padding: 0.8em !important;
            font-size: 1em !important;
        }
        .css-1aumxhk img {
            border-radius: 12px;
            border: 2px solid #0f4c81;
        }
        button[kind="primary"] {
            background-color: #0f4c81 !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 0.5em 1.2em !important;
            transition: background-color 0.3s ease-in-out;
        }
        button[kind="primary"]:hover {
            background-color: #073b5c !important;
            color: blue !important;
        }
        .streamlit-expanderHeader {
            font-weight: 600 !important;
            color: #0f4c81 !important;
        }
        input[type=text] {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 0.5em;
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_ui():
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    st.markdown('<div class="main-title"> Wayfinder </div>', unsafe_allow_html=True)
    st.markdown('<div class="query-container">', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Enter your travel query and get flight, hotel, and attraction information:</div>',
        unsafe_allow_html=True,
    )

    user_input = st.text_area(
        "Travel Query",
        height=200,
        key="query",
        placeholder="Type your travel query here...",
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.sidebar.image("images/ai-travel.png")
    return user_input


def process_query(user_input):
    if user_input:
        try:
            thread_id = st.session_state.thread_id
            result = st.session_state.agent.run(user_input, thread_id)

            st.subheader("Travel Information")
            st.write(result["messages"][-1].content)

            # Save structured travel_info for later email
            st.session_state.travel_info = result["messages"][-1].content
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a travel query.")


def render_email_form():
    if "travel_info" not in st.session_state:
        return

    send_email_option = st.radio(
        "Do you want to send this information via email?", ("No", "Yes")
    )
    if send_email_option == "Yes":
        with st.form(key="email_form"):
            gmail_user = os.environ.get("GMAIL_USER")
            st.text_input("Sender Email", value=gmail_user, disabled=True)

            receiver_email = st.text_input("Receiver Email")
            subject = st.text_input("Email Subject", "Travel Information")
            submit_button = st.form_submit_button(label="Send Email")

        if submit_button:
            if receiver_email and subject:
                send_email(receiver_email, subject, st.session_state.travel_info)
            else:
                st.error("Please fill out all email fields.")


def main():
    initialize_agent()
    render_custom_css()
    user_input = render_ui()

    if st.button("Get Travel Information"):
        process_query(user_input)

    render_email_form()


if __name__ == "__main__":
    main()
