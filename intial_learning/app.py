import streamlit as st
import pandas as pd
import io

# Function to reformat the Excel sheet
def format_df_to_transit(df2):
    df2['int'] = ''
    df2['emp'] = ''
    df2['emp1'] = ''
    df2['emp2'] = ''
    df2['emp3'] = ''
    df2['emp4'] = ''
    df2['emp5'] = ''
    df2['emp6'] = ''
    df2['com'] = ''
    df2['Grade'] = ''
    df2['Total Cost'] = df2['Sale price'] + df2['Buy fee']
    df2['Total Cost'] = df2['Total Cost'].astype(int)
    df2['Buyer'] = 'HAY'
    df2['paid'] = df2['Total Cost'].apply(lambda x: f'-{x}')
    df2['Sale date'] = df2['Sale date'].apply(lambda x: pd.to_datetime(x).date())
    return df2[['Year','Make','Model','Exterior color','Interior color','Trim','Odometer','Vin','emp','emp1','emp2','emp3','emp4','emp5','Seller name','Buyer','emp6','Sale date','Total Cost','paid','com','Grade','Vehicle location']]


# Streamlit app
st.title('Excel Reformatter App')

uploaded_file = st.file_uploader("Choose an Excel file", type="csv")

if uploaded_file is not None:
    # Read the uploaded file
    df = pd.read_csv(uploaded_file)

    st.write("Original Data")
    st.write(df)

    # Reformat the DataFrame
    reformatted_df = format_df_to_transit(df)

    st.write("Reformatted Data")
    st.write(reformatted_df)

    # Convert the reformatted DataFrame to Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        reformatted_df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
        processed_data = output.getvalue()

    st.download_button(
        label="Download Reformatted Excel",
        data=processed_data,
        file_name='reformatted.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
