import streamlit as st
import pandas as pd
import requests
import os
import matplotlib.pyplot as plt

file_path = "War.csv"
st.set_page_config(page_title="Israel-Gaza War", page_icon="🇵🇸")


def download_and_process_data():
    url = "https://data.techforpalestine.org/api/v2/casualties_daily.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data_json = response.json()
        if isinstance(data_json, list):
            data = pd.json_normalize(data_json)
        else:
            st.error("Unexpected JSON structure")
            return None
        data.to_csv(file_path, encoding="utf-8", index=False)
        return data
    except requests.exceptions.RequestException as e:
        if os.path.exists(file_path):
            data = pd.read_csv(file_path, encoding="utf-8")
            return data
        else:
            st.error(f"Unable to fetch the data: {e}")
            return None


data = download_and_process_data()

if data is not None:
    st.title("Israel-Gaza War (October 7 War)")
    st.subheader("By: AL-Hassan Sarrar")
    st.image("https://i.ibb.co/2WRbDST/c1-2659526-231007232113.jpg")
    cum_columns = [col for col in data.columns if "cum" in col]
    data = data.fillna(0)
    data = data.drop_duplicates()
    for col in cum_columns:
        new_col = col.replace("_cum", "_daily")
        data[new_col] = data[col].diff().fillna(0)
        data[new_col] = data[new_col].apply(lambda x: x if x >= 0 else 0)

    data["men_killed_daily"] = (
        data["ext_killed_daily"]
        - data["ext_killed_women_daily"]
        - data["ext_killed_children_daily"]
    ).apply(lambda x: x if x >= 0 else 0)
    st.sidebar.image(
        "https://i.ibb.co/gdHgT0C/palestine-flag-with-grunge-texture-png.png", width=80
    )
    st.sidebar.header("Israel-Gaza War (October 7 War)")
    st.sidebar.subheader("By: AL-Hassan Sarrar")
    num_events = len(data)
    st.sidebar.write("War day:", num_events)
    st.sidebar.write("Date:", data.iloc[-1, 0], "(yesterday)")
    casualties_columns_daily = [
        "ext_killed_daily",
        "ext_injured_daily",
        "ext_killed_children_daily",
        "ext_killed_women_daily",
        "men_killed_daily",
    ]
    total_casualties_columns = [
        "Total Killed",
        "Total Injured",
        "Total Killed Children",
        "Total Killed Women",
        "Total Killed Men",
    ]
    casualties_summary = data[casualties_columns_daily].sum()
    casualties_summary = casualties_summary.rename(
        dict(zip(casualties_columns_daily, total_casualties_columns))
    )
    st.sidebar.subheader("Casualties Summary")
    st.sidebar.write(casualties_summary)
    last_10_days_injured = data["ext_injured_daily"].tail(10).sum()
    last_10_days_killed_children = data["ext_killed_children_daily"].tail(10).sum()
    last_10_days_killed_women = data["ext_killed_women_daily"].tail(10).sum()
    last_10_days_killed_men = data["men_killed_daily"].tail(10).sum()
    last_10_days_killed = (
        last_10_days_killed_children
        + last_10_days_killed_men
        + last_10_days_killed_women
    )
    last10days = [
        {"": "Killed Last 10 Days", "Value": last_10_days_killed},
        {"": "Injured Last 10 Days", "Value": last_10_days_injured},
        {"": "Killed Children Last 10 Days", "Value": last_10_days_killed_children},
        {"": "Killed Women Last 10 Days", "Value": last_10_days_killed_women},
        {"": "Killed Men Last 10 Days", "Value": last_10_days_killed_men},
    ]
    last10days = pd.DataFrame(last10days)
    st.sidebar.subheader("Last 10 Days Information")
    st.sidebar.dataframe(last10days)
    st.header("First 5 days")
    st.write(data.head())
    st.header("Last 5 days")
    st.write(data.tail())
    col1, col2 = st.columns(2)
    with col1:
        daily_killed = data.groupby("report_date")["killed_daily"].sum()
        st.subheader("Daily Killed")
        st.line_chart(daily_killed)
    with col2:
        daily_injured = data.groupby("report_date")["injured_daily"].sum()
        st.subheader("Daily Injuries")
        st.line_chart(daily_injured)
    col1, col2 = st.columns(2)
    with col1:
        daily_massacres = data.groupby("report_date")["massacres_daily"].sum()
        st.subheader("Cumulative Massacres")
        st.line_chart(daily_massacres)
    with col2:
        cumulative_killed = data["killed_cum"]
        st.subheader("Cumulative Killed")
        st.line_chart(cumulative_killed)
    st.subheader("Proportion of Casualties")
    total_killed = data["ext_killed_daily"].sum()
    total_women = data["ext_killed_women_daily"].sum()
    total_children = data["ext_killed_children_daily"].sum()
    total_men = total_killed - total_women - total_children
    total_med = data["ext_med_killed_daily"].sum()
    total_journalists = data["ext_press_killed_daily"].sum()
    total_injured = data["injured_daily"].sum()
    totals = {
        "Women Killed": total_women,
        "Children Killed": total_children,
        "Men Killed": total_men,
        "Medical Personnel Killed": total_med,
        "Journalists Killed": total_journalists,
    }
    fig, ax = plt.subplots(figsize=(4, 5))
    ax.bar(totals.keys(), totals.values())
    ax.set_ylabel("Count")
    ax.set_title("Israel-Gaza War (Gaza and West Bank victims)")
    ax.set_xticklabels(totals.keys(), rotation=45, ha="right")
    st.pyplot(fig)
    st.header("Of those who killed ...")
    st.markdown(f"##### {total_women / total_killed * 100:.2f}% were women")
    st.markdown(f"##### {total_children / total_killed * 100:.2f}% were children")
    st.markdown(f"##### {total_men / total_killed * 100:.2f}% were men")
    st.markdown(f"##### {total_med / total_killed * 100:.2f}% were medical personnel")
    st.markdown(f"##### {total_journalists / total_killed * 100:.2f}% were journalists")
    killed_children = data["ext_killed_children_daily"]
    killed_women = data["ext_killed_women_daily"]
    killed_men = data["men_killed_daily"]
    colors = ["#FF4D4D", "#FFCC00", "#3399FF", "#66CC66"]
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        [killed_children.sum(), killed_women.sum(), killed_men.sum()],
        labels=["Killed Children", "Killed Women", "Killed Men"],
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        wedgeprops={"edgecolor": "black"},
    )
    st.pyplot(fig)
    avg_killed_daily = data["ext_killed_daily"].mean()
    avg_women_killed = data["ext_killed_women_daily"].mean()
    avg_children_killed = data["ext_killed_children_daily"].mean()
    avg_men_killed = data["men_killed_daily"].mean()
    st.header("Average number of ...")
    st.markdown(f"##### People killed daily: {avg_killed_daily:.2f}")
    st.markdown(f"##### Women killed daily: {avg_women_killed:.2f}")
    st.markdown(f"##### Children killed daily: {avg_children_killed:.2f}")
    st.markdown(f"##### Men killed daily: {avg_men_killed:.2f}")
    totals = {
        "Women": avg_women_killed,
        "Children": avg_children_killed,
        "Men Killed": avg_men_killed,
    }
    fig, ax = plt.subplots(figsize=(4, 5))
    ax.bar(totals.keys(), totals.values())
    ax.set_ylabel("Count")
    ax.set_title("Israel-Gaza War (Average daily killed)")
    ax.set_xticklabels(totals.keys(), rotation=45, ha="right")
    st.pyplot(fig)

else:
    st.write("Data is unavailable.")
