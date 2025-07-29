from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load data
df = pd.read_csv('pharmacy_otc_sales_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

@app.route("/", methods=["GET", "POST"])
def dashboard():
    selected_country = request.form.get("country", "")

    # Filter data
    filtered_df = df[df['Country'] == selected_country] if selected_country else df

    # Summary stats
    total_records = len(filtered_df)
    avg_boxes = round(filtered_df["Boxes Shipped"].mean(), 2)
    total_amount = round(filtered_df["Amount ($)"].sum(), 2)
    top_seller = filtered_df["Sales Person"].value_counts().idxmax()

    # Table
    table_html = filtered_df.to_html(classes='data', index=False)

    # Graph 1: Sales Amount by Country
    bar_fig = px.bar(
        df.groupby('Country')['Amount ($)'].sum().reset_index(),
        x='Country', y='Amount ($)',
        title="Total Sales by Country",
        color='Country'
    )
    bar_html = pio.to_html(bar_fig, full_html=False)

    # Graph 2: Sales Trend Over Time
    line_fig = px.line(
        df.groupby('Date')['Amount ($)'].sum().reset_index(),
        x='Date', y='Amount ($)',
        title="Sales Over Time"
    )
    line_html = pio.to_html(line_fig, full_html=False)

    return render_template("dashboard.html",
                           total_records=total_records,
                           avg_boxes=avg_boxes,
                           total_amount=total_amount,
                           top_seller=top_seller,
                           countries=sorted(df['Country'].dropna().unique()),
                           selected_country=selected_country,
                           tables=table_html,
                           bar_chart=bar_html,
                           line_chart=line_html)

if __name__ == "__main__":
    app.run(debug=True)
