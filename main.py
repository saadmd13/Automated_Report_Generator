# main.py

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
import pandas as pd


# -------------------------------------
# Step 1: Prepare Your Data
# -------------------------------------
data = {
    'Date': ['01-10-2025', '01-10-2025', '02-10-2025', '02-10-2025'],
    'Product': ['Product A', 'Product B', 'Product C', 'Product D'],
    'Region': ['North', 'South', 'East', 'West'],
    'Sales': [1200, 900, 1500, 1100],
    'Target': [1500, 1000, 1600, 1200]
}
df = pd.DataFrame(data)

# Metrics
total_sales = df['Sales'].sum()
average_sales = df['Sales'].mean()
total_target = df['Target'].sum()
achievement = total_sales / total_target * 100


# -------------------------------------
# Step 2: PDF Setup
# -------------------------------------
pdf_file = "Sales_Report_Dashboard.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=A4)
styles = getSampleStyleSheet()
story = []

title_style = styles['Title']
heading_style = styles['Heading1']
normal_style = styles['Normal']


# -------------------------------------
# Step 3: Add Page Number Footer
# -------------------------------------
def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(200*2.8, 15, text)


# -------------------------------------
# Step 4: Title Page
# -------------------------------------
story.append(Spacer(1, 150))
story.append(Paragraph("📊 Sales Performance Report", title_style))
story.append(Spacer(1, 20))
story.append(Paragraph("Generated using ReportLab + Python", normal_style))
story.append(Spacer(1, 10))
story.append(Paragraph("Report Period: October 2025", normal_style))
story.append(PageBreak())


# -------------------------------------
# Step 5: KPI Summary Page
# -------------------------------------
story.append(Paragraph("Key Performance Indicators (KPIs)", heading_style))
story.append(Spacer(1, 20))

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


# -------------------------------------
# Step 6: Dynamic Charts Page
# -------------------------------------
story.append(Paragraph("Visual Analysis", heading_style))
story.append(Spacer(1, 20))

# Bar Chart: Sales by Product
sales_by_product = df.groupby('Product')['Sales'].sum()
bar_chart = VerticalBarChart()
bar_chart.x = 50
bar_chart.y = 30
bar_chart.height = 200
bar_chart.width = 400
bar_chart.data = [list(sales_by_product)]
bar_chart.categoryAxis.categoryNames = list(sales_by_product.index)
bar_chart.valueAxis.valueMin = 0
bar_chart.valueAxis.valueMax = max(sales_by_product.values) + 500
bar_chart.valueAxis.valueStep = 500
bar_chart.bars[0].fillColor = colors.lightblue

drawing_bar = Drawing(500, 250)
drawing_bar.add(bar_chart)
story.append(Paragraph("Sales by Product", styles["Heading2"]))
story.append(drawing_bar)
story.append(Spacer(1, 20))

# Pie Chart: Regional Sales Distribution
sales_by_region = df.groupby('Region')['Sales'].sum()
pie = Pie()
pie.x = 100
pie.y = 20
pie.width = 200
pie.height = 200
pie.data = list(sales_by_region)
pie.labels = list(sales_by_region.index)
pie.sideLabels = True

# Assign dynamic colors for clarity
pie_colors = [colors.lightgreen, colors.lightcoral, colors.skyblue, colors.orange]
for i, c in enumerate(pie_colors[:len(sales_by_region)]):
    pie.slices[i].fillColor = c

drawing_pie = Drawing(400, 250)
drawing_pie.add(pie)
story.append(Paragraph("Sales by Region", styles["Heading2"]))
story.append(drawing_pie)
story.append(PageBreak())


# -------------------------------------
# Step 7: Detailed Table (Auto-Scaling)
# -------------------------------------
story.append(Paragraph("Detailed Sales Data", heading_style))
story.append(Spacer(1, 12))

table_data = [df.columns.tolist()] + df.values.tolist()
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


# -------------------------------------
# Step 8: Build the PDF
# -------------------------------------
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(f"✅ Dynamic Dashboard PDF generated successfully: {pdf_file}")
