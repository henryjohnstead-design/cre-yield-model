import streamlit as st
import streamlit.components.v1 as components

# Compress layout gaps for above-the-fold visibility
st.set_page_config(
    page_title="CRE Yield Model",
    layout="wide"
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 0rem !important;
    }
    h1 { margin-bottom: 0.1rem !important; }
    h3 { margin-top: 0.1rem !important; margin-bottom: 0.1rem !important; }
    .stCaption { margin-bottom: 0rem !important; }
    hr { margin: 0.6rem 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# HERO HEXAGON GRAPHIC (Key Results Summary)
# ==========================================
html = """
<html>
<head>
    <style>
    body { margin: 0; padding: 0; }
    .hex-wrap {
        display: flex;
        justify-content: center;
        align-items: stretch;
        gap: 22px;
        flex-wrap: wrap;
        margin: 0px 0 6px 0;
    }
    .hex {
        position: relative;
        width: 178px;
        height: 176px;
        clip-path: polygon(25% 3%, 75% 3%, 100% 50%, 75% 97%, 25% 97%, 0% 50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 14px 20px;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .hex-1 { background: linear-gradient(160deg, #1f2a44, #33456e); }
    .hex-2 { background: linear-gradient(160deg, #7a1f2b, #b23a2f); }
    .hex-3 { background: linear-gradient(160deg, #1e4d3a, #2f7d57); }
    .hex-4 { background: linear-gradient(160deg, #3d3560, #6a4c93); width: 210px; }

    .hex-label {
        font-size: 0.62rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        opacity: 0.85;
        margin-bottom: 4px;
        font-weight: 600;
    }
    .hex-stat {
        font-size: 1.55rem;
        font-weight: 800;
        line-height: 1.05;
    }
    .hex-substat {
        font-size: 0.68rem;
        opacity: 0.9;
        margin-top: 5px;
        line-height: 1.3;
    }
    .hex-multiline .hex-substat div {
        margin-top: 2px;
    }
    </style>
</head>
<body>
    <div class="hex-wrap">
        <div class="hex hex-1">
            <div class="hex-label">Data Coverage</div>
            <div class="hex-stat">10 Years</div>
            <div class="hex-substat">21 bi-annual steps (2016–2026)<br>integrating ONS, BoE &<br>Savills datasets.</div>
        </div>
        <div class="hex hex-2">
            <div class="hex-label">Model Explanatory Power</div>
            <div class="hex-stat">78.6%</div>
            <div class="hex-substat">Of regional office yield variance<br>explained by macro variables<br>(vs. 46.2% for London).</div>
        </div>
        <div class="hex hex-3">
            <div class="hex-label">BOE Rate Sensitivity</div>
            <div class="hex-stat">+41.5 bps</div>
            <div class="hex-substat">Implied regional yield expansion<br>per 1.0% increase in BoE<br>base rate (p < 0.01).</div>
        </div>
        <div class="hex hex-4 hex-multiline">
            <div class="hex-label">Maximum Yield Shock</div>
            <div class="hex-stat">+225 bps</div>
            <div class="hex-substat">
                <div>Historic regional yield surge</div>
                <div>(4.75% &rarr; 7.00%) during the</div>
                <div>2022–2023 inflation spike.</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Main Title & Subtitle
st.title("UK Commercial Real Estate Yield Modelling and Valuation Stress-Testing")
st.markdown("### *An econometric analysis of the impact of CPI inflation, BoE base rate and GDP growth on CRE yields*")
st.caption("Developed by Henry Stead")
st.markdown("---")

# Render Hexagons
components.html(html, height=195, scrolling=False)

# Summary Box
st.info(
    "**Summary:** This dashboard visually illustrates the end to end workflow for synthesising data, "
    "programmatically analysing it then writing a report of what we found and making the finding "
    "accessible through an interactive excel dashboard."
)

st.markdown("## Follow the econometric workflow below:")

ARROW = "<div style='text-align: center; font-size: 20px; color: black; margin: 4px 0;'>↓</div>"

# ==========================================
# PHASE 1: Data Sourcing
# ==========================================
with st.container(border=True):
    st.markdown("### Phase 1: Data Sourcing")
    st.write(
        "**Objective:** Pairing historical UK macroeconomic data with commercial property data from Savills’ Market in Minutes."
    )
    try:
        with open("CRE+Macro.xlsx", "rb") as f:
            sourcing_bytes = f.read()
        st.download_button(
            label="Download Consolidated Dataset (Excel)",
            data=sourcing_bytes,
            file_name="CRE+Macro.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_sourcing"
        )
    except FileNotFoundError:
        st.warning("Connect your uploaded `CRE+Macro.xlsx` file to activate download link.")

# ==========================================
# PHASE 2: Regression Analysis
# ==========================================
st.markdown(ARROW, unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 2: Regression Analysis")
    st.write(
        "**Objective:** Produce a multivariate linear regression in R to determine how sensitive London and Regional "
        "commercial office yields are to changes in key macroeconomic indicators."
    )
    try:
        with open("Project 2.R", "rb") as f:
            r_bytes = f.read()
        st.download_button(
            label="Download Code File (Project 2.R)",
            data=r_bytes,
            file_name="Project 2.R",
            mime="text/x-r",
            key="dl_r_script"
        )
    except FileNotFoundError:
        st.warning("Connect your uploaded `Project 2.R` file to activate script download.")

# ==========================================
# PHASE 3: Reporting & Visualisation Dashboard
# ==========================================
st.markdown(ARROW, unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Phase 3: Producing Econometric Report and Visualisation")
    st.write(
        "**Objective:** Report findings from my regression analysis within an econometric report and build an Excel dashboard "
        "to display a 'stress-test' scenario showing what happens to property values if macroeconomic variables fluctuate."
    )

    tab1, tab2 = st.tabs(["Econometric Report", "Interactive Valuation Model"])

    with tab1:
        st.write("Detailed 6-page institutional risk and documentation analysis report detailing R model parameters.")
        try:
            with open("Regression Analysis Results.docx", "rb") as f:
                report_bytes = f.read()
            st.download_button(
                label="Download Econometric Report (Word Doc)",
                data=report_bytes,
                file_name="Regression_Analysis_Results.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="dl_report"
            )
        except FileNotFoundError:
            st.warning("Connect your uploaded `Regression Analysis Results.docx` to activate download link.")

    with tab2:
        st.write("Dynamic Excel workbook for stress-testing assets and evaluating actual vs. fitted deviations.")
        try:
            with open("Project 2 Dashboard.xlsx", "rb") as f:
                dashboard_bytes = f.read()
            st.download_button(
                label="Download Valuation Stress-Test Model (Excel)",
                data=dashboard_bytes,
                file_name="Project 2 Dashboard.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_dashboard"
            )
        except FileNotFoundError:
            st.warning("Connect your uploaded `Project 2 Dashboard.xlsx` to activate download link.")

st.markdown("---")
st.write("Thank you for reviewing my project.")
