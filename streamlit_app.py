# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the Fruits you want in your Custom Smoothie!
    """
)

# Input: Customer Name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The Name on your Smoothie will be', name_on_order)

# ✅ Create Snowflake connection (reads from .streamlit/secrets.toml)
conn = st.connection("snowflake", type="snowflake")
session = conn.session()

# Get fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# Ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe.collect(),   # convert to Python list
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
