import streamlit as st
import requests
import pandas as pd

st.title("Transactions Table")

# Year search input
year = st.text_input("Search transactions by year (e.g. 2025):")

url = f"http://127.0.0.1:8000/api/v1/transactions/year/{year}"

if year:
    # Fetch data from the API
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Error fetching data: {response.status_code} - {response.text}")
    else:
        # Parse the JSON response
        data = response.json()

        # Convert the data to a DataFrame for tabular display
        df = pd.DataFrame(data)


        # Sort by 'tekst' column
        if 'tekst' in df.columns:
            df = df.sort_values(by='tekst', ascending=True)

        # Sort by 'ut' column descending
        if 'ut' in df.columns:
            df = df.sort_values(by='ut', ascending=False)


        # Show the table in Streamlit without the DataFrame index
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Show total 'ut'
        if 'ut' in df.columns:
            total_ut = df['ut'].sum()
            st.write(f"**Total ut:** {total_ut}")

        # Summarize by 'tekst' for specific stores only
        if 'tekst' in df.columns and 'ut' in df.columns:
            st.subheader("Dagligvarer")
            selected_tekster = [
                "KIWI", "REMA 1000", "MENY", "RUSTAD KJOETT & DAGLIGVAR", "Coop Mega", "SPAR", "Coop Obs", "Wolt", "Coop Extra", "Coop Prix", "Joker", "TRENOGMAT AS"
            ]
            # Add AVARDA as 'Snus' in the summary
            df['tekst'] = df['tekst'].replace({"Avarda": "Snus"})
            summary = (
                df[df['tekst'].isin(selected_tekster + ["Snus"])]
                .groupby('tekst', as_index=False)['ut']
                .sum()
                .sort_values(by='ut', ascending=True)
            )
            st.dataframe(summary, use_container_width=True, hide_index=True)
            # Add sum info of all fields in the summary
            total_summary_ut = round(summary['ut'].sum(), 2)
            st.write(f"**Total ut for selected stores:** {total_summary_ut}")