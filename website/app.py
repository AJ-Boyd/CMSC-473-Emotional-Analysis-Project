import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
st.set_page_config(layout="wide")

# datasets
genres_data = [{'genre': 'comedy', 'joy': 12161, 'sadness': 3044, 'anger': 6783, 'surprise': 347, 'fear': 2414, 'love': 432}, 
{'genre': 'romance', 'joy': 9779, 'sadness': 2615, 'anger': 5195, 'surprise': 252, 'fear': 1919, 'love': 398}, 
{'genre': 'adventure', 'joy': 6325, 'sadness': 1652, 'anger': 4187, 'surprise': 158, 'fear': 2226, 'love': 173}, 
{'genre': 'biography', 'joy': 1692, 'sadness': 427, 'anger': 1190, 'surprise': 37, 'fear': 300, 'love': 54}, 
{'genre': 'drama', 'joy': 20228, 'sadness': 5673, 'anger': 13035, 'surprise': 532, 'fear': 4400, 'love': 683}, 
{'genre': 'history', 'joy': 914, 'sadness': 274, 'anger': 776, 'surprise': 15, 'fear': 267, 'love': 34}, 
{'genre': 'action', 'joy': 8824, 'sadness': 2451, 'anger': 6635, 'surprise': 230, 'fear': 2956, 'love': 220}, 
{'genre': 'crime', 'joy': 8363, 'sadness': 2326, 'anger': 6762, 'surprise': 234, 'fear': 2154, 'love': 246}, 
{'genre': 'thriller', 'joy': 13877, 'sadness': 4201, 'anger': 10966, 'surprise': 387, 'fear': 4607, 'love': 360}, 
{'genre': 'mystery', 'joy': 5473, 'sadness': 1861, 'anger': 4433, 'surprise': 172, 'fear': 2019, 'love': 156}, 
{'genre': 'sci-fi', 'joy': 6178, 'sadness': 1724, 'anger': 4127, 'surprise': 167, 'fear': 2562, 'love': 158}, 
{'genre': 'fantasy', 'joy': 4355, 'sadness': 1284, 'anger': 2477, 'surprise': 112, 'fear': 1269, 'love': 151}, 
{'genre': 'horror', 'joy': 4446, 'sadness': 1485, 'anger': 3289, 'surprise': 118, 'fear': 1720, 'love': 114}, 
{'genre': 'music', 'joy': 975, 'sadness': 229, 'anger': 527, 'surprise': 20, 'fear': 151, 'love': 33}, 
{'genre': 'western', 'joy': 758, 'sadness': 212, 'anger': 576, 'surprise': 13, 'fear': 172, 'love': 18}, 
{'genre': 'war', 'joy': 1196, 'sadness': 301, 'anger': 946, 'surprise': 25, 'fear': 317, 'love': 42}, 
{'genre': 'adult', 'joy': 52, 'sadness': 8, 'anger': 19, 'surprise': 2, 'fear': 6, 'love': 1}, 
{'genre': 'musical', 'joy': 455, 'sadness': 114, 'anger': 247, 'surprise': 10, 'fear': 101, 'love': 19}, 
{'genre': 'animation', 'joy': 941, 'sadness': 244, 'anger': 663, 'surprise': 44, 'fear': 281, 'love': 15}, 
{'genre': 'sport', 'joy': 576, 'sadness': 145, 'anger': 286, 'surprise': 13, 'fear': 81, 'love': 20}, 
{'genre': 'family', 'joy': 1044, 'sadness': 221, 'anger': 485, 'surprise': 29, 'fear': 252, 'love': 26}, 
{'genre': 'short', 'joy': 177, 'sadness': 63, 'anger': 94, 'surprise': 3, 'fear': 31, 'love': 13}, 
{'genre': 'film-noir', 'joy': 280, 'sadness': 88, 'anger': 190, 'surprise': 5, 'fear': 71, 'love': 8}, 
{'genre': 'documentary', 'joy': 227, 'sadness': 65, 'anger': 120, 'surprise': 5, 'fear': 46, 'love': 16}]

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