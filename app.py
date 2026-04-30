import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global System Interactive Simulator",
    page_icon="🌍",
    layout="wide"
)

# ----------------------------
# Core model
# ----------------------------

DIMENSIONS = [
    "Incentive alignment",
    "Verifiable trust",
    "Shared reality",
    "Adaptation speed",
    "Infrastructure resilience",
    "Reinforcement quality",
    "Local-global balance",
    "Complexity management",
]

WEIGHTS = {
    "Incentive alignment": 1.25,
    "Verifiable trust": 1.20,
    "Shared reality": 1.20,
    "Adaptation speed": 1.15,
    "Infrastructure resilience": 1.10,
    "Reinforcement quality": 1.20,
    "Local-global balance": 1.05,
    "Complexity management": 1.10,
}

SCENARIOS = {
    "Balanced transition": {
        "AI pressure": 55,
        "Geopolitical pressure": 45,
        "Resource pressure": 50,
        "Social pressure": 45,
        "description": "Moderate pressure with enough time for systems to adapt."
    },
    "AI acceleration shock": {
        "AI pressure": 90,
        "Geopolitical pressure": 55,
        "Resource pressure": 55,
        "Social pressure": 70,
        "description": "Technology changes faster than education, labor markets, and policy."
    },
    "Geopolitical fragmentation": {
        "AI pressure": 65,
        "Geopolitical pressure": 90,
        "Resource pressure": 70,
        "Social pressure": 65,
        "description": "Coordination weakens and countries optimize for resilience and optionality."
    },
    "Infrastructure stress": {
        "AI pressure": 60,
        "Geopolitical pressure": 65,
        "Resource pressure": 90,
        "Social pressure": 70,
        "description": "Energy, water, transport, and supply systems become the bottleneck."
    },
    "High-trust coordination": {
        "AI pressure": 60,
        "Geopolitical pressure": 35,
        "Resource pressure": 45,
        "Social pressure": 35,
        "description": "Trust, standards, and shared reality make coordination easier."
    },
    "Loop trap economy": {
        "AI pressure": 75,
        "Geopolitical pressure": 60,
        "Resource pressure": 60,
        "Social pressure": 85,
        "description": "Short-term survival loops dominate long-term system building."
    },
}

REGIONS = {
    "European Union": {
        "Incentive alignment": 58,
        "Verifiable trust": 62,
        "Shared reality": 55,
        "Adaptation speed": 48,
        "Infrastructure resilience": 60,
        "Reinforcement quality": 52,
        "Local-global balance": 58,
        "Complexity management": 57,
    },
    "United States": {
        "Incentive alignment": 50,
        "Verifiable trust": 45,
        "Shared reality": 40,
        "Adaptation speed": 62,
        "Infrastructure resilience": 52,
        "Reinforcement quality": 50,
        "Local-global balance": 45,
        "Complexity management": 50,
    },
    "China": {
        "Incentive alignment": 62,
        "Verifiable trust": 42,
        "Shared reality": 55,
        "Adaptation speed": 72,
        "Infrastructure resilience": 70,
        "Reinforcement quality": 60,
        "Local-global balance": 50,
        "Complexity management": 65,
    },
    "India": {
        "Incentive alignment": 48,
        "Verifiable trust": 42,
        "Shared reality": 45,
        "Adaptation speed": 58,
        "Infrastructure resilience": 48,
        "Reinforcement quality": 46,
        "Local-global balance": 52,
        "Complexity management": 48,
    },
    "Global South": {
        "Incentive alignment": 42,
        "Verifiable trust": 38,
        "Shared reality": 42,
        "Adaptation speed": 45,
        "Infrastructure resilience": 40,
        "Reinforcement quality": 42,
        "Local-global balance": 50,
        "Complexity management": 42,
    },
    "Custom": {
        "Incentive alignment": 50,
        "Verifiable trust": 50,
        "Shared reality": 50,
        "Adaptation speed": 50,
        "Infrastructure resilience": 50,
        "Reinforcement quality": 50,
        "Local-global balance": 50,
        "Complexity management": 50,
    }
}

