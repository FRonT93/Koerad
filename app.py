import pandas as pd
import streamlit as st
import plotly.express as px
#This UI was made with help of Chat GPT 5.4

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
    "Project by Olga Khodyreva and Jevgeni Filatov"
)

breed_list = sorted(df["Breed"].unique())

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "🏠 Overview",
        "🐕 Breed Info",
        "⚖️ Breed Comparison",
        "📊 Analysis",
        "🔍 Breed Search",
        "📄 Project Summary"
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
# 6. PROJECT SUMMARY

with tab6:

    st.header("📄 Project Summary")

    st.subheader("Introduction")

    st.write("""
The goal of this project was to create a web application that helps users explore different dog breeds and compare them based on their characteristics. Many people choose a dog because of appearance or popularity, but there are also other important things to consider, such as size, lifespan, temperament, and possible health problems.

We wanted to make a simple and interactive app where users can search for breeds, compare two breeds, and look at different graphics. The app was made with Streamlit, because it allowed us to build a web application using Python. We also used Pandas for working with the data and Plotly for creating interactive charts.

This project was not only about making an app, but also about learning how to work with data: how to clean it, prepare it, analyse it, and show it in a way that is understandable for users.
    """)

    st.subheader("Analysis Description")

    st.write("""

   The project used a dog breed dataset from Kaggle. The dataset was useful for practising data analysis and building the application, but it was also one of the main limitations of the project. Kaggle datasets are not always professionally checked, and this dataset was quite simple. Because of that, we could not treat it as a fully reliable source.

The dataset included information such as breed name, country of origin, fur color, eye color, height, lifespan, traits, and common health problems. This was enough for an educational project, but not enough for a serious dog recommendation system. Important information such as activity level, grooming needs, training difficulty, living conditions, and behaviour with children was missing.

Before using the data in the app, we had to clean and prepare it. The data was loaded with Pandas using pd.read_csv(). One cleaning step was removing duplicate breed names, because some breeds appeared more than once. This was done so that each breed would be shown only once in the application.

Some values also needed to be changed before they could be used in charts. For example, height and lifespan were written as ranges, such as 10-12 years. To make these values usable, we calculated the average of the range. Height was also converted from inches to centimetres, because centimetres are easier for users to understand.

The app includes several sections. In the overview section, users can see general information about the dataset, such as the number of breeds, average height, and average lifespan. There is also a preview of the data.

In the breed information section, the user can choose one breed and see more details about it. The comparison section allows users to compare two breeds side by side. This makes the app more practical, because users can quickly see differences in height, lifespan, traits, and health problems.

We also added different graphics to make the app more visual. The app includes histograms for height and lifespan, a scatter plot showing the relationship between height and lifespan, and bar charts for tallest breeds, longest-living breeds, countries of origin, and health problems. These graphics help users notice patterns more easily than just looking at a table.
The search and recommendation section works with filters. Users can filter breeds by fur color, eye color, traits, height, and lifespan. This is not a machine-learning recommendation system. It is a simple filter-based recommender. This was a more honest choice because the dataset is not strong or reliable enough for serious automatic recommendations.
    """)

    st.subheader("Summary and Reflection")

    st.write("""

    Overall, the project achieved its main goal. We created an interactive Streamlit app where users can explore, compare, and filter dog breeds. The app includes tables, filters, comparison tools, and different visualizations.

One of the strongest parts of the project is that the app gives users several ways to explore the data. They can look at one breed, compare two breeds, analyse charts, or use filters to find breeds that match their preferences. We wanted the app to be simple and understandable, not only for people who know programming.

The project also showed us how important data quality is. The Kaggle dataset was easy to use, but it was not fully reliable. It was simple, and some information was too general. Because of this, the app should be seen as an educational and exploratory tool, not as a professional source for choosing a dog.

From the coding side, we learned how to clean and prepare data, remove duplicates, convert text ranges into numbers, create new columns, use filters, and build visualizations. We also learned how to organise a Streamlit app into clear sections.

If we continued this project, the first improvement would be finding a better and more trustworthy dataset. A stronger dataset should include more detailed information about dog behaviour, activity needs, grooming, training, health, and living conditions.

In conclusion, this project helped us practise data cleaning, data analysis, visualization, and web app development. The app is useful for exploring dog breeds, but because the dataset is simple and not fully trustworthy, the results should be understood as exploration, not final advice.

    """)

    st.subheader("Data Source")

    st.write("""

    Dog Breeds Dataset – Maryna Shut  

    Source: https://www.kaggle.com/datasets/marshuu/dog-breeds

    """)