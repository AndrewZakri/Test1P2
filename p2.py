import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Label Dashboard and configure layout
st.set_page_config(page_title="University Student Dashboard", layout="wide")
st.title("University Student Dashboard")

# Load the provided CSV for problem 2
df = pd.read_csv("university_student_dashboard_data.csv")

# Rename columns for consistency
df.columns = [col.strip().replace(" ", "_") for col in df.columns]

# Convert to appropriate data types
df['Year'] = df['Year'].astype(str)

# Sidebar filters
st.sidebar.header("Filters")
selected_years = st.sidebar.multiselect("Select Year(s):", sorted(df['Year'].unique()), default=df['Year'].unique())
selected_term = st.sidebar.selectbox("Select Term:", ['All', 'Spring', 'Fall'])

# Filter data
filtered_df = df[df['Year'].isin(selected_years)]
if selected_term != 'All':
    filtered_df = filtered_df[filtered_df['Term'] == selected_term]

# Create total applications, admissions and enrollments by term.  Use filters for year and term.
st.header("Key Performance Metrics (KPIs)")

col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", f"{filtered_df['Applications'].sum():,}")
col2.metric("Total Admitted", f"{filtered_df['Admitted'].sum():,}")
col3.metric("Total Enrolled", f"{filtered_df['Enrolled'].sum():,}")

# Create Retention Rate Trends Over Time
st.subheader("Retention Rate Over Time")
retention_trend = filtered_df.groupby('Year')['Retention_Rate_(%)'].mean().reset_index()
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=retention_trend, x='Year', y='Retention_Rate_(%)', marker='o', ax=ax1)
ax1.set_ylabel("Retention Rate (%)")
st.pyplot(fig1)

# Create Student Satisfaction Scores Over the Years
st.subheader("Student Satisfaction Over Time")
satisfaction_trend = filtered_df.groupby('Year')['Student_Satisfaction_(%)'].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.barplot(data=satisfaction_trend, x='Year', y='Student_Satisfaction_(%)', palette="Blues_d", ax=ax2)
ax2.set_ylabel("Satisfaction (%)")
st.pyplot(fig2)

# Create Enrollment breakdown by department (Engineering, Business, Art & Science
st.subheader("Departmental Enrollment Breakdown")
dept_enroll = filtered_df[['Engineering_Enrolled', 'Business_Enrolled', 'Arts_Enrolled', 'Science_Enrolled']].sum()
dept_df = dept_enroll.reset_index()
dept_df.columns = ['Department', 'Enrolled']
dept_df['Department'] = dept_df['Department'].str.replace("_Enrolled", "")

fig3, ax3 = plt.subplots()
sns.barplot(data=dept_df, x='Department', y='Enrolled', palette='Set2', ax=ax3)
st.pyplot(fig3)

# Create Comparison between Spring vs Fall term trends
if selected_term == 'All':
    st.subheader("Spring vs Fall Enrollment Over Time")
    term_trend = filtered_df.groupby(['Year', 'Term'])['Enrolled'].sum().reset_index()
    fig4, ax4 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=term_trend, x='Year', y='Enrolled', hue='Term', marker='o', ax=ax4)
    st.pyplot(fig4)

# Create trends between departments, retention rates and satisfaction levels
st.subheader("Departmental Comparison: Retention vs. Satisfaction")

dept_comp = pd.DataFrame({
    'Department': ['Engineering', 'Business', 'Arts', 'Science'],
    'Avg_Retention': [
        filtered_df['Engineering_Enrolled'].sum() / filtered_df['Enrolled'].sum() * filtered_df['Retention_Rate_(%)'].mean()
        for _ in range(4)],
    'Avg_Satisfaction': [
        filtered_df['Engineering_Enrolled'].sum() / filtered_df['Enrolled'].sum() * filtered_df['Student_Satisfaction_(%)'].mean()
        for _ in range(4)]
})

fig5, ax5 = plt.subplots(figsize=(6, 6))
sns.scatterplot(data=dept_comp, x='Avg_Retention', y='Avg_Satisfaction', hue='Department', s=150, ax=ax5)
ax5.set_xlabel("Retention Score (Weighted)")
ax5.set_ylabel("Satisfaction Score (Weighted)")
st.pyplot(fig5)
