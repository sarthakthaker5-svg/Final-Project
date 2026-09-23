import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="World Happiness Analytics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM DESIGN / CSS
# ============================================================
st.markdown("""
<style>
    /* Main application */
    .stApp {
        background: #0b0f17;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #263244;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    /* Sidebar branding */
    .brand-box {
        padding: 8px 8px 22px 8px;
        text-align: center;
    }

    .brand-title {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #f8fafc;
        margin-bottom: 2px;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #94a3b8;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    /* Page heading */
    .hero {
        padding: 28px 30px;
        border: 1px solid #293548;
        border-radius: 20px;
        background: linear-gradient(135deg, #172033 0%, #101827 55%, #14261f 100%);
        margin-bottom: 24px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.22);
    }

    .hero-kicker {
        color: #5eead4;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .hero-title {
        color: #f8fafc;
        font-size: 38px;
        font-weight: 800;
        line-height: 1.1;
        margin: 0;
    }

    .hero-text {
        color: #aab6c7;
        font-size: 15px;
        margin-top: 12px;
        max-width: 800px;
        line-height: 1.6;
    }

    /* KPI cards */
    .metric-card {
        background: #111827;
        border: 1px solid #293548;
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 112px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.14);
    }

    .metric-label {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 27px;
        font-weight: 800;
    }

    .metric-note {
        color: #64748b;
        font-size: 11px;
        margin-top: 4px;
    }

    /* Section headings */
    .section-title {
        color: #f8fafc;
        font-size: 22px;
        font-weight: 750;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 18px;
    }

    /* Info cards */
    .info-card {
        background: #111827;
        border: 1px solid #293548;
        border-radius: 16px;
        padding: 20px;
        height: 100%;
    }

    .info-title {
        color: #e2e8f0;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .info-text {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.6;
    }

    /* Country profile */
    .country-card {
        background: linear-gradient(135deg, #172033, #111827);
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
    }

    .country-name {
        color: #f8fafc;
        font-size: 27px;
        font-weight: 800;
    }

    .country-small {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 4px;
    }

    /* Pills */
    .pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        background: #173c3a;
        color: #5eead4;
        font-size: 11px;
        font-weight: 700;
        margin-right: 6px;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #293548;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Buttons */
    .stDownloadButton button {
        border-radius: 10px;
        font-weight: 700;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        border-radius: 10px;
    }

    /* Hide unnecessary top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 11px;
        padding: 30px 0 5px 0;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_data():
    files = {
        2015: "2015.csv",
        2016: "2016.csv",
        2017: "2017.csv",
        2018: "2018.csv",
        2019: "2019.csv"
    }

    frames = []

    for year, filename in files.items():
        df_year = pd.read_csv(filename)
        df_year["Year"] = year
        frames.append(df_year)

    df = pd.concat(frames, ignore_index=True, sort=False)

    # Create common columns because the original datasets
    # use different column names in different years.
    def first_existing(columns):
        for col in columns:
            if col in df.columns:
                return col
        return None

    country_col = first_existing(["Country", "Country or region"])
    score_cols = [c for c in ["Happiness Score", "Score"] if c in df.columns]
    gdp_cols = [c for c in [
        "Economy (GDP per Capita)",
        "Economy..GDP.per.Capita.",
        "GDP per capita"
    ] if c in df.columns]
    family_cols = [c for c in [
        "Family",
        "Social support"
    ] if c in df.columns]
    health_cols = [c for c in [
        "Health (Life Expectancy)",
        "Health..Life.Expectancy.",
        "Healthy life expectancy"
    ] if c in df.columns]
    freedom_cols = [c for c in [
        "Freedom",
        "Freedom to make life choices"
    ] if c in df.columns]
    trust_cols = [c for c in [
        "Trust (Government Corruption)",
        "Trust..Government.Corruption.",
        "Perceptions of corruption"
    ] if c in df.columns]
    generosity_cols = [c for c in ["Generosity"] if c in df.columns]

    if country_col:
        df["Country_Name"] = df[country_col]

    if score_cols:
        df["Happiness_Score"] = df[score_cols].bfill(axis=1).iloc[:, 0]

    if gdp_cols:
        df["GDP"] = df[gdp_cols].bfill(axis=1).iloc[:, 0]

    if family_cols:
        df["Social_Support"] = df[family_cols].bfill(axis=1).iloc[:, 0]

    if health_cols:
        df["Life_Expectancy"] = df[health_cols].bfill(axis=1).iloc[:, 0]

    if freedom_cols:
        df["Freedom_Score"] = df[freedom_cols].bfill(axis=1).iloc[:, 0]

    if trust_cols:
        df["Corruption_Trust"] = df[trust_cols].bfill(axis=1).iloc[:, 0]

    if generosity_cols:
        df["Generosity_Score"] = df[generosity_cols].bfill(axis=1).iloc[:, 0]

    df = df.dropna(subset=["Country_Name", "Happiness_Score"]).copy()

    return df


# ============================================================
# CHART HELPER
# ============================================================
def create_plot(kind, data, x=None, y=None, title="", xlabel="", ylabel=""):
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")

    if kind == "bar":
        ax.bar(data[x], data[y])
        ax.tick_params(axis="x", rotation=45, labelsize=9)

    elif kind == "hist":
        ax.hist(data[x], bins=20, edgecolor="#0b0f17")

    elif kind == "scatter":
        ax.scatter(data[x], data[y], alpha=0.65)

    elif kind == "line":
        ax.plot(data[x], data[y], marker="o", linewidth=2)

    elif kind == "box":
        sns.boxplot(y=data[x], ax=ax)

    ax.set_title(title, color="#f8fafc", fontsize=15, fontweight="bold", pad=14)

    if xlabel:
        ax.set_xlabel(xlabel, color="#94a3b8")

    if ylabel:
        ax.set_ylabel(ylabel, color="#94a3b8")

    ax.tick_params(colors="#94a3b8")
    ax.grid(axis="y", alpha=0.12)

    for spine in ax.spines.values():
        spine.set_color("#293548")

    fig.tight_layout()
    return fig


def metric_card(label, value, note=""):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """


# ============================================================
# CHECK DATA FILES
# ============================================================
required_files = [f"{year}.csv" for year in range(2015, 2020)]
missing_files = [f for f in required_files if not os.path.exists(f)]

if missing_files:
    st.error("Required CSV files are missing from the GitHub repository.")
    st.write("Add these files to the same folder as app.py:")
    for file in missing_files:
        st.write(f"- {file}")
    st.info("After adding them to GitHub, Streamlit Cloud will redeploy the app automatically.")
    st.stop()

df = load_data()


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="brand-box">
        <div class="brand-title">🌍 WORLD HAPPINESS</div>
        <div class="brand-subtitle">Analytics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigation")

    page = st.radio(
        "Select Section",
        [
            "Home",
            "Dataset",
            "Data Cleaning",
            "Statistical Analysis",
            "Country Analysis",
            "Visualizations"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.caption("World Happiness Report")
    st.caption("2015 – 2019")


# ============================================================
# HOME
# ============================================================
if page == "Home":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">World Happiness Report • 2015–2019</div>
        <div class="hero-title">🌍 World Happiness Analytics</div>
        <div class="hero-text">
            Explore global happiness through economic, social, health and
            freedom-related indicators. Use the dashboard to inspect the
            dataset, study statistics, compare countries and discover patterns.
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_records = len(df)
    total_countries = df["Country_Name"].nunique()
    total_years = df["Year"].nunique()
    avg_score = df["Happiness_Score"].mean()
    highest_score = df.loc[df["Happiness_Score"].idxmax()]
    avg_gdp = df["GDP"].mean() if "GDP" in df.columns else np.nan

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            metric_card("🌎 Countries", f"{total_countries}", "Unique countries"),
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            metric_card("😊 Avg Happiness", f"{avg_score:.2f}", "Across all records"),
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            metric_card("🏆 Highest Score", f"{highest_score['Happiness_Score']:.2f}",
                        str(highest_score["Country_Name"])),
            unsafe_allow_html=True
        )

    with c4:
        gdp_value = f"{avg_gdp:.2f}" if pd.notna(avg_gdp) else "N/A"
        st.markdown(
            metric_card("💰 Avg GDP Factor", gdp_value, "Average GDP indicator"),
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown('<div class="section-title">📈 Happiness Overview</div>',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Average happiness score by year</div>',
            unsafe_allow_html=True
        )

        year_average = (
            df.groupby("Year")["Happiness_Score"]
            .mean()
            .reset_index()
        )

        fig = create_plot(
            "line",
            year_average,
            "Year",
            "Happiness_Score",
            "Average Happiness Score",
            "Year",
            "Average Score"
        )
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    with right:
        st.markdown('<div class="section-title">🏅 Current Dataset Snapshot</div>',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Highest-scoring records</div>',
            unsafe_allow_html=True
        )

        top5 = df.nlargest(5, "Happiness_Score")[
            ["Country_Name", "Year", "Happiness_Score"]
        ].reset_index(drop=True)

        top5.index = top5.index + 1
        top5.columns = ["Country", "Year", "Score"]

        st.dataframe(
            top5,
            use_container_width=True,
            height=250
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">🔎 What this dashboard covers</div>',
                unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">📋 Dataset Exploration</div>
            <div class="info-text">
                Browse the combined World Happiness datasets and filter
                records by year.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">📊 Statistical Analysis</div>
            <div class="info-text">
                Examine descriptive statistics and correlations between
                happiness-related indicators.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">🌎 Country & Visual Analysis</div>
            <div class="info-text">
                Compare countries and explore relationships using charts
                and visualizations.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# DATASET
# ============================================================
elif page == "Dataset":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Data Explorer</div>
        <div class="hero-title">📋 Dataset</div>
        <div class="hero-text">
            Browse the combined World Happiness Report records from 2015 to 2019.
        </div>
    </div>
    """, unsafe_allow_html=True)

    year = st.selectbox(
        "Select Year",
        ["All"] + sorted(df["Year"].unique().tolist())
    )

    filtered = df if year == "All" else df[df["Year"] == year]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            metric_card("Rows", f"{len(filtered):,}", "Filtered records"),
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            metric_card("Columns", f"{len(filtered.columns):,}", "Available fields"),
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            metric_card("Countries", f"{filtered['Country_Name'].nunique():,}",
                        "Unique countries"),
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Dataset Preview</div>',
                unsafe_allow_html=True)

    st.dataframe(filtered, use_container_width=True, height=500)


# ============================================================
# DATA CLEANING
# ============================================================
elif page == "Data Cleaning":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Data Preparation</div>
        <div class="hero-title">🧹 Data Cleaning</div>
        <div class="hero-text">
            Review missing values, duplicate records and the cleaned analysis dataset.
        </div>
    </div>
    """, unsafe_allow_html=True)

    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    duplicate_count = df.duplicated().sum()

    c1, c2 = st.columns(2)

    with c1:
        missing_value_count = int(df.isnull().sum().sum())
        st.markdown(
            metric_card("Missing Values", f"{missing_value_count:,}",
                        "Across the final dataset"),
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            metric_card("Duplicate Rows", f"{duplicate_count:,}",
                        "Exact duplicate records"),
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Missing Values</div>',
                unsafe_allow_html=True)

    if missing.empty:
        st.success("No missing values found in the final analysis columns.")
    else:
        st.dataframe(
            missing.rename("Missing Values").to_frame(),
            use_container_width=True
        )

    st.markdown('<div class="section-title">Cleaned Dataset</div>',
                unsafe_allow_html=True)

    st.dataframe(df, use_container_width=True, height=450)

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Cleaned CSV",
        data=csv_data,
        file_name="Cleaned_Happiness_Report.csv",
        mime="text/csv"
    )


# ============================================================
# STATISTICAL ANALYSIS
# ============================================================
elif page == "Statistical Analysis":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Data Science</div>
        <div class="hero-title">📈 Statistical Analysis</div>
        <div class="hero-text">
            Understand the distribution and relationships among the main
            happiness indicators.
        </div>
    </div>
    """, unsafe_allow_html=True)

    numeric_columns = [
        "Happiness_Score",
        "GDP",
        "Social_Support",
        "Life_Expectancy",
        "Freedom_Score",
        "Corruption_Trust",
        "Generosity_Score"
    ]

    numeric_columns = [c for c in numeric_columns if c in df.columns]

    st.markdown('<div class="section-title">Descriptive Statistics</div>',
                unsafe_allow_html=True)

    stats = df[numeric_columns].describe().T
    stats = stats.round(3)

    st.dataframe(stats, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Correlation Analysis</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Correlation between major happiness indicators</div>',
        unsafe_allow_html=True
    )

    corr = df[numeric_columns].corr(numeric_only=True)

    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
        ax=ax,
        cbar_kws={"shrink": 0.8}
    )

    ax.set_title(
        "Correlation Heatmap",
        color="#f8fafc",
        fontsize=16,
        fontweight="bold",
        pad=15
    )

    ax.tick_params(colors="#94a3b8")

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# ============================================================
# COUNTRY ANALYSIS
# ============================================================
elif page == "Country Analysis":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Country Explorer</div>
        <div class="hero-title">🌎 Country Analysis</div>
        <div class="hero-text">
            Select a country to inspect its happiness indicators and compare
            it with another country.
        </div>
    </div>
    """, unsafe_allow_html=True)

    countries = sorted(df["Country_Name"].dropna().unique())

    country = st.selectbox("🌎 Select Country", countries)

    country_data = df[df["Country_Name"] == country].copy()

    latest = country_data.sort_values("Year").iloc[-1]

    st.markdown(f"""
    <div class="country-card">
        <div class="country-name">🌍 {country}</div>
        <div class="country-small">
            Showing available World Happiness Report records for this country
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            metric_card("😊 Happiness", f"{latest['Happiness_Score']:.3f}",
                        f"Year {int(latest['Year'])}"),
            unsafe_allow_html=True
        )

    with c2:
        value = latest["GDP"]
        st.markdown(
            metric_card("💰 GDP", f"{value:.3f}" if pd.notna(value) else "N/A",
                        "Latest available"),
            unsafe_allow_html=True
        )

    with c3:
        value = latest["Social_Support"]
        st.markdown(
            metric_card("👨‍👩‍👧 Social Support",
                        f"{value:.3f}" if pd.notna(value) else "N/A",
                        "Latest available"),
            unsafe_allow_html=True
        )

    with c4:
        value = latest["Life_Expectancy"]
        st.markdown(
            metric_card("❤️ Life Expectancy",
                        f"{value:.3f}" if pd.notna(value) else "N/A",
                        "Latest available"),
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Country History</div>',
                unsafe_allow_html=True)

    display_columns = [
        "Year",
        "Country_Name",
        "Happiness_Score",
        "GDP",
        "Social_Support",
        "Life_Expectancy",
        "Freedom_Score"
    ]

    display_columns = [c for c in display_columns if c in country_data.columns]

    st.dataframe(
        country_data[display_columns],
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Compare Two Countries</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    country1 = col1.selectbox(
        "Country 1",
        countries,
        index=0,
        key="country1"
    )

    country2 = col2.selectbox(
        "Country 2",
        countries,
        index=min(1, len(countries) - 1),
        key="country2"
    )

    comparison = df[df["Country_Name"].isin([country1, country2])].copy()

    comparison = comparison[
        [c for c in [
            "Year",
            "Country_Name",
            "Happiness_Score",
            "GDP",
            "Social_Support",
            "Life_Expectancy",
            "Freedom_Score"
        ] if c in comparison.columns]
    ]

    st.dataframe(comparison, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">🏅 Top 10 Records</div>',
                    unsafe_allow_html=True)

        top10 = df.nlargest(10, "Happiness_Score")[
            ["Country_Name", "Year", "Happiness_Score"]
        ]

        st.dataframe(top10.reset_index(drop=True), use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">📉 Bottom 10 Records</div>',
                    unsafe_allow_html=True)

        bottom10 = df.nsmallest(10, "Happiness_Score")[
            ["Country_Name", "Year", "Happiness_Score"]
        ]

        st.dataframe(bottom10.reset_index(drop=True), use_container_width=True)


# ============================================================
# VISUALIZATIONS
# ============================================================
elif page == "Visualizations":

    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Visual Analytics</div>
        <div class="hero-title">📊 Visualizations</div>
        <div class="hero-text">
            Explore happiness distributions, country rankings and relationships
            between important indicators.
        </div>
    </div>
    """, unsafe_allow_html=True)

    chart = st.selectbox(
        "Choose Visualization",
        [
            "Top 10 Happiest Countries",
            "Bottom 10 Happiest Countries",
            "Happiness Score Distribution",
            "GDP vs Happiness",
            "Freedom vs Happiness",
            "Life Expectancy vs Happiness",
            "Happiness Score Box Plot",
            "Top 5 Happiest Countries",
            "Year-wise Happiness Trend"
        ]
    )

    if chart == "Top 10 Happiest Countries":

        data = df.nlargest(10, "Happiness_Score")

        fig = create_plot(
            "bar",
            data,
            "Country_Name",
            "Happiness_Score",
            "Top 10 Happiest Countries",
            "Country",
            "Happiness Score"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif chart == "Bottom 10 Happiest Countries":

        data = df.nsmallest(10, "Happiness_Score")

        fig = create_plot(
            "bar",
            data,
            "Country_Name",
            "Happiness_Score",
            "Bottom 10 Happiest Countries",
            "Country",
            "Happiness Score"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif chart == "Happiness Score Distribution":

        fig = create_plot(
            "hist",
            df,
            x="Happiness_Score",
            title="Distribution of Happiness Score",
            xlabel="Happiness Score",
            ylabel="Frequency"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif chart == "GDP vs Happiness":

        data = df.dropna(subset=["GDP", "Happiness_Score"])

        fig = create_plot(
            "scatter",
            data,
            "GDP",
            "Happiness_Score",
            "GDP vs Happiness Score",
            "GDP",
            "Happiness Score"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif chart == "Freedom vs Happiness":

        data = df.dropna(subset=["Freedom_Score", "Happiness_Score"])

        fig = create_plot(
            "scatter",
            data,
            "Freedom_Score",
            "Happiness_Score",
            "Freedom vs Happiness Score",
            "Freedom",
            "Happiness Score"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif chart == "Life Expectancy vs Happiness":

        data = df.dropna(subset=["Life_Expectancy", "Happiness_Score"])

        fig = create_plot(
            "scatter",
            data,
            "Life_Expectancy",
            "Happiness_Score",
            "Life Expectancy vs Happiness Score",
            "Life Expectancy",
            "Happiness Score"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif chart == "Happiness Score Box Plot":

        data = df.dropna(subset=["Happiness_Score"])

        fig = create_plot(
            "box",
            data,
            x="Happiness_Score",
            title="Box Plot of Happiness Score",
            ylabel="Happiness Score"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif chart == "Top 5 Happiest Countries":

        top5 = df.nlargest(5, "Happiness_Score")

        fig, ax = plt.subplots(figsize=(8, 7))
        fig.patch.set_facecolor("#111827")
        ax.set_facecolor("#111827")

        ax.pie(
            top5["Happiness_Score"],
            labels=top5["Country_Name"],
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(
            "Top 5 Happiest Countries",
            color="#f8fafc",
            fontsize=16,
            fontweight="bold",
            pad=15
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif chart == "Year-wise Happiness Trend":

        year_average = (
            df.groupby("Year")["Happiness_Score"]
            .mean()
            .reset_index()
        )

        fig = create_plot(
            "line",
            year_average,
            "Year",
            "Happiness_Score",
            "Average Happiness Score by Year",
            "Year",
            "Average Happiness Score"
        )

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    🌍 World Happiness Analytics • Data Analysis Project • 2015–2019
</div>
""", unsafe_allow_html=True)
