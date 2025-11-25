import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import time

db_engine = create_engine('postgresql://admin:password123@localhost:5432/bank_data')

st.set_page_config(
    page_title ="Real-Time Fraud Monitor",
    page_icon = "🚨",
    layout="wide",
)

st.title("🛡️ UPI Fraud Detection System")

col1, col2 = st.columns(2)
placeholder = st.empty()

def load_data():
    query = "SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, db_engine)

    with db_engine.connect() as conn:
        total_count = conn.execute(text("SELECT COUNT(*) FROM transactions")).scalar()
        fraud_count = conn.execute(text("SELECT COUNT(*) FROM transactions WHERE is_fraud_flag = 1")).scalar()

    return df, total_count, fraud_count
while True:
    df, total_txns, fraud_total = load_data()

    with placeholder.container():
        kpi1, kpi2, kpi3 = st.columns(3)

        kpi1.metric(label="Total Transactions Processed", value=total_txns)
        kpi2.metric(label="Total Fraud Detected", value=fraud_total, delta_color="inverse")

        fraud_rate = (fraud_total/total_txns * 100) if total_txns > 0 else 0
        kpi3.metric(label="Current Fraud Rate", value=f"{fraud_rate:.2f}%")

        st.subheader("🚨 Recent Security Alerts")

        fraud_df = df[df['is_fraud_flag'] == 1]

        if not fraud_df.empty:
            st.dataframe(
                fraud_df[['timestamp', 'sender_vpa', 'amount_inr', 'location', 'flag_reason']],
                use_container_width = True,
                hide_index = True
            )
        else:
            st.success("No recent threats detected.")
    time.sleep(1)