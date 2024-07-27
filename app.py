import streamlit as st
import pandas as pd
import json

# Load data
wiskeyd_df = pd.read_csv('wiskeyd_with_similarities.csv')
competitor_df1 = pd.read_csv('barrel_cartel_competitor.csv')
competitor_df2 = pd.read_csv('canawineco_competitor.csv')

# Convert string representation of lists back to lists using json.loads
wiskeyd_df['cosine_similarities1'] = wiskeyd_df['cosine_similarities1'].apply(json.loads)
wiskeyd_df['cosine_similarities2'] = wiskeyd_df['cosine_similarities2'].apply(json.loads)

st.title("Closest Products Finder")

# Dropdown for product title selection
selected_title = st.selectbox("Select Product Title", wiskeyd_df['title'].unique())

# Automatically populate description, URL, price, and image based on the selected title
selected_product = wiskeyd_df[wiskeyd_df['title'] == selected_title].iloc[0]
selected_description = selected_product['description']
selected_url = selected_product['url']
selected_price = selected_product['price']
selected_image = selected_product['image']

# Display the selected product details
st.write("### Selected Product Details")
st.write(f"**Title**: {selected_title}")
st.write(f"**Description**: {selected_description}")
st.write(f"**URL**: {selected_url}")
st.write(f"**Price**: {selected_price}")
st.image('https:'+selected_image, caption="WiskeyD Product Image", use_column_width=True)

# Submit button
if st.button("Find Closest Competitor Products"):
    # Extract the cosine similarities for the selected product
    cosine_similarities1 = selected_product['cosine_similarities1']
    cosine_similarities2 = selected_product['cosine_similarities2']

    # Find the index of the closest competitor product for each competitor
    closest_idx1 = cosine_similarities1.index(max(cosine_similarities1))
    closest_idx2 = cosine_similarities2.index(max(cosine_similarities2))

    closest_product1 = competitor_df1.iloc[closest_idx1]
    closest_product2 = competitor_df2.iloc[closest_idx2]

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Closest Competitor 1 Product")
        st.image('https:'+closest_product1['image'], caption="Competitor 1 Product Image", use_column_width=True)
        st.write(f"**Title**: {closest_product1['title']}")
        st.write(f"**Description**: {closest_product1['description']}")
        st.write(f"**URL**: {closest_product1['url']}")
        st.write(f"**Price**: {closest_product1['price']}")
        st.write(f"**Similarity Score**: {max(cosine_similarities1):.2f}")

    with col2:
        st.write("### Closest Competitor 2 Product")
        st.image("https:"+closest_product2['image'], caption="Competitor 2 Product Image", use_column_width=True)
        st.write(f"**Title**: {closest_product2['title']}")
        st.write(f"**Description**: {closest_product2['description']}")
        st.write(f"**URL**: {closest_product2['url']}")
        st.write(f"**Price**: {closest_product2['price']}")
        st.write(f"**Similarity Score**: {max(cosine_similarities2):.2f}")
