import streamlit as st
import pandas as pd
import io

def read_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

def compare_data(df1, df2):
    # Strip whitespace and convert to lowercase
    df1['First Name'] = df1['First Name'].str.strip().str.lower()
    df1['Last Name'] = df1['Last Name'].str.strip().str.lower()
    df2['First Name'] = df2['First Name'].str.strip().str.lower()
    df2['Last Name'] = df2['Last Name'].str.strip().str.lower()

    df1['FullName1'] = df1['First Name'] + ' ' + df1['Last Name']
    df2['FullName2'] = df2['First Name'] + ' ' + df2['Last Name']
    
    if 'Date of Birth' in df1.columns and 'Date of Birth' in df2.columns:
        merged = pd.merge(df1, df2, left_on=['FullName1', 'Date of Birth'], right_on=['FullName2', 'Date of Birth'], how='outer', indicator=True)
        unmatched = merged[merged['_merge'] != 'both']
        result_columns = ['First Name_x', 'Last Name_x', 'Date of Birth_x', 'First Name_y', 'Last Name_y', 'Date of Birth_y']
    else:
        merged = pd.merge(df1, df2, left_on=['FullName1'], right_on=['FullName2'], how='outer', indicator=True)
        unmatched = merged[merged['_merge'] != 'both']
        result_columns = ['First Name_x', 'Last Name_x', 'First Name_y', 'Last Name_y']
    
    return unmatched[result_columns]

# Function to create a template CSV file
def create_template_csv():
    template_data = {
        'First Name': ['John', 'Jane'],
        'Last Name': ['Doe', 'Smith'],
        'Date of Birth': ['1990-01-01', '1992-02-02']
    }
    df_template = pd.DataFrame(template_data)
    output = io.StringIO()
    df_template.to_csv(output, index=False)
    return output.getvalue()

# Streamlit app
st.title('Excel/CSV Comparison App')

st.write("""
## Instructions
1. Upload two Excel or CSV files.
2. The app will compare the names (first and last name) and date of birth (if available) in both files.
3. It will display the names that do not match.

### Column Requirements
- The files must contain the following columns:
  - **First Name**
  - **Last Name**
  - **Date of Birth** (optional, if available)

You can download a [template CSV file](#) to see the required columns.
""")

# Provide a downloadable template CSV file
st.download_button(
    label="Download Template CSV",
    data=create_template_csv(),
    file_name='template.csv',
    mime='text/csv'
)

uploaded_file1 = st.file_uploader("Choose the first Excel/CSV file", type=['csv', 'xlsx'])
uploaded_file2 = st.file_uploader("Choose the second Excel/CSV file", type=['csv', 'xlsx'])

if uploaded_file1 is not None and uploaded_file2 is not None:
    df1 = read_file(uploaded_file1)
    df2 = read_file(uploaded_file2)

    st.write("First File Data")
    st.write(df1)

    st.write("Second File Data")
    st.write(df2)

    if 'First Name' in df1.columns and 'Last Name' in df1.columns and 'First Name' in df2.columns and 'Last Name' in df2.columns:
        unmatched = compare_data(df1, df2)

        st.write("Unmatched Data")
        st.write(unmatched)

        # Convert the unmatched DataFrame to CSV
        output = io.StringIO()
        unmatched.to_csv(output, index=False)
        processed_data = output.getvalue()

        st.download_button(
            label="Download Unmatched Data as CSV",
            data=processed_data,
            file_name='unmatched.csv',
            mime='text/csv'
        )
    else:
        st.error("Both files must contain 'First Name' and 'Last Name' columns.")
