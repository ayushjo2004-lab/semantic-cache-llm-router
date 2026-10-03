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
st.subheader("Router Metrics")
if st.button("Refresh Metrics"):
    st.rerun()

try:
    response = requests.get(f"{API}/metrics", timeout=10)
    response.raise_for_status()
    m = response.json()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Requests", m["total_requests"])
    c2.metric("Cache Hit Rate", f'{m["cache_hit_rate_percent"]}%')
    c3.metric("Avg Latency", f'{m["average_latency_ms"]} ms')
    c4.metric("Estimated Cost", f'${m["estimated_total_cost_usd"]}')
    c5,c6 = st.columns(2)
    c5.metric("Cache Hits", m["cache_hits"])
    c6.metric("Cache Misses", m["cache_misses"])

    left, right = st.columns(2)
    with left:
        st.subheader("Model Usage")
        st.dataframe(pd.DataFrame(m["model_usage"]), hide_index=True, use_container_width=True)
    with right:
        st.subheader("Recent Requests")
        st.dataframe(pd.DataFrame(m["recent_requests"]), hide_index=True, use_container_width=True)
except requests.RequestException as exc:
    st.error(f"Could not load API metrics: {exc}")
except (KeyError, ValueError) as exc:
    st.error(f"The API returned an unexpected metrics response: {exc}")
