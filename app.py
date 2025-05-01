import streamlit as st
import pandas as pd
from main import app
import os

st.set_page_config(layout="wide")

st.title("Automated Prescriptive Analytics")



user_input = st.text_input("Enter your input here:")

if st.button("Run Prescriptive Analysis", type="primary"):

    # st.write(res)
    # Show a loading spinner
    with st.spinner('Running AI Prescriptive Analysis...'):
        res =  app.invoke(
                {"messages": [("user", user_input)]}
            )

    st.title("Prescriptive Analysis Results")

    action_plans = res['action_plans']

    for i, action_plan in enumerate(action_plans):
        st.header(f"{i+1}. {action_plan["area_of_concern"]["division"]} - {action_plan["area_of_concern"]["coverage"]} - {action_plan["area_of_concern"]["type"]}")

        st.subheader("Reason")
        st.write(action_plan['area_of_concern']['reason'])

        st.subheader("Evidence")
        st.write(action_plan['area_of_concern']['evidence'])

        st.subheader("Action Items")
        # Write a list of items
        for j, action_item in enumerate(action_plan['action_items']):
            st.write(f"{j+1}. {action_item}")
        # st.write(action_plan['action_items'])

    # image_analysis_outputs = res["image_analysis_outputs"]
    # images = res["images"]
    #
    # damages = res["damages"].damages
    # image_indices = []
    # for damage in damages:
    #     image_indices.append(damage.image_indices)
    #
    # for i, image_analysis in enumerate(image_analysis_outputs):
    #     st.header(f"{i+1}. {image_analysis.damage_title}".title())
    #
    #     st.subheader(f"Nature of Damage - {image_analysis.nature_of_damage}".title())
    #
    #     st.subheader(f"Extent of Damage - {image_analysis.extent_of_damage}".title())
    #
    #     st.subheader("Images")
    #     image_analysis_images = [images[int(j)] for j in image_indices[i]]
    #     columns = st.columns(IMAGE_COLS)
    #     for j, image in enumerate(image_analysis_images):
    #         with columns[j % IMAGE_COLS]:
    #             st.image(image, caption=f"Image {j+1}")
    #
    #     st.subheader("Damage Analysis")
    #     st.write(image_analysis.analysis_of_damage)
    #
    #     st.markdown(f"Damaged Area in SqFt: **{image_analysis.area_of_damage_sqft}**")
    #
    #     st.subheader("Repair Cost")
    #     st.markdown(f"Minimum: **\$ {image_analysis.repair_cost_min_usd_sqft} /sqft**")
    #     st.markdown(f"Maximum: **\$ {image_analysis.repair_cost_max_usd_sqft} /sqft**")
    #     st.markdown(f"Average Estimated Total Cost: **\$ {round((image_analysis.repair_cost_min_usd_sqft
    #                                                         + image_analysis.repair_cost_max_usd_sqft)
    #                                                        * image_analysis.area_of_damage_sqft/ 2, 2)}**")
    #     st.markdown(f'''Reference: [{image_analysis.repair_reference_text}]({image_analysis.repair_reference_url})''')