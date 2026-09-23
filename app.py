import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

st.set_page_config(
    page_title="Global Happiness Report Analysis",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Global Happiness Report Analysis")
st.caption("World Happiness Report analysis for 2015–2019")

@st.cache_data
def load_data():
    files = {
        2015: "2015.csv",
        2016: "2016.csv",
        2017: "2017.csv",
        2018: "2018.csv",
        2019: "2019.csv",
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

    # Remove rows that do not contain a country or happiness score.
    df = df.dropna(subset=["Country_Name", "Happiness_Score"]).copy()

    return df

def create_plot(kind, data, x=None, y=None, title="", xlabel="", ylabel=""):
    fig, ax = plt.subplots(figsize=(9, 5))

    if kind == "bar":
        ax.bar(data[x], data[y])
        ax.tick_params(axis="x", rotation=90)
    elif kind == "hist":
        ax.hist(data[x], bins=20, edgecolor="black")
    elif kind == "scatter":
        ax.scatter(data[x], data[y], alpha=0.65)
    elif kind == "line":
        ax.plot(data[x], data[y], marker="o")
    elif kind == "box":
        sns.boxplot(y=data[x], ax=ax)

    ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig

# Check that the project data files are available.
required_files = [f"{year}.csv" for year in range(2015, 2020)]
missing_files = [f for f in required_files if not __import__("os").path.exists(f)]

if missing_files:
    st.error("Required CSV files are missing from the GitHub repository.")
    st.write("Add these files to the same folder as app.py:")
    for file in missing_files:
        st.write(f"- {file}")
    st.info("After adding them to GitHub, Streamlit Cloud will redeploy the app automatically.")
    st.stop()

df = load_data()

# Sidebar
st.sidebar.header("📌 Navigation")
page = st.sidebar.radio(
    "Select Section",
    [
        "Home",
        "Dataset",
        "Data Cleaning",
        "Statistical Analysis",
        "Country Analysis",
        "Visualizations"
    ]
)

if page == "Home":
    st.header("Project Overview")
    st.write(
        "This project analyzes World Happiness Report data from 2015 to 2019. "
        "It covers data loading, cleaning, statistical analysis, country analysis "
        "and visualization."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records", len(df))
    c2.metric("Total Columns", len(df.columns))
    c3.metric("Years", df["Year"].nunique())
    c4.metric("Countries", df["Country_Name"].nunique())

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

elif page == "Dataset":
    st.header("📊 Dataset")

    year = st.selectbox("Select Year", ["All"] + sorted(df["Year"].unique().tolist()))

    if year == "All":
        filtered = df
    else:
        filtered = df[df["Year"] == year]

    st.write(f"Rows: {len(filtered)}")
    st.dataframe(filtered, use_container_width=True)

elif page == "Data Cleaning":
    st.header("🧹 Data Cleaning")

    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)

    st.subheader("Missing Values")
    if missing.empty:
        st.success("No missing values found in the final analysis columns.")
    else:
        st.dataframe(
            missing.rename("Missing Values").to_frame(),
            use_container_width=True
        )

    st.subheader("Duplicate Records")
    st.write(f"Duplicate rows: {df.duplicated().sum()}")

    st.subheader("Cleaned Dataset")
    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Cleaned CSV",
        data=csv_data,
        file_name="Cleaned_Happiness_Report.csv",
        mime="text/csv"
    )

elif page == "Statistical Analysis":
    st.header("📈 Statistical Analysis")

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

    st.subheader("Descriptive Statistics")
    st.dataframe(
        df[numeric_columns].describe().T,
        use_container_width=True
    )

    st.subheader("Correlation Matrix")
    corr = df[numeric_columns].corr(numeric_only=True)
    st.dataframe(corr, use_container_width=True)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)
    plt.close(fig)