SECTORS = {
    "AI + labor": {
        "main_pressure": "AI pressure",
        "critical_dimensions": ["Adaptation speed", "Reinforcement quality", "Shared reality"]
    },
    "Energy": {
        "main_pressure": "Resource pressure",
        "critical_dimensions": ["Infrastructure resilience", "Complexity management", "Incentive alignment"]
    },
    "Water + food": {
        "main_pressure": "Resource pressure",
        "critical_dimensions": ["Infrastructure resilience", "Local-global balance", "Complexity management"]
    },
    "Transport": {
        "main_pressure": "Resource pressure",
        "critical_dimensions": ["Infrastructure resilience", "Complexity management", "Incentive alignment"]
    },
    "Governance": {
        "main_pressure": "Geopolitical pressure",
        "critical_dimensions": ["Verifiable trust", "Shared reality", "Local-global balance"]
    },
    "Education": {
        "main_pressure": "AI pressure",
        "critical_dimensions": ["Adaptation speed", "Reinforcement quality", "Shared reality"]
    }
}

AGENT_TYPES = {
    "Citizens": {"needs": "stability, income, safety", "sensitivity": 1.20},
    "Companies": {"needs": "profit, talent, infrastructure", "sensitivity": 1.00},
    "Governments": {"needs": "legitimacy, stability, security", "sensitivity": 1.10},
    "Platforms": {"needs": "scale, data, network effects", "sensitivity": 0.90},
    "Infrastructure operators": {"needs": "reliability, finance, regulation", "sensitivity": 1.05},
}

def weighted_average(values):
    return sum(values[d] * WEIGHTS[d] for d in DIMENSIONS) / sum(WEIGHTS.values())

def clamp(x):
    return max(0, min(100, x))

def simulate(initial, scenario, sector, years, intervention_strength, random_seed=42):
    rng = np.random.default_rng(random_seed)
    state = initial.copy()
    pressure = {k: v for k, v in scenario.items() if k != "description"}
    sector_conf = SECTORS[sector]
    rows = []

    for year in range(years + 1):
        health = weighted_average(state)
        pressure_score = np.mean(list(pressure.values()))
        fragility_gap = max(0, pressure_score - health)
        coordination_capacity = np.mean([
            state["Incentive alignment"],
            state["Verifiable trust"],
            state["Shared reality"],
            state["Complexity management"]
        ])
        resilience = np.mean([
            state["Infrastructure resilience"],
            state["Adaptation speed"],
            state["Reinforcement quality"]
        ])

        rows.append({
            "Year": year,
            "System health": health,
            "Pressure": pressure_score,
            "Fragility gap": fragility_gap,
            "Coordination capacity": coordination_capacity,
            "Resilience": resilience,
            **state
        })

        # Update dynamics
        for d in DIMENSIONS:
            natural_decay = 0.35
            noise = rng.normal(0, 0.8)
            pressure_damage = 0.025 * pressure_score

            improvement = 0
            if d in sector_conf["critical_dimensions"]:
                improvement += intervention_strength * 0.10
            else:
                improvement += intervention_strength * 0.045

            # Feedback loops:
            # better reinforcement improves adaptation and incentives over time
            if d in ["Adaptation speed", "Incentive alignment", "Shared reality"]:
                improvement += (state["Reinforcement quality"] - 50) * 0.025

            # trust and shared reality support coordination
            if d in ["Complexity management", "Local-global balance"]:
                improvement += ((state["Verifiable trust"] + state["Shared reality"]) / 2 - 50) * 0.025

            # infrastructure gets damaged by resource pressure
            if d == "Infrastructure resilience":
                pressure_damage += max(0, pressure["Resource pressure"] - state[d]) * 0.015

            # adaptation damaged by AI pressure
            if d == "Adaptation speed":
                pressure_damage += max(0, pressure["AI pressure"] - state[d]) * 0.018

            state[d] = clamp(state[d] + improvement - pressure_damage - natural_decay + noise)

        # Pressure can decline if coordination improves, or rise if fragility is high
        for p in pressure:
            pressure[p] = clamp(
                pressure[p]
                - max(0, coordination_capacity - 55) * 0.025
                + max(0, fragility_gap - 25) * 0.018
                + rng.normal(0, 0.35)
            )

    return pd.DataFrame(rows)

