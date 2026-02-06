

import streamlit as st
import pandas as pd
import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from core.ModelInitializers.DataIngestion import LoadDocument
from core.ScoreCalculators.ScoreCalculators import (
    CalculateQuantitativeScore, 
    CalculateBooleanScore,
    CalculateTextualScore
)
from core.ModelInitializers.Model import LoadModel
from core.ModelInitializers.Embedding import DownloadGeminiEmbedding
from interfaces.admin.ClassificationModel import ClassifyParameter
from interfaces.utils.ParameterManager import ParameterManager
import time


def setup_page_config():
    st.set_page_config(
        page_title="AI Resume Evaluation System",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton > button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #4CAF50;
            color: white;
        }
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            border-radius: 5px;
        }
        h1 {
            color: #1E88E5;
            text-align: center;
            padding-bottom: 2rem;
        }
        h2 {
            color: #424242;
        }
        </style>
    """, unsafe_allow_html=True)


def admin_interface():
    st.title("Administrator Configuration Panel")

    param_manager = ParameterManager()

    if 'current_session_parameters' not in st.session_state:
        st.session_state.current_session_parameters = []

    if st.button("Reset Parameters"):
        st.session_state.current_session_parameters = []
        st.rerun()

    with st.form("parameter_form"):
        st.write("### Add New Evaluation Parameter")
        name = st.text_input("Parameter Name (e.g., 'Years of Experience')")
        weight = st.slider("Parameter Weight", 0.0, 20.0, 5.0, 0.1)

        if st.form_submit_button("Process Parameter") and name:
            category = ClassifyParameter(name).strip().lower()
            new_param = {
                "name": name,
                "category": category,
                "weight": weight,
                "max_value": None,
                "benefit_type": None
            }

            if category == "quantitative":
                st.session_state.new_param = new_param
            else:
                st.session_state.current_session_parameters.append(new_param)

            st.rerun()

    if 'new_param' in st.session_state:
        st.write("### Configure Quantitative Parameter")
        st.session_state.new_param["max_value"] = st.number_input(
            "Maximum Value", min_value=0.1, value=10.0, step=0.1
        )
        st.session_state.new_param["benefit_type"] = st.selectbox(
            "Scoring Direction", ["High is better", "Low is better"]
        )

        if st.button("Save Quantitative Parameter"):
            st.session_state.current_session_parameters.append(st.session_state.new_param)
            del st.session_state.new_param
            st.rerun()

    if st.session_state.current_session_parameters:
        st.write("### Configured Parameters")

        df = pd.DataFrame(st.session_state.current_session_parameters).rename(columns={
            "name": "Parameter",
            "category": "Type",
            "weight": "Weight",
            "max_value": "Max Value",
            "benefit_type": "Scoring Logic"
        })

        st.dataframe(df, use_container_width=True, hide_index=True)

        if st.button("Save All Parameters"):
            param_manager.save_parameters(st.session_state.current_session_parameters)
            st.success("Parameters saved successfully.")


def user_interface():
    st.title("Candidate Evaluation Interface")

    param_manager = ParameterManager()
    debug_mode = st.sidebar.checkbox("Enable Debug Mode")

    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

    if uploaded_file:
        try:
            with st.spinner("Processing resume..."):
                documents = LoadDocument(uploaded_file)
                model = LoadModel()
                query_engine = DownloadGeminiEmbedding(model, documents)

                resume_text = " ".join(doc.text for doc in documents)
                parameter_details = param_manager.get_parameter_details()

                scores = {}
                total_weighted_score = 0
                total_weight = 0

                for param, details in parameter_details.items():
                    try:
                        p_type = details["type"].lower()
                        weight = float(details.get("weight", 0))

                        if weight <= 0:
                            continue

                        if p_type == "textual":
                            score = CalculateTextualScore(details["description"], resume_text)
                        elif p_type == "quantitative":
                            score = CalculateQuantitativeScore(
                                details["description"],
                                details["max_value"],
                                details["benefit_type"],
                                query_engine
                            )
                        else:
                            score = CalculateBooleanScore(details["description"], query_engine)

                        scores[param] = {
                            "raw_score": score,
                            "weighted_score": score * weight,
                            "weight": weight
                        }

                        total_weighted_score += score * weight
                        total_weight += weight

                    except Exception as e:
                        if debug_mode:
                            st.exception(e)

                if scores and total_weight > 0:
                    final_score = total_weighted_score / total_weight
                    status = "PASS" if final_score >= 70 else "FAIL"

                    st.header("Evaluation Results")
                    st.metric("Final Score", f"{final_score:.2f}", status)

                    st.dataframe(pd.DataFrame([
                        {
                            "Parameter": k,
                            "Score": f"{v['raw_score']:.2f}",
                            "Weight": f"{v['weight']:.2f}",
                            "Weighted Score": f"{v['weighted_score']:.2f}"
                        }
                        for k, v in scores.items()
                    ]), use_container_width=True, hide_index=True)

        except Exception as e:
            st.error("An unexpected error occurred.")
            st.exception(e)


def main():
    setup_page_config()

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select View", ["Administrator Panel", "Candidate Evaluation"])

    if page == "Administrator Panel":
        admin_interface()
    else:
        user_interface()


if __name__ == "__main__":
    main()
