import numpy as np
import pandas as pd
import streamlit as st
from starter import COSTS, PROMISE, TIME_BLOCKS, ZONES, delivery_times


def cost_per_late_order(costs):
    refund_cost = costs["refund"]
    churn_cost = costs["churn_orders"]
    margin_cost = costs["margin"]
    return refund_cost + churn_cost * margin_cost


def choose_best_promise(zone, time_block, promises, costs):
    best_promise = None
    best_net_profit = -np.inf
    all_results = []
    late_order_costs = cost_per_late_order(costs)

    for promise in promises:
        times = np.asarray(delivery_times(zone, time_block, promise, seed=77))
        total_orders = len(times)
        late_orders = np.sum(times > promise)
        profit_from_orders = total_orders * costs["margin"]
        total_late_cost = late_orders * late_order_costs
        net_profit = profit_from_orders - total_late_cost
        all_results.append((promise, total_orders, late_orders, net_profit))

        if net_profit > best_net_profit:
            best_net_profit = net_profit
            best_promise = promise

    return best_promise, best_net_profit, all_results


st.set_page_config(page_title="Rosa's Pizza | Delivery Promise", page_icon="🍕")
st.title("Rosa's Pizza delivery promise")
st.caption(f"Current promise in the starter data: {PROMISE} minutes")

with st.form("promise_calculation"):
    zone_col, block_col = st.columns(2)
    with zone_col:
        selected_zone = st.selectbox("Delivery zone", options=list(ZONES))
    with block_col:
        selected_time_block = st.selectbox("Time block", options=list(TIME_BLOCKS))

    st.subheader("Promises to test")
    min_col, max_col = st.columns(2)
    with min_col:
        minimum_promise = st.number_input(
            "Minimum (minutes)", min_value=5, max_value=180, value=5, step=5
        )
    with max_col:
        maximum_promise = st.number_input(
            "Maximum (minutes)", min_value=5, max_value=180, value=95, step=5
        )

    st.subheader("Per-order economics")
    margin_col, churn_col, refund_col = st.columns(3)
    with margin_col:
        margin = st.number_input(
            "Profit margin ($)",
            min_value=0.0,
            value=float(COSTS["margin"]),
            step=0.5,
            format="%.2f",
        )
    with churn_col:
        churn_orders = st.number_input(
            "Estimated churn per late order (orders)",
            min_value=0.0,
            value=float(COSTS["churn_orders"]),
            step=0.1,
            format="%.1f",
        )
    with refund_col:
        refund = st.number_input(
            "Refund per late order ($)",
            min_value=0.0,
            value=float(COSTS["refund"]),
            step=0.5,
            format="%.2f",
        )

    calculate = st.form_submit_button("Calculate best promise", type="primary")

if calculate:
    if maximum_promise < minimum_promise:
        st.error("The maximum promise must be greater than or equal to the minimum.")
    else:
        promises = list(range(int(minimum_promise), int(maximum_promise) + 1, 5))
        costs = {
            "margin": margin,
            "churn_orders": churn_orders,
            "refund": refund,
        }
        best_promise, best_net_profit, results = choose_best_promise(
            selected_zone, selected_time_block, promises, costs
        )

        result_col, profit_col = st.columns(2)
        result_col.metric("Recommended promise", f"{best_promise} minutes")
        profit_col.metric("Best net profit", f"${best_net_profit:,.2f}")

        st.dataframe(
            pd.DataFrame(
                results,
                columns=["Promise (min)", "Total orders", "Late orders", "Net profit ($)"],
            ).style.format({"Net profit ($)": "${:,.2f}"}),
            hide_index=True,
            width="stretch",
        )