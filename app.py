import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="Cricket Dashboard", layout="wide")

df = pd.read_csv("data.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

all_teams  = sorted(df["Team"].unique())
all_venues = sorted(df["Venue"].unique())
all_years  = sorted(df["Year"].unique())

TEAM_DESC = {
    "MI":   "Mumbai Indians - 5 time IPL champions known for last over finishes.",
    "CSK":  "Chennai Super Kings - 4 time champions led by MS Dhoni.",
    "RCB":  "Royal Challengers Bangalore - Known for explosive batting lineup.",
    "KKR":  "Kolkata Knight Riders - 2 time champions with strong team culture.",
    "RR":   "Rajasthan Royals - Original IPL champions from 2008.",
    "SRH":  "Sunrisers Hyderabad - 2016 champions with strong bowling attack.",
    "DC":   "Delhi Capitals - Young squad with India brightest talents.",
    "PBKS": "Punjab Kings - High scoring entertainers from Mohali.",
}

# SIDEBAR
st.sidebar.title("Filters")

selected_team = st.sidebar.selectbox("Team", all_teams)
st.sidebar.write(TEAM_DESC.get(selected_team, ""))
st.sidebar.markdown("---")

selected_venue = st.sidebar.selectbox("Venue", ["All"] + all_venues)
st.sidebar.markdown("---")

st.sidebar.write("**Year**")
selected_year = st.sidebar.radio("", ["All"] + [str(y) for y in all_years])

# FILTER
mask = df["Team"] == selected_team
if selected_venue != "All":
    mask &= df["Venue"] == selected_venue
if selected_year != "All":
    mask &= df["Year"] == int(selected_year)

fdf = df[mask].copy().sort_values("Date")

# HEADER
st.title("Cricket Performance Dashboard")
st.write(f"Team: {selected_team}  |  Venue: {selected_venue}  |  Year: {selected_year}")
st.markdown("---")

if fdf.empty:
    st.warning("No data for this selection.")
    st.stop()

# KPIs
wins  = (fdf["Result"] == "Win").sum()
losses= (fdf["Result"] == "Loss").sum()
total = len(fdf)

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Matches",  total)
c2.metric("Wins",     wins)
c3.metric("Losses",   losses)
c4.metric("Win Rate", f"{wins/total*100:.1f}%")
c5.metric("Avg Runs", round(fdf["Runs"].mean(),1))
c6.metric("Avg SR",   round(fdf["StrikeRate"].mean(),1))
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Team Dashboard", "Venue Analysis", "Year Timeline", "Match Log"])

# TAB 1
with tab1:
    st.subheader("Recent Matches")
    recent = fdf.tail(6).iloc[::-1]
    for _, row in recent.iterrows():
        rc = "green" if row["Result"] == "Win" else "red"
        c1,c2,c3,c4,c5,c6 = st.columns([2,1,1,1,1,1])
        c1.write(f"vs **{row['Opponent']}** — {row['Date'].strftime('%d %b %Y')} — {row['Venue']}")
        c2.write(f"Runs: **{row['Runs']}**")
        c3.write(f"SR: **{row['StrikeRate']}**")
        c4.write(f"Eco: **{row['Economy']}**")
        c5.write(f"Wkts: **{row['Wickets']}**")
        c6.markdown(f":{rc}[**{row['Result']}**]")

    st.markdown("---")
    st.subheader("Charts")

    c1,c2 = st.columns(2)
    with c1:
        fig,ax = plt.subplots()
        colors = ["green" if r=="Win" else "red" for r in fdf["Result"]]
        ax.bar(range(len(fdf)), fdf["Runs"], color=colors)
        ax.set_title("Runs Per Match (Green=Win, Red=Loss)")
        ax.set_xlabel("Match"); ax.set_ylabel("Runs")
        st.pyplot(fig); plt.close()
    with c2:
        fig,ax = plt.subplots()
        opp_avg = fdf.groupby("Opponent")["Runs"].mean().sort_values()
        ax.barh(opp_avg.index, opp_avg.values)
        ax.set_title("Avg Runs vs Each Opponent")
        ax.set_xlabel("Avg Runs")
        st.pyplot(fig); plt.close()

    c3,c4 = st.columns(2)
    with c3:
        fig,ax = plt.subplots()
        ax.plot(range(len(fdf)), fdf["StrikeRate"].values)
        ax.set_title("Strike Rate Trend")
        ax.set_xlabel("Match"); ax.set_ylabel("Strike Rate")
        st.pyplot(fig); plt.close()
    with c4:
        fig,ax = plt.subplots()
        res = fdf["Result"].value_counts()
        ax.pie(res.values, labels=res.index, autopct="%1.1f%%", colors=["green","red"])
        ax.set_title("Win / Loss")
        st.pyplot(fig); plt.close()

    c5,c6 = st.columns(2)
    with c5:
        fig,ax = plt.subplots()
        colors_sc = ["green" if r=="Win" else "red" for r in fdf["Result"]]
        ax.scatter(fdf["Runs"], fdf["StrikeRate"], c=colors_sc, alpha=0.7)
        ax.set_title("Runs vs Strike Rate")
        ax.set_xlabel("Runs"); ax.set_ylabel("Strike Rate")
        st.pyplot(fig); plt.close()
    with c6:
        fig,ax = plt.subplots()
        corr = fdf[["Runs","Wickets","StrikeRate","Economy"]].corr()
        sns.heatmap(corr, annot=True, fmt=".2f", ax=ax)
        ax.set_title("Correlation Heatmap")
        st.pyplot(fig); plt.close()

    fig,ax = plt.subplots()
    ax.hist(fdf["Runs"], bins=20)
    ax.axvline(fdf["Runs"].mean(), color="red", linestyle="--", label=f"Mean: {fdf['Runs'].mean():.1f}")
    ax.set_title("Runs Distribution"); ax.set_xlabel("Runs"); ax.set_ylabel("Frequency")
    ax.legend(); st.pyplot(fig); plt.close()

# TAB 2
with tab2:
    st.subheader(f"{selected_team} Performance by Venue")
    venue_stats = fdf.groupby("Venue").agg(
        Matches=("Result","count"),
        Wins=("Result", lambda x: (x=="Win").sum()),
        AvgRuns=("Runs","mean"),
        AvgSR=("StrikeRate","mean"),
    ).reset_index()
    venue_stats["WinRate%"] = (venue_stats["Wins"]/venue_stats["Matches"]*100).round(1)
    venue_stats["AvgRuns"]  = venue_stats["AvgRuns"].round(1)
    venue_stats["AvgSR"]    = venue_stats["AvgSR"].round(1)
    st.dataframe(venue_stats.sort_values("WinRate%", ascending=False), use_container_width=True, hide_index=True)

    c1,c2 = st.columns(2)
    with c1:
        fig,ax = plt.subplots()
        v_avg = fdf.groupby("Venue")["Runs"].mean().sort_values()
        ax.barh(v_avg.index, v_avg.values)
        ax.set_title("Avg Runs by Venue"); ax.set_xlabel("Avg Runs")
        st.pyplot(fig); plt.close()
    with c2:
        fig,ax = plt.subplots()
        v_wr = fdf.groupby("Venue").apply(lambda x: (x["Result"]=="Win").sum()/len(x)*100).sort_values()
        colors_wr = ["green" if v>=50 else "red" for v in v_wr.values]
        ax.barh(v_wr.index, v_wr.values, color=colors_wr)
        ax.axvline(50, color="black", linestyle="--")
        ax.set_title("Win Rate % by Venue"); ax.set_xlabel("Win Rate %")
        st.pyplot(fig); plt.close()

    if selected_venue != "All":
        st.subheader(f"All Matches at {selected_venue}")
        vm = fdf[fdf["Venue"]==selected_venue].sort_values("Date", ascending=False)
        for _, row in vm.iterrows():
            rc = "green" if row["Result"]=="Win" else "red"
            c1,c2,c3,c4,c5,c6 = st.columns([2,1,1,1,1,1])
            c1.write(f"vs **{row['Opponent']}** — {row['Date'].strftime('%d %b %Y')}")
            c2.write(f"Runs: **{row['Runs']}**")
            c3.write(f"SR: **{row['StrikeRate']}**")
            c4.write(f"Eco: **{row['Economy']}**")
            c5.write(f"Wkts: **{row['Wickets']}**")
            c6.markdown(f":{rc}[**{row['Result']}**]")

    st.subheader("All Teams — Win Rate by Venue")
    gmask = pd.Series([True]*len(df))
    if selected_year != "All":
        gmask &= df["Year"]==int(selected_year)
    heat = df[gmask].groupby(["Team","Venue"]).apply(
        lambda x: round((x["Result"]=="Win").sum()/len(x)*100,1)
    ).unstack(fill_value=0)
    fig,ax = plt.subplots(figsize=(10,5))
    sns.heatmap(heat, annot=True, fmt=".0f", cmap="RdYlGn", ax=ax, linewidths=0.5)
    ax.set_title("Win Rate % — Team x Venue")
    st.pyplot(fig); plt.close()

# TAB 3
with tab3:
    st.subheader("Year Timeline")
    st.write("Click a year:")
    btn_cols = st.columns(len(all_years)+1)
    with btn_cols[0]:
        if st.button("All Years"):
            st.session_state["tl_year"] = "All"
    for i, yr in enumerate(all_years):
        with btn_cols[i+1]:
            if st.button(str(yr)):
                st.session_state["tl_year"] = str(yr)

    tl_year = st.session_state.get("tl_year","All")
    st.write(f"Showing: **{tl_year}**")

    tl_df = fdf.copy()
    if tl_year != "All":
        tl_df = tl_df[tl_df["Year"]==int(tl_year)]

    if tl_df.empty:
        st.warning("No data for this year.")
    else:
        tw = (tl_df["Result"]=="Win").sum()
        tl = (tl_df["Result"]=="Loss").sum()
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Matches",    len(tl_df))
        c2.metric("Wins",       tw)
        c3.metric("Losses",     tl)
        c4.metric("Avg Runs",   round(tl_df["Runs"].mean(),1))
        c5.metric("Best Score", tl_df["Runs"].max())

        tl_df = tl_df.copy()
        tl_df["YM"] = tl_df["Date"].dt.to_period("M").astype(str)

        c1,c2 = st.columns(2)
        with c1:
            monthly = tl_df.groupby("YM")["Runs"].mean().reset_index()
            fig,ax = plt.subplots()
            ax.plot(monthly["YM"], monthly["Runs"], marker="o")
            ax.set_title("Monthly Avg Runs"); ax.set_xlabel("Month"); ax.set_ylabel("Avg Runs")
            plt.xticks(rotation=30); st.pyplot(fig); plt.close()
        with c2:
            mwr = tl_df.groupby("YM").apply(lambda x: (x["Result"]=="Win").sum()/len(x)*100).reset_index()
            mwr.columns=["YM","WinRate"]
            fig,ax = plt.subplots()
            colors_m = ["green" if w>=50 else "red" for w in mwr["WinRate"]]
            ax.bar(mwr["YM"], mwr["WinRate"], color=colors_m)
            ax.axhline(50, color="black", linestyle="--")
            ax.set_title("Monthly Win Rate %"); ax.set_ylabel("Win Rate %")
            plt.xticks(rotation=30); st.pyplot(fig); plt.close()

        st.subheader("Year on Year Comparison")
        yoy_mask = df["Team"]==selected_team
        if selected_venue != "All":
            yoy_mask &= df["Venue"]==selected_venue
        yoy = df[yoy_mask].groupby("Year").agg(
            Wins=("Result", lambda x: (x=="Win").sum()),
            Losses=("Result", lambda x: (x=="Loss").sum()),
            AvgRuns=("Runs","mean"),
            AvgSR=("StrikeRate","mean"),
        ).reset_index()

        c1,c2 = st.columns(2)
        with c1:
            fig,ax = plt.subplots()
            x = np.arange(len(yoy))
            ax.bar(x-0.2, yoy["Wins"],   width=0.4, color="green", label="Wins")
            ax.bar(x+0.2, yoy["Losses"], width=0.4, color="red",   label="Losses")
            ax.set_xticks(x); ax.set_xticklabels(yoy["Year"].astype(str))
            ax.set_title("Wins vs Losses by Year"); ax.legend()
            st.pyplot(fig); plt.close()
        with c2:
            fig,ax = plt.subplots()
            ax.plot(yoy["Year"].astype(str), yoy["AvgRuns"], marker="o", label="Avg Runs")
            ax2 = ax.twinx()
            ax2.plot(yoy["Year"].astype(str), yoy["AvgSR"], marker="s", linestyle="--", color="orange", label="Avg SR")
            ax2.set_ylabel("Avg Strike Rate")
            ax.set_title("Avg Runs & SR by Year"); ax.set_ylabel("Avg Runs")
            ax.legend(loc="upper left"); ax2.legend(loc="upper right")
            st.pyplot(fig); plt.close()

        st.subheader("Full Match Timeline")
        fig,ax = plt.subplots(figsize=(12,4))
        colors_tl = ["green" if r=="Win" else "red" for r in tl_df["Result"]]
        ax.scatter(tl_df["Date"], tl_df["Runs"], c=colors_tl, alpha=0.8, zorder=3)
        ax.plot(tl_df["Date"], tl_df["Runs"], color="gray", linewidth=0.8, alpha=0.5)
        ax.set_title("Runs over Time (Green=Win, Red=Loss)")
        ax.set_xlabel("Date"); ax.set_ylabel("Runs")
        st.pyplot(fig); plt.close()

# TAB 4
with tab4:
    st.subheader("Match Log")
    search = st.text_input("Search by Opponent")
    show = fdf.copy()
    if search:
        show = show[show["Opponent"].str.upper().str.contains(search.upper())]
    display = show[["Date","Opponent","Venue","Runs","Wickets","Overs","StrikeRate","Economy","Result"]].copy()
    display["Date"] = display["Date"].dt.strftime("%d %b %Y")
    st.dataframe(display.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)

    st.subheader("Head-to-Head vs Each Opponent")
    h2h = fdf.groupby("Opponent").apply(lambda x: pd.Series({
        "Matches":  len(x),
        "Wins":     (x["Result"]=="Win").sum(),
        "Losses":   (x["Result"]=="Loss").sum(),
        "WinRate%": round((x["Result"]=="Win").sum()/len(x)*100,1),
        "AvgRuns":  round(x["Runs"].mean(),1),
    })).reset_index()

    fig,ax = plt.subplots()
    x = np.arange(len(h2h))
    ax.bar(x-0.2, h2h["Wins"],   width=0.4, color="green", label="Wins")
    ax.bar(x+0.2, h2h["Losses"], width=0.4, color="red",   label="Losses")
    ax.set_xticks(x); ax.set_xticklabels(h2h["Opponent"])
    ax.set_title(f"{selected_team} — Win/Loss vs Each Opponent"); ax.legend()
    st.pyplot(fig); plt.close()

    st.dataframe(h2h.sort_values("WinRate%", ascending=False), use_container_width=True, hide_index=True)
 
