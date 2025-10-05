# Sales Report Generator

This is a Streamlit app that generates professional PDF sales reports from CSV/Excel files.

# Features
1. Dynamic KPI calculation
2. Charts preview (Bar chart by Product, Pie chart by Region)
3. PDF report generation with charts, KPIs, and tables
4. Fancy landing page with gradient background and styled UI

# How to Run
1. Clone the repository:
git clone https://github.com/saadmd13/Automated_Report_Generator.git

2. Install dependencies:
pip install -r requirements.txt

3. Run the Streamlit app:
python -m streamlit run app.py

# Sample Data
1. Upload your own CSV/Excel file with columns:
Sales, Target, Region (optional: Product column)

2. Upload to GitHub

3. Initialize Git in your project folder:
git init

4. Add all files:
git add .

5. Commit your files:
git commit -m "Initial commit: Streamlit PDF Report Generator"

6. Push to GitHub:
git branch -M main
git remote add origin https://github.com/saadmd13/Automated_Report_Generator.git

git push -u origin main


# Optional: Add .gitignore
Avoid pushing unnecessary files (like temporary PDFs, .pyc, or virtual environments):
pycache/
*.pyc
*.pyo
*.pyd
*.db
*.pdf
