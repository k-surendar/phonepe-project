# 📊 PhonePe Transaction Insights

## 📌 Overview

PhonePe Transaction Insights is a Data Analytics project that analyzes digital payment data from the PhonePe Pulse dataset. The project extracts data from JSON files, stores it in a MySQL database, performs SQL-based analysis, and presents insights through an interactive Streamlit dashboard.

---

## 🎯 Objectives

- Analyze transaction trends across India.
- Identify top-performing states, districts, and pincodes.
- Study user engagement and growth patterns.
- Analyze insurance-related transactions.
- Create interactive visualizations for data exploration.

---

## 🛠️ Technologies Used

- Python
- MySQL
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Git & GitHub

---

## 📂 Dataset

Dataset Source:

https://github.com/PhonePe/pulse

The dataset contains:

- Aggregated Transaction Data
- Aggregated User Data
- Aggregated Insurance Data
- Map Data
- Top Transaction Data
- Top User Data
- Top Insurance Data

---

## 🔄 Project Workflow

1. Extract data from PhonePe Pulse GitHub repository.
2. Transform JSON data into structured format.
3. Load data into MySQL database.
4. Perform SQL queries for analysis.
5. Generate insights using Python.
6. Create visualizations and dashboard using Streamlit.

---

## 🗄️ Database Tables

### Aggregated Tables
- Aggregated_Transaction
- Aggregated_User
- Aggregated_Insurance

### Map Tables
- Map_Transaction
- Map_User
- Map_Insurance

### Top Tables
- Top_Transaction
- Top_User
- Top_Insurance

---

## 📈 Dashboard Features

- State-wise Transaction Analysis
- District-wise Transaction Analysis
- User Growth Analysis
- Insurance Analysis
- Top States and Districts
- Interactive Filters and Charts

---

## 💡 Key Insights

- Identified states with highest transaction volumes.
- Analyzed user engagement trends.
- Compared transaction categories.
- Evaluated insurance adoption across regions.
- Discovered top-performing districts and pincodes.

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/PhonePe-Transaction-Insights.git
```

### Navigate to Project Folder

```bash
cd PhonePe-Transaction-Insights
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Streamlit App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```text
PhonePe-Transaction-Insights/
│
├── data/
├── sql/
├── app.py
├── data_extraction.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## 🔮 Future Enhancements

- Real-time data integration
- Fraud detection analytics
- Machine Learning predictions
- Advanced geographic visualizations

---

## 👨‍💻 Author

**Surendar K**

- GitHub: https://github.com/yourusername
- LinkedIn: https://linkedin.com/in/yourprofile

---

## ⭐ Acknowledgement

Dataset provided by PhonePe Pulse:

https://github.com/PhonePe/pulse