def classify(score, fragility):
    if score >= 75 and fragility < 15:
        return "Coordinated Stability"
    if score >= 63 and fragility < 25:
        return "Managed Transition"
    if fragility > 35:
        return "Fragmented Adaptation"
    if score < 45:
        return "Loop Trap"
    return "Unstable Optimization"

def agent_outcomes(final_row):
    results = []
    health = final_row["System health"]
    fragility = final_row["Fragility gap"]
    for agent, meta in AGENT_TYPES.items():
        if agent == "Citizens":
            score = health * 0.45 + final_row["Adaptation speed"] * 0.20 + final_row["Infrastructure resilience"] * 0.20 + final_row["Reinforcement quality"] * 0.15 - fragility * meta["sensitivity"] * 0.25
        elif agent == "Companies":
            score = health * 0.55 + final_row["Incentive alignment"] * 0.20 + final_row["Infrastructure resilience"] * 0.15 + final_row["Complexity management"] * 0.10 - fragility * meta["sensitivity"] * 0.15
        elif agent == "Governments":
            score = health * 0.45 + final_row["Shared reality"] * 0.20 + final_row["Verifiable trust"] * 0.20 + final_row["Local-global balance"] * 0.15 - fragility * meta["sensitivity"] * 0.20
        elif agent == "Platforms":
            score = health * 0.40 + final_row["Adaptation speed"] * 0.30 + final_row["Complexity management"] * 0.15 + final_row["Incentive alignment"] * 0.15 - fragility * meta["sensitivity"] * 0.10
        else:
            score = health * 0.40 + final_row["Infrastructure resilience"] * 0.35 + final_row["Verifiable trust"] * 0.15 + final_row["Complexity management"] * 0.10 - fragility * meta["sensitivity"] * 0.12

        results.append({
            "Agent": agent,
            "Needs": meta["needs"],
            "Outcome score": clamp(score)
        })
    return pd.DataFrame(results)

# ----------------------------
# UI
# ----------------------------

st.title("🌍 Global System Interactive Simulator")
st.caption("A working prototype for exploring AI, jobs, infrastructure, trust, incentives, and coordination dynamics.")

st.markdown("""
This simulator is based on one idea:

**The best future is usually not the default future.**

Default futures emerge from existing incentives. Better futures require coordination, trust, feedback, adaptation, and reinforcement.
""")

with st.sidebar:
    st.header("Scenario setup")

    region = st.selectbox("Region baseline", list(REGIONS.keys()))
    scenario_name = st.selectbox("Scenario", list(SCENARIOS.keys()))
    sector = st.selectbox("Sector focus", list(SECTORS.keys()))

    years = st.slider("Simulation years", 5, 30, 15)
    intervention_strength = st.slider("Intervention strength", 0, 100, 45)
    random_seed = st.number_input("Random seed", min_value=1, max_value=9999, value=42)

    st.divider()
    st.subheader("Customize baseline")

    baseline = {}
    for d in DIMENSIONS:
        baseline[d] = st.slider(d, 0, 100, REGIONS[region][d])

scenario = SCENARIOS[scenario_name]
df = simulate(
    baseline,
    scenario,
    sector,
    years,
    intervention_strength,
    random_seed
)

final = df.iloc[-1]
trajectory = classify(final["System health"], final["Fragility gap"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Final system health", f"{final['System health']:.1f}/100")
c2.metric("Final pressure", f"{final['Pressure']:.1f}/100")
c3.metric("Final fragility gap", f"{final['Fragility gap']:.1f}")
c4.metric("Trajectory", trajectory)

st.info(SCENARIOS[scenario_name]["description"])

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Simulation",
    "System dimensions",
    "Agents",
    "Risks + interventions",
    "Export"
])

