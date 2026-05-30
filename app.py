import pandas as pd
import streamlit as st
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Dog Breeds Database",
    layout="wide"
)

# Load data
df = pd.read_csv("dog_breeds.csv")


# Function for converting ranges to averages
def range_to_mean(value):
    value = str(value)
    value = value.replace("–", "-")
    value = value.replace("—", "-")

    low, high = value.split("-")

    return (float(low) + float(high)) / 2


def make_multi_options(column_name):
    all_values = []
    for item in df[column_name].dropna():
        parts = str(item).split(",")
        for part in parts:
            clean_part = part.strip()
            if clean_part:
                all_values.append(clean_part)
    return sorted(set(all_values))


# Data cleaning
df["Height (in)"] = df["Height (in)"].apply(range_to_mean)
df["Longevity (yrs)"] = df["Longevity (yrs)"].apply(range_to_mean)

# Height in centimeters
df["Height (cm)"] = (df["Height (in)"] * 2.54).round(1)

df = df.drop_duplicates(subset=["Breed"])


# Helper function for dropdowns
def make_options(column_name):
    values = sorted(
        df[column_name]
        .dropna()
        .unique()
        .tolist()
    )
    return ["I don't know / no selection"] + values


# Streamlit UI
st.title("🐕 Dog Breeds Database")
st.caption(
    "The dataset comes from Kaggle: "
    "Dog Breeds Dataset by Maryna Shut."
)

breed_list = sorted(df["Breed"].unique())

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏠 Overview",
        "🐕 Breed Info",
        "⚖️ Breed Comparison",
        "📊 Analysis",
        "🔍 Breed Search"
    ]
)


# 1. OVERVIEW
with tab1:
    st.header("General overview of the dataset")

    col1, col2, col3 = st.columns(3)

    col1.metric("Number of breeds", len(df))
    col2.metric("Average height", f"{df['Height (cm)'].mean():.1f} cm")
    col3.metric("Average lifespan", f"{df['Longevity (yrs)'].mean():.1f} years")

    st.subheader("Dataset preview")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Descriptive statistics")
    st.dataframe(
        df[["Height (cm)", "Longevity (yrs)"]].describe(),
        use_container_width=True
    )


# 2. SINGLE BREED INFO
with tab2:
    st.header("Information about one dog breed")

    selected_breed = st.selectbox(
        "Choose a dog breed:",
        breed_list,
        key="single_breed"
    )

    breed_data = df[df["Breed"] == selected_breed].iloc[0]

    st.subheader(selected_breed)

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Country of origin:**", breed_data["Country of Origin"])
        st.write("**Fur color:**", breed_data["Fur Color"])
        st.write("**Eye color:**", breed_data["Color of Eyes"])

    with col2:
        st.metric("Height", f"{breed_data['Height (cm)']} cm")
        st.metric("Lifespan", f"{breed_data['Longevity (yrs)']} years")

    st.write("**Character traits:**")
    st.write(breed_data["Character Traits"])

    st.write("**Common health problems:**")
    st.write(breed_data["Common Health Problems"])


# 3. BREED COMPARISON
with tab3:
    st.header("Comparison of two dog breeds")

    col1, col2 = st.columns(2)

    with col1:
        breed_1 = st.selectbox(
            "Choose the first breed:",
            breed_list,
            key="compare_breed_1"
        )

    with col2:
        breed_2 = st.selectbox(
            "Choose the second breed:",
            breed_list,
            key="compare_breed_2"
        )

    compare_df = df[df["Breed"].isin([breed_1, breed_2])]

    st.subheader("Comparison table")

    st.dataframe(
        compare_df[
            [
                "Breed",
                "Country of Origin",
                "Height (cm)",
                "Longevity (yrs)",
                "Color of Eyes",
                "Character Traits",
                "Common Health Problems"
            ]
        ],
        use_container_width=True
    )

    st.subheader("Height comparison")

    fig_height = px.bar(
        compare_df,
        x="Breed",
        y="Height (cm)",
        text="Height (cm)",
        title="Height comparison of selected breeds"
    )

    st.plotly_chart(fig_height, use_container_width=True)

    st.subheader("Lifespan comparison")

    fig_life = px.bar(
        compare_df,
        x="Breed",
        y="Longevity (yrs)",
        text="Longevity (yrs)",
        title="Lifespan comparison of selected breeds"
    )

    st.plotly_chart(fig_life, use_container_width=True)


