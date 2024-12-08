import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Data: Matchups and player stats
matchups_data = matchups.copy()
player_data = player_historical_stats_df.copy()

# Title
st.title("Interactive NFL Predictions Dashboard")

# Matchup Filters
st.sidebar.header("Filters")
selected_weather = st.sidebar.multiselect("Select Weather Conditions", matchups_data["Weather"].unique(), default=matchups_data["Weather"].unique())
selected_teams = st.sidebar.multiselect("Select Teams", pd.concat([matchups_data["Home_Team"], matchups_data["Away_Team"]]).unique())

# Filter matchups
filtered_matchups = matchups_data[
    (matchups_data["Weather"].isin(selected_weather)) &
    ((matchups_data["Home_Team"].isin(selected_teams)) | (matchups_data["Away_Team"].isin(selected_teams)))
]

# Display Matchups Table
st.subheader("Filtered Matchups")
st.table(filtered_matchups)

# Visualization: Win Probabilities
st.subheader("Win Probabilities")
fig, ax = plt.subplots(figsize=(10, 6))
home_probs = filtered_matchups["Win_Probability_Home"]
away_probs = filtered_matchups["Win_Probability_Away"]
matchup_labels = filtered_matchups["Home_Team"] + " vs " + filtered_matchups["Away_Team"]
bar_width = 0.4
x = range(len(home_probs))
ax.bar(x, home_probs, width=bar_width, label="Home Team", color="blue")
ax.bar([i + bar_width for i in x], away_probs, width=bar_width, label="Away Team", color="orange")
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(matchup_labels, rotation=45, ha="right")
ax.set_title("Win Probabilities for Matchups")
ax.set_ylabel("Probability")
ax.legend()
st.pyplot(fig)

# Visualization: Player Performance
selected_position = st.sidebar.selectbox("Select Position", ["QB", "RB", "WR", "TE"])
top_players = player_data[player_data["Position"] == selected_position].nlargest(5, "Predicted_Yards")
st.subheader(f"Top {selected_position} Performances")
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(top_players["Player"], top_players["Predicted_Yards"], color="skyblue")
ax.set_title(f"Top Predicted {selected_position} Performances (Yards)")
ax.set_xlabel("Predicted Yards")
ax.grid(axis="x", linestyle="--", alpha=0.7)
st.pyplot(fig)

# Weather Pie Chart
st.subheader("Weather Distribution")
fig, ax = plt.subplots(figsize=(6, 6))
weather_counts = filtered_matchups["Weather"].value_counts()
ax.pie(weather_counts, labels=weather_counts.index, autopct="%1.1f%%", startangle=140, colors=["gold", "lightblue", "gray", "orange", "lightgreen"])
ax.set_title("Weather Conditions for Filtered Matchups")
st.pyplot(fig)
