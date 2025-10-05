import streamlit as st
import pandas as pd
import tempfile
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="📊 Sales Report Generator", layout="wide")

# -----------------------------
# Custom CSS for styling
# -----------------------------
st.markdown(
    """
    <style>
    /* Body background */
    .stApp {
        background: linear-gradient(to right, #667eea, #764ba2);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Main title */
    .main-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #FFD700;
    }

    /* Subtitle */
    .subtitle {
        font-size: 20px;
        text-align: center;
        color: #f0f0f0;
    }

    /* Button customization */
    div.stButton > button {
        background-color: #FFA500;
        color: white;
        height: 3em;
        width: 15em;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
    }

    /* File uploader customization */
    .stFileUploader>div>div {
        border: 2px dashed #FFD700;
        border-radius: 10px;
        padding: 1rem;
        background-color: rgba(255,255,255,0.1);
    }

    /* KPI boxes */
    .kpi-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Landing page
# -----------------------------
st.markdown('<h1 class="main-title">📊 Sales Report Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your CSV or Excel file and get a professional PDF report automatically!</p>', unsafe_allow_html=True)

st.write("")  # spacing

uploaded_file = st.file_uploader("Upload your Sales Data (CSV/XLSX)", type=["csv", "xlsx"])

# -----------------------------
# Process uploaded file
# -----------------------------
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()
    st.write("### Preview of Data:")
    st.dataframe(df.head())

    # Detect important columns
    try:
        sales_col = [c for c in df.columns if 'sale' in c][0]
        target_col = [c for c in df.columns if 'target' in c or 'goal' in c][0]
        region_col = [c for c in df.columns if 'region' in c or 'area' in c][0]
    except IndexError as e:
        st.error("Required column missing. Make sure your CSV has 'Sales', 'Target', and 'Region' columns.")
        st.stop()

    # -----------------------------
    # Show KPI preview
    # -----------------------------
    total_sales = df[sales_col].sum()
    average_sales = df[sales_col].mean()
    total_target = df[target_col].sum()
    achievement = (total_sales / total_target * 100) if total_target != 0 else 0

    st.markdown("### 🔑 Key Performance Indicators")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.markdown(f'<div class="kpi-box"><h3>Total Sales</h3><p>₹{total_sales:,.0f}</p></div>', unsafe_allow_html=True)
    kpi2.markdown(f'<div class="kpi-box"><h3>Average Sales</h3><p>₹{average_sales:,.2f}</p></div>', unsafe_allow_html=True)
    kpi3.markdown(f'<div class="kpi-box"><h3>Target Achievement</h3><p>{achievement:.2f}%</p></div>', unsafe_allow_html=True)

    # -----------------------------
    # Chart previews using matplotlib/seaborn
    # -----------------------------
    st.markdown("### 📊 Chart Previews")

    # Sales by Product
    if 'product' in df.columns:
        st.subheader("Sales by Product")
        fig, ax = plt.subplots(figsize=(6,3))
        sns.barplot(data=df.groupby('product')[sales_col].sum().reset_index(), x='product', y=sales_col, palette="viridis", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Sales by Region
    st.subheader("Sales by Region")
    fig2, ax2 = plt.subplots(figsize=(6,3))
    sales_region = df.groupby(region_col)[sales_col].sum().reset_index()
    ax2.pie(sales_region[sales_col], labels=sales_region[region_col], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax2.axis('equal')
    st.pyplot(fig2)

    # -----------------------------
    # Generate PDF Button
    # -----------------------------
    if st.button("Generate PDF Report"):
        with st.spinner("Generating PDF report... ⏳"):
            pdf_path = os.path.join(tempfile.gettempdir(), "Sales_Report.pdf")
            doc = SimpleDocTemplate(pdf_path, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            title_style = styles['Title']
            heading_style = styles['Heading1']
            normal_style = styles['Normal']

            # Title Page
            story.append(Spacer(1, 100))
            story.append(Paragraph("📄 Sales Report", title_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph("Generated automatically from uploaded data", normal_style))
            story.append(PageBreak())

            # KPI Page
            story.append(Paragraph("Key Performance Indicators", heading_style))
            kpi_style = ParagraphStyle(
                name='KPI',
                fontSize=12,
                textColor=colors.white,
                backColor=colors.darkblue,
                alignment=1,
                spaceBefore=8,
                spaceAfter=8,
            )
            story.append(Paragraph(f"Total Sales: ₹{total_sales:,.0f}", kpi_style))
            story.append(Paragraph(f"Average Sales: ₹{average_sales:,.2f}", kpi_style))
            story.append(Paragraph(f"Target Achievement: {achievement:.2f}%", kpi_style))
            story.append(PageBreak())

            # Bar Chart: Sales by Product
            story.append(Paragraph("Sales by Product", heading_style))
            if 'product' in df.columns:
                sales_by_product = df.groupby('product')[sales_col].sum()
                bar_chart = VerticalBarChart()
                bar_chart.x = 50
                bar_chart.y = 30
                bar_chart.height = 200
                bar_chart.width = 400
                bar_chart.data = [list(sales_by_product)]
                bar_chart.categoryAxis.categoryNames = list(sales_by_product.index)
                bar_chart.valueAxis.valueMin = 0
                bar_chart.valueAxis.valueMax = max(sales_by_product.values) + 500
                bar_chart.valueAxis.valueStep = max(sales_by_product.values)//5 + 1
                bar_chart.bars[0].fillColor = colors.lightblue
                drawing_bar = Drawing(500, 250)
                drawing_bar.add(bar_chart)
                story.append(drawing_bar)
            else:
                story.append(Paragraph("No 'Product' column found for bar chart.", normal_style))
            story.append(PageBreak())

            # Pie Chart: Sales by Region
            story.append(Paragraph("Sales by Region", heading_style))
            sales_by_region = df.groupby(region_col)[sales_col].sum()
            pie = Pie()
            pie.x = 100
            pie.y = 20
            pie.width = 200
            pie.height = 200
            pie.data = list(sales_by_region)
            pie.labels = list(sales_by_region.index)
            pie.sideLabels = True
            pie_colors = [colors.lightgreen, colors.lightcoral, colors.skyblue, colors.orange, colors.pink]
            for i, c in enumerate(pie_colors[:len(sales_by_region)]):
                pie.slices[i].fillColor = c
            drawing_pie = Drawing(400, 250)
            drawing_pie.add(pie)
            story.append(drawing_pie)
            story.append(PageBreak())

            # Table: Detailed Data
            story.append(Paragraph("Detailed Sales Data", heading_style))
            table_data = [df.columns.str.title().tolist()] + df.values.tolist()
            col_widths = [A4[0] / len(df.columns)] * len(df.columns)
            table = Table(table_data, colWidths=col_widths, hAlign='CENTER')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.whitesmoke]),
            ]))
            story.append(table)

            # Build PDF
            doc.build(story)
            st.success("🎉 PDF Report generated successfully!")

            # Download button
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=f,
                    file_name="Sales_Report.pdf",
                    mime="application/pdf"
                )