elif page == "Country Analysis":
    st.header("🌎 Country Analysis")

    countries = sorted(df["Country_Name"].dropna().unique())

    st.subheader("Search Country")
    country = st.selectbox("Select Country", countries)

    country_data = df[df["Country_Name"] == country]
    st.dataframe(
        country_data[
            ["Year", "Country_Name", "Happiness_Score", "GDP",
             "Social_Support", "Life_Expectancy", "Freedom_Score"]
        ],
        use_container_width=True
    )

    st.subheader("Compare Two Countries")
    col1, col2 = st.columns(2)
    country1 = col1.selectbox("Country 1", countries, index=0)
    country2 = col2.selectbox("Country 2", countries, index=min(1, len(countries)-1))

    comparison = df[df["Country_Name"].isin([country1, country2])].copy()
    comparison = comparison[
        ["Year", "Country_Name", "Happiness_Score", "GDP",
         "Social_Support", "Life_Expectancy", "Freedom_Score"]
    ]
    st.dataframe(comparison, use_container_width=True)

    st.subheader("Top 10 Happiest Countries")
    top10 = df.nlargest(10, "Happiness_Score")[
        ["Country_Name", "Year", "Happiness_Score"]
    ]
    st.dataframe(top10, use_container_width=True)

    st.subheader("Bottom 10 Happiest Countries")
    bottom10 = df.nsmallest(10, "Happiness_Score")[
        ["Country_Name", "Year", "Happiness_Score"]
    ]
    st.dataframe(bottom10, use_container_width=True)

elif page == "Visualizations":
    st.header("📊 Visualizations")

    chart = st.selectbox(
        "Select Visualization",
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
            "bar", data, "Country_Name", "Happiness_Score",
            "Top 10 Happiest Countries", "Country", "Happiness Score"
        )
        st.pyplot(fig)
        plt.close(fig)

    elif chart == "Bottom 10 Happiest Countries":
        data = df.nsmallest(10, "Happiness_Score")
        fig = create_plot(
            "bar", data, "Country_Name", "Happiness_Score",
            "Bottom 10 Happiest Countries", "Country", "Happiness Score"
        )
        st.pyplot(fig)
        plt.close(fig)

    elif chart == "Happiness Score Distribution":
        fig = create_plot(
            "hist", df, x="Happiness_Score",
            title="Distribution of Happiness Score",
            xlabel="Happiness Score", ylabel="Frequency"
        )
        st.pyplot(fig)
        plt.close(fig)

    elif chart == "GDP vs Happiness":
        data = df.dropna(subset=["GDP", "Happiness_Score"])
        fig = create_plot(
            "scatter", data, "GDP", "Happiness_Score",
            "GDP vs Happiness Score", "GDP", "Happiness Score"
        )
        st.pyplot(fig)
        plt.close(fig)

    elif chart == "Freedom vs Happiness":
        data = df.dropna(subset=["Freedom_Score", "Happiness_Score"])
        fig = create_plot(
            "scatter", data, "Freedom_Score", "Happiness_Score",
            "Freedom vs Happiness Score", "Freedom", "Happiness Score"
        )
        st.pyplot(fig)
        plt.close(fig)

    elif chart == "Life Expectancy vs Happiness":
        data = df.dropna(subset=["Life_Expectancy", "Happiness_Score"])
        fig = create_plot(
            "scatter", data, "Life_Expectancy", "Happiness_Score",
            "Life Expectancy vs Happiness Score",
            "Life Expectancy", "Happiness Score"
        )
        st.pyplot(fig)
        plt.close(fig)

    elif chart == "Happiness Score Box Plot":
        data = df.dropna(subset=["Happiness_Score"])
        fig = create_plot(
            "box", data, x="Happiness_Score",
            title="Box Plot of Happiness Score",
            ylabel="Happiness Score"
        )
        st.pyplot(fig)
        plt.close(fig)

    elif chart == "Top 5 Happiest Countries":
        top5 = df.nlargest(5, "Happiness_Score")
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(
            top5["Happiness_Score"],
            labels=top5["Country_Name"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Top 5 Happiest Countries")
        st.pyplot(fig)
        plt.close(fig)

    elif chart == "Year-wise Happiness Trend":
        year_average = df.groupby("Year")["Happiness_Score"].mean().reset_index()

        fig = create_plot(
            "line", year_average, "Year", "Happiness_Score",
            "Average Happiness Score by Year",
            "Year", "Average Happiness Score"
        )
        st.pyplot(fig)
        plt.close(fig)
