import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
st.set_page_config(layout="wide")

# datasets

# genre data unchunked
genres_data = [{
  "genre": "comedy",
  "joy": 31938,
  "sadness": 6585,
  "anger": 19939,
  "surprise": 622,
  "fear": 11423,
  "love": 1363
 },
{
  "genre": "romance",
  "joy": 26040,
  "sadness": 5670,
  "anger": 16096,
  "surprise": 481,
  "fear": 9401,
  "love": 1277
 },
 {
  "genre": "adventure",
  "joy": 14931,
  "sadness": 3318,
  "anger": 10048,
  "surprise": 251,
  "fear": 7530,
  "love": 403
 },
 {
  "genre": "biography",
  "joy": 4696,
  "sadness": 992,
  "anger": 3589,
  "surprise": 72,
  "fear": 1609,
  "love": 159
 },
 {
  "genre": "drama",
  "joy": 55476,
  "sadness": 12402,
  "anger": 39176,
  "surprise": 987,
  "fear": 21938,
  "love": 2108
 },
 {
  "genre": "history",
  "joy": 2490,
  "sadness": 583,
  "anger": 2140,
  "surprise": 31,
  "fear": 1077,
  "love": 87
 },
 {
  "genre": "action",
  "joy": 21285,
  "sadness": 4884,
  "anger": 16290,
  "surprise": 377,
  "fear": 10825,
  "love": 539
 },
 {
  "genre": "crime",
  "joy": 22806,
  "sadness": 5135,
  "anger": 18883,
  "surprise": 374,
  "fear": 10248,
  "love": 764
 },
 {
  "genre": "thriller",
  "joy": 36099,
  "sadness": 8906,
  "anger": 29286,
  "surprise": 652,
  "fear": 18669,
  "love": 1079
 },
 {
  "genre": "mystery",
  "joy": 14544,
  "sadness": 4006,
  "anger": 12096,
  "surprise": 311,
  "fear": 8099,
  "love": 468
 },
 {
  "genre": "sci-fi",
  "joy": 14742,
  "sadness": 3475,
  "anger": 10102,
  "surprise": 273,
  "fear": 8486,
  "love": 394
 },
 {
  "genre": "fantasy",
  "joy": 10349,
  "sadness": 2591,
  "anger": 6378,
  "surprise": 205,
  "fear": 4546,
  "love": 405
 },
 {
  "genre": "horror",
  "joy": 10683,
  "sadness": 2945,
  "anger": 8036,
  "surprise": 197,
  "fear": 5977,
  "love": 361
 },
 {
  "genre": "music",
  "joy": 2597,
  "sadness": 518,
  "anger": 1580,
  "surprise": 39,
  "fear": 750,
  "love": 96
 },
 {
  "genre": "western",
  "joy": 1963,
  "sadness": 425,
  "anger": 1598,
  "surprise": 26,
  "fear": 826,
  "love": 51
 },
 {
  "genre": "war",
  "joy": 3131,
  "sadness": 650,
  "anger": 2485,
  "surprise": 38,
  "fear": 1393,
  "love": 109
 },
 {
  "genre": "adult",
  "joy": 116,
  "sadness": 18,
  "anger": 60,
  "surprise": 2,
  "fear": 30,
  "love": 6
 },
 {
  "genre": "musical",
  "joy": 1060,
  "sadness": 222,
  "anger": 613,
  "surprise": 16,
  "fear": 345,
  "love": 46
 },
 {
  "genre": "animation",
  "joy": 2271,
  "sadness": 526,
  "anger": 1565,
  "surprise": 61,
  "fear": 963,
  "love": 50
 },
 {
  "genre": "sport",
  "joy": 1568,
  "sadness": 319,
  "anger": 930,
  "surprise": 23,
  "fear": 492,
  "love": 57
 },
 {
  "genre": "family",
  "joy": 2322,
  "sadness": 457,
  "anger": 1318,
  "surprise": 40,
  "fear": 891,
  "love": 86
 },
 {
  "genre": "short",
  "joy": 525,
  "sadness": 118,
  "anger": 296,
  "surprise": 8,
  "fear": 161,
  "love": 32
 },
 {
  "genre": "film-noir",
  "joy": 715,
  "sadness": 166,
  "anger": 510,
  "surprise": 11,
  "fear": 250,
  "love": 25
 },
 {
  "genre": "documentary",
  "joy": 492,
  "sadness": 120,
  "anger": 305,
  "surprise": 6,
  "fear": 183,
  "love": 34
 }]

# ratings data unchunked
ratings_data = [
    {"rating": "bad", "joy": 2071, "sadness": 431, "anger": 1301, "surprise": 27, "fear": 968, "love": 62},
    {"rating": "average", "joy": 56134, "sadness": 13162, "anger": 40953, "surprise": 996, "fear": 25092, "love": 2197},
    {"rating": "good", "joy": 38352, "sadness": 8188, "anger": 26092, "surprise": 672, "fear": 15324, "love": 1315},
]

