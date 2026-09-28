import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Router Dashboard", layout="wide")
st.title("⚡ Semantic Cache & Cost-Aware Router")

API = st.sidebar.text_input("API URL", "http://localhost:8000")
q = st.text_area("Ask something", "Explain Python lists in simple terms.")

if st.button("Run Query", type="primary"):
    r = requests.post(f"{API}/query", json={"query": q}, timeout=120)
    if r.ok:
        data = r.json()
        st.success("Completed")
        st.write(data["answer"])
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Model", data["model"])
        c2.metric("Cache Hit", str(data["cache_hit"]))
        c3.metric("Latency", f'{data["latency_ms"]} ms')
        c4.metric("Cost", f'${data["estimated_cost"]}')
    else:
        st.error(r.text)

st.divider()
if st.button("Refresh Metrics"):
    m = requests.get(f"{API}/metrics", timeout=10).json()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Requests", m["total_requests"])
    c2.metric("Cache Hit Rate", f'{m["cache_hit_rate_percent"]}%')
    c3.metric("Avg Latency", f'{m["average_latency_ms"]} ms')
    c4.metric("Estimated Cost", f'${m["estimated_total_cost_usd"]}')