# 4. ANALYSIS
with tab4:
    st.header("Data analysis and visualization")

    st.subheader("Height distribution")

    fig_height_dist = px.histogram(
        df,
        x="Height (cm)",
        nbins=15,
        title="Distribution of dog breed heights"
    )

    st.plotly_chart(fig_height_dist, use_container_width=True)

    st.subheader("Lifespan distribution")

    fig_life_dist = px.histogram(
        df,
        x="Longevity (yrs)",
        nbins=10,
        title="Distribution of dog breed lifespans"
    )

    st.plotly_chart(fig_life_dist, use_container_width=True)

    st.subheader("Relationship between height and lifespan")

    fig_scatter = px.scatter(
        df,
        x="Height (cm)",
        y="Longevity (yrs)",
        hover_name="Breed",
        title="Relationship between height and lifespan"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    corr = df["Height (cm)"].corr(df["Longevity (yrs)"])

    st.metric(
        "Correlation between height and lifespan",
        f"{corr:.2f}"
    )

    st.subheader("Top 10 tallest breeds")

    top_height = df.sort_values(
        "Height (cm)",
        ascending=False
    ).head(10)

    fig_top_height = px.bar(
        top_height,
        x="Breed",
        y="Height (cm)",
        text="Height (cm)",
        title="Tallest dog breeds"
    )

    st.plotly_chart(fig_top_height, use_container_width=True)

    st.subheader("Top 10 breeds with the longest lifespan")

    top_life = df.sort_values(
        "Longevity (yrs)",
        ascending=False
    ).head(10)

    fig_top_life = px.bar(
        top_life,
        x="Breed",
        y="Longevity (yrs)",
        text="Longevity (yrs)",
        title="Dog breeds with the longest lifespan"
    )

    st.plotly_chart(fig_top_life, use_container_width=True)

    st.subheader("Top 10 countries of origin")

    country_count = df["Country of Origin"].value_counts().head(10)

    fig_country = px.bar(
        x=country_count.index,
        y=country_count.values,
        labels={"x": "Country", "y": "Number of breeds"},
        title="Countries with the highest number of dog breeds"
    )

    st.plotly_chart(fig_country, use_container_width=True)

    st.subheader("Relationship between health problems, height, and lifespan")

    # Split health problems into separate rows
    health_df = df.copy()

    health_df["Common Health Problems"] = health_df["Common Health Problems"].fillna("Unknown")

    health_long = health_df.assign(
        HealthProblem=health_df["Common Health Problems"].str.split(",")
    ).explode("HealthProblem")

    health_long["HealthProblem"] = health_long["HealthProblem"].str.strip()

    # Calculate average height and lifespan for each health problem
    health_summary = (
        health_long
        .groupby("HealthProblem")
        .agg(
            Count=("Breed", "count"),
            AverageHeight=("Height (cm)", "mean"),
            AverageLongevity=("Longevity (yrs)", "mean")
        )
        .reset_index()
    )

    # Show only more common health problems
    health_summary = health_summary[health_summary["Count"] >= 2]

    st.dataframe(
        health_summary.sort_values("Count", ascending=False),
        use_container_width=True
    )

    fig_health_life = px.bar(
        health_summary.sort_values("AverageLongevity"),
        x="HealthProblem",
        y="AverageLongevity",
        color="Count",
        title="Average lifespan by health problem",
        labels={
            "HealthProblem": "Health problem",
            "AverageLongevity": "Average lifespan",
            "Count": "Number of occurrences"
        }
    )

    st.plotly_chart(fig_health_life, use_container_width=True)

    fig_health_height = px.bar(
        health_summary.sort_values("AverageHeight", ascending=False),
        x="HealthProblem",
        y="AverageHeight",
        color="Count",
        title="Average height by health problem",
        labels={
            "HealthProblem": "Health problem",
            "AverageHeight": "Average height in cm",
            "Count": "Number of occurrences"
        }
    )

    st.plotly_chart(fig_health_height, use_container_width=True)


# 5. BREED SEARCH AND RECOMMENDER
with tab5:

    st.header("🔍 Breed Search and Recommender")

    selected_fur_colors = st.multiselect(
        "Choose fur colors:",
        make_multi_options("Fur Color")
    )

    selected_eye_colors = st.multiselect(
        "Choose eye colors:",
        make_multi_options("Color of Eyes")
    )

    selected_traits = st.multiselect(
        "Choose character traits:",
        make_multi_options("Character Traits")
    )

    min_height = st.slider(
        "Minimum height (cm)",
        min_value=int(df["Height (cm)"].min()),
        max_value=int(df["Height (cm)"].max()),
        value=int(df["Height (cm)"].min())
    )

    max_height = st.slider(
        "Maximum height (cm)",
        min_value=int(df["Height (cm)"].min()),
        max_value=int(df["Height (cm)"].max()),
        value=int(df["Height (cm)"].max())
    )

    min_life = st.slider(
        "Minimum lifespan (years)",
        min_value=int(df["Longevity (yrs)"].min()),
        max_value=int(df["Longevity (yrs)"].max()),
        value=int(df["Longevity (yrs)"].min())
    )

    filtered_df = df.copy()

    if selected_fur_colors:
        filtered_df = filtered_df[
            filtered_df["Fur Color"].apply(
                lambda x: any(
                    color in str(x)
                    for color in selected_fur_colors
                )
            )
        ]

    if selected_eye_colors:
        filtered_df = filtered_df[
            filtered_df["Color of Eyes"].apply(
                lambda x: any(
                    color in str(x)
                    for color in selected_eye_colors
                )
            )
        ]

    if selected_traits:
        filtered_df = filtered_df[
            filtered_df["Character Traits"].apply(
                lambda x: any(
                    trait in str(x)
                    for trait in selected_traits
                )
            )
        ]

    filtered_df = filtered_df[
        (filtered_df["Height (cm)"] >= min_height)
        & (filtered_df["Height (cm)"] <= max_height)
        & (filtered_df["Longevity (yrs)"] >= min_life)
    ]

    st.subheader("Found dog breeds")

    st.write(
        f"Found {len(filtered_df)} matching breeds."
    )

    st.dataframe(
        filtered_df[
            [
                "Breed",
                "Country of Origin",
                "Fur Color",
                "Color of Eyes",
                "Height (cm)",
                "Longevity (yrs)",
                "Character Traits",
                "Common Health Problems"
            ]
        ],
        use_container_width=True
    )
