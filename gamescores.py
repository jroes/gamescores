import streamlit as st
import pandas as pd
import altair as alt

scores = pd.read_csv('scores.csv', index_col=6, parse_dates=['Date'])
scores['Month_Year'] = scores['Date'].dt.strftime('%b %Y')
scores = scores.sort_values(by=['Date'])

# Filter by player
unique_peeps = scores.Player.unique()
selected_player = st.sidebar.selectbox('Player', unique_peeps)
filtered_scores = scores.loc[scores.Player == selected_player]

# Filter by date
selected_start_date = st.sidebar.text_input('Start date', scores.Date.min().date())
selected_end_date = st.sidebar.text_input('End date', scores.Date.max().date())
filtered_scores = filtered_scores[filtered_scores.Date.between(selected_start_date, selected_end_date)]

# Filter by game

st.subheader("Games played by month")
games_played_by_month = filtered_scores[['Month_Year','Game']].groupby('Month_Year', sort=False, as_index=False).count()
c = alt.Chart(games_played_by_month).mark_bar().encode(
        x=alt.X('Month_Year:O', sort=None, axis=alt.Axis(title='')),
        y=alt.Y('Game', axis=alt.Axis(title='# of games')))
st.altair_chart(c, use_container_width=True)

st.subheader("Top 5 games played")
top_5_games_played = filtered_scores['Game'].value_counts().nlargest(5).reset_index()
c = alt.Chart(top_5_games_played).mark_bar().encode(
        y=alt.X('index', sort=None, axis=alt.Axis(title='')),
        x=alt.Y('Game', axis=alt.Axis(title='# of games')))
st.altair_chart(c, use_container_width=True)

# Show filtered dataset
with st.beta_expander("See raw data"):
    st.write(filtered_scores)

