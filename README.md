# Global Happiness Report Analysis

## Project Overview

The Global Happiness Report Analysis project is a Python-based data analysis and visualization project developed using Jupyter Notebook. The project analyzes the World Happiness Report datasets from 2015 to 2019 to identify factors affecting happiness across different countries.

The project demonstrates data cleaning, statistical analysis, data visualization, and machine learning techniques using Python libraries.

---

## Technologies Used

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn

---

## Dataset

The project uses the following World Happiness Report datasets:

- 2015.csv
- 2016.csv
- 2017.csv
- 2018.csv
- 2019.csv

The datasets contain information related to:

- Country
- Happiness Score
- GDP per Capita
- Family/Social Support
- Health/Life Expectancy
- Freedom
- Generosity
- Trust/Corruption
- Year

---

## Features

### Data Loading

- Load multiple CSV files
- Combine datasets into a single DataFrame
- Display dataset information

### Data Cleaning

- Check missing values
- Handle missing values
- Check duplicate records
- Remove duplicate records

### Statistical Analysis

- Mean
- Median
- Mode
- Standard Deviation
- Variance
- Correlation Matrix

### Country Analysis

- Search Country
- Compare Two Countries
- Top 10 Happiest Countries
- Bottom 10 Happiest Countries

### Data Visualization

- Correlation Heatmap
- Top 10 Happiest Countries Bar Chart
- Bottom 10 Happiest Countries Bar Chart
- Happiness Score Histogram
- GDP vs Happiness Scatter Plot
- Freedom vs Happiness Scatter Plot
- Life Expectancy vs Happiness Scatter Plot
- Box Plot
- Pie Chart
- Year-wise Happiness Trend

### Machine Learning

- Train/Test Split
- Linear Regression Model
- Happiness Score Prediction
- Model Evaluation using:
  - R² Score
  - RMSE

### File Export

- Save Cleaned Dataset as CSV
- Save Cleaned Dataset as Excel
- Save Graphs as PNG Images

---

## Project Structure

```text
Final_Project/

│
├── 2015.csv
├── 2016.csv
├── 2017.csv
├── 2018.csv
├── 2019.csv
│
├── Graphs/
│   ├── Heatmap.png
│   ├── Top10_Happiest_Countries.png
│   ├── Bottom10_Happiest_Countries.png
│   ├── Histogram.png
│   ├── GDP_vs_Happiness.png
│   ├── Freedom_vs_Happiness.png
│   ├── LifeExpectancy_vs_Happiness.png
│   ├── BoxPlot.png
│   ├── PieChart.png
│   └── Average_Happiness_Score_by_Year.png
│
├── Cleaned_Happiness_Report.csv
├── Cleaned_Happiness_Report.xlsx
│
└── Final_Project.ipynb
```

---

## Installation

Install required libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
```

---

## How to Run

1. Download all dataset files.
2. Place all CSV files in the project folder.
3. Open Jupyter Notebook.
4. Run all cells sequentially.
5. View analysis results and generated visualizations.
6. Export cleaned datasets and graphs.

---

## Sample Outputs

- Correlation Heatmap
- Country-wise Happiness Analysis
- Year-wise Happiness Trend
- Happiness Score Prediction
- Saved Graph Images
- CSV and Excel Reports

---

## Learning Outcomes

This project demonstrates:

- Data Cleaning
- Data Preprocessing
- Exploratory Data Analysis (EDA)
- Statistical Analysis
- Data Visualization
- Machine Learning
- File Handling
- Report Generation

---

## Author

**Sarth Thakar**

MSc IT Student

---

## Conclusion

The Global Happiness Report Analysis project provides insights into factors influencing happiness across countries and years. Through data analysis, visualization, and machine learning, the project helps understand global happiness trends and the impact of economic and social indicators on overall well-being.
