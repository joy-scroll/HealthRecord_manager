def plot_metric_trend():
    import pandas as pd
    import altair as alt

    data = pd.DataFrame({
        "Date": pd.date_range("2023-01-01", periods=6, freq="M"),
        "Hemoglobin": [13.5, 13.8, 13.9, 14.0, 13.7, 14.2]
    })

    chart = alt.Chart(data).mark_line(point=True).encode(
        x="Date",
        y="Hemoglobin"
    ).properties(title="Hemoglobin Level Over Time")

    return chart
