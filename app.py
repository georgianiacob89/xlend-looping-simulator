import streamlit as st
import matplotlib.pyplot as plt
from simulation_engine import simulate_loop_position

st.title("xLend Looping Simulator")

st.sidebar.header("Simulation Parameters")

initial = st.sidebar.number_input(
    "Initial eGLD",
    min_value=1.0,
    value=100.0,
    step=1.0
)

ltv = st.sidebar.slider(
    "Target LTV",
    min_value=0.50,
    max_value=0.975,
    value=0.925,
    step=0.005
)

supply = st.sidebar.number_input(
    "xEGLD Supply APY (%)",
    min_value=0.0,
    value=16.5,
    step=0.1
) / 100.0

borrow = st.sidebar.number_input(
    "Normal Borrow APY (%)",
    min_value=0.0,
    value=12.0,
    step=0.1
) / 100.0

high_borrow = st.sidebar.number_input(
    "High Borrow APY (%)",
    min_value=0.0,
    value=21.0,
    step=0.1
) / 100.0

days = st.sidebar.number_input(
    "Days to simulate",
    min_value=1,
    max_value=3650,
    value=365,
    step=1
)

t, net, supply_curve, borrow_curve = simulate_loop_position(
    initial_capital=initial,
    ltv_target=ltv,
    days=days,
    supply_apr=supply,
    borrow_apr_normal=borrow,
    borrow_apr_high=high_borrow,
)

st.subheader("Final Results")

st.write(f"**Final net position:** {net[-1]:.2f} eGLD (start: {initial:.2f} eGLD)")
st.write(f"**Effective net APY (approx):** {(net[-1]/initial - 1)*100:.2f}%")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t, net, label="Net Position (eGLD)", color="orange")
ax.set_xlabel("Day")
ax.set_ylabel("Net Position (eGLD)")
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.subheader("Supply vs Borrow Over Time")

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(t, supply_curve, label="Total Supplied", linestyle="-")
ax2.plot(t, borrow_curve, label="Total Borrowed", linestyle="--")
ax2.set_xlabel("Day")
ax2.set_ylabel("Amount (eGLD)")
ax2.grid(True)
ax2.legend()
st.pyplot(fig2)