# emotions
emotions = ['joy', 'sadness', 'anger', 'surprise', 'fear', 'love']

# side bar options
# choosing genre or ratings dataset
dataset_option = st.sidebar.radio("Choose Dataset", ("Genres", "Ratings"))
# choose category (joy, anger, etc. or avg, good, bad)
selected_category = st.sidebar.selectbox(
    f"Select a {'Genre' if dataset_option == 'Genres' else 'Rating'}",
    [entry['genre'] for entry in genres_data] if dataset_option == "Genres" else [entry['rating'] for entry in ratings_data]
)
# stacked bar or heatmap for overall stats
visualization_option = st.sidebar.radio("Choose Visualization", ('Stacked Bar Chart', 'Heatmap'))
# normalize or dont
normalize_data = st.sidebar.checkbox("Normalize Data", value=True)

# select data based on user's chosen dataset
current_data = genres_data if dataset_option == "Genres" else ratings_data
category_key = 'genre' if dataset_option == "Genres" else 'rating'

def plot_radial_chart(data, emotions, category, normalize=False):
    category_data = next(entry for entry in data if entry[category_key] == selected_category)
    values = [category_data[emotion] for emotion in emotions]
    # normalize data if selected
    if normalize:
        # find max value and divide each emotion value by max value
        max_value = max(max(entry[emotion] for emotion in emotions) for entry in data)
        values = [v / max_value for v in values]
    
    # calculate angles for radar chart
    angles = np.linspace(0, 2 * np.pi, len(emotions), endpoint=False).tolist()
    values += values[:1]  # close circle
    angles += angles[:1]  # close circle
    # create fig and polar subplot
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': 'polar'})
    # plot radial chart
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    # set emotion labels as x ticks
    ax.set_yticks([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(emotions)
    # title and position
    ax.set_title(f"Emotion Distribution for {category}", y=1.1, fontsize=16)
    return fig

def plot_stacked_bar_chart(data, emotions, normalize=False):
    category_data = [entry[category_key] for entry in data]
    # normalize data if selected
    if normalize:
        # emotion values turned into proportions
        values = {emotion: [entry[emotion] / sum(entry[e] for e in emotions) for entry in data] for emotion in emotions}
    else:
        values = {emotion: [entry[emotion] for entry in data] for emotion in emotions}

    fig, ax = plt.subplots(figsize=(12, 8.5))
    bottom_values = np.zeros(len(data))
    # plot stacked bars for each emotion
    for emotion, val in values.items():
        ax.bar(category_data, val, bottom=bottom_values, label=emotion)
        bottom_values += np.array(val)
    # chart labels, title, legend
    ax.set_title(f"Stacked Bar Chart of Emotions by {'Genre' if category_key == 'genre' else 'Rating'}", fontsize=16)
    ax.set_xlabel("Category", fontsize=12)
    ax.set_ylabel("Proportion" if normalize else "Emotion Count", fontsize=12)
    ax.legend(title="Emotions", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    return fig

def plot_heatmap(data, emotions, normalize=False):
    category_data = [entry[category_key] for entry in data]
    emotion_values = np.array([[entry[emotion] for emotion in emotions] for entry in data])
    # normalize values if selected
    if normalize:
        # emotion values turned into proportions
        values = np.array([
            [value / sum(entry[emotion] for emotion in emotions) for value in entry_values]
            for entry_values, entry in zip(emotion_values, data)
        ])
    else:
        values = emotion_values

    fig, ax = plt.subplots(figsize=(12, 8))
    # plot heatmap
    cax = ax.imshow(values, cmap='YlGnBu', aspect='auto')
    # x ticks labels are emotions, y tick labels are categories
    ax.set_xticks(np.arange(len(emotions)))
    ax.set_xticklabels(emotions, fontsize=10)
    ax.set_yticks(np.arange(len(category_data)))
    ax.set_yticklabels(category_data, fontsize=10)
    # add colorbar for emotion intensity
    fig.colorbar(cax, ax=ax, orientation='vertical', label='Normalized Emotion Intensity' if normalize else 'Emotion Intensity')
    # chart labels, title
    ax.set_title(f"Emotion Heatmap by {'Genre' if category_key == 'genre' else 'Rating'}", fontsize=16)
    ax.set_xlabel("Emotion", fontsize=12)
    ax.set_ylabel("Category", fontsize=12)

    return fig

# display plots
col1, col2 = st.columns([2, 3])

# column 1 is radial plot
with col1:
    fig_radial = plot_radial_chart(current_data, emotions, selected_category, normalize=normalize_data)
    st.pyplot(fig_radial)
# column 2 is stacked bar or heatmap
with col2:
    if visualization_option == 'Stacked Bar Chart':
        fig_bar = plot_stacked_bar_chart(current_data, emotions, normalize=normalize_data)
        st.pyplot(fig_bar)
    elif visualization_option == 'Heatmap':
        fig_heatmap = plot_heatmap(current_data, emotions, normalize=normalize_data)
        st.pyplot(fig_heatmap)