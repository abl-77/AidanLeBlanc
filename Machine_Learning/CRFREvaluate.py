import pandas as pd
import altair as alt
import pickle

with open("./abl77/results/fastfood_times.pkl", "rb") as f:
    fastfood_times = pickle.load(f)
    
with open("./abl77/results/fourier_times.pkl", "rb") as f:
    fourier_times = pickle.load(f)
    
with open("./abl77/results/random_times.pkl", "rb") as f:
    random_times = pickle.load(f)
    
electricity_df = pd.DataFrame({
    "x": [1, 5, 10, 25] * 3,
    "y": fastfood_times[:4] + fourier_times[:4] + random_times[:4],
    "category": ["Fastfood"] * 4 + ["Fourier"] * 4 + ["Random"] * 4
})

electricity_chart = alt.Chart(electricity_df).mark_line(point=True).encode(
    x=alt.X("x:Q", title="Number of Training Epochs"),  
    y=alt.Y("y:Q", title="Runtime"),  
    color=alt.Color("category:N", title="Line"),  
    tooltip=["category:N", "x:Q", "y:Q"] 
).properties(
    title="Training Runtime for Electricity Dataset",
    width=600,
    height=400
)

electricity_chart.save("./abl77/results/electricity_runtime.html")

stock_df = pd.DataFrame({
    "x": [1, 5, 10, 25] * 3,
    "y": fastfood_times[4:] + fourier_times[4:] + random_times[4:],
    "category": ["Fastfood"] * 4 + ["Fourier"] * 4 + ["Random"] * 4
})

stock_chart = alt.Chart(stock_df).mark_line(point=True).encode(
    x=alt.X("x:Q", title="Number of Training Epochs"),  
    y=alt.Y("y:Q", title="Runtime"),  
    color=alt.Color("category:N", title="Line"),  
    tooltip=["category:N", "x:Q", "y:Q"] 
).properties(
    title="Training Runtime for Stock Dataset",
    width=600,
    height=400
)

stock_chart.save("./abl77/results/stock_runtime.html")

df = pd.read_pickle("./abl77/results/Results.pkl")

df["model"] = df["names"].str.replace(r"\d+", "", regex=True).str.strip()
df["x_value"] = df["names"].str.extract(r"(\d+)\s\w+$").astype(int)

# Reshape DataFrame for plotting
df_melted = df.melt(
    id_vars=["model", "x_value"], 
    value_vars=["MAE", "MSE"], 
    var_name="Metric", 
    value_name="Value"
)


df_melted = df_melted.sort_values(by=["model", "Metric", "x_value"])

# Line chart with multiple lines
chart = alt.Chart(df_melted).mark_line(point=False).encode(
    x=alt.X('x_value:Q', title='Number of Training Epochs'),
    y=alt.Y('Value:Q', title='Metric Value'),
    color=alt.Color('model:N', title='Model'),  # Differentiates lines by color
    strokeDash=alt.StrokeDash('Metric:N', title='Metric'),
    tooltip=['model:N', 'Metric:N', 'x_value:Q', 'Value:Q']  # Optional: Add tooltips
).properties(
    title="MSE and MAE Values Vs. Number of Training Epochs Graph",
    width=600,
    height=400
)

chart.save("./abl77/results/Results.html")

df[['model', 'environment']] = df['model'].str.split(' ', n=1, expand=True)

df_environment = df.melt(
    id_vars=["model", "x_value", "environment"], 
    value_vars=["MAE", "MSE"], 
    var_name="Metric", 
    value_name="Value"
)

filtered_df = df_environment[df_environment["x_value"] == 5]

electricity_df = filtered_df[filtered_df["environment"] == "Electricity"][["model", "Metric", "Value"]]
stock_df = filtered_df[filtered_df["environment"] == "Stock"][["model", "Metric", "Value"]]


electricity_table = alt.Chart(electricity_df).mark_text().encode(
        row=alt.Row("model:N", title="Model"),
        column=alt.Column("Metric:N", title="Metric"),
        text=alt.Text("Value:Q", format=".2f")
    ).properties(
        title="Electricity Table",
        width=200,
        height=100
    )
    
stock_table = alt.Chart(stock_df).mark_text().encode(
        row=alt.Row("model:N", title="Model"),
        column=alt.Column("Metric:N", title="Metric"),
        text=alt.Text("Value:Q", format=".2f")
    ).properties(
        title="Stock Table",
        width=200,
        height=100
    )

# Combine the charts
table = alt.vconcat(electricity_table, stock_table, spacing=20).configure_view(
    strokeWidth=1,
    stroke="lightgray",
    fill="#f9f9f9"  # Set the background fill for each chart
)


table.save("./abl77/results/ResultsTable.html")


