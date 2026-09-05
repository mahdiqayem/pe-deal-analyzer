import streamlit as st
import pandas as pd
import plotly.express as px
from pe_engine import run_deal, run_scenarios, sensitivity_analysis

st.title("Private Equity Deal Analyzer")

st.subheader("Deal Terms")
investment = st.number_input("Investment ($)", min_value=1, value=2_000_000, step=100_000)
ownership_pct = st.slider("Ownership (%)", 0, 100, 50) / 100
holding_period = st.slider("Holding Period (years)", 1, 10, 5)

st.subheader("Operating Assumptions")
entry_revenue = st.number_input("Entry Revenue ($)", min_value=0, value=5_000_000, step=100_000)
ebitda_margin = st.slider("EBITDA Margin (%)", 0, 100, 20) / 100
growth_rate = st.slider("Growth Rate (%)", -10, 40, 15) / 100

st.subheader("Exit Assumptions")
exit_multiple = st.number_input("Exit Multiple (x)", min_value=1.0, value=8.0, step=0.5)

try:
    result = run_deal(
        investment=investment, ownership_pct=ownership_pct, entry_revenue=entry_revenue,
        ebitda_margin=ebitda_margin, growth_rate=growth_rate,
        exit_multiple=exit_multiple, holding_period=holding_period,
    )
    st.metric("MOIC", f"{result['moic']:.2f}x")
    st.metric("IRR", f"{result['irr']:.1%}")
except ValueError as e:
    st.error(f"Invalid input: {e}")

st.subheader("Cash Flow Projection")
cash_flow_data = pd.DataFrame({
    "Year": range(holding_period + 1),
    "Cash Flow": result["cash_flows"]
})
fig = px.bar(
    cash_flow_data,
    x="Year",
    y="Cash Flow",
    title="Cash Flow Projection"
)
st.plotly_chart(fig)

st.subheader("Scenario Comparison")
scenarios = run_scenarios(
    investment=investment, ownership_pct=ownership_pct, entry_revenue=entry_revenue,
    ebitda_margin=ebitda_margin, holding_period=holding_period,
)
col1, col2, col3 = st.columns(3)
for col, name in zip([col1, col2, col3], ["bear", "base", "bull"]):
    with col:
        st.metric(f"{name.capitalize()} MOIC", f"{scenarios[name]['moic']:.2f}x")
        st.metric(f"{name.capitalize()} IRR", f"{scenarios[name]['irr']:.1%}")

scenario_data = pd.DataFrame({
    "Scenario": ["Bear", "Base", "Bull"],
    "MOIC": [scenarios["bear"]["moic"], scenarios["base"]["moic"], scenarios["bull"]["moic"]],
})
fig = px.bar(scenario_data, x="Scenario", y="MOIC", title="MOIC by Scenario")
st.plotly_chart(fig)

st.subheader("Sensitivity Analysis")
growth_rates = [0.05, 0.10, 0.15, 0.20, 0.25]
exit_multiples = [6, 7, 8, 9, 10]
grid = sensitivity_analysis(
    investment=investment, ownership_pct=ownership_pct, entry_revenue=entry_revenue,
    ebitda_margin=ebitda_margin, holding_period=holding_period,
    growth_rates=growth_rates, exit_multiples=exit_multiples,
)
st.dataframe(grid)

st.subheader("Sensitivity Heatmap")

fig = px.imshow(
    grid,
    labels={
        "x": "Exit Multiple",
        "y": "Growth Rate",
        "color": "MOIC"
    },
    text_auto=True,
    title="MOIC Sensitivity Analysis",
    aspect="auto"
)

st.plotly_chart(fig)