with tab1:
    st.subheader("System trajectory over time")

    line_df = df[["Year", "System health", "Pressure", "Fragility gap", "Coordination capacity", "Resilience"]]
    fig = px.line(
        line_df,
        x="Year",
        y=["System health", "Pressure", "Fragility gap", "Coordination capacity", "Resilience"],
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Reading the chart**

    - If pressure stays above system health, fragility grows.
    - If coordination capacity improves, pressure becomes easier to absorb.
    - If resilience rises, the system survives shocks better.
    """)

with tab2:
    st.subheader("Final system dimension scores")

    dim_final = pd.DataFrame({
        "Dimension": DIMENSIONS,
        "Initial": [baseline[d] for d in DIMENSIONS],
        "Final": [final[d] for d in DIMENSIONS]
    })

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="Initial", x=dim_final["Dimension"], y=dim_final["Initial"]))
    fig2.add_trace(go.Bar(name="Final", x=dim_final["Dimension"], y=dim_final["Final"]))
    fig2.update_layout(barmode="group", yaxis_range=[0, 100])
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(dim_final, use_container_width=True)

with tab3:
    st.subheader("Agent outcome model")

    agents_df = agent_outcomes(final)
    fig3 = px.bar(agents_df, x="Agent", y="Outcome score", range_y=[0, 100], hover_data=["Needs"])
    st.plotly_chart(fig3, use_container_width=True)

    st.dataframe(agents_df, use_container_width=True)

    weakest = agents_df.sort_values("Outcome score").iloc[0]
    st.warning(f"Weakest agent outcome: **{weakest['Agent']}** — this is where system stress appears first.")

with tab4:
    st.subheader("Risk diagnosis")

    risks = pd.DataFrame({
        "Risk": [
            "AI-job synchronization failure",
            "Infrastructure bottleneck",
            "Narrative fragmentation",
            "Coordination collapse",
            "Short-term loop trap",
            "Local-global conflict",
            "Systems-of-systems interface failure"
        ],
        "Score": [
            max(0, scenario["AI pressure"] - final["Adaptation speed"]),
            max(0, scenario["Resource pressure"] - final["Infrastructure resilience"]),
            max(0, 100 - final["Shared reality"]),
            max(0, 100 - ((final["Incentive alignment"] + final["Verifiable trust"]) / 2)),
            max(0, 100 - final["Reinforcement quality"]),
            max(0, 100 - final["Local-global balance"]),
            max(0, 100 - final["Complexity management"])
        ]
    })

    fig4 = px.bar(risks, x="Risk", y="Score", range_y=[0, 100])
    st.plotly_chart(fig4, use_container_width=True)
    st.dataframe(risks, use_container_width=True)

    st.subheader("Recommended interventions")

    recommendations = []
    if final["Incentive alignment"] < 60:
        recommendations.append("Reward coordination instead of only individual optimization.")
    if final["Verifiable trust"] < 60:
        recommendations.append("Build auditable trust layers: shared dashboards, verification, transparent commitments.")
    if final["Shared reality"] < 60:
        recommendations.append("Create common data infrastructure and reduce narrative fragmentation.")
    if final["Adaptation speed"] < scenario["AI pressure"]:
        recommendations.append("Accelerate reskilling, bridge roles, and institutional feedback loops.")
    if final["Infrastructure resilience"] < scenario["Resource pressure"]:
        recommendations.append("Invest in redundancy, distributed infrastructure, storage, and maintenance capacity.")
    if final["Reinforcement quality"] < 60:
        recommendations.append("Make better behavior easier, visible, rewarded, and repeated.")
    if final["Complexity management"] < 60:
        recommendations.append("Govern interfaces between systems, not only individual systems.")

    for r in recommendations:
        st.markdown(f"- {r}")

with tab5:
    st.subheader("Export simulation results")

    st.download_button(
        "Download simulation CSV",
        df.to_csv(index=False),
        file_name="simulation_results.csv",
        mime="text/csv"
    )

    summary = f"""
# Global System Simulator Report

Region: {region}
Scenario: {scenario_name}
Sector focus: {sector}
Years simulated: {years}
Intervention strength: {intervention_strength}

Final system health: {final['System health']:.1f}/100
Final pressure: {final['Pressure']:.1f}/100
Final fragility gap: {final['Fragility gap']:.1f}
Trajectory: {trajectory}

Main interpretation:
The system moves toward '{trajectory}' under the selected assumptions.

Core thesis:
The future will not be built only by better technology.
It will be built by whoever can turn coordination into infrastructure.
"""

    st.download_button(
        "Download markdown report",
        summary,
        file_name="system_simulation_report.md",
        mime="text/markdown"
    )

st.divider()
st.caption("Prototype model — useful for strategic thinking, not scientific forecasting.")
