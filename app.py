import pandas as pd
import streamlit as st
import plotly.express as px

# Andmete laadimine
df = pd.read_csv("dog_breeds.csv")


# Funktsioon vahemike teisendamiseks keskmiseks
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


# Andmete puhastamine
df["Height (in)"] = df["Height (in)"].apply(range_to_mean)
df["Longevity (yrs)"] = df["Longevity (yrs)"].apply(range_to_mean)

# Kõrgus sentimeetrites
df["Height (cm)"] = (df["Height (in)"] * 2.54).round(1)

# Kõrgus sentimeetrites

df["Height (cm)"] = (df["Height (in)"] * 2.54).round(1)
df = df.drop_duplicates(subset=["Breed"])

# Abifunktsioon dropdownide jaoks

def make_options(column_name):
    values = sorted(
        df[column_name]
        .dropna()
        .unique()
        .tolist()
    )
    return ["Ei tea / ei vali"] + values

# Streamlit UI

st.title("🐕 Koeratõugude andmebaas")
# Lehe seaded
st.set_page_config(
    page_title="Koeratõugude andmebaas",
    layout="wide"
)

st.title("🐕 Koeratõugude andmebaas")
breed_list = sorted(df["Breed"].unique())
# Vahelehed
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏠 Ülevaade",
        "🐕 Tõu info",
        "⚖️ Tõugude võrdlus",
        "📊 Analüüs",
        "🔍 Tõu otsing"
    ]
)

# 1. ÜLEVAADE
with tab1:
    st.header("Üldine ülevaade andmestikust")

    col1, col2, col3 = st.columns(3)

    col1.metric("Tõugude arv", len(df))
    col2.metric("Keskmine kõrgus", f"{df['Height (cm)'].mean():.1f} cm")
    col3.metric("Keskmine eluiga", f"{df['Longevity (yrs)'].mean():.1f} aastat")

    st.subheader("Andmestiku eelvaade")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Kirjeldav statistika")
    st.dataframe(
        df[["Height (cm)", "Longevity (yrs)"]].describe(),
        use_container_width=True
    )


# 2. ÜHE TÕU INFO
with tab2:
    st.header("Ühe koeratõu info")

    selected_breed = st.selectbox(
        "Vali koeratõug:",
        breed_list,
        key="single_breed"
    )

    breed_data = df[df["Breed"] == selected_breed].iloc[0]

    st.subheader(selected_breed)

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Päritoluriik:**", breed_data["Country of Origin"])
        st.write("**Karvavärv:**", breed_data["Fur Color"])
        st.write("**Silmade värv:**", breed_data["Color of Eyes"])

    with col2:
        st.metric("Kõrgus", f"{breed_data['Height (cm)']} cm")
        st.metric("Eluiga", f"{breed_data['Longevity (yrs)']} aastat")

    st.write("**Iseloomuomadused:**")
    st.write(breed_data["Character Traits"])

    st.write("**Levinud terviseprobleemid:**")
    st.write(breed_data["Common Health Problems"])


# 3. KAHE TÕU VÕRDLUS
with tab3:
    st.header("Kahe koeratõu võrdlus")

    col1, col2 = st.columns(2)

    with col1:
        breed_1 = st.selectbox(
            "Vali esimene tõug:",
            breed_list,
            key="compare_breed_1"
        )

    with col2:
        breed_2 = st.selectbox(
            "Vali teine tõug:",
            breed_list,
            key="compare_breed_2"
        )

    compare_df = df[df["Breed"].isin([breed_1, breed_2])]

    st.subheader("Võrdlustabel")

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

    st.subheader("Kõrguse võrdlus")

    fig_height = px.bar(
        compare_df,
        x="Breed",
        y="Height (cm)",
        text="Height (cm)",
        title="Valitud tõugude kõrguse võrdlus"
    )

    st.plotly_chart(fig_height, use_container_width=True)

    st.subheader("Eluea võrdlus")

    fig_life = px.bar(
        compare_df,
        x="Breed",
        y="Longevity (yrs)",
        text="Longevity (yrs)",
        title="Valitud tõugude eluea võrdlus"
    )

    st.plotly_chart(fig_life, use_container_width=True)


# 4. ANALÜÜS
with tab4:
    st.header("Andmete analüüs ja visualiseerimine")

    st.subheader("Kõrguste jaotus")

    fig_height_dist = px.histogram(
        df,
        x="Height (cm)",
        nbins=15,
        title="Koeratõugude kõrguse jaotus"
    )

    st.plotly_chart(fig_height_dist, use_container_width=True)

    st.subheader("Eluea jaotus")

    fig_life_dist = px.histogram(
        df,
        x="Longevity (yrs)",
        nbins=10,
        title="Koeratõugude eluea jaotus"
    )

    st.plotly_chart(fig_life_dist, use_container_width=True)

    st.subheader("Kõrguse ja eluea seos")

    fig_scatter = px.scatter(
        df,
        x="Height (cm)",
        y="Longevity (yrs)",
        hover_name="Breed",
        title="Kõrguse ja eluea seos"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    corr = df["Height (cm)"].corr(df["Longevity (yrs)"])

    st.metric(
        "Kõrguse ja eluea korrelatsioon",
        f"{corr:.2f}"
    )

    st.subheader("Top 10 kõige kõrgemat tõugu")

    top_height = df.sort_values(
        "Height (cm)",
        ascending=False
    ).head(10)

    fig_top_height = px.bar(
        top_height,
        x="Breed",
        y="Height (cm)",
        text="Height (cm)",
        title="Kõige kõrgemad koeratõud"
    )

    st.plotly_chart(fig_top_height, use_container_width=True)

    st.subheader("Top 10 pikima elueaga tõugu")

    top_life = df.sort_values(
        "Longevity (yrs)",
        ascending=False
    ).head(10)

    fig_top_life = px.bar(
        top_life,
        x="Breed",
        y="Longevity (yrs)",
        text="Longevity (yrs)",
        title="Kõige pikema elueaga koeratõud"
    )

    st.plotly_chart(fig_top_life, use_container_width=True)

    st.subheader("Top 10 päritoluriiki")

    country_count = df["Country of Origin"].value_counts().head(10)

    fig_country = px.bar(
        x=country_count.index,
        y=country_count.values,
        labels={"x": "Riik", "y": "Tõugude arv"},
        title="Riigid, kust pärineb kõige rohkem koeratõuge"
    )

    st.plotly_chart(fig_country, use_container_width=True)


# 5. TÕU OTSING JA SOOVITAJA
with tab5:

    st.header("🔍 Tõu otsing ja soovitaja")

    selected_fur_colors = st.multiselect(

        "Vali karvavärvid:",

        make_multi_options("Fur Color")

    )

    selected_eye_colors = st.multiselect(

        "Vali silmade värvid:",

        make_multi_options("Color of Eyes")

    )

    selected_traits = st.multiselect(

        "Vali iseloomuomadused:",

        make_multi_options("Character Traits")

    )

    min_height = st.slider(

        "Minimaalne kõrgus (cm)",

        min_value=int(df["Height (cm)"].min()),

        max_value=int(df["Height (cm)"].max()),

        value=int(df["Height (cm)"].min())

    )

    max_height = st.slider(

        "Maksimaalne kõrgus (cm)",

        min_value=int(df["Height (cm)"].min()),

        max_value=int(df["Height (cm)"].max()),

        value=int(df["Height (cm)"].max())

    )

    min_life = st.slider(

        "Minimaalne eluiga (aastates)",

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

    st.subheader("Leitud koeratõud")

    st.write(

        f"Leiti {len(filtered_df)} sobivat tõugu."

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