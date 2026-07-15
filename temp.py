# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import numpy as np
# import joblib
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import load_img, img_to_array
# from PIL import Image

# from groq import Groq
# from gtts import gTTS
# from streamlit_mic_recorder import mic_recorder
# import speech_recognition as sr

# from dotenv import load_dotenv
# import tempfile
# import os

# # Load .env file
# load_dotenv()

# # Get Groq API Key
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # Create Groq Client
# client = Groq(api_key=GROQ_API_KEY)
 
# # =========================================================
# # ================= PAGE CONFIG ===========================
# # =========================================================
 
# st.set_page_config(
#     page_title="Krishi AI",
#     layout="wide"
# )
 
# # =========================================================
# # ================= LOAD DATASET ==========================
# # =========================================================
 
# df = pd.read_csv("Krishi_ai_dataset/cleaned_crop_dataset.csv")
 
# # =========================================================
# # ================= LOAD ML FILES =========================
# # =========================================================
 
# @st.cache_resource
# def load_ml_files():
#     try:
#         model         = joblib.load("crop_model.pkl")
#         scaler        = joblib.load("scaler.pkl")
#         label_encoder = joblib.load("label_encoder.pkl")
#         return model, scaler, label_encoder, None
#     except FileNotFoundError as e:
#         return None, None, None, str(e)
#     except Exception as e:
#         return None, None, None, str(e)
 
# model, scaler, label_encoder, ml_error = load_ml_files()

# # =========================================================
# # ================= LOAD DISEASE MODEL ====================
# # =========================================================

# disease_model = load_model("plant_disease_model.h5")

# disease_encoder = joblib.load("disease_label_encoder.pkl")
    
# # =========================================================
# # ================= FEATURE CATEGORIES ====================
# # =========================================================
 
# def nitrogen_category(n):
#     if n <= 50:        return "Low"
#     elif n <= 120:     return "Medium"
#     else:              return "High"
 
# def phosphorus_category(p):
#     if p <= 40:        return "Low"
#     elif p <= 80:      return "Medium"
#     else:              return "High"
 
# def potassium_category(k):
#     if k <= 40:        return "Low"
#     elif k <= 80:      return "Medium"
#     else:              return "High"
 
# def temperature_category(temp):
#     if temp <= 20:     return "Cool"
#     elif temp <= 30:   return "Moderate"
#     else:              return "Hot"
 
# def humidity_category(humidity):
#     if humidity <= 40: return "Low"
#     elif humidity <= 70: return "Medium"
#     else:              return "High"
 
# def ph_category(ph):
#     if ph < 6:         return "Acidic"
#     elif ph <= 7.5:    return "Neutral"
#     else:              return "Alkaline"
 
# def rainfall_category(rainfall):
#     if rainfall <= 100:  return "Low"
#     elif rainfall <= 200: return "Medium"
#     else:                return "High"
 
# # =========================================================
# # ================= ADD NEW COLUMNS =======================
# # =========================================================
 
# df["Nitrogen_Category"]    = df["N"].apply(nitrogen_category)
# df["Phosphorus_Category"]  = df["P"].apply(phosphorus_category)
# df["Potassium_Category"]   = df["K"].apply(potassium_category)
# df["Temperature_Category"] = df["temperature"].apply(temperature_category)
# df["Humidity_Category"]    = df["humidity"].apply(humidity_category)
# df["PH_Category"]          = df["ph"].apply(ph_category)
# df["Rainfall_Category"]    = df["rainfall"].apply(rainfall_category)
 
# # =========================================================
# # ====================== TITLE ============================
# # =========================================================
 
# st.markdown(
#     "<h1 style='text-align:center; color:green;'>🌱 Krishi AI</h1>",
#     unsafe_allow_html=True
# )
 
# # =========================================================
# # ===================== SIDEBAR ===========================
# # =========================================================
 
# st.sidebar.title("Navigation")
 
# page = st.sidebar.selectbox(
#     "Go To",
#     ["Home", "Analytics", "ML Prediction", "Disease Detection"]
# )
 
# # =========================================================
# # ====================== HOME PAGE ========================
# # =========================================================

 
# if page == "Home":
 
#     st.markdown(
#         "<h2 style='text-align:center;'>AI Farmer Assistant</h2>",
#         unsafe_allow_html=True
#     )
 
#     st.markdown("---")
 
#     col1, col2, col3 = st.columns([1, 2, 1])
 
#     with col2:
#         user_input = st.text_input(
#             "Farmer Question",
#             placeholder="Ask your farming question...",
#             label_visibility="collapsed"
#         )
 
#         if st.button("Get Advice", use_container_width=True):
#             if user_input:
#                 st.success(f"✅ Your Question: {user_input}")
#                 st.info("🤖 AI response feature will be integrated soon.")
#             else:
#                 st.warning("⚠️ Please enter a farming question.")
 
# # =========================================================
# # ==================== ANALYTICS PAGE =====================
# # =========================================================
 
# elif page == "Analytics":
 
#     st.header("📊 Krishi Data Analytics Dashboard")
 
#     # =====================================================
#     # 1. DATASET OVERVIEW
#     # =====================================================
 
#     st.subheader("📁 Dataset Overview")
 
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.metric("Total Rows", df.shape[0])
#     with col2:
#         st.metric("Total Columns", df.shape[1])
#     with col3:
#         st.metric("Total Crops", df["label"].nunique())
#     with col4:
#         st.metric("Duplicate Rows", int(df.duplicated().sum()))
#     with col5:
#         st.metric("Missing Values", int(df.isnull().sum().sum()))
 
#     st.markdown("---")
 
#     # =====================================================
#     # 2. DATA QUALITY CHECK
#     # =====================================================
 
#     st.subheader("🔬 Data Quality Check")
 
#     col1, col2 = st.columns(2)
 
#     with col1:
#         st.write("#### Data Types")
#         dtype_df = df.dtypes.reset_index()
#         dtype_df.columns = ["Feature", "Data Type"]
#         dtype_df["Data Type"] = dtype_df["Data Type"].astype(str)
#         st.dataframe(dtype_df, use_container_width=True)
 
#     with col2:
#         st.write("#### Missing Values per Feature")
#         missing_values = df.isnull().sum().reset_index()
#         missing_values.columns = ["Feature", "Missing Values"]
#         st.dataframe(missing_values, use_container_width=True)
 
#         if missing_values["Missing Values"].sum() == 0:
#             st.success("✅ No missing values found!")
 
#         dup = df.duplicated().sum()
#         if dup == 0:
#             st.success("✅ No duplicate rows found!")
#         else:
#             st.warning(f"⚠️ {dup} duplicate rows found!")
 
#     st.markdown("---")
 
#     # =====================================================
#     # 3. DATASET PREVIEW
#     # =====================================================
 
#     st.subheader("🔍 Dataset Preview")
#     st.dataframe(df, use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 4. STATISTICAL SUMMARY
#     # =====================================================
 
#     st.subheader("📈 Statistical Summary")
#     st.dataframe(df.describe().round(2), use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 5. CROP DISTRIBUTION
#     # =====================================================
 
#     st.subheader("🌾 Crop Distribution")
 
#     crop_count = df["label"].value_counts().reset_index()
#     crop_count.columns = ["Crop", "Count"]
 
#     col1, col2 = st.columns(2)
 
#     with col1:
#         fig_bar = px.bar(
#             crop_count, x="Crop", y="Count",
#             title="Crop Count (Bar Chart)",
#             color="Count",
#             color_continuous_scale="Greens",
#             text="Count"
#         )
#         fig_bar.update_traces(textposition="outside")
#         fig_bar.update_layout(xaxis_tickangle=-45, showlegend=False)
#         st.plotly_chart(fig_bar, use_container_width=True)
 
#     with col2:
#         fig_pie = px.pie(
#             crop_count, names="Crop", values="Count",
#             title="Crop Distribution (Pie Chart)",
#             color_discrete_sequence=px.colors.sequential.Greens_r
#         )
#         fig_pie.update_traces(textposition="inside", textinfo="percent+label")
#         st.plotly_chart(fig_pie, use_container_width=True)
 
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write("#### 🏆 Top 5 Most Common Crops")
#         st.dataframe(crop_count.head(5), use_container_width=True)
#     with col2:
#         st.write("#### 📉 Bottom 5 Least Common Crops")
#         st.dataframe(crop_count.tail(5), use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 6. FEATURE CATEGORY ANALYSIS
#     # =====================================================
 
#     st.subheader("📊 Feature Category Analysis")
 
#     categories = [
#         ("Nitrogen_Category",    "Nitrogen"),
#         ("Phosphorus_Category",  "Phosphorus"),
#         ("Potassium_Category",   "Potassium"),
#         ("Temperature_Category", "Temperature"),
#         ("Humidity_Category",    "Humidity"),
#         ("PH_Category",          "Soil pH"),
#         ("Rainfall_Category",    "Rainfall"),
#     ]
 
#     col1, col2 = st.columns(2)
 
#     for i, (col_name, title) in enumerate(categories):
#         counts = df[col_name].value_counts().reset_index()
#         counts.columns = ["Category", "Count"]
 
#         fig = px.pie(
#             counts, names="Category", values="Count",
#             title=f"{title} Distribution",
#             hole=0.4,
#             color_discrete_sequence=px.colors.qualitative.Set2
#         )
#         fig.update_traces(textinfo="percent+label")
 
#         if i % 2 == 0:
#             with col1:
#                 st.plotly_chart(fig, use_container_width=True)
#         else:
#             with col2:
#                 st.plotly_chart(fig, use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 7. TEMPERATURE ANALYSIS
#     # =====================================================
 
#     st.subheader("🌡 Average Temperature by Crop")
 
#     temp_crop = (
#         df.groupby("label")["temperature"].mean()
#         .round(2).reset_index()
#     )
#     temp_crop.columns = ["Crop", "Avg Temperature (°C)"]
#     temp_crop = temp_crop.sort_values("Avg Temperature (°C)", ascending=True)
 
#     fig_temp = px.bar(
#         temp_crop, x="Avg Temperature (°C)", y="Crop",
#         orientation="h",
#         title="Average Temperature Required per Crop",
#         color="Avg Temperature (°C)",
#         color_continuous_scale="RdYlGn_r",
#         text="Avg Temperature (°C)"
#     )
#     fig_temp.update_traces(textposition="outside")
#     fig_temp.update_layout(height=600, yaxis_title="")
#     st.plotly_chart(fig_temp, use_container_width=True)
 
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write("#### 🔥 Top 5 Crops (Highest Temp)")
#         st.dataframe(
#             temp_crop.tail(5)[["Crop", "Avg Temperature (°C)"]][::-1],
#             use_container_width=True
#         )
#     with col2:
#         st.write("#### ❄️ Top 5 Crops (Lowest Temp)")
#         st.dataframe(
#             temp_crop.head(5)[["Crop", "Avg Temperature (°C)"]],
#             use_container_width=True
#         )
 
#     st.markdown("---")
 
#     # =====================================================
#     # 8. RAINFALL ANALYSIS
#     # =====================================================
 
#     st.subheader("🌧 Average Rainfall by Crop")
 
#     rainfall_crop = (
#         df.groupby("label")["rainfall"].mean()
#         .round(2).reset_index()
#     )
#     rainfall_crop.columns = ["Crop", "Avg Rainfall (mm)"]
#     rainfall_crop = rainfall_crop.sort_values("Avg Rainfall (mm)", ascending=True)
 
#     fig_rain = px.bar(
#         rainfall_crop, x="Avg Rainfall (mm)", y="Crop",
#         orientation="h",
#         title="Average Rainfall Required per Crop",
#         color="Avg Rainfall (mm)",
#         color_continuous_scale="Blues",
#         text="Avg Rainfall (mm)"
#     )
#     fig_rain.update_traces(textposition="outside")
#     fig_rain.update_layout(height=600, yaxis_title="")
#     st.plotly_chart(fig_rain, use_container_width=True)
 
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write("#### 🌊 Top 5 Crops (Most Rainfall)")
#         st.dataframe(
#             rainfall_crop.tail(5)[["Crop", "Avg Rainfall (mm)"]][::-1],
#             use_container_width=True
#         )
#     with col2:
#         st.write("#### 🏜 Top 5 Crops (Least Rainfall)")
#         st.dataframe(
#             rainfall_crop.head(5)[["Crop", "Avg Rainfall (mm)"]],
#             use_container_width=True
#         )
 
#     st.markdown("---")
 
#     # =====================================================
#     # 9. HUMIDITY ANALYSIS
#     # =====================================================
 
#     st.subheader("💧 Average Humidity by Crop")
 
#     humidity_crop = (
#         df.groupby("label")["humidity"].mean()
#         .round(2).reset_index()
#     )
#     humidity_crop.columns = ["Crop", "Avg Humidity (%)"]
#     humidity_crop = humidity_crop.sort_values("Avg Humidity (%)", ascending=True)
 
#     fig_hum = px.bar(
#         humidity_crop, x="Avg Humidity (%)", y="Crop",
#         orientation="h",
#         title="Average Humidity Required per Crop",
#         color="Avg Humidity (%)",
#         color_continuous_scale="Teal",
#         text="Avg Humidity (%)"
#     )
#     fig_hum.update_traces(textposition="outside")
#     fig_hum.update_layout(height=600, yaxis_title="")
#     st.plotly_chart(fig_hum, use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 10. PH ANALYSIS
#     # =====================================================
 
#     st.subheader("🧪 Average Soil pH by Crop")
 
#     ph_crop = (
#         df.groupby("label")["ph"].mean()
#         .round(2).reset_index()
#     )
#     ph_crop.columns = ["Crop", "Avg pH"]
#     ph_crop = ph_crop.sort_values("Avg pH", ascending=True)
 
#     fig_ph = px.bar(
#         ph_crop, x="Avg pH", y="Crop",
#         orientation="h",
#         title="Average Soil pH per Crop",
#         color="Avg pH",
#         color_continuous_scale="RdYlGn",
#         text="Avg pH"
#     )
#     fig_ph.update_traces(textposition="outside")
#     fig_ph.update_layout(height=600, yaxis_title="")
#     st.plotly_chart(fig_ph, use_container_width=True)
 
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write("#### 🔴 Most Alkaline Crops (High pH)")
#         st.dataframe(
#             ph_crop.tail(5)[["Crop", "Avg pH"]][::-1],
#             use_container_width=True
#         )
#     with col2:
#         st.write("#### 🟢 Most Acidic Crops (Low pH)")
#         st.dataframe(
#             ph_crop.head(5)[["Crop", "Avg pH"]],
#             use_container_width=True
#         )
 
#     st.markdown("---")
 
#     # =====================================================
#     # 11. NPK ANALYSIS
#     # =====================================================
 
#     st.subheader("🪴 NPK Analysis")
 
#     avg_npk_crop = (
#         df.groupby("label")[["N", "P", "K"]]
#         .mean().round(2).reset_index()
#     )
 
#     npk_melted = avg_npk_crop.melt(
#         id_vars="label", value_vars=["N", "P", "K"],
#         var_name="Nutrient", value_name="Value"
#     )
 
#     fig_npk_group = px.bar(
#         npk_melted, x="label", y="Value", color="Nutrient",
#         barmode="group",
#         title="Average N, P, K per Crop (Grouped)",
#         color_discrete_map={"N": "#2ca02c", "P": "#ff7f0e", "K": "#1f77b4"},
#         labels={"label": "Crop", "Value": "mg/kg"}
#     )
#     fig_npk_group.update_layout(xaxis_tickangle=-45, height=450)
#     st.plotly_chart(fig_npk_group, use_container_width=True)
 
#     fig_npk_stack = px.bar(
#         npk_melted, x="label", y="Value", color="Nutrient",
#         barmode="stack",
#         title="NPK Ratio per Crop — Stacked",
#         color_discrete_map={"N": "#2ca02c", "P": "#ff7f0e", "K": "#1f77b4"},
#         labels={"label": "Crop", "Value": "mg/kg"}
#     )
#     fig_npk_stack.update_layout(xaxis_tickangle=-45, height=450)
#     st.plotly_chart(fig_npk_stack, use_container_width=True)
 
#     st.write("#### 📋 Average NPK Table by Crop")
#     st.dataframe(avg_npk_crop.set_index("label"), use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 12. SOIL HEALTH SCORE
#     # =====================================================
 
#     st.subheader("🧪 Soil Health Analysis")
 
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Average Nitrogen",   round(df["N"].mean(), 2))
#     with col2:
#         st.metric("Average Phosphorus", round(df["P"].mean(), 2))
#     with col3:
#         st.metric("Average Potassium",  round(df["K"].mean(), 2))
 
#     soil_score = df.groupby("label")[["N", "P", "K"]].mean()
#     soil_score["Soil Health Score"] = (
#         soil_score[["N", "P", "K"]].mean(axis=1).round(2)
#     )
#     soil_score = soil_score.reset_index().sort_values(
#         "Soil Health Score", ascending=False
#     )
#     avg_score = soil_score["Soil Health Score"].mean()
 
#     fig_soil = px.bar(
#         soil_score, x="label", y="Soil Health Score",
#         title="Soil Health Score per Crop (avg of N + P + K)",
#         color="Soil Health Score",
#         color_continuous_scale="YlGn",
#         text="Soil Health Score",
#         labels={"label": "Crop"}
#     )
#     fig_soil.add_hline(
#         y=avg_score, line_dash="dash", line_color="red",
#         annotation_text=f"Dataset Avg: {avg_score:.1f}",
#         annotation_position="top right"
#     )
#     fig_soil.update_traces(textposition="outside")
#     fig_soil.update_layout(xaxis_tickangle=-45, height=450)
#     st.plotly_chart(fig_soil, use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 13. NUTRIENT DEFICIENCY FLAG
#     # =====================================================
 
#     st.subheader("⚠️ Nutrient Deficiency Flag")
#     st.caption("Crops where average N, P, or K falls in the Low category threshold.")
 
#     npk_flag = (
#         df.groupby("label")[["N", "P", "K"]]
#         .mean().round(2).reset_index()
#     )
#     npk_flag["N_Flag"] = npk_flag["N"].apply(
#         lambda x: "⚠️ Low" if x <= 50 else "✅ OK"
#     )
#     npk_flag["P_Flag"] = npk_flag["P"].apply(
#         lambda x: "⚠️ Low" if x <= 40 else "✅ OK"
#     )
#     npk_flag["K_Flag"] = npk_flag["K"].apply(
#         lambda x: "⚠️ Low" if x <= 40 else "✅ OK"
#     )
#     npk_flag["Status"] = npk_flag[["N_Flag", "P_Flag", "K_Flag"]].apply(
#         lambda row: "⚠️ Deficient" if "⚠️ Low" in row.values else "✅ Sufficient",
#         axis=1
#     )
 
#     deficient = npk_flag[npk_flag["Status"] == "⚠️ Deficient"]
 
#     if len(deficient) > 0:
#         st.warning(f"⚠️ {len(deficient)} crops have at least one nutrient in the Low range.")
#         st.dataframe(
#             deficient[["label", "N", "N_Flag", "P", "P_Flag", "K", "K_Flag"]],
#             use_container_width=True
#         )
#     else:
#         st.success("✅ All crops have sufficient average NPK levels.")
 
#     st.markdown("---")
 
#     # =====================================================
#     # 14. FEATURE RANGE
#     # =====================================================
 
#     st.subheader("📏 Feature Range per Crop (Min / Max / Std Dev)")
#     st.caption("Averages alone can be misleading — this shows the actual spread of values.")
 
#     range_feature = st.selectbox(
#         "Select Feature to Explore Range",
#         ["temperature", "humidity", "rainfall", "ph", "N", "P", "K"]
#     )
 
#     range_df = (
#         df.groupby("label")[range_feature]
#         .agg(["min", "max", "mean", "std"])
#         .round(2).reset_index()
#     )
#     range_df.columns = ["Crop", "Min", "Max", "Mean", "Std Dev"]
#     range_df = range_df.sort_values("Mean", ascending=False)
 
#     fig_range = go.Figure()
#     fig_range.add_trace(go.Bar(
#         x=range_df["Crop"], y=range_df["Mean"],
#         name="Mean",
#         marker_color="#2ca02c",
#         error_y=dict(type="data", array=range_df["Std Dev"], visible=True),
#         text=range_df["Mean"],
#         textposition="outside"
#     ))
#     fig_range.update_layout(
#         title=f"{range_feature.capitalize()} — Mean ± Std Dev per Crop",
#         xaxis_tickangle=-45,
#         height=480,
#         xaxis_title="Crop",
#         yaxis_title=range_feature
#     )
#     st.plotly_chart(fig_range, use_container_width=True)
#     st.dataframe(range_df.set_index("Crop"), use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 15. SCATTER PLOTS
#     # =====================================================
 
#     st.subheader("🔵 Scatter Plot Analysis")
 
#     col1, col2 = st.columns(2)
 
#     with col1:
#         fig_s1 = px.scatter(
#             df, x="rainfall", y="humidity",
#             color="label", hover_name="label",
#             title="Rainfall vs Humidity by Crop",
#             labels={"rainfall": "Rainfall (mm)", "humidity": "Humidity (%)"},
#             opacity=0.6
#         )
#         fig_s1.update_layout(height=450, showlegend=False)
#         st.plotly_chart(fig_s1, use_container_width=True)
 
#     with col2:
#         fig_s2 = px.scatter(
#             df, x="temperature", y="ph",
#             color="label", hover_name="label",
#             title="Temperature vs Soil pH by Crop",
#             labels={"temperature": "Temperature (°C)", "ph": "Soil pH"},
#             opacity=0.6
#         )
#         fig_s2.update_layout(height=450, showlegend=False)
#         st.plotly_chart(fig_s2, use_container_width=True)
 
#     col1, col2 = st.columns(2)
 
#     with col1:
#         fig_s3 = px.scatter(
#             df, x="N", y="K",
#             color="label", hover_name="label",
#             title="Nitrogen vs Potassium by Crop",
#             labels={"N": "Nitrogen (mg/kg)", "K": "Potassium (mg/kg)"},
#             opacity=0.6
#         )
#         fig_s3.update_layout(height=450, showlegend=False)
#         st.plotly_chart(fig_s3, use_container_width=True)
 
#     with col2:
#         fig_s4 = px.scatter(
#             df, x="temperature", y="rainfall",
#             color="label", hover_name="label",
#             title="Temperature vs Rainfall by Crop",
#             labels={"temperature": "Temperature (°C)", "rainfall": "Rainfall (mm)"},
#             opacity=0.6
#         )
#         fig_s4.update_layout(height=450, showlegend=False)
#         st.plotly_chart(fig_s4, use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 16. BOX PLOT
#     # =====================================================
 
#     st.subheader("📦 Feature Distribution (Box Plot)")
#     st.caption("Shows median, quartiles, and outliers for each feature across all crops.")
 
#     box_feature = st.selectbox(
#         "Select Feature for Box Plot",
#         ["temperature", "humidity", "rainfall", "ph", "N", "P", "K"],
#         key="box_sel"
#     )
 
#     fig_box = px.box(
#         df, x="label", y=box_feature,
#         color="label", hover_name="label",
#         title=f"{box_feature.capitalize()} Distribution by Crop",
#         color_discrete_sequence=px.colors.qualitative.Pastel,
#         labels={"label": "Crop"}
#     )
#     fig_box.update_layout(
#         xaxis_tickangle=-45, height=520,
#         showlegend=False, xaxis_title=""
#     )
#     st.plotly_chart(fig_box, use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 17. CROP FULL PROFILE TABLE
#     # =====================================================
 
#     st.subheader("📋 Complete Crop Profile (All Features Averaged)")
#     st.caption("One row per crop — all 7 features side by side for easy comparison.")
 
#     numeric_features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
 
#     full_profile = (
#         df.groupby("label")[numeric_features]
#         .mean().round(2)
#     )
#     full_profile.columns = [
#         "N (mg/kg)", "P (mg/kg)", "K (mg/kg)",
#         "Temp (°C)", "Humidity (%)", "pH", "Rainfall (mm)"
#     ]
 
#     st.dataframe(
#         full_profile.style.background_gradient(cmap="YlGn", axis=0),
#         use_container_width=True
#     )
 
#     st.markdown("---")
 
#     # =====================================================
#     # 18. CROP-TO-CROP COMPARISON
#     # =====================================================
 
#     st.subheader("⚖️ Crop-to-Crop Comparison")
 
#     crops_list = sorted(df["label"].unique())
 
#     col1, col2 = st.columns(2)
#     with col1:
#         crop_a = st.selectbox("Select Crop A", crops_list, index=0, key="crop_a")
#     with col2:
#         crop_b = st.selectbox("Select Crop B", crops_list, index=1, key="crop_b")
 
#     numeric_features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
 
#     a_vals = df[df["label"] == crop_a][numeric_features].mean().round(2)
#     b_vals = df[df["label"] == crop_b][numeric_features].mean().round(2)
 
#     compare_df = pd.DataFrame({
#         "Feature": numeric_features,
#         crop_a:    a_vals.values,
#         crop_b:    b_vals.values
#     })
 
#     fig_comp = go.Figure()
#     fig_comp.add_trace(go.Bar(
#         name=crop_a, x=compare_df["Feature"], y=compare_df[crop_a],
#         marker_color="#2ca02c",
#         text=compare_df[crop_a], textposition="outside"
#     ))
#     fig_comp.add_trace(go.Bar(
#         name=crop_b, x=compare_df["Feature"], y=compare_df[crop_b],
#         marker_color="#1f77b4",
#         text=compare_df[crop_b], textposition="outside"
#     ))
#     fig_comp.update_layout(
#         barmode="group",
#         title=f"Side-by-Side: {crop_a}  vs  {crop_b}",
#         height=420,
#         xaxis_title="Feature",
#         yaxis_title="Value"
#     )
#     st.plotly_chart(fig_comp, use_container_width=True)
 
#     crop_means = df.groupby("label")[numeric_features].mean()
#     crop_norm  = (crop_means - crop_means.min()) / (
#         crop_means.max() - crop_means.min()
#     )
 
#     a_norm = crop_norm.loc[crop_a].values.tolist()
#     b_norm = crop_norm.loc[crop_b].values.tolist()
 
#     fig_radar = go.Figure()
#     fig_radar.add_trace(go.Scatterpolar(
#         r=a_norm + [a_norm[0]],
#         theta=numeric_features + [numeric_features[0]],
#         fill="toself", name=crop_a,
#         line_color="#2ca02c",
#         fillcolor="rgba(44,160,44,0.15)"
#     ))
#     fig_radar.add_trace(go.Scatterpolar(
#         r=b_norm + [b_norm[0]],
#         theta=numeric_features + [numeric_features[0]],
#         fill="toself", name=crop_b,
#         line_color="#1f77b4",
#         fillcolor="rgba(31,119,180,0.15)"
#     ))
#     fig_radar.update_layout(
#         polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
#         title=f"Radar Chart: {crop_a} vs {crop_b} (Normalized 0–1)",
#         height=500
#     )
#     st.plotly_chart(fig_radar, use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 19. SIMILAR CROPS FINDER
#     # =====================================================
 
#     st.subheader("🔍 Similar Crops Finder")
#     st.caption(
#         "Finds the 3 most similar crops by soil and climate conditions "
#         "(Euclidean distance on normalized features)."
#     )
 
#     target_crop = st.selectbox(
#         "Select a Crop to Find Similar Crops", crops_list, key="sim_crop"
#     )
 
#     target_vec = crop_norm.loc[target_crop]
#     distances  = crop_norm.drop(target_crop).apply(
#         lambda row: np.sqrt(((row - target_vec) ** 2).sum()), axis=1
#     )
#     top3 = distances.nsmallest(3).reset_index()
#     top3.columns = ["Similar Crop", "Distance (lower = more similar)"]
#     top3["Distance (lower = more similar)"] = top3[
#         "Distance (lower = more similar)"
#     ].round(4)
 
#     st.write(f"#### Top 3 Crops Most Similar to **{target_crop}**")
#     st.dataframe(top3, use_container_width=True)
 
#     sim_names   = top3["Similar Crop"].tolist()
#     sim_profile = crop_means.loc[[target_crop] + sim_names].round(2)
#     st.dataframe(
#         sim_profile.style.background_gradient(cmap="Greens", axis=0),
#         use_container_width=True
#     )
 
#     st.markdown("---")
 
#     # =====================================================
#     # 20. CROP FILTER
#     # =====================================================
 
#     st.subheader("🔍 Crop Filter")
 
#     selected_crop = st.selectbox(
#         "Select Crop", crops_list, key="crop_filter"
#     )
#     crop_data = df[df["label"] == selected_crop]
 
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         st.metric("Avg Temperature", f"{crop_data['temperature'].mean():.1f} °C")
#     with col2:
#         st.metric("Avg Humidity",    f"{crop_data['humidity'].mean():.1f} %")
#     with col3:
#         st.metric("Avg Rainfall",    f"{crop_data['rainfall'].mean():.1f} mm")
#     with col4:
#         st.metric("Avg pH",          f"{crop_data['ph'].mean():.2f}")
 
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Avg Nitrogen",   round(crop_data["N"].mean(), 2))
#     with col2:
#         st.metric("Avg Phosphorus", round(crop_data["P"].mean(), 2))
#     with col3:
#         st.metric("Avg Potassium",  round(crop_data["K"].mean(), 2))
 
#     st.dataframe(crop_data, use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 21. CORRELATION MATRIX
#     # =====================================================
 
#     st.subheader("🔗 Feature Correlation Matrix")
 
#     numeric_features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
#     correlation = df[numeric_features].corr().round(3)
 
#     fig_corr = px.imshow(
#         correlation,
#         text_auto=True,
#         color_continuous_scale="RdYlGn",
#         zmin=-1, zmax=1,
#         title="Feature Correlation Heatmap",
#         aspect="auto"
#     )
#     fig_corr.update_layout(height=500)
#     st.plotly_chart(fig_corr, use_container_width=True)
 
#     st.caption(
#         "🟢 Green = strong positive correlation | "
#         "🔴 Red = strong negative correlation | "
#         "⚪ White = no correlation"
#     )
 
#     st.write("#### 📌 Strongest Correlations (Auto-Extracted)")
 
#     corr_pairs = correlation.unstack().reset_index()
#     corr_pairs.columns = ["Feature A", "Feature B", "Correlation"]
#     corr_pairs = corr_pairs[corr_pairs["Feature A"] < corr_pairs["Feature B"]]
#     corr_pairs["Abs"] = corr_pairs["Correlation"].abs()
#     corr_pairs = corr_pairs.sort_values("Abs", ascending=False).drop(columns="Abs")
 
#     col1, col2 = st.columns(2)
#     with col1:
#         st.write("**Top 3 Positive Correlations**")
#         pos = corr_pairs[corr_pairs["Correlation"] > 0].head(3)
#         st.dataframe(pos.reset_index(drop=True), use_container_width=True)
#     with col2:
#         st.write("**Top 3 Negative Correlations**")
#         neg = corr_pairs[corr_pairs["Correlation"] < 0].head(3)
#         st.dataframe(neg.reset_index(drop=True), use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 22. FEATURE MEANING
#     # =====================================================
 
#     st.subheader("📘 Feature Meaning")
 
#     feature_info = pd.DataFrame({
#         "Feature": ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"],
#         "Meaning": [
#             "Nitrogen — helps leaf and stem growth",
#             "Phosphorus — helps root and flower growth",
#             "Potassium — improves plant strength and disease resistance",
#             "Temperature — optimal growing temperature for the crop",
#             "Humidity — moisture level in the air (%)",
#             "Soil pH — acidity or alkalinity of the soil",
#             "Rainfall — amount of rain required (mm)"
#         ],
#         "Unit": ["mg/kg", "mg/kg", "mg/kg", "°C", "%", "0–14 scale", "mm"]
#     })
 
#     st.dataframe(feature_info, use_container_width=True)
 
#     st.markdown("---")
 
#     # =====================================================
#     # 23. FARMER UNDERSTANDING GUIDE
#     # =====================================================
 
#     st.subheader("🌱 Farmer Understanding Guide")
 
#     col1, col2 = st.columns(2)
 
#     with col1:
#         st.success("🟢 **Low Nitrogen (≤50)** → Light fertilizer needed")
#         st.info("🔵 **Medium Nitrogen (51–120)** → Balanced fertilizer")
#         st.warning("🟡 **High Nitrogen (>120)** → Heavy fertilizer required")
#         st.success("🟢 **Cool Temperature (≤20°C)** → Cool climate crops (wheat)")
#         st.info("🔵 **Moderate Temperature (21–30°C)** → Most common crops")
#         st.warning("🟡 **Hot Temperature (>30°C)** → Summer/tropical crops")
 
#     with col2:
#         st.success("🟢 **Acidic Soil (pH < 6)** → Suits tea, rice, blueberry")
#         st.info("🔵 **Neutral Soil (pH 6–7.5)** → Best for most crops")
#         st.warning("🟡 **Alkaline Soil (pH > 7.5)** → Suits cotton, maize")
#         st.success("🟢 **Low Rainfall (≤100mm)** → Drought-tolerant crops")
#         st.info("🔵 **Medium Rainfall (101–200mm)** → General crops")
#         st.warning("🟡 **High Rainfall (>200mm)** → Water-intensive crops")
 
#     st.markdown("---")
 
#     # =====================================================
#     # 24. KEY INSIGHTS
#     # =====================================================
 
#     st.subheader("📌 Key Insights")
 
#     st.success("✅ Dataset is balanced with nearly equal crop distribution.")
#     st.success("✅ No missing values and no duplicate rows found.")
#     st.success("✅ Dataset is clean and ready for ML model training.")
#     st.info(
#         "📊 Rainfall, temperature, humidity, and soil nutrients "
#         "play a major role in crop recommendation."
#     )
#     st.info(
#         "🌱 Crops like rice and jute need high humidity & rainfall, "
#         "while chickpea and kidney beans prefer dry conditions."
#     )
#     st.info(
#         "🧪 Use Scatter Plots and Box Plots to identify natural crop "
#         "clusters — useful for ML feature selection."
#     )
#     st.info(
#         "⚖️ Use the Crop Comparison and Similar Crops tools to help "
#         "farmers choose alternative crops for their soil conditions."
#     )
 
#     st.markdown("---")
 
# # =========================================================
# # ==================== ML PREDICTION ======================
# # =========================================================
 
# elif page == "ML Prediction":
 
#     st.header("🤖 Crop Prediction System")
 
#     st.markdown("---")
 
#     # =====================================================
#     # CHECK IF MODEL FILES ARE LOADED
#     # =====================================================
 
#     if ml_error:
#         st.error(
#             f"❌ Could not load ML model files.\n\n"
#             f"**Error:** `{ml_error}`\n\n"
#             "Please make sure `crop_model.pkl`, `scaler.pkl`, and "
#             "`label_encoder.pkl` are in the same folder as `app.py`."
#         )
#         st.stop()
 
#     # =====================================================
#     # FEATURE IMPORTANCE — always visible (above prediction)
#     # =====================================================
 
#     if hasattr(model, "feature_importances_"):
 
#         st.subheader("📈 Model Feature Importance")
#         st.caption("How much each feature contributes to crop prediction decisions.")
 
#         importance_df = pd.DataFrame({
#             "Feature": [
#                 "Nitrogen", "Phosphorus", "Potassium",
#                 "Temperature", "Humidity", "Soil pH", "Rainfall"
#             ],
#             "Importance": model.feature_importances_
#         }).sort_values("Importance", ascending=False)
 
#         fig_imp = px.bar(
#             importance_df,
#             x="Feature", y="Importance",
#             color="Importance",
#             text=importance_df["Importance"].round(3),
#             color_continuous_scale="Teal",
#             title="Feature Importance (Higher = More Influential)"
#         )
#         fig_imp.update_traces(textposition="outside")
#         fig_imp.update_layout(height=420)
#         st.plotly_chart(fig_imp, use_container_width=True)
 
#         most_imp = importance_df.iloc[0]["Feature"]
#         least_imp = importance_df.iloc[-1]["Feature"]
#         st.info(
#             f"🔑 **Most important feature:** {most_imp}  |  "
#             f"📉 **Least important feature:** {least_imp}"
#         )
 
#         st.markdown("---")
 
#     # =====================================================
#     # INPUT SLIDERS — use dataset min/max for all features
#     # =====================================================
 
#     st.subheader("🌱 Enter Soil and Weather Details")
 
#     col1, col2 = st.columns(2)
 
#     with col1:
#         N = st.slider(
#             "Nitrogen (N) mg/kg",
#             int(df["N"].min()), int(df["N"].max()),
#             int(df["N"].mean())
#         )
#         P = st.slider(
#             "Phosphorus (P) mg/kg",
#             int(df["P"].min()), int(df["P"].max()),
#             int(df["P"].mean())
#         )
#         K = st.slider(
#             "Potassium (K) mg/kg",
#             int(df["K"].min()), int(df["K"].max()),
#             int(df["K"].mean())
#         )
#         temperature = st.slider(
#             "Temperature (°C)",
#             float(df["temperature"].min()),
#             float(df["temperature"].max()),
#             round(float(df["temperature"].mean()), 1)
#         )
 
#     with col2:
#         humidity = st.slider(
#             "Humidity (%)",
#             float(df["humidity"].min()),
#             float(df["humidity"].max()),
#             round(float(df["humidity"].mean()), 1)
#         )
#         ph = st.slider(
#             "Soil pH",
#             float(df["ph"].min()),
#             float(df["ph"].max()),
#             round(float(df["ph"].mean()), 1)
#         )
#         rainfall = st.slider(
#             "Rainfall (mm)",
#             float(df["rainfall"].min()),
#             float(df["rainfall"].max()),
#             round(float(df["rainfall"].mean()), 1)
#         )
 
#     # Live input category display
#     st.markdown("---")
#     st.subheader("📊 Your Input Analysis")
 
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         st.info(f"🌿 Nitrogen: **{nitrogen_category(N)}**")
#         st.info(f"🌿 Phosphorus: **{phosphorus_category(P)}**")
#     with col2:
#         st.info(f"🌿 Potassium: **{potassium_category(K)}**")
#         st.info(f"🌡 Temperature: **{temperature_category(temperature)}**")
#     with col3:
#         st.info(f"💧 Humidity: **{humidity_category(humidity)}**")
#         st.info(f"🧪 Soil pH: **{ph_category(ph)}**")
#     with col4:
#         st.info(f"🌧 Rainfall: **{rainfall_category(rainfall)}**")
 
#     st.markdown("---")
 
#     # =====================================================
#     # PREDICTION BUTTON
#     # =====================================================
 
#     if st.button("🌾 Predict Best Crop", use_container_width=True):
 
#         input_data = [[N, P, K, temperature, humidity, ph, rainfall]]
 
#         try:
#             # Scale input
#             scaled_input = scaler.transform(input_data)
 
#             # Predict
#             prediction    = model.predict(scaled_input)
#             predicted_crop = label_encoder.inverse_transform(prediction)[0]
 
#             # =================================================
#             # RESULT
#             # =================================================
 
#             st.success(f"✅ Recommended Crop: **{predicted_crop.upper()}**")
 
#             st.markdown("---")
 
#             # =================================================
#             # TOP 5 PREDICTIONS WITH PROBABILITY
#             # =================================================
 
#             if hasattr(model, "predict_proba"):
 
#                 st.subheader("📊 Top 5 Predicted Crops")
 
#                 probability = model.predict_proba(scaled_input)[0]
 
#                 prob_df = pd.DataFrame({
#                     "Crop":        label_encoder.classes_,
#                     "Probability": probability
#                 }).sort_values("Probability", ascending=False).head(5)
 
#                 prob_df["Probability (%)"] = (
#                     prob_df["Probability"] * 100
#                 ).round(2)
 
#                 fig_prob = px.bar(
#                     prob_df,
#                     x="Crop", y="Probability",
#                     color="Probability",
#                     text=prob_df["Probability (%)"].astype(str) + "%",
#                     color_continuous_scale="Greens",
#                     title="Prediction Confidence (Top 5 Crops)"
#                 )
#                 fig_prob.update_traces(textposition="outside")
#                 fig_prob.update_layout(height=450)
#                 st.plotly_chart(fig_prob, use_container_width=True)
 
#                 top_conf = prob_df.iloc[0]["Probability (%)"]
#                 if top_conf >= 80:
#                     st.success(f"🎯 High confidence prediction: {top_conf}%")
#                 elif top_conf >= 50:
#                     st.info(f"🔍 Moderate confidence: {top_conf}% — verify with local conditions.")
#                 else:
#                     st.warning(
#                         f"⚠️ Low confidence: {top_conf}% — "
#                         "soil conditions may be unusual. Consult an agronomist."
#                     )
 
#             else:
#                 st.info(
#                     "ℹ️ This model does not support probability output. "
#                     "Only the top prediction is shown."
#                 )
 
#             st.markdown("---")
 
#             # =================================================
#             # INPUT SUMMARY
#             # =================================================
 
#             st.subheader("📋 Farmer Input Summary")
 
#             summary_df = pd.DataFrame({
#                 "Feature": [
#                     "Nitrogen (mg/kg)", "Phosphorus (mg/kg)", "Potassium (mg/kg)",
#                     "Temperature (°C)", "Humidity (%)", "Soil pH", "Rainfall (mm)"
#                 ],
#                 "Your Value": [N, P, K, temperature, humidity, ph, rainfall],
#                 "Category": [
#                     nitrogen_category(N), phosphorus_category(P),
#                     potassium_category(K), temperature_category(temperature),
#                     humidity_category(humidity), ph_category(ph),
#                     rainfall_category(rainfall)
#                 ]
#             })
 
#             st.dataframe(summary_df, use_container_width=True)
 
#             st.markdown("---")
 
#             # =================================================
#             # COMPARE INPUT vs PREDICTED CROP AVERAGES
#             # =================================================
 
#             st.subheader("📐 Your Inputs vs Ideal Conditions for Predicted Crop")
#             st.caption(
#                 f"Comparing your entered values against the dataset averages "
#                 f"for **{predicted_crop}**."
#             )
 
#             numeric_features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
#             feature_labels   = [
#                 "Nitrogen", "Phosphorus", "Potassium",
#                 "Temperature", "Humidity", "pH", "Rainfall"
#             ]
 
#             crop_avg = df[df["label"] == predicted_crop][numeric_features].mean().round(2)
#             user_vals = [N, P, K, temperature, humidity, ph, rainfall]
 
#             compare_fig = go.Figure()
#             compare_fig.add_trace(go.Bar(
#                 name="Your Input",
#                 x=feature_labels,
#                 y=user_vals,
#                 marker_color="#1f77b4",
#                 text=[round(v, 2) for v in user_vals],
#                 textposition="outside"
#             ))
#             compare_fig.add_trace(go.Bar(
#                 name=f"Ideal for {predicted_crop}",
#                 x=feature_labels,
#                 y=crop_avg.values,
#                 marker_color="#2ca02c",
#                 text=crop_avg.values,
#                 textposition="outside"
#             ))
#             compare_fig.update_layout(
#                 barmode="group",
#                 title=f"Your Input vs Ideal: {predicted_crop}",
#                 height=430,
#                 xaxis_title="Feature",
#                 yaxis_title="Value"
#             )
#             st.plotly_chart(compare_fig, use_container_width=True)
 
#             st.markdown("---")
 
#             # =================================================
#             # CROP ADVICE — comprehensive for all known crops
#             # =================================================
 
#             st.subheader("🌱 Crop Guidance")
 
#             crop_advice = {
#                 "rice":        "Requires high rainfall (150–300mm), high humidity (80–90%), and slightly acidic soil (pH 5.5–6.5). Best in flooded or waterlogged conditions.",
#                 "maize":       "Needs moderate rainfall (50–75mm/month), moderate temperature (21–27°C), and fertile loamy soil (pH 5.5–7.0).",
#                 "jute":        "Thrives in high humidity and high rainfall. Requires warm climate (25–35°C) and alluvial soil.",
#                 "cotton":      "Grows well in well-drained black soil (pH 6–8), warm climate (21–35°C), and moderate rainfall.",
#                 "coconut":     "Requires tropical climate, high humidity (70–80%), and sandy loam soil. High rainfall preferred.",
#                 "papaya":      "Needs warm climate (25–30°C), well-drained soil, moderate rainfall, and high humidity.",
#                 "banana":      "Requires rich loamy soil, high humidity, warm temperature (26–30°C), and regular rainfall or irrigation.",
#                 "mango":       "Prefers dry season at flowering, deep well-drained soil (pH 5.5–7.5), and tropical/subtropical climate.",
#                 "grapes":      "Needs well-drained sandy loam soil, dry hot summers and cool winters, low humidity to avoid disease.",
#                 "watermelon":  "Requires warm climate (25–35°C), sandy loam soil, and moderate to high rainfall or irrigation.",
#                 "muskmelon":   "Grows best in warm climate, sandy soil with good drainage, and moderate humidity.",
#                 "apple":       "Requires cool climate (cold winters for dormancy), well-drained loamy soil, and moderate rainfall.",
#                 "orange":      "Needs subtropical climate, well-drained sandy loam soil, and moderate rainfall (750–1200mm).",
#                 "pomegranate": "Tolerates a wide pH range (5.5–7.5), drought-tolerant, grows well in semi-arid regions.",
#                 "lentil":      "Cool season crop, needs well-drained loamy soil (pH 6–8), low rainfall, and moderate temperature.",
#                 "blackgram":   "Prefers warm climate (25–35°C), well-drained loamy soil, and moderate rainfall (600–800mm).",
#                 "mungbean":    "Warm season crop, needs sandy loam soil, short rainfall, and moderate temperature (28–30°C).",
#                 "mothbeans":   "Drought-tolerant, grows in arid and semi-arid regions with sandy soil and very low rainfall.",
#                 "pigeonpeas":  "Drought-tolerant legume, grows in well-drained soil (pH 5–7), moderate rainfall.",
#                 "kidneybeans": "Requires cool temperature, well-drained fertile loam soil (pH 6–7), and moderate rainfall.",
#                 "chickpea":    "Cool season crop, drought-tolerant, well-drained loamy soil (pH 5.5–7), low rainfall.",
#                 "coffee":      "Requires tropical climate (15–28°C), high humidity, well-drained acidic soil (pH 6–6.5), and high rainfall."
#             }
 
#             advice = crop_advice.get(
#                 predicted_crop.lower(),
#                 f"**{predicted_crop}** is suited to the conditions you entered. "
#                 "Consult local agricultural guidelines for detailed advice."
#             )
 
#             st.info(f"🌿 **{predicted_crop.capitalize()} Advice:** {advice}")
 
#             st.markdown("---")
 
#             # =================================================
#             # SOIL CONDITION ANALYSIS
#             # =================================================
 
#             st.subheader("🧪 Soil & Climate Condition Summary")
 
#             col1, col2 = st.columns(2)
 
#             with col1:
#                 # Soil pH
#                 if ph < 6:
#                     st.warning("⚠️ **Soil is Acidic** (pH < 6) — consider adding lime to raise pH.")
#                 elif ph > 7.5:
#                     st.warning("⚠️ **Soil is Alkaline** (pH > 7.5) — consider adding sulfur to lower pH.")
#                 else:
#                     st.success("✅ **Soil pH is Neutral** (pH 6–7.5) — ideal for most crops.")
 
#                 # Nitrogen
#                 n_cat = nitrogen_category(N)
#                 if n_cat == "Low":
#                     st.warning("⚠️ Low Nitrogen — apply nitrogen-rich fertilizer (urea).")
#                 elif n_cat == "High":
#                     st.info("ℹ️ High Nitrogen — reduce nitrogen fertilizer to avoid over-fertilization.")
#                 else:
#                     st.success("✅ Nitrogen level is balanced.")
 
#             with col2:
#                 # Rainfall
#                 if rainfall > 200:
#                     st.info("🌧 High rainfall region detected — ensure good drainage.")
#                 elif rainfall < 80:
#                     st.info("☀️ Low rainfall region — consider drip irrigation.")
#                 else:
#                     st.success("✅ Moderate rainfall — suitable for general crops.")
 
#                 # Temperature
#                 temp_cat = temperature_category(temperature)
#                 if temp_cat == "Cool":
#                     st.info("❄️ Cool temperature — suitable for wheat, lentil, chickpea.")
#                 elif temp_cat == "Hot":
#                     st.info("🔥 Hot temperature — suitable for tropical/summer crops.")
#                 else:
#                     st.success("✅ Moderate temperature — good for most crops.")
 
#         except Exception as e:
#             st.error(
#                 f"❌ Prediction failed.\n\n**Error:** `{str(e)}`\n\n"
#                 "Please check that your model files match the input features."
#             )
 
# # =========================================================
# # ================= DISEASE DETECTION =====================
# # =========================================================

# elif page == "Disease Detection":

#     st.header("🌿 Plant Disease Detection System")

#     st.markdown("---")

#     st.subheader("📤 Upload Leaf Image")

#     uploaded_file = st.file_uploader(
#         "Upload plant leaf image",
#         type=["jpg", "jpeg", "png"]
#     )

#     if uploaded_file is not None:

#         # =================================================
#         # SHOW IMAGE
#         # =================================================

#         image = Image.open(uploaded_file)

#         st.image(
#             image,
#             caption="Uploaded Leaf Image",
#             width=400
#         )

#         st.markdown("---")

#         # =================================================
#         # PREPROCESS IMAGE
#         # =================================================

#         img = image.resize((128, 128))

#         img_array = img_to_array(img)

#         img_array = img_array / 255.0

#         img_array = np.expand_dims(img_array, axis=0)

#         # =================================================
#         # PREDICTION
#         # =================================================

#         prediction = disease_model.predict(img_array)

#         predicted_class = np.argmax(prediction)

#         disease_name = disease_encoder.inverse_transform(
#             [predicted_class]
#         )[0]

#         confidence = np.max(prediction) * 100

#         # =================================================
#         # RESULT
#         # =================================================

#         st.success(
#             f"✅ Predicted Disease: {disease_name}"
#         )

#         st.info(
#             f"🎯 Confidence: {confidence:.2f}%"
#         )

#         st.markdown("---")

#         # =================================================
#         # TREATMENT ADVICE
#         # =================================================

#         st.subheader("🌱 Treatment Advice")

#         disease_advice = {

#             "Tomato_healthy":
#                 "✅ Plant is healthy. Maintain proper watering and sunlight.",

#             "Tomato_Early_blight":
#                 "⚠️ Remove infected leaves and use fungicide spray.",

#             "Tomato_Late_blight":
#                 "⚠️ Avoid overwatering and apply copper-based fungicide.",

#             "Tomato_Leaf_Mold":
#                 "⚠️ Improve air circulation and reduce humidity."
#         }

#         advice = disease_advice.get(
#             disease_name,
#             "General plant care recommended."
#         )

#         st.warning(advice)

#         st.markdown("---")

#         # =================================================
#         # PREDICTION PROBABILITIES
#         # =================================================

#         st.subheader("📊 Prediction Confidence")

#         prob_df = pd.DataFrame({
#             "Disease": disease_encoder.classes_,
#             "Confidence": prediction[0]
#         })

#         prob_df = prob_df.sort_values(
#             "Confidence",
#             ascending=False
#         )

#         fig = px.bar(
#             prob_df,
#             x="Disease",
#             y="Confidence",
#             color="Confidence",
#             text="Confidence",
#             color_continuous_scale="Reds"
#         )

#         fig.update_traces(
#             texttemplate='%{text:.2f}',
#             textposition='outside'
#         )

#         fig.update_layout(height=450)

#         st.plotly_chart(fig, use_container_width=True)





# import os
# import io
# import numpy as np
# import pandas as pd
# import joblib
# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.io as pio
# from PIL import Image

# # =========================================================
# # ===== GLOBAL PLOTLY THEME — force white bg, dark text ===
# # =========================================================

# pio.templates["krishi"] = go.layout.Template(
#     layout=go.Layout(
#         paper_bgcolor="#ffffff",
#         plot_bgcolor="#f9fdf9",
#         font=dict(
#             color="#ffffff",
#             family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
#         ),
#         title=dict(font=dict(color="#0d2e0d", size=16)),
#         xaxis=dict(
#             color="#ffffff",
#             gridcolor="#d4ecd4",
#             linecolor="#81c784",
#             tickfont=dict(color="#ffffff"),
#             title=dict(font=dict(color="#ffffff")),
#             zerolinecolor="#c8e6c9",
#         ),
#         yaxis=dict(
#             color="#ffffff",
#             gridcolor="#d4ecd4",
#             linecolor="#81c784",
#             tickfont=dict(color="#ffffff"),
#             title=dict(font=dict(color="#ffffff")),
#             zerolinecolor="#c8e6c9",
#         ),
#         legend=dict(
#             bgcolor="#ffffff",
#             bordercolor="#c8e6c9",
#             font=dict(color="#ffffff"),
#         ),
#         coloraxis=dict(
#             colorbar=dict(
#                 tickfont=dict(color="#ffffff", size=12),
#                 tickcolor="#ffffff",
#                 title=dict(font=dict(color="#ffffff", size=13), side="right"),
#                 bgcolor="#ffffff",
#                 outlinecolor="#c8e6c9",
#                 outlinewidth=1,
#                 bordercolor="#c8e6c9",
#                 borderwidth=1,
#                 len=0.85,
#             )
#         ),
#         polar=dict(
#             bgcolor="#f9fdf9",
#             radialaxis=dict(color="#ffffff", gridcolor="#d4ecd4"),
#             angularaxis=dict(color="#ffffff", gridcolor="#d4ecd4"),
#         ),
#         colorway=["#2e7d32","#1f77b4","#ff7f0e","#d62728","#9467bd",
#                   "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"],
#     )
# )
# pio.templates.default = "krishi"
 
# # =========================================================
# # ================= PAGE CONFIG ===========================
# # =========================================================
 
# st.set_page_config(
#     page_title="Krishi AI — Smart Farming Assistant",
#     page_icon="🌱",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
 
# # =========================================================
# # ================= CUSTOM CSS ============================
# # =========================================================
 
# st.markdown("""
# <style>
#     /* ── Global font & base ── */
#     html, body, [class*="css"] {
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }

#     /* ── Main app background: light green-white ── */
#     .stApp {
#         background-color: #f0f7f0;
#         color: #ffffff !important;
#     }

#     /* ── Force all generic text dark on light bg ── */
#     .stApp p, .stApp span, .stApp div, .stApp label,
#     .stApp li, .stApp td, .stApp th, .stApp caption {
#         color: #ffffff !important;
#     }

#     /* ── Headings ── */
#     .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
#         color: #0d2e0d !important;
#         font-weight: 700;
#     }

#     /* ── Sidebar: dark green gradient ── */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #0d2e0d 0%, #1a5c2a 50%, #2e7d32 100%);
#     }
#     /* ALL text inside sidebar must be white */
#     [data-testid="stSidebar"] *,
#     [data-testid="stSidebar"] p,
#     [data-testid="stSidebar"] span,
#     [data-testid="stSidebar"] div,
#     [data-testid="stSidebar"] label,
#     [data-testid="stSidebar"] h1,
#     [data-testid="stSidebar"] h2,
#     [data-testid="stSidebar"] h3,
#     [data-testid="stSidebar"] .stMarkdown,
#     [data-testid="stSidebar"] .stCaption,
#     [data-testid="stSidebar"] .stSelectbox label {
#         color: #ffffff !important;
#     }
#     [data-testid="stSidebar"] option {
#         color: #ffffff !important;
#         background-color: white !important;
#     }

#     /* ── Header banner ── */
#     .krishi-header {
#         background: linear-gradient(135deg, #0d2e0d, #1b5e20, #2e7d32, #388e3c);
#         padding: 2.2rem 1.5rem 1.8rem 1.5rem;
#         border-radius: 18px;
#         text-align: center;
#         margin-bottom: 1.8rem;
#         box-shadow: 0 6px 28px rgba(13,46,13,0.35);
#     }
#     .krishi-header h1 {
#         color: #ffffff !important;
#         font-size: 2.6rem;
#         margin: 0;
#         letter-spacing: 2px;
#         text-shadow: 0 2px 8px rgba(0,0,0,0.4);
#     }
#     .krishi-header p {
#         color: #c8e6c9 !important;
#         margin: 0.4rem 0 0 0;
#         font-size: 1.05rem;
#     }

#     /* ── Metric cards: white bg, dark text ── */
#     [data-testid="stMetric"] {
#         background: #ffffff !important;
#         border-radius: 12px !important;
#         padding: 0.9rem 1.1rem !important;
#         border-left: 4px solid #2e7d32 !important;
#         box-shadow: 0 3px 10px rgba(0,0,0,0.09) !important;
#     }
#     [data-testid="stMetric"] label,
#     [data-testid="stMetric"] [data-testid="stMetricLabel"],
#     [data-testid="stMetric"] [data-testid="stMetricValue"],
#     [data-testid="stMetric"] div {
#         color: #0d2e0d !important;
#     }
#     [data-testid="stMetricLabel"] p {
#         color: #4a7c4a !important;
#         font-weight: 600;
#     }
#     [data-testid="stMetricValue"] {
#         color: #0d2e0d !important;
#         font-size: 1.6rem !important;
#         font-weight: 700 !important;
#     }

#     /* ── Dataframe / table text ── */
#     .stDataFrame, .stDataFrame * {
#         color: #ffffff !important;
#     }
#     [data-testid="stDataFrameContainer"] {
#         border: 1px solid #c8e6c9;
#         border-radius: 10px;
#     }

#     /* ── Chat bubbles ── */
#     .chat-user {
#         background: #1b5e20;
#         border-radius: 16px 16px 4px 16px;
#         padding: 0.75rem 1.2rem;
#         margin: 0.4rem 0;
#         max-width: 80%;
#         margin-left: auto;
#         color: #ffffff !important;
#         font-weight: 500;
#         box-shadow: 0 2px 8px rgba(27,94,32,0.25);
#     }
#     .chat-ai {
#         background: #ffffff;
#         border-radius: 16px 16px 16px 4px;
#         padding: 0.75rem 1.2rem;
#         margin: 0.4rem 0;
#         max-width: 85%;
#         border-left: 3px solid #43a047;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#         color: #ffffff !important;
#     }
#     .chat-label-user {
#         text-align: right;
#         font-size: 0.75rem;
#         color: #4a7c4a !important;
#         margin-bottom: 3px;
#         font-weight: 600;
#     }
#     .chat-label-ai {
#         font-size: 0.75rem;
#         color: #4a7c4a !important;
#         margin-bottom: 3px;
#         font-weight: 600;
#     }

#     /* ── Disease result card: white bg, dark text ── */
#     .disease-card {
#         background: #ffffff;
#         border-radius: 16px;
#         padding: 1.6rem;
#         box-shadow: 0 4px 18px rgba(0,0,0,0.10);
#         margin: 1rem 0;
#         color: #ffffff !important;
#         border-top: 4px solid #2e7d32;
#     }
#     .disease-card * {
#         color: #ffffff !important;
#     }

#     /* ── Buttons ── */
#     .stButton > button {
#         background: linear-gradient(135deg, #1b5e20, #2e7d32, #43a047) !important;
#         color: #ffffff !important;
#         border: none !important;
#         border-radius: 10px !important;
#         font-weight: 700 !important;
#         font-size: 0.95rem !important;
#         padding: 0.55rem 1.2rem !important;
#         transition: all 0.2s ease !important;
#         letter-spacing: 0.3px;
#     }
#     .stButton > button:hover {
#         transform: translateY(-2px) !important;
#         box-shadow: 0 6px 16px rgba(46,125,50,0.4) !important;
#         background: linear-gradient(135deg, #155218, #256427, #36883a) !important;
#     }
#     .stButton > button * {
#         color: #ffffff !important;
#     }

#     /* ── Alert / Info / Warning / Success / Error boxes ── */
#     /* Streamlit uses .stAlert for all alert types */
#     div[data-testid="stNotification"],
#     .stAlert > div,
#     div.stSuccess > div,
#     div.stInfo > div,


#     div.stWarning > div,
#     div.stError > div {
#         border-radius: 12px !important;
#     }
#     /* Make sure text inside alerts is legible */
#     .stSuccess p, .stSuccess div, .stSuccess span, .stSuccess li {
#         color: #1b4332 !important;
#     }
#     .stInfo p, .stInfo div, .stInfo span, .stInfo li {
#         color: #0c3547 !important;
#     }
#     .stWarning p, .stWarning div, .stWarning span, .stWarning li {
#         color: #4a3000 !important;
#     }
#     .stError p, .stError div, .stError span, .stError li {
#         color: #5c0a0a !important;
#     }

#     /* ── Selectbox & slider labels ── */
#     .stSelectbox label,
#     .stSlider label,
#     .stTextInput label,
#     .stFileUploader label {
#         color: #ffffff !important;
#         font-weight: 600 !important;
#     }

#     /* ── Text input box ── */
#     .stTextInput input {
#         background: #ffffff !important;
#         color: #ffffff !important;
#         border: 1.5px solid #81c784 !important;
#         border-radius: 8px !important;
#     }
#     .stTextInput input::placeholder {
#         color: #7aaa7a !important;
#     }
#     .stTextInput input:focus {
#         border-color: #2e7d32 !important;
#         box-shadow: 0 0 0 2px rgba(46,125,50,0.2) !important;
#     }

#     /* ── Slider values ── */
#     .stSlider [data-testid="stTickBar"],
#     .stSlider .stSlider div {
#         color: #ffffff !important;
#     }

#     /* ── Plotly chart container ── */
#     .js-plotly-plot, .plotly, .plot-container {
#         background: #ffffff !important;
#         border-radius: 12px;
#     }

#     /* ── Plotly SVG: axis labels, tick text, titles, colorbar — dark on white bg ── */
#     .js-plotly-plot .plotly .xtick text,
#     .js-plotly-plot .plotly .ytick text,
#     .js-plotly-plot .plotly .xtitle,
#     .js-plotly-plot .plotly .ytitle,
#     .js-plotly-plot .plotly .g-xtitle text,
#     .js-plotly-plot .plotly .g-ytitle text,
#     .js-plotly-plot .plotly .gtitle,
#     .js-plotly-plot .plotly .cbaxis text,
#     .js-plotly-plot .plotly .cbtitle text,
#     .js-plotly-plot .plotly .legend text {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly bar/trace text labels (shown ON bars) — white so visible on colored bars ── */
#     .js-plotly-plot .plotly .bartext text,
#     .js-plotly-plot .plotly .bar text,
#     .js-plotly-plot .plotly g.points text,
#     .js-plotly-plot .plotly .textpoint text,
#     .js-plotly-plot .plotly .trace text {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly colorbar background ── */
#     .js-plotly-plot .plotly .cbfill,
#     .js-plotly-plot .plotly rect.cbbg {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly modebar (toolbar icons on chart hover) ── */
#     .modebar-container {
#         background: rgba(0,0,0,0.6) !important;
#         border-radius: 6px !important;
#     }
#     .modebar-btn path {
#         fill: #ffffff !important;
#     }
#     .modebar-btn:hover path {
#         fill: #ffffff !important;
#     }

#     /* ── Dataframe toolbar (download, search, fullscreen icons) ── */
#     [data-testid="stDataFrameContainer"] [data-testid="stElementToolbar"],
#     [data-testid="stElementToolbar"] {
#         background: #2e7d32 !important;
#         border-radius: 8px !important;
#         padding: 2px 4px !important;
#     }
#     [data-testid="stElementToolbar"] button,
#     [data-testid="stElementToolbar"] button svg,
#     [data-testid="stElementToolbar"] button svg path,
#     [data-testid="stElementToolbar"] button svg rect,
#     [data-testid="stElementToolbar"] button svg circle {
#         color: #ffffff !important;
#         fill: #ffffff !important;
#         stroke: #ffffff !important;
#     }
#     [data-testid="stElementToolbar"] button:hover {
#         background: #1b5e20 !important;
#         border-radius: 4px !important;
#     }

#     /* ── Divider ── */
#     hr {
#         border-color: #a5d6a7;
#         margin: 1.8rem 0;
#     }

#     /* ── Caption text ── */
#     .stCaption, [data-testid="stCaptionContainer"] {
#         color: #4a7c4a !important;
#     }

#     /* ── Feature info cards on Home page ── */
#     /* st.info / st.success / st.warning used as feature cards */
#     .element-container .stInfo,
#     .element-container .stSuccess,
#     .element-container .stWarning {
#         border-radius: 14px !important;
#     }

#     /* ── Column containers ── */
#     [data-testid="column"] {
#         padding: 0 0.4rem;
#     }

#     /* ── Header anchor links ── */
#     h2 a, h3 a { color: #2e7d32 !important; }

#     /* ── Scrollbar ── */
#     ::-webkit-scrollbar { width: 7px; height: 7px; }
#     ::-webkit-scrollbar-track { background: #e8f5e9; }
#     ::-webkit-scrollbar-thumb { background: #81c784; border-radius: 4px; }
#     ::-webkit-scrollbar-thumb:hover { background: #2e7d32; }
# </style>
# """, unsafe_allow_html=True)
 
# # =========================================================
# # ================= HEADER ================================
# # =========================================================
 
# st.markdown("""
# <div class="krishi-header">
#     <h1>🌱 Krishi AI</h1>
#     <p>AI-Powered Smart Farming Assistant — Crop Recommendation · Disease Detection · Analytics</p>
# </div>
# """, unsafe_allow_html=True)
 
# # =========================================================
# # ================= LOAD DATASET ==========================
# # =========================================================
 
# DATASET_PATH = "Krishi_ai_dataset/cleaned_crop_dataset.csv"
 
# @st.cache_data(show_spinner=False)
# def load_dataset(path):
#     if not os.path.exists(path):
#         return None
#     return pd.read_csv(path)
 
# df = load_dataset(DATASET_PATH)
 
# if df is None:
#     st.error(
#         f"❌ Dataset not found at `{DATASET_PATH}`. "
#         "Please add the CSV file and restart."
#     )
#     st.stop()
 
# # =========================================================
# # ================= FEATURE CATEGORIES ====================
# # =========================================================
 
# def nitrogen_category(n):
#     if n <= 50:         return "Low"
#     elif n <= 120:      return "Medium"
#     else:               return "High"
 
# def phosphorus_category(p):
#     if p <= 40:         return "Low"
#     elif p <= 80:       return "Medium"
#     else:               return "High"
 
# def potassium_category(k):
#     if k <= 40:         return "Low"
#     elif k <= 80:       return "Medium"
#     else:               return "High"
 
# def temperature_category(temp):
#     if temp <= 20:      return "Cool"
#     elif temp <= 30:    return "Moderate"
#     else:               return "Hot"
 
# def humidity_category(hum):
#     if hum <= 40:       return "Low"
#     elif hum <= 70:     return "Medium"
#     else:               return "High"
 
# def ph_category(ph):
#     if ph < 6:          return "Acidic"
#     elif ph <= 7.5:     return "Neutral"
#     else:               return "Alkaline"
 
# def rainfall_category(rain):
#     if rain <= 100:     return "Low"
#     elif rain <= 200:   return "Medium"
#     else:               return "High"
 
# # =========================================================
# # ================= ADD CATEGORY COLUMNS ==================
# # =========================================================
 
# @st.cache_data(show_spinner=False)
# def enrich_dataframe(dataframe):
#     df2 = dataframe.copy()
#     df2["Nitrogen_Category"]    = df2["N"].apply(nitrogen_category)
#     df2["Phosphorus_Category"]  = df2["P"].apply(phosphorus_category)
#     df2["Potassium_Category"]   = df2["K"].apply(potassium_category)
#     df2["Temperature_Category"] = df2["temperature"].apply(temperature_category)
#     df2["Humidity_Category"]    = df2["humidity"].apply(humidity_category)
#     df2["PH_Category"]          = df2["ph"].apply(ph_category)
#     df2["Rainfall_Category"]    = df2["rainfall"].apply(rainfall_category)
#     return df2
 
# df = enrich_dataframe(df)
 
# # =========================================================
# # ================= LOAD ML FILES =========================
# # =========================================================
 
# @st.cache_resource(show_spinner=False)
# def load_ml_files():
#     try:
#         ml_model      = joblib.load("crop_model.pkl")
#         ml_scaler     = joblib.load("scaler.pkl")
#         ml_encoder    = joblib.load("label_encoder.pkl")
#         return ml_model, ml_scaler, ml_encoder, None
#     except FileNotFoundError as e:
#         return None, None, None, str(e)
#     except Exception as e:
#         return None, None, None, str(e)
 
# crop_model, crop_scaler, crop_encoder, ml_error = load_ml_files()
 
# # =========================================================
# # ================= LOAD DISEASE MODEL ====================
# # =========================================================
 
# @st.cache_resource(show_spinner=False)
# def load_disease_model():
#     try:
#         from tensorflow.keras.models import load_model
#         d_model   = load_model("plant_disease_model.h5")
#         d_encoder = joblib.load("disease_label_encoder.pkl")
#         return d_model, d_encoder, None
#     except FileNotFoundError as e:
#         return None, None, str(e)
#     except Exception as e:
#         return None, None, str(e)
 
# disease_model, disease_encoder, disease_error = load_disease_model()
 
# # =========================================================
# # ================= SIDEBAR ===============================
# # =========================================================
 
# with st.sidebar:
#     st.markdown("### 🌾 Navigation")
#     page = st.selectbox(
#         "Go To",
#         ["🏠 Home", "📊 Analytics", "🤖 ML Prediction", "🌿 Disease Detection"],
#         label_visibility="collapsed"
#     )
 
#     st.markdown("---")
#     st.markdown("### 📌 Quick Info")
 
#     total_crops  = df["label"].nunique()
#     total_rows   = df.shape[0]
#     ml_status    = "✅ Loaded" if crop_model  else "❌ Not Found"
#     dis_status   = "✅ Loaded" if disease_model else "❌ Not Found"
 
#     st.markdown(f"**Dataset Crops :** {total_crops}")
#     st.markdown(f"**Dataset Rows  :** {total_rows:,}")
#     st.markdown(f"**Crop Model    :** {ml_status}")
#     st.markdown(f"**Disease Model :** {dis_status}")
#     st.markdown("---")
#     st.caption("Krishi AI v2.0 — Built with ❤️ for Farmers")
 
# # =========================================================
# # Shared constants
# # =========================================================
 
# NUMERIC_FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
# FEATURE_LABELS   = ["Nitrogen", "Phosphorus", "Potassium",
#                     "Temperature", "Humidity", "pH", "Rainfall"]
# CROPS_LIST       = sorted(df["label"].unique())
 
# @st.cache_data(show_spinner=False)
# def get_crop_stats(dataframe):
#     means = dataframe.groupby("label")[NUMERIC_FEATURES].mean()
#     norm  = (means - means.min()) / (means.max() - means.min())
#     return means, norm
 
# CROP_MEANS, CROP_NORM = get_crop_stats(df)
 
# # =========================================================
# # PAGE: HOME
# # =========================================================
 
# if page == "🏠 Home":
 
#     col_left, col_mid, col_right = st.columns([1, 2, 1])
 
#     with col_mid:
 
#         st.markdown("## 💬 Ask Your Farming Question")
#         st.caption(
#             "Get instant AI-powered advice on crops, soil, fertilizers, "
#             "weather, and more."
#         )
 
#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = []
 
#         for entry in st.session_state.chat_history:
#             if entry["role"] == "user":
#                 st.markdown(
#                     f"<div class='chat-label-user'>You</div>"
#                     f"<div class='chat-user'>{entry['text']}</div>",
#                     unsafe_allow_html=True
#                 )
#             else:
#                 st.markdown(
#                     f"<div class='chat-label-ai'>🌱 Krishi AI</div>"
#                     f"<div class='chat-ai'>{entry['text']}</div>",
#                     unsafe_allow_html=True
#                 )
 
#         user_input = st.text_input(
#             "Your question",
#             placeholder="e.g.  What crop grows best in red soil with low rainfall?",
#             label_visibility="collapsed",
#             key="home_input"
#         )
 
#         btn_col1, btn_col2 = st.columns([3, 1])
#         with btn_col1:
#             ask_clicked = st.button("🌾 Get Advice", use_container_width=True)
#         with btn_col2:
#             if st.button("🗑️ Clear", use_container_width=True):
#                 st.session_state.chat_history = []
#                 st.rerun()
 
#         if ask_clicked:
#             if not user_input.strip():
#                 st.warning("⚠️ Please type a farming question first.")
#             else:
#                 st.session_state.chat_history.append(
#                     {"role": "user", "text": user_input}
#                 )
 
#                 q = user_input.lower()
 
#                 if any(k in q for k in ["fertilizer", "npk", "nitrogen", "urea"]):
#                     reply = (
#                         "🌿 <b>Fertilizer Advice:</b><br><br>"
#                         "• <b>Nitrogen (N):</b> Use urea or ammonium nitrate for leafy growth.<br>"
#                         "• <b>Phosphorus (P):</b> DAP or SSP promotes root development.<br>"
#                         "• <b>Potassium (K):</b> MOP (muriate of potash) improves crop strength.<br><br>"
#                         "Apply based on a soil test for best results."
#                     )
#                 elif any(k in q for k in ["soil", "ph", "acidic", "alkaline"]):
#                     reply = (
#                         "🧪 <b>Soil Health Tips:</b><br><br>"
#                         "• <b>pH 6–7.5 (Neutral):</b> Ideal for most crops.<br>"
#                         "• <b>pH &lt; 6 (Acidic):</b> Add lime (calcium carbonate) to raise pH.<br>"
#                         "• <b>pH &gt; 7.5 (Alkaline):</b> Add sulfur or gypsum to lower pH.<br>"
#                         "• Get a soil test every season for accurate readings."
#                     )
#                 elif any(k in q for k in ["water", "irrigation", "rainfall", "drought"]):
#                     reply = (
#                         "💧 <b>Irrigation &amp; Water Management:</b><br><br>"
#                         "• <b>Drip irrigation</b> saves up to 60% water vs flood irrigation.<br>"
#                         "• Water crops in early morning or late evening to reduce evaporation.<br>"
#                         "• Mulching retains soil moisture and reduces weed growth.<br>"
#                         "• Drought-tolerant crops: chickpea, sorghum, moth beans."
#                     )
#                 elif any(k in q for k in ["disease", "pest", "fungus", "blight", "rust"]):
#                     reply = (
#                         "🦠 <b>Disease &amp; Pest Control:</b><br><br>"
#                         "• Use the <b>Disease Detection</b> tab to identify plant diseases from photos.<br>"
#                         "• <b>Fungal diseases:</b> Apply copper-based or systemic fungicides.<br>"
#                         "• <b>Pests:</b> Neem oil spray is an organic option; consult an agronomist.<br>"
#                         "• Rotate crops every season to break pest/disease cycles."
#                     )
#                 elif any(k in q for k in ["crop", "grow", "plant", "best crop", "which crop"]):
#                     reply = (
#                         "🌾 <b>Crop Recommendation:</b><br><br>"
#                         "Use the <b>ML Prediction</b> tab for an AI-based crop recommendation!<br><br>"
#                         "Just enter your soil nutrients (N, P, K), temperature, humidity, "
#                         "rainfall and soil pH — our trained Random Forest model will "
#                         "suggest the best crop with confidence scores."
#                     )
#                 elif any(k in q for k in ["weather", "temperature", "season", "monsoon"]):
#                     reply = (
#                         "🌤️ <b>Seasonal Farming Tips:</b><br><br>"
#                         "• <b>Kharif (June–Nov):</b> Rice, maize, cotton, soybean, groundnut.<br>"
#                         "• <b>Rabi (Nov–Apr):</b> Wheat, barley, mustard, pea, chickpea.<br>"
#                         "• <b>Zaid (Apr–Jun):</b> Watermelon, muskmelon, cucumber, moong.<br>"
#                         "• Always check local weather forecasts before sowing."
#                     )
#                 elif any(k in q for k in ["hello", "hi", "hey", "namaste"]):
#                     reply = (
#                         "🙏 <b>Namaste! Welcome to Krishi AI.</b><br><br>"
#                         "I can help you with:<br>"
#                         "• 🌾 Which crop to grow based on your soil conditions<br>"
#                         "• 🧪 Soil health and fertilizer advice<br>"
#                         "• 💧 Irrigation and water management<br>"
#                         "• 🌿 Plant disease identification<br><br>"
#                         "Ask me anything about farming!"
#                     )
#                 else:
#                     reply = (
#                         "🤖 <b>Krishi AI Response:</b><br><br>"
#                         f"Your question: <i>\"{user_input}\"</i><br><br>"
#                         "I recommend using our AI tools:<br>"
#                         "• 📊 <b>Analytics</b> — explore crop data &amp; trends<br>"
#                         "• 🤖 <b>ML Prediction</b> — get the best crop recommendation for your soil<br>"
#                         "• 🌿 <b>Disease Detection</b> — upload a leaf photo to detect disease<br><br>"
#                         "For detailed guidance, consult your local KVK (Krishi Vigyan Kendra)."
#                     )
 
#                 st.session_state.chat_history.append(
#                     {"role": "ai", "text": reply}
#                 )
#                 st.rerun()
 
#     st.markdown("---")
 
#     st.markdown("### 🚀 What Krishi AI Can Do For You")
#     c1, c2, c3 = st.columns(3)
 
#     with c1:
#         st.info(
#             "### 📊 Smart Analytics\n"
#             "Explore 24+ charts and insights about crops, soil nutrients, "
#             "rainfall, temperature, and more."
#         )
#     with c2:
#         st.success(
#             "### 🤖 Crop Prediction\n"
#             "Enter your soil and weather data to get an ML-powered crop "
#             "recommendation with confidence scores."
#         )
#     with c3:
#         st.warning(
#             "### 🌿 Disease Detection\n"
#             "Upload a leaf image and our CNN model will identify plant "
#             "diseases and suggest treatment in seconds."
#         )
 
# # =========================================================
# # PAGE: ANALYTICS
# # =========================================================
 
# elif page == "📊 Analytics":
 
#     st.header("📊 Krishi Data Analytics Dashboard")
 
#     st.subheader("📁 Dataset Overview")
#     c1, c2, c3, c4, c5 = st.columns(5)
#     c1.metric("Total Rows",      f"{df.shape[0]:,}")
#     c2.metric("Total Columns",   df.shape[1])
#     c3.metric("Unique Crops",    df["label"].nunique())
#     c4.metric("Duplicate Rows",  int(df.duplicated().sum()))
#     c5.metric("Missing Values",  int(df.isnull().sum().sum()))
#     st.markdown("---")
 
#     st.subheader("🔬 Data Quality Check")
#     q1, q2 = st.columns(2)
#     with q1:
#         st.write("#### Data Types")
#         dtype_df = df.dtypes.reset_index()
#         dtype_df.columns = ["Feature", "Type"]
#         dtype_df["Type"] = dtype_df["Type"].astype(str)
#         st.dataframe(dtype_df, use_container_width=True)
#     with q2:
#         st.write("#### Missing Values")
#         mv = df.isnull().sum().reset_index()
#         mv.columns = ["Feature", "Missing"]
#         st.dataframe(mv, use_container_width=True)
#         if mv["Missing"].sum() == 0:
#             st.success("✅ No missing values!")
#         if df.duplicated().sum() == 0:
#             st.success("✅ No duplicate rows!")
#     st.markdown("---")
 
#     st.subheader("🔍 Dataset Preview")
#     st.dataframe(df.head(50), use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("📈 Statistical Summary")
#     st.dataframe(df.describe().round(2), use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("🌾 Crop Distribution")
#     crop_count = df["label"].value_counts().reset_index()
#     crop_count.columns = ["Crop", "Count"]
 
#     d1, d2 = st.columns(2)
#     with d1:
#         fig = px.bar(crop_count, x="Crop", y="Count",
#                      color="Count", color_continuous_scale="Greens",
#                      text="Count", title="Crop Count")
#         fig.update_traces(textposition="outside", textfont_color="#ffffff")
#         fig.update_layout(xaxis_tickangle=-45, showlegend=False, height=380)
#         fig.update_coloraxes(colorbar=dict(
#             bgcolor="#ffffff", tickfont=dict(color="#ffffff", size=12),
#             tickcolor="#ffffff", title=dict(font=dict(color="#ffffff", size=13)),
#             outlinecolor="#c8e6c9", outlinewidth=1,
#         ))
#         st.plotly_chart(fig, use_container_width=True)
#     with d2:
#         fig2 = px.pie(crop_count, names="Crop", values="Count",
#                       title="Crop Share",
#                       color_discrete_sequence=px.colors.sequential.Greens_r)
#         fig2.update_traces(textposition="inside", textinfo="percent+label")
#         fig2.update_layout()
#         st.plotly_chart(fig2, use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("📊 Feature Category Analysis")
#     cat_cols = [
#         ("Nitrogen_Category", "Nitrogen"),
#         ("Phosphorus_Category", "Phosphorus"),
#         ("Potassium_Category", "Potassium"),
#         ("Temperature_Category", "Temperature"),
#         ("Humidity_Category", "Humidity"),
#         ("PH_Category", "Soil pH"),
#         ("Rainfall_Category", "Rainfall"),
#     ]
#     ca1, ca2 = st.columns(2)
#     for i, (col_name, title) in enumerate(cat_cols):
#         counts = df[col_name].value_counts().reset_index()
#         counts.columns = ["Category", "Count"]
#         fig = px.pie(counts, names="Category", values="Count",
#                      title=f"{title} Distribution", hole=0.4,
#                      color_discrete_sequence=px.colors.qualitative.Set2)
#         fig.update_traces(textinfo="percent+label")
#         fig.update_layout()
#         (ca1 if i % 2 == 0 else ca2).plotly_chart(fig, use_container_width=True)
#     st.markdown("---")
 
#     def climate_bar(feature, label, color_scale, unit=""):
#         grp = df.groupby("label")[feature].mean().round(2).reset_index()
#         grp.columns = ["Crop", label]
#         grp = grp.sort_values(label, ascending=True)
#         fig = px.bar(grp, x=label, y="Crop", orientation="h",
#                      title=f"Average {label} per Crop",
#                      color=label, color_continuous_scale=color_scale,
#                      text=label)
#         fig.update_traces(textposition="outside", textfont_color="#ffffff")
#         fig.update_layout(height=580, yaxis_title="")
#         fig.update_coloraxes(colorbar=dict(
#             bgcolor="#ffffff", tickfont=dict(color="#ffffff", size=12),
#             tickcolor="#ffffff", title=dict(font=dict(color="#ffffff", size=13)),
#             outlinecolor="#c8e6c9", outlinewidth=1,
#         ))
#         return fig, grp
 
#     for feat, lbl, scale in [
#         ("temperature", "Avg Temperature (°C)", "RdYlGn_r"),
#         ("rainfall",    "Avg Rainfall (mm)",    "Blues"),
#         ("humidity",    "Avg Humidity (%)",      "Teal"),
#         ("ph",          "Avg pH",               "RdYlGn"),
#     ]:
#         icon = '🌡' if 'Temp' in lbl else '🌧' if 'Rain' in lbl else '💧' if 'Hum' in lbl else '🧪'
#         st.subheader(f"{icon} {lbl}")
#         fig, grp = climate_bar(feat, lbl, scale)
#         st.plotly_chart(fig, use_container_width=True)
#         t1, t2 = st.columns(2)
#         with t1:
#             st.write("**Top 5 (Highest)**")
#             st.dataframe(grp.tail(5)[::-1].reset_index(drop=True), use_container_width=True)
#         with t2:
#             st.write("**Bottom 5 (Lowest)**")
#             st.dataframe(grp.head(5).reset_index(drop=True), use_container_width=True)
#         st.markdown("---")
 
#     st.subheader("🪴 NPK Analysis")
#     avg_npk = df.groupby("label")[["N","P","K"]].mean().round(2).reset_index()
#     npk_m   = avg_npk.melt(id_vars="label", value_vars=["N","P","K"],
#                             var_name="Nutrient", value_name="Value")
#     cmap = {"N": "#2ca02c", "P": "#ff7f0e", "K": "#1f77b4"}
 
#     for mode, title in [("group","Grouped"), ("stack","Stacked — shows proportion")]:
#         fig = px.bar(npk_m, x="label", y="Value", color="Nutrient",
#                      barmode=mode, title=f"N, P, K per Crop ({title})",
#                      color_discrete_map=cmap,
#                      labels={"label":"Crop","Value":"mg/kg"})
#         fig.update_layout(xaxis_tickangle=-45, height=420)
#         st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(avg_npk.set_index("label"), use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("🧪 Soil Health Analysis")
#     c1,c2,c3 = st.columns(3)
#     c1.metric("Avg Nitrogen",   round(df["N"].mean(),2))
#     c2.metric("Avg Phosphorus", round(df["P"].mean(),2))
#     c3.metric("Avg Potassium",  round(df["K"].mean(),2))
 
#     soil = df.groupby("label")[["N","P","K"]].mean()
#     soil["Score"] = soil.mean(axis=1).round(2)
#     soil = soil.reset_index().sort_values("Score", ascending=False)
#     avg_s = soil["Score"].mean()
 
#     fig = px.bar(soil, x="label", y="Score", color="Score",
#                  color_continuous_scale="YlGn", text="Score",
#                  title="Soil Health Score (avg of N+P+K)")
#     fig.add_hline(y=avg_s, line_dash="dash", line_color="red",
#                   annotation_text=f"Avg: {avg_s:.1f}")
#     fig.update_traces(textposition="outside", textfont_color="#ffffff")
#     fig.update_layout(xaxis_tickangle=-45, height=420)
#     fig.update_coloraxes(
#         colorbar=dict(
#             bgcolor="#ffffff",
#             tickfont=dict(color="#ffffff", size=12),
#             tickcolor="#ffffff",
#             title=dict(font=dict(color="#ffffff", size=13)),
#             outlinecolor="#c8e6c9",
#             outlinewidth=1,
#         )
#     )
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("⚠️ Nutrient Deficiency Flag")
#     npk_flag = df.groupby("label")[["N","P","K"]].mean().round(2).reset_index()
#     npk_flag["N_Flag"] = npk_flag["N"].apply(lambda x: "⚠️ Low" if x<=50 else "✅ OK")
#     npk_flag["P_Flag"] = npk_flag["P"].apply(lambda x: "⚠️ Low" if x<=40 else "✅ OK")
#     npk_flag["K_Flag"] = npk_flag["K"].apply(lambda x: "⚠️ Low" if x<=40 else "✅ OK")
#     npk_flag["Status"] = npk_flag[["N_Flag","P_Flag","K_Flag"]].apply(
#         lambda r: "⚠️ Deficient" if "⚠️ Low" in r.values else "✅ Sufficient", axis=1)
#     deficient = npk_flag[npk_flag["Status"]=="⚠️ Deficient"]
#     if len(deficient):
#         st.warning(f"⚠️ {len(deficient)} crops have a nutrient in the Low range.")
#         st.dataframe(deficient[["label","N","N_Flag","P","P_Flag","K","K_Flag"]],
#                      use_container_width=True)
#     else:
#         st.success("✅ All crops have sufficient average NPK levels.")
#     st.markdown("---")
 
#     st.subheader("📏 Feature Range per Crop")
#     sel_feat = st.selectbox("Select Feature", NUMERIC_FEATURES, key="range_sel")
#     range_df = (df.groupby("label")[sel_feat]
#                 .agg(["min","max","mean","std"]).round(2).reset_index())
#     range_df.columns = ["Crop","Min","Max","Mean","Std Dev"]
#     range_df = range_df.sort_values("Mean", ascending=False)
#     fig = go.Figure(go.Bar(
#         x=range_df["Crop"], y=range_df["Mean"], name="Mean",
#         marker_color="#2ca02c",
#         error_y=dict(type="data", array=range_df["Std Dev"], visible=True),
#         text=range_df["Mean"], textposition="outside"
#     ))
#     fig.update_layout(title=f"{sel_feat} — Mean ± Std Dev",
#                       xaxis_tickangle=-45, height=440)
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(range_df.set_index("Crop"), use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("🔵 Scatter Plot Analysis")
#     scatter_pairs = [
#         ("rainfall","humidity","Rainfall vs Humidity"),
#         ("temperature","ph","Temperature vs Soil pH"),
#         ("N","K","Nitrogen vs Potassium"),
#         ("temperature","rainfall","Temperature vs Rainfall"),
#     ]
#     s1, s2 = st.columns(2)
#     for i, (x, y, title) in enumerate(scatter_pairs):
#         fig = px.scatter(df, x=x, y=y, color="label",
#                          hover_name="label", title=title, opacity=0.6)
#         fig.update_layout(height=420, showlegend=False)
#         (s1 if i % 2 == 0 else s2).plotly_chart(fig, use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("📦 Feature Distribution (Box Plot)")
#     box_sel = st.selectbox("Select Feature", NUMERIC_FEATURES, key="box_sel")
#     fig = px.box(df, x="label", y=box_sel, color="label",
#                  title=f"{box_sel} Distribution by Crop",
#                  color_discrete_sequence=px.colors.qualitative.Pastel)
#     fig.update_layout(xaxis_tickangle=-45, height=500, showlegend=False)
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("📋 Complete Crop Profile")
#     full_prof = df.groupby("label")[NUMERIC_FEATURES].mean().round(2)
#     full_prof.columns = ["N (mg/kg)","P (mg/kg)","K (mg/kg)",
#                          "Temp (°C)","Humidity (%)","pH","Rainfall (mm)"]
#     st.dataframe(full_prof.style.background_gradient(cmap="YlGn", axis=0),
#                  use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("⚖️ Crop-to-Crop Comparison")
#     cc1, cc2 = st.columns(2)
#     crop_a = cc1.selectbox("Crop A", CROPS_LIST, index=0, key="ca")
#     crop_b = cc2.selectbox("Crop B", CROPS_LIST, index=1, key="cb")
 
#     a_v = df[df["label"]==crop_a][NUMERIC_FEATURES].mean().round(2)
#     b_v = df[df["label"]==crop_b][NUMERIC_FEATURES].mean().round(2)
 
#     fig = go.Figure([
#         go.Bar(name=crop_a, x=FEATURE_LABELS, y=a_v.values,
#                marker_color="#2ca02c", text=a_v.values, textposition="outside"),
#         go.Bar(name=crop_b, x=FEATURE_LABELS, y=b_v.values,
#                marker_color="#1f77b4", text=b_v.values, textposition="outside"),
#     ])
#     fig.update_layout(barmode="group",
#                       title=f"{crop_a} vs {crop_b}", height=400)
#     st.plotly_chart(fig, use_container_width=True)
 
#     a_n = CROP_NORM.loc[crop_a].values.tolist()
#     b_n = CROP_NORM.loc[crop_b].values.tolist()
#     fig2 = go.Figure([
#         go.Scatterpolar(r=a_n+[a_n[0]], theta=NUMERIC_FEATURES+[NUMERIC_FEATURES[0]],
#                         fill="toself", name=crop_a,
#                         line_color="#2ca02c", fillcolor="rgba(44,160,44,0.15)"),
#         go.Scatterpolar(r=b_n+[b_n[0]], theta=NUMERIC_FEATURES+[NUMERIC_FEATURES[0]],
#                         fill="toself", name=crop_b,
#                         line_color="#1f77b4", fillcolor="rgba(31,119,180,0.15)"),
#     ])
#     fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])),
#                        title=f"Radar: {crop_a} vs {crop_b} (Normalized 0–1)", height=460)
#     st.plotly_chart(fig2, use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("🔍 Similar Crops Finder")
#     target = st.selectbox("Select a Crop", CROPS_LIST, key="sim")
#     vec    = CROP_NORM.loc[target]
#     dists  = CROP_NORM.drop(target).apply(
#         lambda r: np.sqrt(((r - vec)**2).sum()), axis=1)
#     top3 = dists.nsmallest(3).reset_index()
#     top3.columns = ["Similar Crop","Distance (lower=closer)"]
#     top3["Distance (lower=closer)"] = top3["Distance (lower=closer)"].round(4)
#     st.write(f"**Top 3 crops most similar to {target}:**")
#     st.dataframe(top3, use_container_width=True)
#     sim_names   = top3["Similar Crop"].tolist()
#     sim_profile = CROP_MEANS.loc[[target]+sim_names].round(2)
#     st.dataframe(sim_profile.style.background_gradient(cmap="Greens", axis=0),
#                  use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("🔍 Crop Filter")
#     sel_crop  = st.selectbox("Select Crop", CROPS_LIST, key="filter")
#     crop_data = df[df["label"]==sel_crop]
#     m1,m2,m3,m4 = st.columns(4)
#     m1.metric("Avg Temp",     f"{crop_data['temperature'].mean():.1f} °C")
#     m2.metric("Avg Humidity", f"{crop_data['humidity'].mean():.1f} %")
#     m3.metric("Avg Rainfall", f"{crop_data['rainfall'].mean():.1f} mm")
#     m4.metric("Avg pH",       f"{crop_data['ph'].mean():.2f}")
#     n1,n2,n3 = st.columns(3)
#     n1.metric("Avg Nitrogen",   round(crop_data["N"].mean(),2))
#     n2.metric("Avg Phosphorus", round(crop_data["P"].mean(),2))
#     n3.metric("Avg Potassium",  round(crop_data["K"].mean(),2))
#     st.dataframe(crop_data, use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("🔗 Feature Correlation Matrix")
#     corr = df[NUMERIC_FEATURES].corr().round(3)
#     fig  = px.imshow(corr, text_auto=True, color_continuous_scale="RdYlGn",
#                      zmin=-1, zmax=1, title="Feature Correlation Heatmap")
#     fig.update_layout(height=480)
#     fig.update_coloraxes(
#         colorbar=dict(
#             bgcolor="#ffffff",
#             tickfont=dict(color="#ffffff", size=12),
#             tickcolor="#ffffff",
#             title=dict(font=dict(color="#ffffff", size=13)),
#             outlinecolor="#c8e6c9",
#             outlinewidth=1,
#         )
#     )
#     st.plotly_chart(fig, use_container_width=True)
#     st.caption("🟢 Green = positive | 🔴 Red = negative | ⚪ White = no correlation")
 
#     pairs = corr.unstack().reset_index()
#     pairs.columns = ["Feature A","Feature B","Correlation"]
#     pairs = pairs[pairs["Feature A"] < pairs["Feature B"]]
#     pairs["Abs"] = pairs["Correlation"].abs()
#     pairs = pairs.sort_values("Abs", ascending=False).drop(columns="Abs")
#     pc1, pc2 = st.columns(2)
#     with pc1:
#         st.write("**Top 3 Positive**")
#         st.dataframe(pairs[pairs["Correlation"]>0].head(3).reset_index(drop=True),
#                      use_container_width=True)
#     with pc2:
#         st.write("**Top 3 Negative**")
#         st.dataframe(pairs[pairs["Correlation"]<0].head(3).reset_index(drop=True),
#                      use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("📘 Feature Meaning")
#     feat_info = pd.DataFrame({
#         "Feature": ["N","P","K","temperature","humidity","ph","rainfall"],
#         "Meaning": [
#             "Nitrogen — leaf and stem growth",
#             "Phosphorus — root and flower growth",
#             "Potassium — plant strength and disease resistance",
#             "Temperature — optimal growing temperature",
#             "Humidity — moisture level in the air",
#             "Soil pH — acidity or alkalinity",
#             "Rainfall — water requirement"
#         ],
#         "Unit": ["mg/kg","mg/kg","mg/kg","°C","%","0–14","mm"]
#     })
#     st.dataframe(feat_info, use_container_width=True)
#     st.markdown("---")
 
#     st.subheader("🌱 Farmer Understanding Guide")
#     g1, g2 = st.columns(2)
#     with g1:
#         st.success("🟢 **Low Nitrogen (≤50)** → Light fertilizer needed")
#         st.info("🔵 **Medium Nitrogen (51–120)** → Balanced fertilizer")
#         st.warning("🟡 **High Nitrogen (>120)** → Heavy fertilizer needed")
#         st.success("🟢 **Cool (≤20°C)** → Wheat, lentil, chickpea")
#         st.info("🔵 **Moderate (21–30°C)** → Most common crops")
#         st.warning("🟡 **Hot (>30°C)** → Tropical/summer crops")
#     with g2:
#         st.success("🟢 **Acidic (pH<6)** → Tea, rice, blueberry")
#         st.info("🔵 **Neutral (pH 6–7.5)** → Best for most crops")
#         st.warning("🟡 **Alkaline (pH>7.5)** → Cotton, maize")
#         st.success("🟢 **Low Rainfall (≤100mm)** → Drought-tolerant crops")
#         st.info("🔵 **Medium Rainfall (101–200mm)** → General crops")
#         st.warning("🟡 **High Rainfall (>200mm)** → Water-intensive crops")
#     st.markdown("---")
 
#     st.subheader("📌 Key Insights")
#     st.success("✅ Dataset is balanced with nearly equal crop distribution.")
#     st.success("✅ No missing values or duplicate rows found.")
#     st.success("✅ Dataset is clean and ready for ML model training.")
#     st.info("📊 Rainfall, temperature, humidity and soil nutrients drive crop suitability.")
#     st.info("🌱 Rice and jute need high humidity & rainfall; chickpea and kidney beans prefer dry conditions.")
#     st.info("🧪 Use Scatter and Box Plots to identify natural clusters for ML feature selection.")
#     st.info("⚖️ Use Crop Comparison and Similar Crops to help farmers choose alternative crops.")
 
# # =========================================================
# # PAGE: ML PREDICTION
# # =========================================================
 
# elif page == "🤖 ML Prediction":
 
#     st.header("🤖 AI-Powered Crop Recommendation")
#     st.markdown("---")
 
#     if ml_error:
#         st.error(
#             f"❌ Could not load ML model files.\n\n"
#             f"**Error:** `{ml_error}`\n\n"
#             "Please make sure `crop_model.pkl`, `scaler.pkl`, and "
#             "`label_encoder.pkl` are in the same folder as `app.py`."
#         )
#         st.stop()
 
#     if hasattr(crop_model, "feature_importances_"):
#         st.subheader("📈 Model Feature Importance")
#         imp_df = pd.DataFrame({
#             "Feature":    FEATURE_LABELS,
#             "Importance": crop_model.feature_importances_
#         }).sort_values("Importance", ascending=False)
 
#         fig = px.bar(imp_df, x="Feature", y="Importance",
#                      color="Importance", color_continuous_scale="Teal",
#                      text=imp_df["Importance"].round(3),
#                      title="Feature Importance (Higher = More Influential)")
#         fig.update_traces(textposition="outside", textfont_color="#ffffff")
#         fig.update_layout(height=380)
#         fig.update_coloraxes(colorbar=dict(
#             bgcolor="#ffffff", tickfont=dict(color="#ffffff", size=12),
#             tickcolor="#ffffff", title=dict(font=dict(color="#ffffff", size=13)),
#             outlinecolor="#c8e6c9", outlinewidth=1,
#         ))
#         st.plotly_chart(fig, use_container_width=True)
#         st.info(
#             f"🔑 Most influential: **{imp_df.iloc[0]['Feature']}**  |  "
#             f"📉 Least influential: **{imp_df.iloc[-1]['Feature']}**"
#         )
#         st.markdown("---")
 
#     st.subheader("🌱 Enter Your Soil and Weather Conditions")
 
#     sl1, sl2 = st.columns(2)
 
#     with sl1:
#         N = st.slider("Nitrogen (N) mg/kg",
#                       int(df["N"].min()), int(df["N"].max()), int(df["N"].mean()))
#         P = st.slider("Phosphorus (P) mg/kg",
#                       int(df["P"].min()), int(df["P"].max()), int(df["P"].mean()))
#         K = st.slider("Potassium (K) mg/kg",
#                       int(df["K"].min()), int(df["K"].max()), int(df["K"].mean()))
#         temperature = st.slider("Temperature (°C)",
#                                 float(df["temperature"].min()),
#                                 float(df["temperature"].max()),
#                                 round(float(df["temperature"].mean()),1))
#     with sl2:
#         humidity = st.slider("Humidity (%)",
#                              float(df["humidity"].min()),
#                              float(df["humidity"].max()),
#                              round(float(df["humidity"].mean()),1))
#         ph = st.slider("Soil pH",
#                        float(df["ph"].min()), float(df["ph"].max()),
#                        round(float(df["ph"].mean()),1))
#         rainfall = st.slider("Rainfall (mm)",
#                              float(df["rainfall"].min()),
#                              float(df["rainfall"].max()),
#                              round(float(df["rainfall"].mean()),1))
 
#     st.markdown("---")
#     st.subheader("📊 Real-Time Input Analysis")
#     ia1, ia2, ia3, ia4 = st.columns(4)
#     ia1.info(f"🌿 N: **{nitrogen_category(N)}**\n\n💧 Humidity: **{humidity_category(humidity)}**")
#     ia2.info(f"🌿 P: **{phosphorus_category(P)}**\n\n🧪 Soil pH: **{ph_category(ph)}**")
#     ia3.info(f"🌿 K: **{potassium_category(K)}**\n\n🌧 Rainfall: **{rainfall_category(rainfall)}**")
#     ia4.info(f"🌡 Temp: **{temperature_category(temperature)}**")
 
#     st.markdown("---")
 
#     if st.button("🌾 Predict Best Crop", use_container_width=True):
#         try:
#             inp        = [[N, P, K, temperature, humidity, ph, rainfall]]
#             scaled     = crop_scaler.transform(inp)
#             prediction = crop_model.predict(scaled)
#             pred_crop  = crop_encoder.inverse_transform(prediction)[0]
 
#             st.success(f"✅ Recommended Crop: **{pred_crop.upper()}**")
#             st.markdown("---")
 
#             if hasattr(crop_model, "predict_proba"):
#                 st.subheader("📊 Top 5 Crop Predictions")
#                 proba  = crop_model.predict_proba(scaled)[0]
#                 prob_df = pd.DataFrame({
#                     "Crop":        crop_encoder.classes_,
#                     "Probability": proba
#                 }).sort_values("Probability", ascending=False).head(5)
#                 prob_df["Pct"] = (prob_df["Probability"]*100).round(2)
 
#                 fig = px.bar(prob_df, x="Crop", y="Probability",
#                              color="Probability",
#                              text=prob_df["Pct"].astype(str)+"%",
#                              color_continuous_scale="Greens",
#                              title="Prediction Confidence (Top 5)")
#                 fig.update_traces(textposition="outside", textfont_color="#000000")
#                 fig.update_layout(height=420)
#                 fig.update_coloraxes(colorbar=dict(
#                     bgcolor="#ffffff", tickfont=dict(color="#ffffff", size=12),
#                     tickcolor="#ffffff", title=dict(font=dict(color="#ffffff", size=13)),
#                     outlinecolor="#c8e6c9", outlinewidth=1,
#                 ))
#                 st.plotly_chart(fig, use_container_width=True)
 
#                 top_pct = prob_df.iloc[0]["Pct"]
#                 if top_pct >= 80:
#                     st.success(f"🎯 High confidence: {top_pct}%")
#                 elif top_pct >= 50:
#                     st.info(f"🔍 Moderate confidence: {top_pct}% — verify with local conditions.")
#                 else:
#                     st.warning(f"⚠️ Low confidence: {top_pct}% — consult an agronomist.")
#                 st.markdown("---")
 
#             st.subheader(f"📐 Your Conditions vs Ideal for {pred_crop.capitalize()}")
#             ideal = df[df["label"]==pred_crop][NUMERIC_FEATURES].mean().round(2)
#             user_vals = [N, P, K, temperature, humidity, ph, rainfall]
 
#             fig = go.Figure([
#                 go.Bar(name="Your Input", x=FEATURE_LABELS, y=user_vals,
#                        marker_color="#1f77b4",
#                        text=[round(v,2) for v in user_vals], textposition="outside"),
#                 go.Bar(name=f"Ideal for {pred_crop}", x=FEATURE_LABELS,
#                        y=ideal.values, marker_color="#2ca02c",
#                        text=ideal.values, textposition="outside"),
#             ])
#             fig.update_layout(barmode="group",
#                               title=f"Your Input vs Ideal: {pred_crop}",
#                               height=400)
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown("---")
 
#             st.subheader("📋 Input Summary")
#             summ = pd.DataFrame({
#                 "Feature": ["Nitrogen (mg/kg)","Phosphorus (mg/kg)","Potassium (mg/kg)",
#                             "Temperature (°C)","Humidity (%)","Soil pH","Rainfall (mm)"],
#                 "Value":    [N, P, K, temperature, humidity, ph, rainfall],
#                 "Category": [nitrogen_category(N), phosphorus_category(P),
#                              potassium_category(K), temperature_category(temperature),
#                              humidity_category(humidity), ph_category(ph),
#                              rainfall_category(rainfall)]
#             })
#             st.dataframe(summ, use_container_width=True)
#             st.markdown("---")
 
#             st.subheader("🌱 Crop Advice")
#             crop_advice = {
#                 "rice":        "Requires high rainfall (150–300mm), high humidity (80–90%), and slightly acidic soil (pH 5.5–6.5).",
#                 "maize":       "Needs moderate rainfall, moderate temperature (21–27°C), and fertile loamy soil (pH 5.5–7.0).",
#                 "jute":        "Thrives in high humidity and rainfall. Requires warm climate (25–35°C) and alluvial soil.",
#                 "cotton":      "Grows well in well-drained black soil (pH 6–8), warm climate (21–35°C), and moderate rainfall.",
#                 "coconut":     "Requires tropical climate, high humidity (70–80%), and sandy loam soil.",
#                 "papaya":      "Needs warm climate (25–30°C), well-drained soil, moderate rainfall, and high humidity.",
#                 "banana":      "Requires rich loamy soil, high humidity, warm temperature (26–30°C), and regular rainfall.",
#                 "mango":       "Prefers deep well-drained soil, dry season at flowering, and tropical/subtropical climate.",
#                 "grapes":      "Needs well-drained sandy loam, dry hot summers and cool winters.",
#                 "watermelon":  "Requires warm climate (25–35°C), sandy loam soil, and moderate to high rainfall.",
#                 "muskmelon":   "Grows best in warm climate, sandy soil with good drainage, and moderate humidity.",
#                 "apple":       "Requires cool climate (cold winters for dormancy), loamy soil, and moderate rainfall.",
#                 "orange":      "Needs subtropical climate, well-drained sandy loam, and moderate rainfall (750–1200mm).",
#                 "pomegranate": "Drought-tolerant, wide pH range (5.5–7.5), grows well in semi-arid regions.",
#                 "lentil":      "Cool season crop, well-drained loamy soil (pH 6–8), low rainfall.",
#                 "blackgram":   "Warm climate (25–35°C), well-drained loamy soil, moderate rainfall (600–800mm).",
#                 "mungbean":    "Warm season, sandy loam soil, short rainfall period, moderate temperature (28–30°C).",
#                 "mothbeans":   "Drought-tolerant, arid/semi-arid regions, sandy soil, very low rainfall.",
#                 "pigeonpeas":  "Drought-tolerant legume, well-drained soil (pH 5–7), moderate rainfall.",
#                 "kidneybeans": "Cool temperature, well-drained fertile loam (pH 6–7), moderate rainfall.",
#                 "chickpea":    "Cool season, drought-tolerant, loamy soil (pH 5.5–7), low rainfall.",
#                 "coffee":      "Tropical climate (15–28°C), high humidity, acidic well-drained soil (pH 6–6.5), high rainfall."
#             }
#             advice = crop_advice.get(
#                 pred_crop.lower(),
#                 f"{pred_crop.capitalize()} is suited to the conditions you entered. "
#                 "Consult local agricultural guidelines for detailed advice."
#             )
#             st.info(f"🌿 **{pred_crop.capitalize()} Advice:** {advice}")
#             st.markdown("---")
 
#             st.subheader("🧪 Soil & Climate Summary")
#             sc1, sc2 = st.columns(2)
#             with sc1:
#                 if ph < 6:
#                     st.warning("⚠️ **Acidic Soil** — add lime to raise pH.")
#                 elif ph > 7.5:
#                     st.warning("⚠️ **Alkaline Soil** — add sulfur to lower pH.")
#                 else:
#                     st.success("✅ **Neutral Soil pH** — ideal for most crops.")
#                 n_cat = nitrogen_category(N)
#                 if n_cat == "Low":
#                     st.warning("⚠️ Low Nitrogen — apply urea or nitrogen-rich fertilizer.")
#                 elif n_cat == "High":
#                     st.info("ℹ️ High Nitrogen — reduce fertilizer application.")
#                 else:
#                     st.success("✅ Nitrogen level is balanced.")
#             with sc2:
#                 if rainfall > 200:
#                     st.info("🌧 High rainfall — ensure good field drainage.")
#                 elif rainfall < 80:
#                     st.info("☀️ Low rainfall — consider drip irrigation.")
#                 else:
#                     st.success("✅ Moderate rainfall — suitable for most crops.")
#                 t_cat = temperature_category(temperature)
#                 if t_cat == "Cool":
#                     st.info("❄️ Cool climate — suitable for wheat, lentil, chickpea.")
#                 elif t_cat == "Hot":
#                     st.info("🔥 Hot climate — suitable for tropical/summer crops.")
#                 else:
#                     st.success("✅ Moderate temperature — good for most crops.")
 
#         except Exception as e:
#             st.error(f"❌ Prediction failed: `{str(e)}`")
 
# # =========================================================
# # PAGE: DISEASE DETECTION
# # =========================================================
 
# elif page == "🌿 Disease Detection":
 
#     st.header("🌿 Plant Disease Detection System")
#     st.markdown("---")
 
#     if disease_error:
#         st.error(
#             f"❌ Disease model not found.\n\n"
#             f"**Error:** `{disease_error}`\n\n"
#             "Run `train_disease_model.py` first to train and save the model, "
#             "then restart the app."
#         )
#         st.stop()
 
#     st.subheader("📤 Upload a Plant Leaf Image")
#     st.caption(
#         "Upload a clear photo of a plant leaf. "
#         "The AI will predict whether it is healthy or diseased."
#     )
 
#     uploaded = st.file_uploader(
#         "Drag & drop or click to browse",
#         type=["jpg","jpeg","png","webp"],
#         label_visibility="collapsed"
#     )
 
#     if uploaded is not None:
 
#         image = Image.open(uploaded).convert("RGB")
 
#         col_img, col_res = st.columns([1, 1])
 
#         with col_img:
#             st.image(image, caption="Uploaded Leaf Image", use_column_width=True)
 
#         img_resized = image.resize((128, 128))
#         img_array   = np.array(img_resized, dtype="float32") / 255.0
#         img_array   = np.expand_dims(img_array, axis=0)
 
#         try:
#             preds         = disease_model.predict(img_array, verbose=0)
#             pred_idx      = int(np.argmax(preds))
#             disease_name  = disease_encoder.inverse_transform([pred_idx])[0]
#             confidence    = float(np.max(preds)) * 100
#             all_probs     = preds[0]
 
#             with col_res:
#                 st.markdown('<div class="disease-card">', unsafe_allow_html=True)
 
#                 if confidence >= 75:
#                     st.success(f"✅ **Predicted:** {disease_name.replace('_', ' ')}")
#                 elif confidence >= 50:
#                     st.warning(f"⚠️ **Predicted (Moderate Confidence):** {disease_name.replace('_', ' ')}")
#                 else:
#                     st.error(f"❓ **Low Confidence Prediction:** {disease_name.replace('_', ' ')}")
 
#                 st.metric("Confidence", f"{confidence:.2f}%")
#                 st.progress(int(min(confidence, 100)))
 
#                 is_healthy = "healthy" in disease_name.lower()
#                 if is_healthy:
#                     st.success("🌿 Your plant appears **HEALTHY**!")
#                 else:
#                     st.error("🦠 Disease detected — see treatment advice below.")
 
#                 st.markdown('</div>', unsafe_allow_html=True)
 
#             st.markdown("---")
 
#             st.subheader("💊 Treatment & Care Advice")
 
#             disease_advice = {
#                 "Tomato_healthy":
#                     ("✅ Healthy Plant", "success",
#                      "Maintain regular watering (avoid overhead irrigation), "
#                      "balanced fertilization, and good air circulation."),
#                 "Tomato_Early_blight":
#                     ("⚠️ Early Blight (Alternaria solani)", "warning",
#                      "Remove infected lower leaves immediately. Apply **mancozeb** "
#                      "or **chlorothalonil** fungicide every 7–10 days. Avoid overhead "
#                      "watering and ensure good air flow around plants."),
#                 "Tomato_Late_blight":
#                     ("🚨 Late Blight (Phytophthora infestans)", "error",
#                      "Act fast — this spreads rapidly. Remove and destroy infected "
#                      "plants. Apply **copper-based fungicide** or **metalaxyl**. "
#                      "Avoid watering leaves; water at the base."),
#                 "Tomato_Leaf_Mold":
#                     ("⚠️ Leaf Mold (Passalora fulva)", "warning",
#                      "Improve greenhouse/field air circulation. Reduce humidity. "
#                      "Apply **copper** or **sulfur-based fungicide**. Remove affected leaves."),
#                 "Tomato_Septoria_leaf_spot":
#                     ("⚠️ Septoria Leaf Spot", "warning",
#                      "Remove infected leaves. Apply **mancozeb** fungicide. "
#                      "Rotate crops and avoid overhead irrigation."),
#                 "Tomato_Spider_mites":
#                     ("⚠️ Spider Mites", "warning",
#                      "Spray plants with water to dislodge mites. "
#                      "Apply **neem oil** or **insecticidal soap**. "
#                      "Introduce predatory mites as biological control."),
#                 "Tomato_Target_Spot":
#                     ("⚠️ Target Spot", "warning",
#                      "Remove infected leaves. Apply **azoxystrobin** or "
#                      "**chlorothalonil** fungicide. Ensure good air circulation."),
#                 "Tomato_Mosaic_Virus":
#                     ("🚨 Tomato Mosaic Virus", "error",
#                      "No cure available. Remove and destroy infected plants to prevent spread. "
#                      "Control aphids (virus vectors) with **neem oil**. Sanitize tools."),
#                 "Tomato_Yellow_Leaf_Curl_Virus":
#                     ("🚨 Yellow Leaf Curl Virus", "error",
#                      "Spread by whiteflies — apply **imidacloprid** to control them. "
#                      "Remove infected plants. Use virus-resistant tomato varieties."),
#                 "Tomato_Bacterial_spot":
#                     ("⚠️ Bacterial Spot (Xanthomonas)", "warning",
#                      "Apply **copper-based bactericide** (copper hydroxide). "
#                      "Avoid working with plants when wet. Practice crop rotation."),
#                 "Potato_healthy":
#                     ("✅ Healthy Potato Plant", "success",
#                      "Keep soil consistently moist but not waterlogged. "
#                      "Earth up around stems to prevent greening."),
#                 "Potato_Early_blight":
#                     ("⚠️ Potato Early Blight", "warning",
#                      "Apply **mancozeb** or **chlorothalonil** fungicide. "
#                      "Remove heavily infected leaves. Avoid nitrogen excess."),
#                 "Potato_Late_blight":
#                     ("🚨 Potato Late Blight (Phytophthora infestans)", "error",
#                      "Most destructive potato disease. Apply **metalaxyl** or "
#                      "**cymoxanil** fungicide immediately. Destroy infected tubers. "
#                      "Do not compost infected material."),
#                 "Pepper,_bell_healthy":
#                     ("✅ Healthy Bell Pepper", "success",
#                      "Maintain consistent moisture, full sun, and warm temperatures (20–30°C)."),
#                 "Pepper,_bell_Bacterial_spot":
#                     ("⚠️ Bacterial Spot (Xanthomonas)", "warning",
#                      "Apply **copper hydroxide** spray. Avoid overhead watering. "
#                      "Use certified disease-free seeds."),
#                 "Corn_(maize)_healthy":
#                     ("✅ Healthy Maize Plant", "success",
#                      "Ensure adequate nitrogen levels and consistent irrigation."),
#                 "Corn_(maize)_Common_rust":
#                     ("⚠️ Common Rust (Puccinia sorghi)", "warning",
#                      "Apply **propiconazole** fungicide early. "
#                      "Use rust-resistant hybrid varieties."),
#                 "Corn_(maize)_Northern_Leaf_Blight":
#                     ("⚠️ Northern Leaf Blight", "warning",
#                      "Apply **azoxystrobin** or **propiconazole** at early stages. "
#                      "Practice crop rotation; avoid corn-after-corn."),
#                 "Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot":
#                     ("⚠️ Gray Leaf Spot", "warning",
#                      "Apply **strobilurin** fungicide. Choose tolerant hybrids. "
#                      "Till crop residues to reduce inoculum."),
#                 "Apple_healthy":
#                     ("✅ Healthy Apple Tree", "success",
#                      "Prune for good air flow. Apply dormant oil spray in late winter."),
#                 "Apple_Apple_scab":
#                     ("⚠️ Apple Scab (Venturia inaequalis)", "warning",
#                      "Apply **myclobutanil** or **captan** fungicide at bud break. "
#                      "Remove fallen leaves to reduce infection source."),
#                 "Apple_Black_rot":
#                     ("⚠️ Black Rot (Botryosphaeria obtusa)", "warning",
#                      "Prune out dead/infected wood. Apply **captan** fungicide. "
#                      "Remove mummified fruits from the tree."),
#                 "Apple_Cedar_apple_rust":
#                     ("⚠️ Cedar Apple Rust", "warning",
#                      "Apply **myclobutanil** fungicide early in spring. "
#                      "Remove nearby cedar/juniper trees if possible."),
#             }
 
#             advice_key = disease_name
#             if advice_key in disease_advice:
#                 diag_label, diag_type, diag_text = disease_advice[advice_key]
#                 if diag_type == "success":
#                     st.success(f"**{diag_label}**\n\n{diag_text}")
#                 elif diag_type == "warning":
#                     st.warning(f"**{diag_label}**\n\n{diag_text}")
#                 else:
#                     st.error(f"**{diag_label}**\n\n{diag_text}")
#             else:
#                 if is_healthy:
#                     st.success(
#                         f"**{disease_name.replace('_',' ')}** — Plant appears healthy. "
#                         "Maintain good watering, fertilization, and pest monitoring practices."
#                     )
#                 else:
#                     st.warning(
#                         f"**Detected: {disease_name.replace('_',' ')}**\n\n"
#                         "🌿 General advice:\n"
#                         "• Remove visibly infected leaves immediately.\n"
#                         "• Apply an appropriate fungicide or bactericide.\n"
#                         "• Improve air circulation and avoid overhead irrigation.\n"
#                         "• Consult your local agricultural extension officer for a precise diagnosis."
#                     )
 
#             st.markdown("---")
 
#             st.subheader("📊 Prediction Confidence (All Classes)")
 
#             prob_df = pd.DataFrame({
#                 "Disease":    disease_encoder.classes_,
#                 "Confidence": all_probs
#             }).sort_values("Confidence", ascending=False)
 
#             fig = px.bar(
#                 prob_df, x="Disease", y="Confidence",
#                 color="Confidence",
#                 text=(prob_df["Confidence"]*100).round(2).astype(str)+"%",
#                 color_continuous_scale="Reds",
#                 title="Model Confidence per Disease Class"
#             )
#             fig.update_traces(textposition="outside", textfont_color="#ffffff")
#             fig.update_layout(
#                 xaxis_tickangle=-35, height=430, showlegend=False
#             )
#             fig.update_coloraxes(
#                 colorbar=dict(
#                     bgcolor="#ffffff",
#                     tickfont=dict(color="#ffffff", size=12),
#                     tickcolor="#ffffff",
#                     title=dict(font=dict(color="#ffffff", size=13)),
#                     outlinecolor="#c8e6c9",
#                     outlinewidth=1,
#                 )
#             )
#             st.plotly_chart(fig, use_container_width=True)
 
#             st.markdown("---")
 
#             st.subheader("📝 General Plant Health Tips")
#             t1, t2, t3 = st.columns(3)
#             t1.info("💧 **Water at the Base**\nAvoid wetting leaves — wet leaves promote fungal disease.")
#             t2.info("🌬️ **Air Circulation**\nProper spacing between plants reduces humidity and disease spread.")
#             t3.info("🔄 **Crop Rotation**\nRotate crops every season to break disease and pest cycles.")
 
#         except Exception as e:
#             st.error(f"❌ Disease prediction failed: `{str(e)}`")
 
#     else:
#         st.info(
#             "👆 Upload a leaf image above to get started.\n\n"
#             "**Supported formats:** JPG, JPEG, PNG, WEBP\n\n"
#             "**Tips for best results:**\n"
#             "• Use a clear, well-lit photo of a single leaf\n"
#             "• Avoid blurry or dark images\n"
#             "• Capture the affected area clearly\n"
#             "• Image size: any — the model resizes automatically to 128×128"
#         )
 
#         st.markdown("---")
#         st.subheader("🌿 Diseases This Model Can Detect")
#         st.caption(
#             "The model is trained on the classes present in your Disease_Dataset folder. "
#             "Below are the common diseases supported when using the PlantVillage dataset."
#         )
 
#         sample_diseases = [
#             "Tomato — Healthy",        "Tomato — Early Blight",
#             "Tomato — Late Blight",    "Tomato — Leaf Mold",
#             "Tomato — Mosaic Virus",   "Tomato — Spider Mites",
#             "Potato — Healthy",        "Potato — Early Blight",
#             "Potato — Late Blight",    "Pepper — Bacterial Spot",
#             "Corn — Common Rust",      "Corn — Northern Leaf Blight",
#             "Apple — Apple Scab",      "Apple — Black Rot",
#         ]
 
#         cols = st.columns(3)
#         for i, d in enumerate(sample_diseases):
#             cols[i % 3].write(f"• {d}")



# import os
# import io
# import numpy as np
# import pandas as pd
# import joblib
# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.io as pio
# from PIL import Image

# # =========================================================
# # ===== GLOBAL PLOTLY THEME ================================
# # =========================================================

# pio.templates["krishi"] = go.layout.Template(
#     layout=go.Layout(
#         paper_bgcolor="#ffffff",
#         plot_bgcolor="#f9fdf9",
#         font=dict(
#             color="#1a1a1a",
#             family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
#         ),
#         title=dict(font=dict(color="#0d2e0d", size=16)),
#         xaxis=dict(
#             color="#1a1a1a",
#             gridcolor="#d4ecd4",
#             linecolor="#81c784",
#             tickfont=dict(color="#1a1a1a"),
#             title=dict(font=dict(color="#1a1a1a")),
#             zerolinecolor="#c8e6c9",
#         ),
#         yaxis=dict(
#             color="#1a1a1a",
#             gridcolor="#d4ecd4",
#             linecolor="#81c784",
#             tickfont=dict(color="#1a1a1a"),
#             title=dict(font=dict(color="#1a1a1a")),
#             zerolinecolor="#c8e6c9",
#         ),
#         legend=dict(
#             bgcolor="#ffffff",
#             bordercolor="#c8e6c9",
#             font=dict(color="#1a1a1a"),
#         ),
#         coloraxis=dict(
#             colorbar=dict(
#                 tickfont=dict(color="#1a1a1a", size=12),
#                 tickcolor="#1a1a1a",
#                 title=dict(font=dict(color="#1a1a1a", size=13), side="right"),
#                 bgcolor="#ffffff",
#                 outlinecolor="#c8e6c9",
#                 outlinewidth=1,
#                 bordercolor="#c8e6c9",
#                 borderwidth=1,
#                 len=0.85,
#             )
#         ),
#         polar=dict(
#             bgcolor="#f9fdf9",
#             radialaxis=dict(color="#1a1a1a", gridcolor="#d4ecd4"),
#             angularaxis=dict(color="#1a1a1a", gridcolor="#d4ecd4"),
#         ),
#         colorway=["#2e7d32","#1f77b4","#ff7f0e","#d62728","#9467bd",
#                   "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"],
#     )
# )
# pio.templates.default = "krishi"

# # =========================================================
# # ================= PAGE CONFIG ===========================
# # =========================================================

# st.set_page_config(
#     page_title="Krishi AI — Smart Farming Assistant",
#     page_icon="🌱",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # =========================================================
# # ================= CUSTOM CSS ============================
# # =========================================================

# st.markdown("""
# <style>
#     /* ── Reset & Base ── */
#     html, body, [class*="css"] {
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }

#     /* ── Main app background: light green-white ── */
#     .stApp {
#         background-color: #f0f7f0;
#     }

#     /* ── ALL main content text: DARK (visible on light bg) ── */
#     .stApp p,
#     .stApp span,
#     .stApp div,
#     .stApp label,
#     .stApp li,
#     .stApp td,
#     .stApp th,
#     .stApp caption,
#     .stApp small,
#     .stApp strong,
#     .stApp em {
#         color: #1a1a1a !important;
#     }

#     /* ── Headings: dark green ── */
#     .stApp h1, .stApp h2, .stApp h3,
#     .stApp h4, .stApp h5, .stApp h6 {
#         color: #0d2e0d !important;
#         font-weight: 700;
#     }

#     /* ── Markdown text ── */
#     .stMarkdown, .stMarkdown p,
#     .stMarkdown span, .stMarkdown div,
#     .stMarkdown li, .stMarkdown strong,
#     .stMarkdown em {
#         color: #1a1a1a !important;
#     }

#     /* ── Sidebar: dark green gradient — WHITE text ── */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #0d2e0d 0%, #1a5c2a 50%, #2e7d32 100%);
#     }
#     [data-testid="stSidebar"],
#     [data-testid="stSidebar"] *,
#     [data-testid="stSidebar"] p,
#     [data-testid="stSidebar"] span,
#     [data-testid="stSidebar"] div,
#     [data-testid="stSidebar"] label,
#     [data-testid="stSidebar"] h1,
#     [data-testid="stSidebar"] h2,
#     [data-testid="stSidebar"] h3,
#     [data-testid="stSidebar"] strong,
#     [data-testid="stSidebar"] em,
#     [data-testid="stSidebar"] li,
#     [data-testid="stSidebar"] .stMarkdown,
#     [data-testid="stSidebar"] .stMarkdown p,
#     [data-testid="stSidebar"] .stMarkdown span,
#     [data-testid="stSidebar"] .stMarkdown div,
#     [data-testid="stSidebar"] .stCaption,
#     [data-testid="stSidebar"] .stSelectbox label {
#         color: #ffffff !important;
#     }

#     /* ── Header banner: WHITE text on dark bg ── */
#     .krishi-header {
#         background: linear-gradient(135deg, #0d2e0d, #1b5e20, #2e7d32, #388e3c);
#         padding: 2.2rem 1.5rem 1.8rem 1.5rem;
#         border-radius: 18px;
#         text-align: center;
#         margin-bottom: 1.8rem;
#         box-shadow: 0 6px 28px rgba(13,46,13,0.35);
#     }
#     .krishi-header h1 {
#         color: #ffffff !important;
#         font-size: 2.6rem;
#         margin: 0;
#         letter-spacing: 2px;
#         text-shadow: 0 2px 8px rgba(0,0,0,0.4);
#     }
#     .krishi-header p {
#         color: #c8e6c9 !important;
#         margin: 0.4rem 0 0 0;
#         font-size: 1.05rem;
#     }

#     /* ── Metric cards: WHITE bg, DARK text ── */
#     [data-testid="stMetric"] {
#         background: #ffffff !important;
#         border-radius: 12px !important;
#         padding: 0.9rem 1.1rem !important;
#         border-left: 4px solid #2e7d32 !important;
#         box-shadow: 0 3px 10px rgba(0,0,0,0.09) !important;
#     }
#     [data-testid="stMetric"] *,
#     [data-testid="stMetric"] label,
#     [data-testid="stMetric"] div,
#     [data-testid="stMetricLabel"],
#     [data-testid="stMetricLabel"] p,
#     [data-testid="stMetricLabel"] div,
#     [data-testid="stMetricValue"],
#     [data-testid="stMetricValue"] div {
#         color: #0d2e0d !important;
#     }
#     [data-testid="stMetricLabel"] p {
#         color: #2e7d32 !important;
#         font-weight: 600;
#     }
#     [data-testid="stMetricValue"] {
#         font-size: 1.6rem !important;
#         font-weight: 700 !important;
#     }

#     /* ── Dataframe: DARK text on light bg ── */
#     .stDataFrame,
#     .stDataFrame *,
#     [data-testid="stDataFrameContainer"],
#     [data-testid="stDataFrameContainer"] * {
#         color: #1a1a1a !important;
#     }
#     [data-testid="stDataFrameContainer"] {
#         border: 1px solid #c8e6c9;
#         border-radius: 10px;
#     }

#     /* ── Chat bubbles ── */
#     .chat-user {
#         background: #1b5e20;
#         border-radius: 16px 16px 4px 16px;
#         padding: 0.75rem 1.2rem;
#         margin: 0.4rem 0;
#         max-width: 80%;
#         margin-left: auto;
#         color: #ffffff !important;
#         font-weight: 500;
#         box-shadow: 0 2px 8px rgba(27,94,32,0.25);
#     }
#     .chat-user * { color: #ffffff !important; }

#     .chat-ai {
#         background: #ffffff;
#         border-radius: 16px 16px 16px 4px;
#         padding: 0.75rem 1.2rem;
#         margin: 0.4rem 0;
#         max-width: 85%;
#         border-left: 3px solid #43a047;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#         color: #1a1a1a !important;
#     }
#     .chat-ai * { color: #1a1a1a !important; }

#     .chat-label-user {
#         text-align: right;
#         font-size: 0.75rem;
#         color: #2e7d32 !important;
#         margin-bottom: 3px;
#         font-weight: 600;
#     }
#     .chat-label-ai {
#         font-size: 0.75rem;
#         color: #2e7d32 !important;
#         margin-bottom: 3px;
#         font-weight: 600;
#     }

#     /* ── Disease result card: WHITE bg, DARK text ── */
#     .disease-card {
#         background: #ffffff;
#         border-radius: 16px;
#         padding: 1.6rem;
#         box-shadow: 0 4px 18px rgba(0,0,0,0.10);
#         margin: 1rem 0;
#         border-top: 4px solid #2e7d32;
#     }
#     .disease-card,
#     .disease-card * {
#         color: #1a1a1a !important;
#     }

#     /* ── Buttons: WHITE text on dark green bg ── */
#     .stButton > button {
#         background: linear-gradient(135deg, #1b5e20, #2e7d32, #43a047) !important;
#         color: #ffffff !important;
#         border: none !important;
#         border-radius: 10px !important;
#         font-weight: 700 !important;
#         font-size: 0.95rem !important;
#         padding: 0.55rem 1.2rem !important;
#         transition: all 0.2s ease !important;
#         letter-spacing: 0.3px;
#     }
#     .stButton > button:hover {
#         transform: translateY(-2px) !important;
#         box-shadow: 0 6px 16px rgba(46,125,50,0.4) !important;
#         background: linear-gradient(135deg, #155218, #256427, #36883a) !important;
#     }
#     .stButton > button *,
#     .stButton > button span,
#     .stButton > button p {
#         color: #ffffff !important;
#     }

#     /* ── Alert boxes: DARK text on coloured bg ── */
#     div[data-testid="stNotification"] {
#         border-radius: 12px !important;
#     }
#     /* SUCCESS box */
#     [data-testid="stNotification"][kind="success"],
#     div.stSuccess,
#     div.stSuccess > div {
#         background-color: #d4edda !important;
#         border-color: #28a745 !important;
#         border-radius: 12px !important;
#     }
#     div.stSuccess p,
#     div.stSuccess div,
#     div.stSuccess span,
#     div.stSuccess li,
#     div.stSuccess strong,
#     div.stSuccess em {
#         color: #155724 !important;
#     }
#     /* INFO box */
#     div.stInfo,
#     div.stInfo > div {
#         background-color: #d1ecf1 !important;
#         border-color: #17a2b8 !important;
#         border-radius: 12px !important;
#     }
#     div.stInfo p,
#     div.stInfo div,
#     div.stInfo span,
#     div.stInfo li,
#     div.stInfo strong,
#     div.stInfo em {
#         color: #0c5460 !important;
#     }
#     /* WARNING box */
#     div.stWarning,
#     div.stWarning > div {
#         background-color: #fff3cd !important;
#         border-color: #ffc107 !important;
#         border-radius: 12px !important;
#     }
#     div.stWarning p,
#     div.stWarning div,
#     div.stWarning span,
#     div.stWarning li,
#     div.stWarning strong,
#     div.stWarning em {
#         color: #856404 !important;
#     }
#     /* ERROR box */
#     div.stError,
#     div.stError > div {
#         background-color: #f8d7da !important;
#         border-color: #dc3545 !important;
#         border-radius: 12px !important;
#     }
#     div.stError p,
#     div.stError div,
#     div.stError span,
#     div.stError li,
#     div.stError strong,
#     div.stError em {
#         color: #721c24 !important;
#     }

#     /* ── Selectbox & input labels: DARK text ── */
#     .stSelectbox label,
#     .stSlider label,
#     .stTextInput label,
#     .stFileUploader label,
#     .stMultiSelect label {
#         color: #1a1a1a !important;
#         font-weight: 600 !important;
#     }

#     /* ── Text input box ── */
#     .stTextInput input {
#         background: #ffffff !important;
#         color: #1a1a1a !important;
#         border: 1.5px solid #81c784 !important;
#         border-radius: 8px !important;
#     }
#     .stTextInput input::placeholder {
#         color: #5a8c5a !important;
#     }
#     .stTextInput input:focus {
#         border-color: #2e7d32 !important;
#         box-shadow: 0 0 0 2px rgba(46,125,50,0.2) !important;
#     }

#     /* ── Slider: DARK labels ── */
#     .stSlider [data-testid="stTickBar"] div,
#     [data-testid="stSlider"] div[data-testid="stThumbValue"],
#     [data-testid="stSlider"] * {
#         color: #1a1a1a !important;
#     }

#     /* ── Plotly chart container background ── */
#     .js-plotly-plot, .plotly, .plot-container {
#         background: #ffffff !important;
#         border-radius: 12px;
#     }

#     /* ── Plotly SVG text: DARK on white chart bg ── */
#     .js-plotly-plot .plotly .xtick text,
#     .js-plotly-plot .plotly .ytick text,
#     .js-plotly-plot .plotly .xtitle,
#     .js-plotly-plot .plotly .ytitle,
#     .js-plotly-plot .plotly .g-xtitle text,
#     .js-plotly-plot .plotly .g-ytitle text,
#     .js-plotly-plot .plotly .gtitle,
#     .js-plotly-plot .plotly .cbaxis text,
#     .js-plotly-plot .plotly .cbtitle text,
#     .js-plotly-plot .plotly .legend text {
#         fill: #1a1a1a !important;
#     }

#     /* ── Plotly bar text labels ON bars: WHITE ── */
#     .js-plotly-plot .plotly .bartext text,
#     .js-plotly-plot .plotly g.points text,
#     .js-plotly-plot .plotly .textpoint text,
#     .js-plotly-plot .plotly .trace text {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly colorbar background ── */
#     .js-plotly-plot .plotly .cbfill,
#     .js-plotly-plot .plotly rect.cbbg {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly modebar ── */
#     .modebar-container {
#         background: rgba(0,0,0,0.6) !important;
#         border-radius: 6px !important;
#     }
#     .modebar-btn path { fill: #ffffff !important; }
#     .modebar-btn:hover path { fill: #cccccc !important; }

#     /* ── Dataframe toolbar ── */
#     [data-testid="stElementToolbar"] {
#         background: #2e7d32 !important;
#         border-radius: 8px !important;
#         padding: 2px 4px !important;
#     }
#     [data-testid="stElementToolbar"] button svg path,
#     [data-testid="stElementToolbar"] button svg rect,
#     [data-testid="stElementToolbar"] button svg circle {
#         fill: #ffffff !important;
#         stroke: #ffffff !important;
#     }
#     [data-testid="stElementToolbar"] button:hover {
#         background: #1b5e20 !important;
#         border-radius: 4px !important;
#     }

#     /* ── Divider ── */
#     hr {
#         border-color: #a5d6a7;
#         margin: 1.8rem 0;
#     }

#     /* ── Caption text ── */
#     .stCaption,
#     [data-testid="stCaptionContainer"],
#     [data-testid="stCaptionContainer"] p {
#         color: #4a7c4a !important;
#     }

#     /* ── Selectbox dropdown: DARK text ── */ 
            
#     [data-testid="stSelectbox"] div[data-baseweb="select"] {
#         background: #0b1220 !important;  /* dark background */
#     }

#     [data-testid="stSelectbox"] div[data-baseweb="select"] *,
#     [data-testid="stSelectbox"] span {
#         color: #ffffff !important;       /* white text */
#     }
                
    

#     /* ── File uploader ── */
#     [data-testid="stFileUploader"] {
#         background: #ffffff !important;
#         border: 2px dashed #81c784 !important;
#         border-radius: 10px !important;
#     }
#     [data-testid="stFileUploader"] *,
#     [data-testid="stFileUploader"] p,
#     [data-testid="stFileUploader"] span,
#     [data-testid="stFileUploader"] div {
#         color: #1a1a1a !important;
#     }

#     /* ── Progress bar ── */
#     [data-testid="stProgressBar"] > div {
#         background-color: #2e7d32 !important;
#     }

#     /* ── Tabs ── */
#     [data-testid="stTabs"] [data-baseweb="tab"] {
#         color: #1a1a1a !important;
#     }
#     [data-testid="stTabs"] [aria-selected="true"] {
#         color: #2e7d32 !important;
#         border-bottom-color: #2e7d32 !important;
#     }

#     /* ── Column containers ── */
#     [data-testid="column"] { padding: 0 0.4rem; }

#     /* ── Scrollbar ── */
#     ::-webkit-scrollbar { width: 7px; height: 7px; }
#     ::-webkit-scrollbar-track { background: #e8f5e9; }
#     ::-webkit-scrollbar-thumb { background: #81c784; border-radius: 4px; }
#     ::-webkit-scrollbar-thumb:hover { background: #2e7d32; }
# </style>
# """, unsafe_allow_html=True)

# # =========================================================
# # ================= HEADER ================================
# # =========================================================

# st.markdown("""
# <div class="krishi-header">
#     <h1>🌱 Krishi AI</h1>
#     <p>AI-Powered Smart Farming Assistant — Crop Recommendation · Disease Detection · Analytics</p>
# </div>
# """, unsafe_allow_html=True)

# # =========================================================
# # ================= LOAD DATASET ==========================
# # =========================================================

# DATASET_PATH = "Krishi_ai_dataset/cleaned_crop_dataset.csv"

# @st.cache_data(show_spinner=False)
# def load_dataset(path):
#     if not os.path.exists(path):
#         return None
#     return pd.read_csv(path)

# df = load_dataset(DATASET_PATH)

# if df is None:
#     st.error(
#         f"❌ Dataset not found at `{DATASET_PATH}`. "
#         "Please add the CSV file and restart."
#     )
#     st.stop()

# # =========================================================
# # ================= FEATURE CATEGORIES ====================
# # =========================================================

# def nitrogen_category(n):
#     if n <= 50:         return "Low"
#     elif n <= 120:      return "Medium"
#     else:               return "High"

# def phosphorus_category(p):
#     if p <= 40:         return "Low"
#     elif p <= 80:       return "Medium"
#     else:               return "High"

# def potassium_category(k):
#     if k <= 40:         return "Low"
#     elif k <= 80:       return "Medium"
#     else:               return "High"

# def temperature_category(temp):
#     if temp <= 20:      return "Cool"
#     elif temp <= 30:    return "Moderate"
#     else:               return "Hot"

# def humidity_category(hum):
#     if hum <= 40:       return "Low"
#     elif hum <= 70:     return "Medium"
#     else:               return "High"

# def ph_category(ph):
#     if ph < 6:          return "Acidic"
#     elif ph <= 7.5:     return "Neutral"
#     else:               return "Alkaline"

# def rainfall_category(rain):
#     if rain <= 100:     return "Low"
#     elif rain <= 200:   return "Medium"
#     else:               return "High"

# # =========================================================
# # ================= ADD CATEGORY COLUMNS ==================
# # =========================================================

# @st.cache_data(show_spinner=False)
# def enrich_dataframe(dataframe):
#     df2 = dataframe.copy()
#     df2["Nitrogen_Category"]    = df2["N"].apply(nitrogen_category)
#     df2["Phosphorus_Category"]  = df2["P"].apply(phosphorus_category)
#     df2["Potassium_Category"]   = df2["K"].apply(potassium_category)
#     df2["Temperature_Category"] = df2["temperature"].apply(temperature_category)
#     df2["Humidity_Category"]    = df2["humidity"].apply(humidity_category)
#     df2["PH_Category"]          = df2["ph"].apply(ph_category)
#     df2["Rainfall_Category"]    = df2["rainfall"].apply(rainfall_category)
#     return df2

# df = enrich_dataframe(df)

# # =========================================================
# # ================= LOAD ML FILES =========================
# # =========================================================

# @st.cache_resource(show_spinner=False)
# def load_ml_files():
#     try:
#         ml_model      = joblib.load("crop_model.pkl")
#         ml_scaler     = joblib.load("scaler.pkl")
#         ml_encoder    = joblib.load("label_encoder.pkl")
#         return ml_model, ml_scaler, ml_encoder, None
#     except FileNotFoundError as e:
#         return None, None, None, str(e)
#     except Exception as e:
#         return None, None, None, str(e)

# crop_model, crop_scaler, crop_encoder, ml_error = load_ml_files()

# # =========================================================
# # ================= LOAD DISEASE MODEL ====================
# # =========================================================

# @st.cache_resource(show_spinner=False)
# def load_disease_model():
#     try:
#         from tensorflow.keras.models import load_model
#         d_model   = load_model("plant_disease_model.h5")
#         d_encoder = joblib.load("disease_label_encoder.pkl")
#         return d_model, d_encoder, None
#     except FileNotFoundError as e:
#         return None, None, str(e)
#     except Exception as e:
#         return None, None, str(e)

# disease_model, disease_encoder, disease_error = load_disease_model()

# # =========================================================
# # ================= SIDEBAR ===============================
# # =========================================================

# with st.sidebar:
#     st.markdown("### 🌾 Navigation")
#     page = st.selectbox(
#         "Go To",
#         ["🏠 Home", "📊 Analytics", "🤖 ML Prediction", "🌿 Disease Detection"],
#         label_visibility="collapsed"
#     )

#     st.markdown("---")
#     st.markdown("### 📌 Quick Info")

#     total_crops  = df["label"].nunique()
#     total_rows   = df.shape[0]
#     ml_status    = "✅ Loaded" if crop_model  else "❌ Not Found"
#     dis_status   = "✅ Loaded" if disease_model else "❌ Not Found"

#     st.markdown(f"**Dataset Crops :** {total_crops}")
#     st.markdown(f"**Dataset Rows  :** {total_rows:,}")
#     st.markdown(f"**Crop Model    :** {ml_status}")
#     st.markdown(f"**Disease Model :** {dis_status}")
#     st.markdown("---")
#     st.caption("Krishi AI v2.0 — Built with ❤️ for Farmers")

# # =========================================================
# # Shared constants
# # =========================================================

# NUMERIC_FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
# FEATURE_LABELS   = ["Nitrogen", "Phosphorus", "Potassium",
#                     "Temperature", "Humidity", "pH", "Rainfall"]
# CROPS_LIST       = sorted(df["label"].unique())

# @st.cache_data(show_spinner=False)
# def get_crop_stats(dataframe):
#     means = dataframe.groupby("label")[NUMERIC_FEATURES].mean()
#     norm  = (means - means.min()) / (means.max() - means.min())
#     return means, norm

# CROP_MEANS, CROP_NORM = get_crop_stats(df)

# # =========================================================
# # Helper: colorbar config (dark tick text on white bg)
# # =========================================================

# def colorbar_cfg():
#     return dict(
#         bgcolor="#ffffff",
#         tickfont=dict(color="#1a1a1a", size=12),
#         tickcolor="#1a1a1a",
#         title=dict(font=dict(color="#1a1a1a", size=13)),
#         outlinecolor="#c8e6c9",
#         outlinewidth=1,
#     )

# # =========================================================
# # PAGE: HOME
# # =========================================================

# if page == "🏠 Home":

#     col_left, col_mid, col_right = st.columns([1, 2, 1])

#     with col_mid:

#         st.markdown("## 💬 Ask Your Farming Question")
#         st.caption(
#             "Get instant AI-powered advice on crops, soil, fertilizers, "
#             "weather, and more."
#         )

#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = []

#         for entry in st.session_state.chat_history:
#             if entry["role"] == "user":
#                 st.markdown(
#                     f"<div class='chat-label-user'>You</div>"
#                     f"<div class='chat-user'>{entry['text']}</div>",
#                     unsafe_allow_html=True
#                 )
#             else:
#                 st.markdown(
#                     f"<div class='chat-label-ai'>🌱 Krishi AI</div>"
#                     f"<div class='chat-ai'>{entry['text']}</div>",
#                     unsafe_allow_html=True
#                 )

#         user_input = st.text_input(
#             "Your question",
#             placeholder="e.g.  What crop grows best in red soil with low rainfall?",
#             label_visibility="collapsed",
#             key="home_input"
#         )

#         btn_col1, btn_col2 = st.columns([3, 1])
#         with btn_col1:
#             ask_clicked = st.button("🌾 Get Advice", use_container_width=True)
#         with btn_col2:
#             if st.button("🗑️ Clear", use_container_width=True):
#                 st.session_state.chat_history = []
#                 st.rerun()

#         if ask_clicked:
#             if not user_input.strip():
#                 st.warning("⚠️ Please type a farming question first.")
#             else:
#                 st.session_state.chat_history.append(
#                     {"role": "user", "text": user_input}
#                 )

#                 q = user_input.lower()

#                 if any(k in q for k in ["fertilizer", "npk", "nitrogen", "urea"]):
#                     reply = (
#                         "🌿 <b>Fertilizer Advice:</b><br><br>"
#                         "• <b>Nitrogen (N):</b> Use urea or ammonium nitrate for leafy growth.<br>"
#                         "• <b>Phosphorus (P):</b> DAP or SSP promotes root development.<br>"
#                         "• <b>Potassium (K):</b> MOP (muriate of potash) improves crop strength.<br><br>"
#                         "Apply based on a soil test for best results."
#                     )
#                 elif any(k in q for k in ["soil", "ph", "acidic", "alkaline"]):
#                     reply = (
#                         "🧪 <b>Soil Health Tips:</b><br><br>"
#                         "• <b>pH 6–7.5 (Neutral):</b> Ideal for most crops.<br>"
#                         "• <b>pH &lt; 6 (Acidic):</b> Add lime (calcium carbonate) to raise pH.<br>"
#                         "• <b>pH &gt; 7.5 (Alkaline):</b> Add sulfur or gypsum to lower pH.<br>"
#                         "• Get a soil test every season for accurate readings."
#                     )
#                 elif any(k in q for k in ["water", "irrigation", "rainfall", "drought"]):
#                     reply = (
#                         "💧 <b>Irrigation &amp; Water Management:</b><br><br>"
#                         "• <b>Drip irrigation</b> saves up to 60% water vs flood irrigation.<br>"
#                         "• Water crops in early morning or late evening to reduce evaporation.<br>"
#                         "• Mulching retains soil moisture and reduces weed growth.<br>"
#                         "• Drought-tolerant crops: chickpea, sorghum, moth beans."
#                     )
#                 elif any(k in q for k in ["disease", "pest", "fungus", "blight", "rust"]):
#                     reply = (
#                         "🦠 <b>Disease &amp; Pest Control:</b><br><br>"
#                         "• Use the <b>Disease Detection</b> tab to identify plant diseases from photos.<br>"
#                         "• <b>Fungal diseases:</b> Apply copper-based or systemic fungicides.<br>"
#                         "• <b>Pests:</b> Neem oil spray is an organic option; consult an agronomist.<br>"
#                         "• Rotate crops every season to break pest/disease cycles."
#                     )
#                 elif any(k in q for k in ["crop", "grow", "plant", "best crop", "which crop"]):
#                     reply = (
#                         "🌾 <b>Crop Recommendation:</b><br><br>"
#                         "Use the <b>ML Prediction</b> tab for an AI-based crop recommendation!<br><br>"
#                         "Just enter your soil nutrients (N, P, K), temperature, humidity, "
#                         "rainfall and soil pH — our trained Random Forest model will "
#                         "suggest the best crop with confidence scores."
#                     )
#                 elif any(k in q for k in ["weather", "temperature", "season", "monsoon"]):
#                     reply = (
#                         "🌤️ <b>Seasonal Farming Tips:</b><br><br>"
#                         "• <b>Kharif (June–Nov):</b> Rice, maize, cotton, soybean, groundnut.<br>"
#                         "• <b>Rabi (Nov–Apr):</b> Wheat, barley, mustard, pea, chickpea.<br>"
#                         "• <b>Zaid (Apr–Jun):</b> Watermelon, muskmelon, cucumber, moong.<br>"
#                         "• Always check local weather forecasts before sowing."
#                     )
#                 elif any(k in q for k in ["hello", "hi", "hey", "namaste"]):
#                     reply = (
#                         "🙏 <b>Namaste! Welcome to Krishi AI.</b><br><br>"
#                         "I can help you with:<br>"
#                         "• 🌾 Which crop to grow based on your soil conditions<br>"
#                         "• 🧪 Soil health and fertilizer advice<br>"
#                         "• 💧 Irrigation and water management<br>"
#                         "• 🌿 Plant disease identification<br><br>"
#                         "Ask me anything about farming!"
#                     )
#                 else:
#                     reply = (
#                         "🤖 <b>Krishi AI Response:</b><br><br>"
#                         f"Your question: <i>\"{user_input}\"</i><br><br>"
#                         "I recommend using our AI tools:<br>"
#                         "• 📊 <b>Analytics</b> — explore crop data &amp; trends<br>"
#                         "• 🤖 <b>ML Prediction</b> — get the best crop recommendation for your soil<br>"
#                         "• 🌿 <b>Disease Detection</b> — upload a leaf photo to detect disease<br><br>"
#                         "For detailed guidance, consult your local KVK (Krishi Vigyan Kendra)."
#                     )

#                 st.session_state.chat_history.append(
#                     {"role": "ai", "text": reply}
#                 )
#                 st.rerun()

#     st.markdown("---")

#     st.markdown("### 🚀 What Krishi AI Can Do For You")
#     c1, c2, c3 = st.columns(3)

#     with c1:
#         st.info(
#             "### 📊 Smart Analytics\n"
#             "Explore 24+ charts and insights about crops, soil nutrients, "
#             "rainfall, temperature, and more."
#         )
#     with c2:
#         st.success(
#             "### 🤖 Crop Prediction\n"
#             "Enter your soil and weather data to get an ML-powered crop "
#             "recommendation with confidence scores."
#         )
#     with c3:
#         st.warning(
#             "### 🌿 Disease Detection\n"
#             "Upload a leaf image and our CNN model will identify plant "
#             "diseases and suggest treatment in seconds."
#         )

# # =========================================================
# # PAGE: ANALYTICS
# # =========================================================

# elif page == "📊 Analytics":

#     st.header("📊 Krishi Data Analytics Dashboard")

#     st.subheader("📁 Dataset Overview")
#     c1, c2, c3, c4, c5 = st.columns(5)
#     c1.metric("Total Rows",      f"{df.shape[0]:,}")
#     c2.metric("Total Columns",   df.shape[1])
#     c3.metric("Unique Crops",    df["label"].nunique())
#     c4.metric("Duplicate Rows",  int(df.duplicated().sum()))
#     c5.metric("Missing Values",  int(df.isnull().sum().sum()))
#     st.markdown("---")

#     st.subheader("🔬 Data Quality Check")
#     q1, q2 = st.columns(2)
#     with q1:
#         st.write("#### Data Types")
#         dtype_df = df.dtypes.reset_index()
#         dtype_df.columns = ["Feature", "Type"]
#         dtype_df["Type"] = dtype_df["Type"].astype(str)
#         st.dataframe(dtype_df, use_container_width=True)
#     with q2:
#         st.write("#### Missing Values")
#         mv = df.isnull().sum().reset_index()
#         mv.columns = ["Feature", "Missing"]
#         st.dataframe(mv, use_container_width=True)
#         if mv["Missing"].sum() == 0:
#             st.success("✅ No missing values!")
#         if df.duplicated().sum() == 0:
#             st.success("✅ No duplicate rows!")
#     st.markdown("---")

#     st.subheader("🔍 Dataset Preview")
#     st.dataframe(df.head(50), use_container_width=True)
#     st.markdown("---")

#     st.subheader("📈 Statistical Summary")
#     st.dataframe(df.describe().round(2), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🌾 Crop Distribution")
#     crop_count = df["label"].value_counts().reset_index()
#     crop_count.columns = ["Crop", "Count"]

#     d1, d2 = st.columns(2)
#     with d1:
#         fig = px.bar(crop_count, x="Crop", y="Count",
#                      color="Count", color_continuous_scale="Greens",
#                      text="Count", title="Crop Count")
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(xaxis_tickangle=-45, showlegend=False, height=380)
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         st.plotly_chart(fig, use_container_width=True)
#     with d2:
#         fig2 = px.pie(crop_count, names="Crop", values="Count",
#                       title="Crop Share",
#                       color_discrete_sequence=px.colors.sequential.Greens_r)
#         fig2.update_traces(textposition="inside", textinfo="percent+label")
#         st.plotly_chart(fig2, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📊 Feature Category Analysis")
#     cat_cols = [
#         ("Nitrogen_Category", "Nitrogen"),
#         ("Phosphorus_Category", "Phosphorus"),
#         ("Potassium_Category", "Potassium"),
#         ("Temperature_Category", "Temperature"),
#         ("Humidity_Category", "Humidity"),
#         ("PH_Category", "Soil pH"),
#         ("Rainfall_Category", "Rainfall"),
#     ]
#     ca1, ca2 = st.columns(2)
#     for i, (col_name, title) in enumerate(cat_cols):
#         counts = df[col_name].value_counts().reset_index()
#         counts.columns = ["Category", "Count"]
#         fig = px.pie(counts, names="Category", values="Count",
#                      title=f"{title} Distribution", hole=0.4,
#                      color_discrete_sequence=px.colors.qualitative.Set2)
#         fig.update_traces(textinfo="percent+label")
#         (ca1 if i % 2 == 0 else ca2).plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     def climate_bar(feature, label, color_scale, unit=""):
#         grp = df.groupby("label")[feature].mean().round(2).reset_index()
#         grp.columns = ["Crop", label]
#         grp = grp.sort_values(label, ascending=True)
#         fig = px.bar(grp, x=label, y="Crop", orientation="h",
#                      title=f"Average {label} per Crop",
#                      color=label, color_continuous_scale=color_scale,
#                      text=label)
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(height=580, yaxis_title="")
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         return fig, grp

#     for feat, lbl, scale in [
#         ("temperature", "Avg Temperature (°C)", "RdYlGn_r"),
#         ("rainfall",    "Avg Rainfall (mm)",    "Blues"),
#         ("humidity",    "Avg Humidity (%)",      "Teal"),
#         ("ph",          "Avg pH",               "RdYlGn"),
#     ]:
#         icon = '🌡' if 'Temp' in lbl else '🌧' if 'Rain' in lbl else '💧' if 'Hum' in lbl else '🧪'
#         st.subheader(f"{icon} {lbl}")
#         fig, grp = climate_bar(feat, lbl, scale)
#         st.plotly_chart(fig, use_container_width=True)
#         t1, t2 = st.columns(2)
#         with t1:
#             st.write("**Top 5 (Highest)**")
#             st.dataframe(grp.tail(5)[::-1].reset_index(drop=True), use_container_width=True)
#         with t2:
#             st.write("**Bottom 5 (Lowest)**")
#             st.dataframe(grp.head(5).reset_index(drop=True), use_container_width=True)
#         st.markdown("---")

#     st.subheader("🪴 NPK Analysis")
#     avg_npk = df.groupby("label")[["N","P","K"]].mean().round(2).reset_index()
#     npk_m   = avg_npk.melt(id_vars="label", value_vars=["N","P","K"],
#                             var_name="Nutrient", value_name="Value")
#     cmap = {"N": "#2ca02c", "P": "#ff7f0e", "K": "#1f77b4"}

#     for mode, title in [("group","Grouped"), ("stack","Stacked — shows proportion")]:
#         fig = px.bar(npk_m, x="label", y="Value", color="Nutrient",
#                      barmode=mode, title=f"N, P, K per Crop ({title})",
#                      color_discrete_map=cmap,
#                      labels={"label":"Crop","Value":"mg/kg"})
#         fig.update_layout(xaxis_tickangle=-45, height=420)
#         st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(avg_npk.set_index("label"), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🧪 Soil Health Analysis")
#     c1,c2,c3 = st.columns(3)
#     c1.metric("Avg Nitrogen",   round(df["N"].mean(),2))
#     c2.metric("Avg Phosphorus", round(df["P"].mean(),2))
#     c3.metric("Avg Potassium",  round(df["K"].mean(),2))

#     soil = df.groupby("label")[["N","P","K"]].mean()
#     soil["Score"] = soil.mean(axis=1).round(2)
#     soil = soil.reset_index().sort_values("Score", ascending=False)
#     avg_s = soil["Score"].mean()

#     fig = px.bar(soil, x="label", y="Score", color="Score",
#                  color_continuous_scale="YlGn", text="Score",
#                  title="Soil Health Score (avg of N+P+K)")
#     fig.add_hline(y=avg_s, line_dash="dash", line_color="red",
#                   annotation_text=f"Avg: {avg_s:.1f}")
#     fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#     fig.update_layout(xaxis_tickangle=-45, height=420)
#     fig.update_coloraxes(colorbar=colorbar_cfg())
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("⚠️ Nutrient Deficiency Flag")
#     npk_flag = df.groupby("label")[["N","P","K"]].mean().round(2).reset_index()
#     npk_flag["N_Flag"] = npk_flag["N"].apply(lambda x: "⚠️ Low" if x<=50 else "✅ OK")
#     npk_flag["P_Flag"] = npk_flag["P"].apply(lambda x: "⚠️ Low" if x<=40 else "✅ OK")
#     npk_flag["K_Flag"] = npk_flag["K"].apply(lambda x: "⚠️ Low" if x<=40 else "✅ OK")
#     npk_flag["Status"] = npk_flag[["N_Flag","P_Flag","K_Flag"]].apply(
#         lambda r: "⚠️ Deficient" if "⚠️ Low" in r.values else "✅ Sufficient", axis=1)
#     deficient = npk_flag[npk_flag["Status"]=="⚠️ Deficient"]
#     if len(deficient):
#         st.warning(f"⚠️ {len(deficient)} crops have a nutrient in the Low range.")
#         st.dataframe(deficient[["label","N","N_Flag","P","P_Flag","K","K_Flag"]],
#                      use_container_width=True)
#     else:
#         st.success("✅ All crops have sufficient average NPK levels.")
#     st.markdown("---")

#     st.subheader("📏 Feature Range per Crop")
#     sel_feat = st.selectbox("Select Feature", NUMERIC_FEATURES, key="range_sel")
#     range_df = (df.groupby("label")[sel_feat]
#                 .agg(["min","max","mean","std"]).round(2).reset_index())
#     range_df.columns = ["Crop","Min","Max","Mean","Std Dev"]
#     range_df = range_df.sort_values("Mean", ascending=False)
#     fig = go.Figure(go.Bar(
#         x=range_df["Crop"], y=range_df["Mean"], name="Mean",
#         marker_color="#2ca02c",
#         error_y=dict(type="data", array=range_df["Std Dev"], visible=True),
#         text=range_df["Mean"], textposition="outside"
#     ))
#     fig.update_layout(title=f"{sel_feat} — Mean ± Std Dev",
#                       xaxis_tickangle=-45, height=440)
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(range_df.set_index("Crop"), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔵 Scatter Plot Analysis")
#     scatter_pairs = [
#         ("rainfall","humidity","Rainfall vs Humidity"),
#         ("temperature","ph","Temperature vs Soil pH"),
#         ("N","K","Nitrogen vs Potassium"),
#         ("temperature","rainfall","Temperature vs Rainfall"),
#     ]
#     s1, s2 = st.columns(2)
#     for i, (x, y, title) in enumerate(scatter_pairs):
#         fig = px.scatter(df, x=x, y=y, color="label",
#                          hover_name="label", title=title, opacity=0.6)
#         fig.update_layout(height=420, showlegend=False)
#         (s1 if i % 2 == 0 else s2).plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📦 Feature Distribution (Box Plot)")
#     box_sel = st.selectbox("Select Feature", NUMERIC_FEATURES, key="box_sel")
#     fig = px.box(df, x="label", y=box_sel, color="label",
#                  title=f"{box_sel} Distribution by Crop",
#                  color_discrete_sequence=px.colors.qualitative.Pastel)
#     fig.update_layout(xaxis_tickangle=-45, height=500, showlegend=False)
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📋 Complete Crop Profile")
#     full_prof = df.groupby("label")[NUMERIC_FEATURES].mean().round(2)
#     full_prof.columns = ["N (mg/kg)","P (mg/kg)","K (mg/kg)",
#                          "Temp (°C)","Humidity (%)","pH","Rainfall (mm)"]
#     st.dataframe(full_prof.style.background_gradient(cmap="YlGn", axis=0),
#                  use_container_width=True)
#     st.markdown("---")

#     st.subheader("⚖️ Crop-to-Crop Comparison")
#     cc1, cc2 = st.columns(2)
#     crop_a = cc1.selectbox("Crop A", CROPS_LIST, index=0, key="ca")
#     crop_b = cc2.selectbox("Crop B", CROPS_LIST, index=1, key="cb")

#     a_v = df[df["label"]==crop_a][NUMERIC_FEATURES].mean().round(2)
#     b_v = df[df["label"]==crop_b][NUMERIC_FEATURES].mean().round(2)

#     fig = go.Figure([
#         go.Bar(name=crop_a, x=FEATURE_LABELS, y=a_v.values,
#                marker_color="#2ca02c", text=a_v.values, textposition="outside"),
#         go.Bar(name=crop_b, x=FEATURE_LABELS, y=b_v.values,
#                marker_color="#1f77b4", text=b_v.values, textposition="outside"),
#     ])
#     fig.update_layout(barmode="group",
#                       title=f"{crop_a} vs {crop_b}", height=400)
#     st.plotly_chart(fig, use_container_width=True)

#     a_n = CROP_NORM.loc[crop_a].values.tolist()
#     b_n = CROP_NORM.loc[crop_b].values.tolist()
#     fig2 = go.Figure([
#         go.Scatterpolar(r=a_n+[a_n[0]], theta=NUMERIC_FEATURES+[NUMERIC_FEATURES[0]],
#                         fill="toself", name=crop_a,
#                         line_color="#2ca02c", fillcolor="rgba(44,160,44,0.15)"),
#         go.Scatterpolar(r=b_n+[b_n[0]], theta=NUMERIC_FEATURES+[NUMERIC_FEATURES[0]],
#                         fill="toself", name=crop_b,
#                         line_color="#1f77b4", fillcolor="rgba(31,119,180,0.15)"),
#     ])
#     fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])),
#                        title=f"Radar: {crop_a} vs {crop_b} (Normalized 0–1)", height=460)
#     st.plotly_chart(fig2, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔍 Similar Crops Finder")
#     target = st.selectbox("Select a Crop", CROPS_LIST, key="sim")
#     vec    = CROP_NORM.loc[target]
#     dists  = CROP_NORM.drop(target).apply(
#         lambda r: np.sqrt(((r - vec)**2).sum()), axis=1)
#     top3 = dists.nsmallest(3).reset_index()
#     top3.columns = ["Similar Crop","Distance (lower=closer)"]
#     top3["Distance (lower=closer)"] = top3["Distance (lower=closer)"].round(4)
#     st.write(f"**Top 3 crops most similar to {target}:**")
#     st.dataframe(top3, use_container_width=True)
#     sim_names   = top3["Similar Crop"].tolist()
#     sim_profile = CROP_MEANS.loc[[target]+sim_names].round(2)
#     st.dataframe(sim_profile.style.background_gradient(cmap="Greens", axis=0),
#                  use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔍 Crop Filter")
#     sel_crop  = st.selectbox("Select Crop", CROPS_LIST, key="filter")
#     crop_data = df[df["label"]==sel_crop]
#     m1,m2,m3,m4 = st.columns(4)
#     m1.metric("Avg Temp",     f"{crop_data['temperature'].mean():.1f} °C")
#     m2.metric("Avg Humidity", f"{crop_data['humidity'].mean():.1f} %")
#     m3.metric("Avg Rainfall", f"{crop_data['rainfall'].mean():.1f} mm")
#     m4.metric("Avg pH",       f"{crop_data['ph'].mean():.2f}")
#     n1,n2,n3 = st.columns(3)
#     n1.metric("Avg Nitrogen",   round(crop_data["N"].mean(),2))
#     n2.metric("Avg Phosphorus", round(crop_data["P"].mean(),2))
#     n3.metric("Avg Potassium",  round(crop_data["K"].mean(),2))
#     st.dataframe(crop_data, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔗 Feature Correlation Matrix")
#     corr = df[NUMERIC_FEATURES].corr().round(3)
#     fig  = px.imshow(corr, text_auto=True, color_continuous_scale="RdYlGn",
#                      zmin=-1, zmax=1, title="Feature Correlation Heatmap")
#     fig.update_layout(height=480)
#     fig.update_coloraxes(colorbar=colorbar_cfg())
#     st.plotly_chart(fig, use_container_width=True)
#     st.caption("🟢 Green = positive | 🔴 Red = negative | ⚪ White = no correlation")

#     pairs = corr.unstack().reset_index()
#     pairs.columns = ["Feature A","Feature B","Correlation"]
#     pairs = pairs[pairs["Feature A"] < pairs["Feature B"]]
#     pairs["Abs"] = pairs["Correlation"].abs()
#     pairs = pairs.sort_values("Abs", ascending=False).drop(columns="Abs")
#     pc1, pc2 = st.columns(2)
#     with pc1:
#         st.write("**Top 3 Positive**")
#         st.dataframe(pairs[pairs["Correlation"]>0].head(3).reset_index(drop=True),
#                      use_container_width=True)
#     with pc2:
#         st.write("**Top 3 Negative**")
#         st.dataframe(pairs[pairs["Correlation"]<0].head(3).reset_index(drop=True),
#                      use_container_width=True)
#     st.markdown("---")

#     st.subheader("📘 Feature Meaning")
#     feat_info = pd.DataFrame({
#         "Feature": ["N","P","K","temperature","humidity","ph","rainfall"],
#         "Meaning": [
#             "Nitrogen — leaf and stem growth",
#             "Phosphorus — root and flower growth",
#             "Potassium — plant strength and disease resistance",
#             "Temperature — optimal growing temperature",
#             "Humidity — moisture level in the air",
#             "Soil pH — acidity or alkalinity",
#             "Rainfall — water requirement"
#         ],
#         "Unit": ["mg/kg","mg/kg","mg/kg","°C","%","0–14","mm"]
#     })
#     st.dataframe(feat_info, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🌱 Farmer Understanding Guide")
#     g1, g2 = st.columns(2)
#     with g1:
#         st.success("🟢 **Low Nitrogen (≤50)** → Light fertilizer needed")
#         st.info("🔵 **Medium Nitrogen (51–120)** → Balanced fertilizer")
#         st.warning("🟡 **High Nitrogen (>120)** → Heavy fertilizer needed")
#         st.success("🟢 **Cool (≤20°C)** → Wheat, lentil, chickpea")
#         st.info("🔵 **Moderate (21–30°C)** → Most common crops")
#         st.warning("🟡 **Hot (>30°C)** → Tropical/summer crops")
#     with g2:
#         st.success("🟢 **Acidic (pH<6)** → Tea, rice, blueberry")
#         st.info("🔵 **Neutral (pH 6–7.5)** → Best for most crops")
#         st.warning("🟡 **Alkaline (pH>7.5)** → Cotton, maize")
#         st.success("🟢 **Low Rainfall (≤100mm)** → Drought-tolerant crops")
#         st.info("🔵 **Medium Rainfall (101–200mm)** → General crops")
#         st.warning("🟡 **High Rainfall (>200mm)** → Water-intensive crops")
#     st.markdown("---")

#     st.subheader("📌 Key Insights")
#     st.success("✅ Dataset is balanced with nearly equal crop distribution.")
#     st.success("✅ No missing values or duplicate rows found.")
#     st.success("✅ Dataset is clean and ready for ML model training.")
#     st.info("📊 Rainfall, temperature, humidity and soil nutrients drive crop suitability.")
#     st.info("🌱 Rice and jute need high humidity & rainfall; chickpea and kidney beans prefer dry conditions.")
#     st.info("🧪 Use Scatter and Box Plots to identify natural clusters for ML feature selection.")
#     st.info("⚖️ Use Crop Comparison and Similar Crops to help farmers choose alternative crops.")

# # =========================================================
# # PAGE: ML PREDICTION
# # =========================================================

# elif page == "🤖 ML Prediction":

#     st.header("🤖 AI-Powered Crop Recommendation")
#     st.markdown("---")

#     if ml_error:
#         st.error(
#             f"❌ Could not load ML model files.\n\n"
#             f"**Error:** `{ml_error}`\n\n"
#             "Please make sure `crop_model.pkl`, `scaler.pkl`, and "
#             "`label_encoder.pkl` are in the same folder as `app.py`."
#         )
#         st.stop()

#     if hasattr(crop_model, "feature_importances_"):
#         st.subheader("📈 Model Feature Importance")
#         imp_df = pd.DataFrame({
#             "Feature":    FEATURE_LABELS,
#             "Importance": crop_model.feature_importances_
#         }).sort_values("Importance", ascending=False)

#         fig = px.bar(imp_df, x="Feature", y="Importance",
#                      color="Importance", color_continuous_scale="Teal",
#                      text=imp_df["Importance"].round(3),
#                      title="Feature Importance (Higher = More Influential)")
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(height=380)
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         st.plotly_chart(fig, use_container_width=True)
#         st.info(
#             f"🔑 Most influential: **{imp_df.iloc[0]['Feature']}**  |  "
#             f"📉 Least influential: **{imp_df.iloc[-1]['Feature']}**"
#         )
#         st.markdown("---")

#     st.subheader("🌱 Enter Your Soil and Weather Conditions")

#     sl1, sl2 = st.columns(2)

#     with sl1:
#         N = st.slider("Nitrogen (N) mg/kg",
#                       int(df["N"].min()), int(df["N"].max()), int(df["N"].mean()))
#         P = st.slider("Phosphorus (P) mg/kg",
#                       int(df["P"].min()), int(df["P"].max()), int(df["P"].mean()))
#         K = st.slider("Potassium (K) mg/kg",
#                       int(df["K"].min()), int(df["K"].max()), int(df["K"].mean()))
#         temperature = st.slider("Temperature (°C)",
#                                 float(df["temperature"].min()),
#                                 float(df["temperature"].max()),
#                                 round(float(df["temperature"].mean()),1))
#     with sl2:
#         humidity = st.slider("Humidity (%)",
#                              float(df["humidity"].min()),
#                              float(df["humidity"].max()),
#                              round(float(df["humidity"].mean()),1))
#         ph = st.slider("Soil pH",
#                        float(df["ph"].min()), float(df["ph"].max()),
#                        round(float(df["ph"].mean()),1))
#         rainfall = st.slider("Rainfall (mm)",
#                              float(df["rainfall"].min()),
#                              float(df["rainfall"].max()),
#                              round(float(df["rainfall"].mean()),1))

#     st.markdown("---")
#     st.subheader("📊 Real-Time Input Analysis")
#     ia1, ia2, ia3, ia4 = st.columns(4)
#     ia1.info(f"🌿 N: **{nitrogen_category(N)}**\n\n💧 Humidity: **{humidity_category(humidity)}**")
#     ia2.info(f"🌿 P: **{phosphorus_category(P)}**\n\n🧪 Soil pH: **{ph_category(ph)}**")
#     ia3.info(f"🌿 K: **{potassium_category(K)}**\n\n🌧 Rainfall: **{rainfall_category(rainfall)}**")
#     ia4.info(f"🌡 Temp: **{temperature_category(temperature)}**")

#     st.markdown("---")

#     if st.button("🌾 Predict Best Crop", use_container_width=True):
#         try:
#             inp        = [[N, P, K, temperature, humidity, ph, rainfall]]
#             scaled     = crop_scaler.transform(inp)
#             prediction = crop_model.predict(scaled)
#             pred_crop  = crop_encoder.inverse_transform(prediction)[0]

#             st.success(f"✅ Recommended Crop: **{pred_crop.upper()}**")
#             st.markdown("---")

#             if hasattr(crop_model, "predict_proba"):
#                 st.subheader("📊 Top 5 Crop Predictions")
#                 proba  = crop_model.predict_proba(scaled)[0]
#                 prob_df = pd.DataFrame({
#                     "Crop":        crop_encoder.classes_,
#                     "Probability": proba
#                 }).sort_values("Probability", ascending=False).head(5)
#                 prob_df["Pct"] = (prob_df["Probability"]*100).round(2)

#                 fig = px.bar(prob_df, x="Crop", y="Probability",
#                              color="Probability",
#                              text=prob_df["Pct"].astype(str)+"%",
#                              color_continuous_scale="Greens",
#                              title="Prediction Confidence (Top 5)")
#                 fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#                 fig.update_layout(height=420)
#                 fig.update_coloraxes(colorbar=colorbar_cfg())
#                 st.plotly_chart(fig, use_container_width=True)

#                 top_pct = prob_df.iloc[0]["Pct"]
#                 if top_pct >= 80:
#                     st.success(f"🎯 High confidence: {top_pct}%")
#                 elif top_pct >= 50:
#                     st.info(f"🔍 Moderate confidence: {top_pct}% — verify with local conditions.")
#                 else:
#                     st.warning(f"⚠️ Low confidence: {top_pct}% — consult an agronomist.")
#                 st.markdown("---")

#             st.subheader(f"📐 Your Conditions vs Ideal for {pred_crop.capitalize()}")
#             ideal = df[df["label"]==pred_crop][NUMERIC_FEATURES].mean().round(2)
#             user_vals = [N, P, K, temperature, humidity, ph, rainfall]

#             fig = go.Figure([
#                 go.Bar(name="Your Input", x=FEATURE_LABELS, y=user_vals,
#                        marker_color="#1f77b4",
#                        text=[round(v,2) for v in user_vals], textposition="outside"),
#                 go.Bar(name=f"Ideal for {pred_crop}", x=FEATURE_LABELS,
#                        y=ideal.values, marker_color="#2ca02c",
#                        text=ideal.values, textposition="outside"),
#             ])
#             fig.update_layout(barmode="group",
#                               title=f"Your Input vs Ideal: {pred_crop}",
#                               height=400)
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown("---")

#             st.subheader("📋 Input Summary")
#             summ = pd.DataFrame({
#                 "Feature": ["Nitrogen (mg/kg)","Phosphorus (mg/kg)","Potassium (mg/kg)",
#                             "Temperature (°C)","Humidity (%)","Soil pH","Rainfall (mm)"],
#                 "Value":    [N, P, K, temperature, humidity, ph, rainfall],
#                 "Category": [nitrogen_category(N), phosphorus_category(P),
#                              potassium_category(K), temperature_category(temperature),
#                              humidity_category(humidity), ph_category(ph),
#                              rainfall_category(rainfall)]
#             })
#             st.dataframe(summ, use_container_width=True)
#             st.markdown("---")

#             st.subheader("🌱 Crop Advice")
#             crop_advice = {
#                 "rice":        "Requires high rainfall (150–300mm), high humidity (80–90%), and slightly acidic soil (pH 5.5–6.5).",
#                 "maize":       "Needs moderate rainfall, moderate temperature (21–27°C), and fertile loamy soil (pH 5.5–7.0).",
#                 "jute":        "Thrives in high humidity and rainfall. Requires warm climate (25–35°C) and alluvial soil.",
#                 "cotton":      "Grows well in well-drained black soil (pH 6–8), warm climate (21–35°C), and moderate rainfall.",
#                 "coconut":     "Requires tropical climate, high humidity (70–80%), and sandy loam soil.",
#                 "papaya":      "Needs warm climate (25–30°C), well-drained soil, moderate rainfall, and high humidity.",
#                 "banana":      "Requires rich loamy soil, high humidity, warm temperature (26–30°C), and regular rainfall.",
#                 "mango":       "Prefers deep well-drained soil, dry season at flowering, and tropical/subtropical climate.",
#                 "grapes":      "Needs well-drained sandy loam, dry hot summers and cool winters.",
#                 "watermelon":  "Requires warm climate (25–35°C), sandy loam soil, and moderate to high rainfall.",
#                 "muskmelon":   "Grows best in warm climate, sandy soil with good drainage, and moderate humidity.",
#                 "apple":       "Requires cool climate (cold winters for dormancy), loamy soil, and moderate rainfall.",
#                 "orange":      "Needs subtropical climate, well-drained sandy loam, and moderate rainfall (750–1200mm).",
#                 "pomegranate": "Drought-tolerant, wide pH range (5.5–7.5), grows well in semi-arid regions.",
#                 "lentil":      "Cool season crop, well-drained loamy soil (pH 6–8), low rainfall.",
#                 "blackgram":   "Warm climate (25–35°C), well-drained loamy soil, moderate rainfall (600–800mm).",
#                 "mungbean":    "Warm season, sandy loam soil, short rainfall period, moderate temperature (28–30°C).",
#                 "mothbeans":   "Drought-tolerant, arid/semi-arid regions, sandy soil, very low rainfall.",
#                 "pigeonpeas":  "Drought-tolerant legume, well-drained soil (pH 5–7), moderate rainfall.",
#                 "kidneybeans": "Cool temperature, well-drained fertile loam (pH 6–7), moderate rainfall.",
#                 "chickpea":    "Cool season, drought-tolerant, loamy soil (pH 5.5–7), low rainfall.",
#                 "coffee":      "Tropical climate (15–28°C), high humidity, acidic well-drained soil (pH 6–6.5), high rainfall."
#             }
#             advice = crop_advice.get(
#                 pred_crop.lower(),
#                 f"{pred_crop.capitalize()} is suited to the conditions you entered. "
#                 "Consult local agricultural guidelines for detailed advice."
#             )
#             st.info(f"🌿 **{pred_crop.capitalize()} Advice:** {advice}")
#             st.markdown("---")

#             st.subheader("🧪 Soil & Climate Summary")
#             sc1, sc2 = st.columns(2)
#             with sc1:
#                 if ph < 6:
#                     st.warning("⚠️ **Acidic Soil** — add lime to raise pH.")
#                 elif ph > 7.5:
#                     st.warning("⚠️ **Alkaline Soil** — add sulfur to lower pH.")
#                 else:
#                     st.success("✅ **Neutral Soil pH** — ideal for most crops.")
#                 n_cat = nitrogen_category(N)
#                 if n_cat == "Low":
#                     st.warning("⚠️ Low Nitrogen — apply urea or nitrogen-rich fertilizer.")
#                 elif n_cat == "High":
#                     st.info("ℹ️ High Nitrogen — reduce fertilizer application.")
#                 else:
#                     st.success("✅ Nitrogen level is balanced.")
#             with sc2:
#                 if rainfall > 200:
#                     st.info("🌧 High rainfall — ensure good field drainage.")
#                 elif rainfall < 80:
#                     st.info("☀️ Low rainfall — consider drip irrigation.")
#                 else:
#                     st.success("✅ Moderate rainfall — suitable for most crops.")
#                 t_cat = temperature_category(temperature)
#                 if t_cat == "Cool":
#                     st.info("❄️ Cool climate — suitable for wheat, lentil, chickpea.")
#                 elif t_cat == "Hot":
#                     st.info("🔥 Hot climate — suitable for tropical/summer crops.")
#                 else:
#                     st.success("✅ Moderate temperature — good for most crops.")

#         except Exception as e:
#             st.error(f"❌ Prediction failed: `{str(e)}`")

# # =========================================================
# # PAGE: DISEASE DETECTION
# # =========================================================

# elif page == "🌿 Disease Detection":

#     st.header("🌿 Plant Disease Detection System")
#     st.markdown("---")

#     if disease_error:
#         st.error(
#             f"❌ Disease model not found.\n\n"
#             f"**Error:** `{disease_error}`\n\n"
#             "Run `train_disease_model.py` first to train and save the model, "
#             "then restart the app."
#         )
#         st.stop()

#     st.subheader("📤 Upload a Plant Leaf Image")
#     st.caption(
#         "Upload a clear photo of a plant leaf. "
#         "The AI will predict whether it is healthy or diseased."
#     )

#     uploaded = st.file_uploader(
#         "Drag & drop or click to browse",
#         type=["jpg","jpeg","png","webp"],
#         label_visibility="collapsed"
#     )

#     if uploaded is not None:

#         image = Image.open(uploaded).convert("RGB")

#         col_img, col_res = st.columns([1, 1])

#         with col_img:
#             st.image(image, caption="Uploaded Leaf Image", use_column_width=True)

#         img_resized = image.resize((128, 128))
#         img_array   = np.array(img_resized, dtype="float32") / 255.0
#         img_array   = np.expand_dims(img_array, axis=0)

#         try:
#             preds         = disease_model.predict(img_array, verbose=0)
#             pred_idx      = int(np.argmax(preds))
#             disease_name  = disease_encoder.inverse_transform([pred_idx])[0]
#             confidence    = float(np.max(preds)) * 100
#             all_probs     = preds[0]

#             with col_res:
#                 st.markdown('<div class="disease-card">', unsafe_allow_html=True)

#                 if confidence >= 75:
#                     st.success(f"✅ **Predicted:** {disease_name.replace('_', ' ')}")
#                 elif confidence >= 50:
#                     st.warning(f"⚠️ **Predicted (Moderate Confidence):** {disease_name.replace('_', ' ')}")
#                 else:
#                     st.error(f"❓ **Low Confidence Prediction:** {disease_name.replace('_', ' ')}")

#                 st.metric("Confidence", f"{confidence:.2f}%")
#                 st.progress(int(min(confidence, 100)))

#                 is_healthy = "healthy" in disease_name.lower()
#                 if is_healthy:
#                     st.success("🌿 Your plant appears **HEALTHY**!")
#                 else:
#                     st.error("🦠 Disease detected — see treatment advice below.")

#                 st.markdown('</div>', unsafe_allow_html=True)

#             st.markdown("---")

#             st.subheader("💊 Treatment & Care Advice")

#             disease_advice = {
#                 "Tomato_healthy":
#                     ("✅ Healthy Plant", "success",
#                      "Maintain regular watering (avoid overhead irrigation), "
#                      "balanced fertilization, and good air circulation."),
#                 "Tomato_Early_blight":
#                     ("⚠️ Early Blight (Alternaria solani)", "warning",
#                      "Remove infected lower leaves immediately. Apply **mancozeb** "
#                      "or **chlorothalonil** fungicide every 7–10 days. Avoid overhead "
#                      "watering and ensure good air flow around plants."),
#                 "Tomato_Late_blight":
#                     ("🚨 Late Blight (Phytophthora infestans)", "error",
#                      "Act fast — this spreads rapidly. Remove and destroy infected "
#                      "plants. Apply **copper-based fungicide** or **metalaxyl**. "
#                      "Avoid watering leaves; water at the base."),
#                 "Tomato_Leaf_Mold":
#                     ("⚠️ Leaf Mold (Passalora fulva)", "warning",
#                      "Improve greenhouse/field air circulation. Reduce humidity. "
#                      "Apply **copper** or **sulfur-based fungicide**. Remove affected leaves."),
#                 "Tomato_Septoria_leaf_spot":
#                     ("⚠️ Septoria Leaf Spot", "warning",
#                      "Remove infected leaves. Apply **mancozeb** fungicide. "
#                      "Rotate crops and avoid overhead irrigation."),
#                 "Tomato_Spider_mites":
#                     ("⚠️ Spider Mites", "warning",
#                      "Spray plants with water to dislodge mites. "
#                      "Apply **neem oil** or **insecticidal soap**. "
#                      "Introduce predatory mites as biological control."),
#                 "Tomato_Target_Spot":
#                     ("⚠️ Target Spot", "warning",
#                      "Remove infected leaves. Apply **azoxystrobin** or "
#                      "**chlorothalonil** fungicide. Ensure good air circulation."),
#                 "Tomato_Mosaic_Virus":
#                     ("🚨 Tomato Mosaic Virus", "error",
#                      "No cure available. Remove and destroy infected plants to prevent spread. "
#                      "Control aphids (virus vectors) with **neem oil**. Sanitize tools."),
#                 "Tomato_Yellow_Leaf_Curl_Virus":
#                     ("🚨 Yellow Leaf Curl Virus", "error",
#                      "Spread by whiteflies — apply **imidacloprid** to control them. "
#                      "Remove infected plants. Use virus-resistant tomato varieties."),
#                 "Tomato_Bacterial_spot":
#                     ("⚠️ Bacterial Spot (Xanthomonas)", "warning",
#                      "Apply **copper-based bactericide** (copper hydroxide). "
#                      "Avoid working with plants when wet. Practice crop rotation."),
#                 "Potato_healthy":
#                     ("✅ Healthy Potato Plant", "success",
#                      "Keep soil consistently moist but not waterlogged. "
#                      "Earth up around stems to prevent greening."),
#                 "Potato_Early_blight":
#                     ("⚠️ Potato Early Blight", "warning",
#                      "Apply **mancozeb** or **chlorothalonil** fungicide. "
#                      "Remove heavily infected leaves. Avoid nitrogen excess."),
#                 "Potato_Late_blight":
#                     ("🚨 Potato Late Blight (Phytophthora infestans)", "error",
#                      "Most destructive potato disease. Apply **metalaxyl** or "
#                      "**cymoxanil** fungicide immediately. Destroy infected tubers. "
#                      "Do not compost infected material."),
#                 "Pepper,_bell_healthy":
#                     ("✅ Healthy Bell Pepper", "success",
#                      "Maintain consistent moisture, full sun, and warm temperatures (20–30°C)."),
#                 "Pepper,_bell_Bacterial_spot":
#                     ("⚠️ Bacterial Spot (Xanthomonas)", "warning",
#                      "Apply **copper hydroxide** spray. Avoid overhead watering. "
#                      "Use certified disease-free seeds."),
#                 "Corn_(maize)_healthy":
#                     ("✅ Healthy Maize Plant", "success",
#                      "Ensure adequate nitrogen levels and consistent irrigation."),
#                 "Corn_(maize)_Common_rust":
#                     ("⚠️ Common Rust (Puccinia sorghi)", "warning",
#                      "Apply **propiconazole** fungicide early. "
#                      "Use rust-resistant hybrid varieties."),
#                 "Corn_(maize)_Northern_Leaf_Blight":
#                     ("⚠️ Northern Leaf Blight", "warning",
#                      "Apply **azoxystrobin** or **propiconazole** at early stages. "
#                      "Practice crop rotation; avoid corn-after-corn."),
#                 "Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot":
#                     ("⚠️ Gray Leaf Spot", "warning",
#                      "Apply **strobilurin** fungicide. Choose tolerant hybrids. "
#                      "Till crop residues to reduce inoculum."),
#                 "Apple_healthy":
#                     ("✅ Healthy Apple Tree", "success",
#                      "Prune for good air flow. Apply dormant oil spray in late winter."),
#                 "Apple_Apple_scab":
#                     ("⚠️ Apple Scab (Venturia inaequalis)", "warning",
#                      "Apply **myclobutanil** or **captan** fungicide at bud break. "
#                      "Remove fallen leaves to reduce infection source."),
#                 "Apple_Black_rot":
#                     ("⚠️ Black Rot (Botryosphaeria obtusa)", "warning",
#                      "Prune out dead/infected wood. Apply **captan** fungicide. "
#                      "Remove mummified fruits from the tree."),
#                 "Apple_Cedar_apple_rust":
#                     ("⚠️ Cedar Apple Rust", "warning",
#                      "Apply **myclobutanil** fungicide early in spring. "
#                      "Remove nearby cedar/juniper trees if possible."),
#             }

#             advice_key = disease_name
#             if advice_key in disease_advice:
#                 diag_label, diag_type, diag_text = disease_advice[advice_key]
#                 if diag_type == "success":
#                     st.success(f"**{diag_label}**\n\n{diag_text}")
#                 elif diag_type == "warning":
#                     st.warning(f"**{diag_label}**\n\n{diag_text}")
#                 else:
#                     st.error(f"**{diag_label}**\n\n{diag_text}")
#             else:
#                 if is_healthy:
#                     st.success(
#                         f"**{disease_name.replace('_',' ')}** — Plant appears healthy. "
#                         "Maintain good watering, fertilization, and pest monitoring practices."
#                     )
#                 else:
#                     st.warning(
#                         f"**Detected: {disease_name.replace('_',' ')}**\n\n"
#                         "🌿 General advice:\n"
#                         "• Remove visibly infected leaves immediately.\n"
#                         "• Apply an appropriate fungicide or bactericide.\n"
#                         "• Improve air circulation and avoid overhead irrigation.\n"
#                         "• Consult your local agricultural extension officer for a precise diagnosis."
#                     )

#             st.markdown("---")

#             st.subheader("📊 Prediction Confidence (All Classes)")

#             prob_df = pd.DataFrame({
#                 "Disease":    disease_encoder.classes_,
#                 "Confidence": all_probs
#             }).sort_values("Confidence", ascending=False)

#             fig = px.bar(
#                 prob_df, x="Disease", y="Confidence",
#                 color="Confidence",
#                 text=(prob_df["Confidence"]*100).round(2).astype(str)+"%",
#                 color_continuous_scale="Reds",
#                 title="Model Confidence per Disease Class"
#             )
#             fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#             fig.update_layout(xaxis_tickangle=-35, height=430, showlegend=False)
#             fig.update_coloraxes(colorbar=colorbar_cfg())
#             st.plotly_chart(fig, use_container_width=True)

#             st.markdown("---")

#             st.subheader("📝 General Plant Health Tips")
#             t1, t2, t3 = st.columns(3)
#             t1.info("💧 **Water at the Base**\nAvoid wetting leaves — wet leaves promote fungal disease.")
#             t2.info("🌬️ **Air Circulation**\nProper spacing between plants reduces humidity and disease spread.")
#             t3.info("🔄 **Crop Rotation**\nRotate crops every season to break disease and pest cycles.")

#         except Exception as e:
#             st.error(f"❌ Disease prediction failed: `{str(e)}`")

#     else:
#         st.info(
#             "👆 Upload a leaf image above to get started.\n\n"
#             "**Supported formats:** JPG, JPEG, PNG, WEBP\n\n"
#             "**Tips for best results:**\n"
#             "• Use a clear, well-lit photo of a single leaf\n"
#             "• Avoid blurry or dark images\n"
#             "• Capture the affected area clearly\n"
#             "• Image size: any — the model resizes automatically to 128×128"
#         )

#         st.markdown("---")
#         st.subheader("🌿 Diseases This Model Can Detect")
#         st.caption(
#             "The model is trained on the classes present in your Disease_Dataset folder. "
#             "Below are the common diseases supported when using the PlantVillage dataset."
#         )

#         sample_diseases = [
#             "Tomato — Healthy",        "Tomato — Early Blight",
#             "Tomato — Late Blight",    "Tomato — Leaf Mold",
#             "Tomato — Mosaic Virus",   "Tomato — Spider Mites",
#             "Potato — Healthy",        "Potato — Early Blight",
#             "Potato — Late Blight",    "Pepper — Bacterial Spot",
#             "Corn — Common Rust",      "Corn — Northern Leaf Blight",
#             "Apple — Apple Scab",      "Apple — Black Rot",
#         ]

#         cols = st.columns(3)
#         for i, d in enumerate(sample_diseases):
#             cols[i % 3].write(f"• {d}")


# import os
# import io
# import numpy as np
# import pandas as pd
# import joblib
# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.io as pio
# from PIL import Image

# # ── Multilingual Voice Assistant: optional deps, fail gracefully ──
# try:
#     import speech_recognition as sr
#     from gtts import gTTS
#     from audio_recorder_streamlit import audio_recorder
#     VOICE_DEPS_OK = True
#     voice_import_error = None
# except Exception as _e:
#     VOICE_DEPS_OK = False
#     voice_import_error = str(_e)

# try:
#     from groq import Groq
#     GROQ_SDK_OK = True
# except Exception:
#     GROQ_SDK_OK = False

# # Load variables from a .env file (e.g. GROQ_API_KEY=...) into os.environ.
# DOTENV_PATH_FOUND = None
# try:
#     from dotenv import load_dotenv, find_dotenv
#     _dotenv_path = find_dotenv(usecwd=True)
#     if not _dotenv_path:
#         # Fallback: look right next to this script, regardless of which
#         # folder `streamlit run` was launched from.
#         _candidate = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
#         if os.path.exists(_candidate):
#             _dotenv_path = _candidate
#     if _dotenv_path:
#         DOTENV_PATH_FOUND = _dotenv_path
#     load_dotenv(_dotenv_path if _dotenv_path else None)
#     DOTENV_OK = True
# except Exception:
#     DOTENV_OK = False

# # =========================================================
# # ===== GLOBAL PLOTLY THEME ================================
# # =========================================================

# pio.templates["krishi"] = go.layout.Template(
#     layout=go.Layout(
#         paper_bgcolor="#ffffff",
#         plot_bgcolor="#f9fdf9",
#         font=dict(
#             color="#1a1a1a",
#             family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
#         ),
#         title=dict(font=dict(color="#0d2e0d", size=16)),
#         xaxis=dict(
#             color="#1a1a1a",
#             gridcolor="#d4ecd4",
#             linecolor="#81c784",
#             tickfont=dict(color="#1a1a1a"),
#             title=dict(font=dict(color="#1a1a1a")),
#             zerolinecolor="#c8e6c9",
#         ),
#         yaxis=dict(
#             color="#1a1a1a",
#             gridcolor="#d4ecd4",
#             linecolor="#81c784",
#             tickfont=dict(color="#1a1a1a"),
#             title=dict(font=dict(color="#1a1a1a")),
#             zerolinecolor="#c8e6c9",
#         ),
#         legend=dict(
#             bgcolor="#ffffff",
#             bordercolor="#c8e6c9",
#             font=dict(color="#1a1a1a"),
#         ),
#         coloraxis=dict(
#             colorbar=dict(
#                 tickfont=dict(color="#1a1a1a", size=12),
#                 tickcolor="#1a1a1a",
#                 title=dict(font=dict(color="#1a1a1a", size=13), side="right"),
#                 bgcolor="#ffffff",
#                 outlinecolor="#c8e6c9",
#                 outlinewidth=1,
#                 bordercolor="#c8e6c9",
#                 borderwidth=1,
#                 len=0.85,
#             )
#         ),
#         polar=dict(
#             bgcolor="#f9fdf9",
#             radialaxis=dict(color="#1a1a1a", gridcolor="#d4ecd4"),
#             angularaxis=dict(color="#1a1a1a", gridcolor="#d4ecd4"),
#         ),
#         colorway=["#2e7d32","#1f77b4","#ff7f0e","#d62728","#9467bd",
#                   "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"],
#     )
# )
# pio.templates.default = "krishi"

# # =========================================================
# # ================= PAGE CONFIG ===========================
# # =========================================================

# st.set_page_config(
#     page_title="Krishi AI — Smart Farming Assistant",
#     page_icon="🌱",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # =========================================================
# # ================= CUSTOM CSS ============================
# # =========================================================

# st.markdown("""
# <style>
#     /* ── Reset & Base ── */
#     html, body, [class*="css"] {
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }

#     /* ── Main app background: light green-white ── */
#     .stApp {
#         background-color: #f0f7f0;
#     }

#     /* ── ALL main content text: DARK (visible on light bg) ── */
#     .stApp p,
#     .stApp span,
#     .stApp div,
#     .stApp label,
#     .stApp li,
#     .stApp td,
#     .stApp th,
#     .stApp caption,
#     .stApp small,
#     .stApp strong,
#     .stApp em {
#         color: #1a1a1a !important;
#     }

#     /* ── Headings: dark green ── */
#     .stApp h1, .stApp h2, .stApp h3,
#     .stApp h4, .stApp h5, .stApp h6 {
#         color: #0d2e0d !important;
#         font-weight: 700;
#     }

#     /* ── Markdown text ── */
#     .stMarkdown, .stMarkdown p,
#     .stMarkdown span, .stMarkdown div,
#     .stMarkdown li, .stMarkdown strong,
#     .stMarkdown em {
#         color: #1a1a1a !important;
#     }

#     /* ── Sidebar: dark green gradient — WHITE text ── */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #0d2e0d 0%, #1a5c2a 50%, #2e7d32 100%);
#     }
#     [data-testid="stSidebar"],
#     [data-testid="stSidebar"] *,
#     [data-testid="stSidebar"] p,
#     [data-testid="stSidebar"] span,
#     [data-testid="stSidebar"] div,
#     [data-testid="stSidebar"] label,
#     [data-testid="stSidebar"] h1,
#     [data-testid="stSidebar"] h2,
#     [data-testid="stSidebar"] h3,
#     [data-testid="stSidebar"] strong,
#     [data-testid="stSidebar"] em,
#     [data-testid="stSidebar"] li,
#     [data-testid="stSidebar"] .stMarkdown,
#     [data-testid="stSidebar"] .stMarkdown p,
#     [data-testid="stSidebar"] .stMarkdown span,
#     [data-testid="stSidebar"] .stMarkdown div,
#     [data-testid="stSidebar"] .stCaption,
#     [data-testid="stSidebar"] .stSelectbox label {
#         color: #ffffff !important;
#     }

#     /* ── Header banner: WHITE text on dark bg ── */
#     .krishi-header {
#         background: linear-gradient(135deg, #0d2e0d, #1b5e20, #2e7d32, #388e3c);
#         padding: 2.2rem 1.5rem 1.8rem 1.5rem;
#         border-radius: 18px;
#         text-align: center;
#         margin-bottom: 1.8rem;
#         box-shadow: 0 6px 28px rgba(13,46,13,0.35);
#     }
#     .krishi-header h1 {
#         color: #ffffff !important;
#         font-size: 2.6rem;
#         margin: 0;
#         letter-spacing: 2px;
#         text-shadow: 0 2px 8px rgba(0,0,0,0.4);
#     }
#     .krishi-header p {
#         color: #c8e6c9 !important;
#         margin: 0.4rem 0 0 0;
#         font-size: 1.05rem;
#     }

#     /* ── Metric cards: WHITE bg, DARK text ── */
#     [data-testid="stMetric"] {
#         background: #ffffff !important;
#         border-radius: 12px !important;
#         padding: 0.9rem 1.1rem !important;
#         border-left: 4px solid #2e7d32 !important;
#         box-shadow: 0 3px 10px rgba(0,0,0,0.09) !important;
#     }
#     [data-testid="stMetric"] *,
#     [data-testid="stMetric"] label,
#     [data-testid="stMetric"] div,
#     [data-testid="stMetricLabel"],
#     [data-testid="stMetricLabel"] p,
#     [data-testid="stMetricLabel"] div,
#     [data-testid="stMetricValue"],
#     [data-testid="stMetricValue"] div {
#         color: #0d2e0d !important;
#     }
#     [data-testid="stMetricLabel"] p {
#         color: #2e7d32 !important;
#         font-weight: 600;
#     }
#     [data-testid="stMetricValue"] {
#         font-size: 1.6rem !important;
#         font-weight: 700 !important;
#     }

#     /* ── Dataframe: DARK text on light bg ── */
#     .stDataFrame,
#     .stDataFrame *,
#     [data-testid="stDataFrameContainer"],
#     [data-testid="stDataFrameContainer"] * {
#         color: #1a1a1a !important;
#     }
#     [data-testid="stDataFrameContainer"] {
#         border: 1px solid #c8e6c9;
#         border-radius: 10px;
#     }

#     /* ── Chat bubbles ── */
#     .chat-user {
#         background: #1b5e20;
#         border-radius: 16px 16px 4px 16px;
#         padding: 0.75rem 1.2rem;
#         margin: 0.4rem 0;
#         max-width: 80%;
#         margin-left: auto;
#         color: #ffffff !important;
#         font-weight: 500;
#         box-shadow: 0 2px 8px rgba(27,94,32,0.25);
#     }
#     .chat-user * { color: #ffffff !important; }

#     .chat-ai {
#         background: #ffffff;
#         border-radius: 16px 16px 16px 4px;
#         padding: 0.75rem 1.2rem;
#         margin: 0.4rem 0;
#         max-width: 85%;
#         border-left: 3px solid #43a047;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#         color: #1a1a1a !important;
#     }
#     .chat-ai * { color: #1a1a1a !important; }

#     .chat-label-user {
#         text-align: right;
#         font-size: 0.75rem;
#         color: #2e7d32 !important;
#         margin-bottom: 3px;
#         font-weight: 600;
#     }
#     .chat-label-ai {
#         font-size: 0.75rem;
#         color: #2e7d32 !important;
#         margin-bottom: 3px;
#         font-weight: 600;
#     }

#     /* ── Disease result card: WHITE bg, DARK text ── */
#     .disease-card {
#         background: #ffffff;
#         border-radius: 16px;
#         padding: 1.6rem;
#         box-shadow: 0 4px 18px rgba(0,0,0,0.10);
#         margin: 1rem 0;
#         border-top: 4px solid #2e7d32;
#     }
#     .disease-card,
#     .disease-card * {
#         color: #1a1a1a !important;
#     }

#     /* ── Buttons: WHITE text on dark green bg ── */
#     .stButton > button {
#         background: linear-gradient(135deg, #1b5e20, #2e7d32, #43a047) !important;
#         color: #ffffff !important;
#         border: none !important;
#         border-radius: 10px !important;
#         font-weight: 700 !important;
#         font-size: 0.95rem !important;
#         padding: 0.55rem 1.2rem !important;
#         transition: all 0.2s ease !important;
#         letter-spacing: 0.3px;
#     }
#     .stButton > button:hover {
#         transform: translateY(-2px) !important;
#         box-shadow: 0 6px 16px rgba(46,125,50,0.4) !important;
#         background: linear-gradient(135deg, #155218, #256427, #36883a) !important;
#     }
#     .stButton > button *,
#     .stButton > button span,
#     .stButton > button p {
#         color: #ffffff !important;
#     }

#     /* ── Alert boxes: DARK text on coloured bg ── */
#     div[data-testid="stNotification"] {
#         border-radius: 12px !important;
#     }
#     /* SUCCESS box */
#     [data-testid="stNotification"][kind="success"],
#     div.stSuccess,
#     div.stSuccess > div {
#         background-color: #d4edda !important;
#         border-color: #28a745 !important;
#         border-radius: 12px !important;
#     }
#     div.stSuccess p,
#     div.stSuccess div,
#     div.stSuccess span,
#     div.stSuccess li,
#     div.stSuccess strong,
#     div.stSuccess em {
#         color: #155724 !important;
#     }
#     /* INFO box */
#     div.stInfo,
#     div.stInfo > div {
#         background-color: #d1ecf1 !important;
#         border-color: #17a2b8 !important;
#         border-radius: 12px !important;
#     }
#     div.stInfo p,
#     div.stInfo div,
#     div.stInfo span,
#     div.stInfo li,
#     div.stInfo strong,
#     div.stInfo em {
#         color: #0c5460 !important;
#     }
#     /* WARNING box */
#     div.stWarning,
#     div.stWarning > div {
#         background-color: #fff3cd !important;
#         border-color: #ffc107 !important;
#         border-radius: 12px !important;
#     }
#     div.stWarning p,
#     div.stWarning div,
#     div.stWarning span,
#     div.stWarning li,
#     div.stWarning strong,
#     div.stWarning em {
#         color: #856404 !important;
#     }
#     /* ERROR box */
#     div.stError,
#     div.stError > div {
#         background-color: #f8d7da !important;
#         border-color: #dc3545 !important;
#         border-radius: 12px !important;
#     }
#     div.stError p,
#     div.stError div,
#     div.stError span,
#     div.stError li,
#     div.stError strong,
#     div.stError em {
#         color: #721c24 !important;
#     }

#     /* ── Selectbox & input labels: DARK text ── */
#     .stSelectbox label,
#     .stSlider label,
#     .stTextInput label,
#     .stFileUploader label,
#     .stMultiSelect label {
#         color: #1a1a1a !important;
#         font-weight: 600 !important;
#     }

#     /* ── Text input box ── */
#     .stTextInput input {
#         background: #ffffff !important;
#         color: #1a1a1a !important;
#         border: 1.5px solid #81c784 !important;
#         border-radius: 8px !important;
#     }
#     .stTextInput input::placeholder {
#         color: #5a8c5a !important;
#     }
#     .stTextInput input:focus {
#         border-color: #2e7d32 !important;
#         box-shadow: 0 0 0 2px rgba(46,125,50,0.2) !important;
#     }

#     /* ── Slider: DARK labels ── */
#     .stSlider [data-testid="stTickBar"] div,
#     [data-testid="stSlider"] div[data-testid="stThumbValue"],
#     [data-testid="stSlider"] * {
#         color: #1a1a1a !important;
#     }

#     /* ── Plotly chart container background ── */
#     .js-plotly-plot, .plotly, .plot-container {
#         background: #ffffff !important;
#         border-radius: 12px;
#     }

#     /* ── Plotly SVG text: DARK on white chart bg ── */
#     .js-plotly-plot .plotly .xtick text,
#     .js-plotly-plot .plotly .ytick text,
#     .js-plotly-plot .plotly .xtitle,
#     .js-plotly-plot .plotly .ytitle,
#     .js-plotly-plot .plotly .g-xtitle text,
#     .js-plotly-plot .plotly .g-ytitle text,
#     .js-plotly-plot .plotly .gtitle,
#     .js-plotly-plot .plotly .cbaxis text,
#     .js-plotly-plot .plotly .cbtitle text,
#     .js-plotly-plot .plotly .legend text {
#         fill: #1a1a1a !important;
#     }

#     /* ── Plotly bar text labels ON bars: WHITE ── */
#     .js-plotly-plot .plotly .bartext text,
#     .js-plotly-plot .plotly g.points text,
#     .js-plotly-plot .plotly .textpoint text,
#     .js-plotly-plot .plotly .trace text {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly colorbar background ── */
#     .js-plotly-plot .plotly .cbfill,
#     .js-plotly-plot .plotly rect.cbbg {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly modebar ── */
#     .modebar-container {
#         background: rgba(0,0,0,0.6) !important;
#         border-radius: 6px !important;
#     }
#     .modebar-btn path { fill: #ffffff !important; }
#     .modebar-btn:hover path { fill: #cccccc !important; }

#     /* ── Dataframe toolbar ── */
#     [data-testid="stElementToolbar"] {
#         background: #2e7d32 !important;
#         border-radius: 8px !important;
#         padding: 2px 4px !important;
#     }
#     [data-testid="stElementToolbar"] button svg path,
#     [data-testid="stElementToolbar"] button svg rect,
#     [data-testid="stElementToolbar"] button svg circle {
#         fill: #ffffff !important;
#         stroke: #ffffff !important;
#     }
#     [data-testid="stElementToolbar"] button:hover {
#         background: #1b5e20 !important;
#         border-radius: 4px !important;
#     }

#     /* ── Divider ── */
#     hr {
#         border-color: #a5d6a7;
#         margin: 1.8rem 0;
#     }

#     /* ── Caption text ── */
#     .stCaption,
#     [data-testid="stCaptionContainer"],
#     [data-testid="stCaptionContainer"] p {
#         color: #4a7c4a !important;
#     }

#     /* ── Selectbox dropdown: DARK text ── */ 
            
#     [data-testid="stSelectbox"] div[data-baseweb="select"] {
#         background: #0b1220 !important;  /* dark background */
#     }

#     [data-testid="stSelectbox"] div[data-baseweb="select"] *,
#     [data-testid="stSelectbox"] span {
#         color: #ffffff !important;       /* white text */
#     }
                
    

#     /* ── File uploader ── */
#     [data-testid="stFileUploader"] {
#         background: #ffffff !important;
#         border: 2px dashed #81c784 !important;
#         border-radius: 10px !important;
#     }
#     [data-testid="stFileUploader"] *,
#     [data-testid="stFileUploader"] p,
#     [data-testid="stFileUploader"] span,
#     [data-testid="stFileUploader"] div {
#         color: #1a1a1a !important;
#     }

#     /* ── Progress bar ── */
#     [data-testid="stProgressBar"] > div {
#         background-color: #2e7d32 !important;
#     }

#     /* ── Tabs ── */
#     [data-testid="stTabs"] [data-baseweb="tab"] {
#         color: #1a1a1a !important;
#     }
#     [data-testid="stTabs"] [aria-selected="true"] {
#         color: #2e7d32 !important;
#         border-bottom-color: #2e7d32 !important;
#     }

#     /* ── Column containers ── */
#     [data-testid="column"] { padding: 0 0.4rem; }

#     /* ── Scrollbar ── */
#     ::-webkit-scrollbar { width: 7px; height: 7px; }
#     ::-webkit-scrollbar-track { background: #e8f5e9; }
#     ::-webkit-scrollbar-thumb { background: #81c784; border-radius: 4px; }
#     ::-webkit-scrollbar-thumb:hover { background: #2e7d32; }
# </style>
# """, unsafe_allow_html=True)

# # =========================================================
# # ================= MULTILINGUAL VOICE ASSISTANT ==========
# # =========================================================
# # Setup:
# #   pip install SpeechRecognition gTTS audio-recorder-streamlit groq python-dotenv
# #   Put your key in a .env file (same folder as app.py):
# #       GROQ_API_KEY=gsk_....
# #   — or in .streamlit/secrets.toml:
# #       GROQ_API_KEY = "gsk_...."
# #   (Get a free key at https://console.groq.com/keys)
# # (Swap the LLM call in get_ai_response() for another provider
# #  if you prefer — only that one function needs to change.)

# LANGUAGES = {
#     "English":            {"speech": "en-IN", "tts": "en"},
#     "हिंदी (Hindi)":       {"speech": "hi-IN", "tts": "hi"},
#     "मराठी (Marathi)":     {"speech": "mr-IN", "tts": "mr"},
#     "বাংলা (Bengali)":     {"speech": "bn-IN", "tts": "bn"},
#     "தமிழ் (Tamil)":       {"speech": "ta-IN", "tts": "ta"},
#     "తెలుగు (Telugu)":     {"speech": "te-IN", "tts": "te"},
#     "ਪੰਜਾਬੀ (Punjabi)":    {"speech": "pa-IN", "tts": "pa"},
#     "ગુજરાતી (Gujarati)":  {"speech": "gu-IN", "tts": "gu"},
#     "ಕನ್ನಡ (Kannada)":     {"speech": "kn-IN", "tts": "kn"},
#     "മലയാളം (Malayalam)":  {"speech": "ml-IN", "tts": "ml"},
# }


# @st.cache_resource(show_spinner=False)
# def get_groq_client():
#     if not GROQ_SDK_OK:
#         return None
#     # Check the environment variable first (works even with no secrets.toml).
#     api_key = os.environ.get("GROQ_API_KEY")
#     # st.secrets raises an error (not just empty) if no secrets.toml exists
#     # anywhere — so this lookup must be wrapped in try/except.
#     if not api_key:
#         try:
#             api_key = st.secrets.get("GROQ_API_KEY")
#         except Exception:
#             api_key = None
#     if not api_key:
#         return None
#     try:
#         return Groq(api_key=api_key)
#     except Exception as e:
#         # e.g. "got an unexpected keyword argument 'proxies'" — a version
#         # mismatch between the groq package and httpx. Don't crash the
#         # whole app; report it in the diagnostics panel instead.
#         global GROQ_INIT_ERROR
#         GROQ_INIT_ERROR = str(e)
#         return None


# GROQ_INIT_ERROR = None


# groq_client = get_groq_client()


# def speech_to_text(audio_bytes, lang_code):
#     """Convert recorded microphone audio (WAV bytes) into text, in the
#     farmer's chosen Indian language, using free Google speech recognition."""
#     recognizer = sr.Recognizer()
#     try:
#         with io.BytesIO(audio_bytes) as wav_io:
#             with sr.AudioFile(wav_io) as source:
#                 audio_data = recognizer.record(source)
#         text = recognizer.recognize_google(audio_data, language=lang_code)
#         return text, None
#     except sr.UnknownValueError:
#         return None, "🙇 Sorry, I couldn't understand the audio clearly. Please try again, speaking slowly and close to the mic."
#     except sr.RequestError as e:
#         return None, f"⚠️ Speech recognition service error: {e}"
#     except Exception as e:
#         return None, f"⚠️ Could not process the audio: {e}"


# def text_to_speech(text, tts_lang_code):
#     """Synthesize speech audio (MP3 bytes) from text in real time using
#     gTTS — generated fresh every call, never pre-recorded."""
#     try:
#         clean_text = text.replace("**", "").replace("*", "")
#         tts = gTTS(text=clean_text, lang=tts_lang_code)
#         buf = io.BytesIO()
#         tts.write_to_fp(buf)
#         buf.seek(0)
#         return buf.read()
#     except Exception:
#         return None


# def rule_based_fallback(user_text):
#     """Tiny keyword fallback (English) so the assistant still responds
#     even if no LLM API key has been configured yet."""
#     q = user_text.lower()
#     if any(k in q for k in ["fertilizer", "npk", "urea", "nitrogen"]):
#         return "Get a soil test, then choose N-P-K fertilizer based on the deficiency it shows."
#     if any(k in q for k in ["disease", "pest", "blight", "fungus"]):
#         return "Try the Disease Detection tab — upload a leaf photo for a diagnosis and treatment advice."
#     if any(k in q for k in ["water", "irrigation", "rain"]):
#         return "Drip irrigation and morning/evening watering save water and reduce disease risk."
#     if any(k in q for k in ["crop", "grow", "plant"]):
#         return "Use the ML Prediction tab — enter your soil and weather values for an AI crop recommendation."
#     return "Please ask about crops, soil, fertilizer, irrigation, or plant disease for tailored advice."


# def get_ai_response(user_text, lang_name):
#     """Ask an LLM to respond like a knowledgeable Indian agricultural
#     extension officer, replying ONLY in the farmer's chosen language."""

#     system_prompt = (
#         "You are Krishi AI, a friendly, knowledgeable agricultural assistant "
#         "for Indian farmers. Give clear, practical, locally-relevant advice on "
#         "crops, soil, fertilizers, irrigation, weather, government schemes, "
#         "market prices, and plant diseases. "
#         f"Always reply ONLY in {lang_name}, using simple everyday language a "
#         "farmer can easily understand. Keep answers concise (under 120 words) "
#         "unless asked for more detail. Use a warm, respectful tone."
#     )

#     if groq_client is None:
#         if not GROQ_SDK_OK:
#             reason = "the `groq` Python package isn't installed — run `pip install groq` in your venv"
#         elif GROQ_INIT_ERROR:
#             reason = (
#                 f"the Groq client failed to start (`{GROQ_INIT_ERROR}`) — likely an "
#                 "`httpx` version mismatch. Try `pip install \"httpx==0.27.2\"`, then restart"
#             )
#         else:
#             reason = (
#                 "no `GROQ_API_KEY` could be found — check your `.env` file, "
#                 "environment variable, or `.streamlit/secrets.toml`, then "
#                 "**fully restart** `streamlit run app.py`"
#             )
#         return (
#             f"⚠️ *AI assistant not fully configured* — {reason}. "
#             "See the **🔧 AI Chat Diagnostics** panel in the sidebar for exact "
#             "status. Showing a basic English fallback for now:\n\n"
#             + rule_based_fallback(user_text)
#         )

#     try:
#         completion = groq_client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_text},
#             ],
#             temperature=0.4,
#             max_tokens=400,
#         )
#         return completion.choices[0].message.content.strip()
#     except Exception as e:
#         return f"⚠️ AI service error: {e}"


# # =========================================================
# # ================= HEADER ================================
# # =========================================================

# st.markdown("""
# <div class="krishi-header">
#     <h1>🌱 Krishi AI</h1>
#     <p>AI-Powered Smart Farming Assistant — Crop Recommendation · Disease Detection · Analytics</p>
# </div>
# """, unsafe_allow_html=True)

# # =========================================================
# # ================= LOAD DATASET ==========================
# # =========================================================

# DATASET_PATH = "Krishi_ai_dataset/cleaned_crop_dataset.csv"

# @st.cache_data(show_spinner=False)
# def load_dataset(path):
#     if not os.path.exists(path):
#         return None
#     return pd.read_csv(path)

# df = load_dataset(DATASET_PATH)

# if df is None:
#     st.error(
#         f"❌ Dataset not found at `{DATASET_PATH}`. "
#         "Please add the CSV file and restart."
#     )
#     st.stop()

# # =========================================================
# # ================= FEATURE CATEGORIES ====================
# # =========================================================

# def nitrogen_category(n):
#     if n <= 50:         return "Low"
#     elif n <= 120:      return "Medium"
#     else:               return "High"

# def phosphorus_category(p):
#     if p <= 40:         return "Low"
#     elif p <= 80:       return "Medium"
#     else:               return "High"

# def potassium_category(k):
#     if k <= 40:         return "Low"
#     elif k <= 80:       return "Medium"
#     else:               return "High"

# def temperature_category(temp):
#     if temp <= 20:      return "Cool"
#     elif temp <= 30:    return "Moderate"
#     else:               return "Hot"

# def humidity_category(hum):
#     if hum <= 40:       return "Low"
#     elif hum <= 70:     return "Medium"
#     else:               return "High"

# def ph_category(ph):
#     if ph < 6:          return "Acidic"
#     elif ph <= 7.5:     return "Neutral"
#     else:               return "Alkaline"

# def rainfall_category(rain):
#     if rain <= 100:     return "Low"
#     elif rain <= 200:   return "Medium"
#     else:               return "High"

# # =========================================================
# # ================= ADD CATEGORY COLUMNS ==================
# # =========================================================

# @st.cache_data(show_spinner=False)
# def enrich_dataframe(dataframe):
#     df2 = dataframe.copy()
#     df2["Nitrogen_Category"]    = df2["N"].apply(nitrogen_category)
#     df2["Phosphorus_Category"]  = df2["P"].apply(phosphorus_category)
#     df2["Potassium_Category"]   = df2["K"].apply(potassium_category)
#     df2["Temperature_Category"] = df2["temperature"].apply(temperature_category)
#     df2["Humidity_Category"]    = df2["humidity"].apply(humidity_category)
#     df2["PH_Category"]          = df2["ph"].apply(ph_category)
#     df2["Rainfall_Category"]    = df2["rainfall"].apply(rainfall_category)
#     return df2

# df = enrich_dataframe(df)

# # =========================================================
# # ================= LOAD ML FILES =========================
# # =========================================================

# @st.cache_resource(show_spinner=False)
# def load_ml_files():
#     try:
#         ml_model      = joblib.load("crop_model.pkl")
#         ml_scaler     = joblib.load("scaler.pkl")
#         ml_encoder    = joblib.load("label_encoder.pkl")
#         return ml_model, ml_scaler, ml_encoder, None
#     except FileNotFoundError as e:
#         return None, None, None, str(e)
#     except Exception as e:
#         return None, None, None, str(e)

# crop_model, crop_scaler, crop_encoder, ml_error = load_ml_files()

# # =========================================================
# # ================= LOAD DISEASE MODEL ====================
# # =========================================================

# @st.cache_resource(show_spinner=False)
# def load_disease_model():
#     try:
#         from tensorflow.keras.models import load_model
#         d_model   = load_model("plant_disease_model.h5")
#         d_encoder = joblib.load("disease_label_encoder.pkl")
#         return d_model, d_encoder, None
#     except FileNotFoundError as e:
#         return None, None, str(e)
#     except Exception as e:
#         return None, None, str(e)

# disease_model, disease_encoder, disease_error = load_disease_model()

# # =========================================================
# # ================= SIDEBAR ===============================
# # =========================================================

# with st.sidebar:
#     st.markdown("### 🌾 Navigation")
#     page = st.selectbox(
#         "Go To",
#         ["🏠 Home", "📊 Analytics", "🤖 ML Prediction", "🌿 Disease Detection"],
#         label_visibility="collapsed"
#     )

#     st.markdown("---")
#     st.markdown("### 📌 Quick Info")

#     total_crops  = df["label"].nunique()
#     total_rows   = df.shape[0]
#     ml_status    = "✅ Loaded" if crop_model  else "❌ Not Found"
#     dis_status   = "✅ Loaded" if disease_model else "❌ Not Found"

#     if not GROQ_SDK_OK:
#         ai_status = "❌ Package Missing"
#     elif groq_client is None:
#         ai_status = f"❌ Init Error: {GROQ_INIT_ERROR}" if GROQ_INIT_ERROR else "❌ No API Key Found"
#     else:
#         ai_status = "✅ Ready"

#     st.markdown(f"**Dataset Crops :** {total_crops}")
#     st.markdown(f"**Dataset Rows  :** {total_rows:,}")
#     st.markdown(f"**Crop Model    :** {ml_status}")
#     st.markdown(f"**Disease Model :** {dis_status}")
#     st.markdown(f"**AI Chat (Groq):** {ai_status}")

#     with st.expander("🔧 AI Chat Diagnostics"):
#         st.write("Groq package installed:", "✅ Yes" if GROQ_SDK_OK else "❌ No — run `pip install groq`")
#         st.write("python-dotenv installed:", "✅ Yes" if DOTENV_OK else "❌ No — run `pip install python-dotenv`")
#         st.write(".env file found at:", DOTENV_PATH_FOUND if DOTENV_PATH_FOUND else "❌ Not found")
#         if not DOTENV_PATH_FOUND:
#             try:
#                 _script_dir = os.path.dirname(os.path.abspath(__file__))
#                 _suspects = [
#                     f for f in os.listdir(_script_dir)
#                     if "env" in f.lower() and not f.lower().startswith("venv")
#                 ]
#                 st.write("Files with 'env' in the app folder:", _suspects if _suspects else "(none found)")
#                 st.caption(
#                     "If you see `.env.txt` above instead of `.env`, that's a common "
#                     "Windows Notepad issue — rename it so it has **no .txt at the end**."
#                 )
#             except Exception:
#                 pass
#         env_key_found = bool(os.environ.get("GROQ_API_KEY"))
#         try:
#             secrets_key_found = bool(st.secrets.get("GROQ_API_KEY"))
#         except Exception:
#             secrets_key_found = False
#         st.write("Key found (.env or environment variable):", "✅ Yes" if env_key_found else "❌ No")
#         st.write("Key found in .streamlit/secrets.toml:", "✅ Yes" if secrets_key_found else "❌ No")
#         if GROQ_INIT_ERROR:
#             st.error(
#                 f"Groq client failed to initialize: `{GROQ_INIT_ERROR}`\n\n"
#                 "This usually means `httpx` is too new for your `groq` package "
#                 "version (httpx ≥0.28 removed the `proxies` argument). Fix with:\n\n"
#                 "`pip install \"httpx==0.27.2\"`\n\nthen fully restart the app."
#             )
#         st.caption(
#             "If you just added/changed the key, you must **fully stop and restart** "
#             "`streamlit run app.py` — the key is only read once per server "
#             "start (cached), so a page refresh alone won't pick it up."
#         )

#     st.markdown("---")
#     st.caption("Krishi AI v2.0 — Built with ❤️ for Farmers")

# # =========================================================
# # Shared constants
# # =========================================================

# NUMERIC_FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
# FEATURE_LABELS   = ["Nitrogen", "Phosphorus", "Potassium",
#                     "Temperature", "Humidity", "pH", "Rainfall"]
# CROPS_LIST       = sorted(df["label"].unique())

# @st.cache_data(show_spinner=False)
# def get_crop_stats(dataframe):
#     means = dataframe.groupby("label")[NUMERIC_FEATURES].mean()
#     norm  = (means - means.min()) / (means.max() - means.min())
#     return means, norm

# CROP_MEANS, CROP_NORM = get_crop_stats(df)

# # =========================================================
# # Helper: colorbar config (dark tick text on white bg)
# # =========================================================

# def colorbar_cfg():
#     return dict(
#         bgcolor="#ffffff",
#         tickfont=dict(color="#1a1a1a", size=12),
#         tickcolor="#1a1a1a",
#         title=dict(font=dict(color="#1a1a1a", size=13)),
#         outlinecolor="#c8e6c9",
#         outlinewidth=1,
#     )

# # =========================================================
# # PAGE: HOME
# # =========================================================

# if page == "🏠 Home":

#     col_left, col_mid, col_right = st.columns([1, 2, 1])

#     with col_mid:

#         st.markdown("## 💬 Krishi AI Voice Assistant")
#         st.caption(
#             "Speak or type your farming question in your own language. "
#             "Krishi AI answers instantly — in text **and** voice."
#         )

#         if not VOICE_DEPS_OK:
#             st.warning(
#                 "🎤 Voice features need a few extra packages.\n\n"
#                 "Run: `pip install SpeechRecognition gTTS audio-recorder-streamlit`\n\n"
#                 f"(Details: `{voice_import_error}`)"
#             )

#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = []
#         if "selected_lang" not in st.session_state:
#             st.session_state.selected_lang = "हिंदी (Hindi)"

#         lang_col, clear_col = st.columns([3, 1])
#         with lang_col:
#             st.session_state.selected_lang = st.selectbox(
#                 "🌐 Choose your language",
#                 list(LANGUAGES.keys()),
#                 index=list(LANGUAGES.keys()).index(st.session_state.selected_lang),
#             )
#         with clear_col:
#             st.write("")
#             if st.button("🗑️ Clear Chat", use_container_width=True):
#                 st.session_state.chat_history = []
#                 st.rerun()

#         lang_codes = LANGUAGES[st.session_state.selected_lang]

#         # ── render chat history ──
#         for i, entry in enumerate(st.session_state.chat_history):
#             if entry["role"] == "user":
#                 st.markdown(
#                     f"<div class='chat-label-user'>You</div>"
#                     f"<div class='chat-user'>{entry['text']}</div>",
#                     unsafe_allow_html=True
#                 )
#             else:
#                 st.markdown(
#                     f"<div class='chat-label-ai'>🌱 Krishi AI</div>"
#                     f"<div class='chat-ai'>{entry['text']}</div>",
#                     unsafe_allow_html=True
#                 )
#                 if VOICE_DEPS_OK and st.button("🔊 Listen", key=f"listen_{i}"):
#                     audio_bytes = text_to_speech(entry["text"], lang_codes["tts"])
#                     if audio_bytes:
#                         st.audio(audio_bytes, format="audio/mp3", autoplay=True)
#                     else:
#                         st.warning("Could not generate voice for this reply.")

#         if VOICE_DEPS_OK:
#             st.markdown("#### 🎤 Speak your question")
#             rec_col, hint_col = st.columns([1, 3])
#             with rec_col:
#                 audio_bytes_in = audio_recorder(
#                     text="",
#                     icon_size="2x",
#                     pause_threshold=2.0,
#                     recording_color="#dc3545",
#                     neutral_color="#2e7d32",
#                     key="mic_recorder",
#                 )
#             with hint_col:
#                 st.caption(
#                     f"Tap the mic and speak in **{st.session_state.selected_lang}**. "
#                     "Recording stops automatically after a short pause."
#                 )

#             if audio_bytes_in:
#                 with st.spinner("🎧 Listening & transcribing..."):
#                     transcribed, err = speech_to_text(audio_bytes_in, lang_codes["speech"])
#                 if err:
#                     st.warning(err)
#                 elif transcribed:
#                     st.session_state.chat_history.append({"role": "user", "text": transcribed})
#                     with st.spinner("🤖 Thinking..."):
#                         reply = get_ai_response(transcribed, st.session_state.selected_lang)
#                     st.session_state.chat_history.append({"role": "ai", "text": reply})
#                     audio_out = text_to_speech(reply, lang_codes["tts"])
#                     if audio_out:
#                         st.audio(audio_out, format="audio/mp3", autoplay=True)
#                     st.rerun()

#             st.markdown("#### ⌨️ Or type your question")
#         else:
#             st.markdown("#### ⌨️ Type your question")

#         user_input = st.text_input(
#             "Your question",
#             placeholder="e.g.  लाल मिट्टी और कम बारिश में कौन सी फसल अच्छी होती है?",
#             label_visibility="collapsed",
#             key="home_input"
#         )

#         if st.button("🌾 Get Advice", use_container_width=True):
#             if not user_input.strip():
#                 st.warning("⚠️ Please type or speak a farming question first.")
#             else:
#                 st.session_state.chat_history.append({"role": "user", "text": user_input})
#                 with st.spinner("🤖 Thinking..."):
#                     reply = get_ai_response(user_input, st.session_state.selected_lang)
#                 st.session_state.chat_history.append({"role": "ai", "text": reply})
#                 if VOICE_DEPS_OK:
#                     audio_out = text_to_speech(reply, lang_codes["tts"])
#                     if audio_out:
#                         st.audio(audio_out, format="audio/mp3", autoplay=True)
#                 st.rerun()

#     st.markdown("---")

#     st.markdown("### 🚀 What Krishi AI Can Do For You")
#     c1, c2, c3 = st.columns(3)

#     with c1:
#         st.info(
#             "### 📊 Smart Analytics\n"
#             "Explore 24+ charts and insights about crops, soil nutrients, "
#             "rainfall, temperature, and more."
#         )
#     with c2:
#         st.success(
#             "### 🤖 Crop Prediction\n"
#             "Enter your soil and weather data to get an ML-powered crop "
#             "recommendation with confidence scores."
#         )
#     with c3:
#         st.warning(
#             "### 🌿 Disease Detection\n"
#             "Upload a leaf image and our CNN model will identify plant "
#             "diseases and suggest treatment in seconds."
#         )

# # =========================================================
# # PAGE: ANALYTICS
# # =========================================================

# elif page == "📊 Analytics":

#     st.header("📊 Krishi Data Analytics Dashboard")

#     st.subheader("📁 Dataset Overview")
#     c1, c2, c3, c4, c5 = st.columns(5)
#     c1.metric("Total Rows",      f"{df.shape[0]:,}")
#     c2.metric("Total Columns",   df.shape[1])
#     c3.metric("Unique Crops",    df["label"].nunique())
#     c4.metric("Duplicate Rows",  int(df.duplicated().sum()))
#     c5.metric("Missing Values",  int(df.isnull().sum().sum()))
#     st.markdown("---")

#     st.subheader("🔬 Data Quality Check")
#     q1, q2 = st.columns(2)
#     with q1:
#         st.write("#### Data Types")
#         dtype_df = df.dtypes.reset_index()
#         dtype_df.columns = ["Feature", "Type"]
#         dtype_df["Type"] = dtype_df["Type"].astype(str)
#         st.dataframe(dtype_df, use_container_width=True)
#     with q2:
#         st.write("#### Missing Values")
#         mv = df.isnull().sum().reset_index()
#         mv.columns = ["Feature", "Missing"]
#         st.dataframe(mv, use_container_width=True)
#         if mv["Missing"].sum() == 0:
#             st.success("✅ No missing values!")
#         if df.duplicated().sum() == 0:
#             st.success("✅ No duplicate rows!")
#     st.markdown("---")

#     st.subheader("🔍 Dataset Preview")
#     st.dataframe(df.head(50), use_container_width=True)
#     st.markdown("---")

#     st.subheader("📈 Statistical Summary")
#     st.dataframe(df.describe().round(2), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🌾 Crop Distribution")
#     crop_count = df["label"].value_counts().reset_index()
#     crop_count.columns = ["Crop", "Count"]

#     d1, d2 = st.columns(2)
#     with d1:
#         fig = px.bar(crop_count, x="Crop", y="Count",
#                      color="Count", color_continuous_scale="Greens",
#                      text="Count", title="Crop Count")
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(xaxis_tickangle=-45, showlegend=False, height=380)
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         st.plotly_chart(fig, use_container_width=True)
#     with d2:
#         fig2 = px.pie(crop_count, names="Crop", values="Count",
#                       title="Crop Share",
#                       color_discrete_sequence=px.colors.sequential.Greens_r)
#         fig2.update_traces(textposition="inside", textinfo="percent+label")
#         st.plotly_chart(fig2, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📊 Feature Category Analysis")
#     cat_cols = [
#         ("Nitrogen_Category", "Nitrogen"),
#         ("Phosphorus_Category", "Phosphorus"),
#         ("Potassium_Category", "Potassium"),
#         ("Temperature_Category", "Temperature"),
#         ("Humidity_Category", "Humidity"),
#         ("PH_Category", "Soil pH"),
#         ("Rainfall_Category", "Rainfall"),
#     ]
#     ca1, ca2 = st.columns(2)
#     for i, (col_name, title) in enumerate(cat_cols):
#         counts = df[col_name].value_counts().reset_index()
#         counts.columns = ["Category", "Count"]
#         fig = px.pie(counts, names="Category", values="Count",
#                      title=f"{title} Distribution", hole=0.4,
#                      color_discrete_sequence=px.colors.qualitative.Set2)
#         fig.update_traces(textinfo="percent+label")
#         (ca1 if i % 2 == 0 else ca2).plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     def climate_bar(feature, label, color_scale, unit=""):
#         grp = df.groupby("label")[feature].mean().round(2).reset_index()
#         grp.columns = ["Crop", label]
#         grp = grp.sort_values(label, ascending=True)
#         fig = px.bar(grp, x=label, y="Crop", orientation="h",
#                      title=f"Average {label} per Crop",
#                      color=label, color_continuous_scale=color_scale,
#                      text=label)
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(height=580, yaxis_title="")
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         return fig, grp

#     for feat, lbl, scale in [
#         ("temperature", "Avg Temperature (°C)", "RdYlGn_r"),
#         ("rainfall",    "Avg Rainfall (mm)",    "Blues"),
#         ("humidity",    "Avg Humidity (%)",      "Teal"),
#         ("ph",          "Avg pH",               "RdYlGn"),
#     ]:
#         icon = '🌡' if 'Temp' in lbl else '🌧' if 'Rain' in lbl else '💧' if 'Hum' in lbl else '🧪'
#         st.subheader(f"{icon} {lbl}")
#         fig, grp = climate_bar(feat, lbl, scale)
#         st.plotly_chart(fig, use_container_width=True)
#         t1, t2 = st.columns(2)
#         with t1:
#             st.write("**Top 5 (Highest)**")
#             st.dataframe(grp.tail(5)[::-1].reset_index(drop=True), use_container_width=True)
#         with t2:
#             st.write("**Bottom 5 (Lowest)**")
#             st.dataframe(grp.head(5).reset_index(drop=True), use_container_width=True)
#         st.markdown("---")

#     st.subheader("🪴 NPK Analysis")
#     avg_npk = df.groupby("label")[["N","P","K"]].mean().round(2).reset_index()
#     npk_m   = avg_npk.melt(id_vars="label", value_vars=["N","P","K"],
#                             var_name="Nutrient", value_name="Value")
#     cmap = {"N": "#2ca02c", "P": "#ff7f0e", "K": "#1f77b4"}

#     for mode, title in [("group","Grouped"), ("stack","Stacked — shows proportion")]:
#         fig = px.bar(npk_m, x="label", y="Value", color="Nutrient",
#                      barmode=mode, title=f"N, P, K per Crop ({title})",
#                      color_discrete_map=cmap,
#                      labels={"label":"Crop","Value":"mg/kg"})
#         fig.update_layout(xaxis_tickangle=-45, height=420)
#         st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(avg_npk.set_index("label"), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🧪 Soil Health Analysis")
#     c1,c2,c3 = st.columns(3)
#     c1.metric("Avg Nitrogen",   round(df["N"].mean(),2))
#     c2.metric("Avg Phosphorus", round(df["P"].mean(),2))
#     c3.metric("Avg Potassium",  round(df["K"].mean(),2))

#     soil = df.groupby("label")[["N","P","K"]].mean()
#     soil["Score"] = soil.mean(axis=1).round(2)
#     soil = soil.reset_index().sort_values("Score", ascending=False)
#     avg_s = soil["Score"].mean()

#     fig = px.bar(soil, x="label", y="Score", color="Score",
#                  color_continuous_scale="YlGn", text="Score",
#                  title="Soil Health Score (avg of N+P+K)")
#     fig.add_hline(y=avg_s, line_dash="dash", line_color="red",
#                   annotation_text=f"Avg: {avg_s:.1f}")
#     fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#     fig.update_layout(xaxis_tickangle=-45, height=420)
#     fig.update_coloraxes(colorbar=colorbar_cfg())
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("⚠️ Nutrient Deficiency Flag")
#     npk_flag = df.groupby("label")[["N","P","K"]].mean().round(2).reset_index()
#     npk_flag["N_Flag"] = npk_flag["N"].apply(lambda x: "⚠️ Low" if x<=50 else "✅ OK")
#     npk_flag["P_Flag"] = npk_flag["P"].apply(lambda x: "⚠️ Low" if x<=40 else "✅ OK")
#     npk_flag["K_Flag"] = npk_flag["K"].apply(lambda x: "⚠️ Low" if x<=40 else "✅ OK")
#     npk_flag["Status"] = npk_flag[["N_Flag","P_Flag","K_Flag"]].apply(
#         lambda r: "⚠️ Deficient" if "⚠️ Low" in r.values else "✅ Sufficient", axis=1)
#     deficient = npk_flag[npk_flag["Status"]=="⚠️ Deficient"]
#     if len(deficient):
#         st.warning(f"⚠️ {len(deficient)} crops have a nutrient in the Low range.")
#         st.dataframe(deficient[["label","N","N_Flag","P","P_Flag","K","K_Flag"]],
#                      use_container_width=True)
#     else:
#         st.success("✅ All crops have sufficient average NPK levels.")
#     st.markdown("---")

#     st.subheader("📏 Feature Range per Crop")
#     sel_feat = st.selectbox("Select Feature", NUMERIC_FEATURES, key="range_sel")
#     range_df = (df.groupby("label")[sel_feat]
#                 .agg(["min","max","mean","std"]).round(2).reset_index())
#     range_df.columns = ["Crop","Min","Max","Mean","Std Dev"]
#     range_df = range_df.sort_values("Mean", ascending=False)
#     fig = go.Figure(go.Bar(
#         x=range_df["Crop"], y=range_df["Mean"], name="Mean",
#         marker_color="#2ca02c",
#         error_y=dict(type="data", array=range_df["Std Dev"], visible=True),
#         text=range_df["Mean"], textposition="outside"
#     ))
#     fig.update_layout(title=f"{sel_feat} — Mean ± Std Dev",
#                       xaxis_tickangle=-45, height=440)
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(range_df.set_index("Crop"), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔵 Scatter Plot Analysis")
#     scatter_pairs = [
#         ("rainfall","humidity","Rainfall vs Humidity"),
#         ("temperature","ph","Temperature vs Soil pH"),
#         ("N","K","Nitrogen vs Potassium"),
#         ("temperature","rainfall","Temperature vs Rainfall"),
#     ]
#     s1, s2 = st.columns(2)
#     for i, (x, y, title) in enumerate(scatter_pairs):
#         fig = px.scatter(df, x=x, y=y, color="label",
#                          hover_name="label", title=title, opacity=0.6)
#         fig.update_layout(height=420, showlegend=False)
#         (s1 if i % 2 == 0 else s2).plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📦 Feature Distribution (Box Plot)")
#     box_sel = st.selectbox("Select Feature", NUMERIC_FEATURES, key="box_sel")
#     fig = px.box(df, x="label", y=box_sel, color="label",
#                  title=f"{box_sel} Distribution by Crop",
#                  color_discrete_sequence=px.colors.qualitative.Pastel)
#     fig.update_layout(xaxis_tickangle=-45, height=500, showlegend=False)
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📋 Complete Crop Profile")
#     full_prof = df.groupby("label")[NUMERIC_FEATURES].mean().round(2)
#     full_prof.columns = ["N (mg/kg)","P (mg/kg)","K (mg/kg)",
#                          "Temp (°C)","Humidity (%)","pH","Rainfall (mm)"]
#     st.dataframe(full_prof.style.background_gradient(cmap="YlGn", axis=0),
#                  use_container_width=True)
#     st.markdown("---")

#     st.subheader("⚖️ Crop-to-Crop Comparison")
#     cc1, cc2 = st.columns(2)
#     crop_a = cc1.selectbox("Crop A", CROPS_LIST, index=0, key="ca")
#     crop_b = cc2.selectbox("Crop B", CROPS_LIST, index=1, key="cb")

#     a_v = df[df["label"]==crop_a][NUMERIC_FEATURES].mean().round(2)
#     b_v = df[df["label"]==crop_b][NUMERIC_FEATURES].mean().round(2)

#     fig = go.Figure([
#         go.Bar(name=crop_a, x=FEATURE_LABELS, y=a_v.values,
#                marker_color="#2ca02c", text=a_v.values, textposition="outside"),
#         go.Bar(name=crop_b, x=FEATURE_LABELS, y=b_v.values,
#                marker_color="#1f77b4", text=b_v.values, textposition="outside"),
#     ])
#     fig.update_layout(barmode="group",
#                       title=f"{crop_a} vs {crop_b}", height=400)
#     st.plotly_chart(fig, use_container_width=True)

#     a_n = CROP_NORM.loc[crop_a].values.tolist()
#     b_n = CROP_NORM.loc[crop_b].values.tolist()
#     fig2 = go.Figure([
#         go.Scatterpolar(r=a_n+[a_n[0]], theta=NUMERIC_FEATURES+[NUMERIC_FEATURES[0]],
#                         fill="toself", name=crop_a,
#                         line_color="#2ca02c", fillcolor="rgba(44,160,44,0.15)"),
#         go.Scatterpolar(r=b_n+[b_n[0]], theta=NUMERIC_FEATURES+[NUMERIC_FEATURES[0]],
#                         fill="toself", name=crop_b,
#                         line_color="#1f77b4", fillcolor="rgba(31,119,180,0.15)"),
#     ])
#     fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])),
#                        title=f"Radar: {crop_a} vs {crop_b} (Normalized 0–1)", height=460)
#     st.plotly_chart(fig2, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔍 Similar Crops Finder")
#     target = st.selectbox("Select a Crop", CROPS_LIST, key="sim")
#     vec    = CROP_NORM.loc[target]
#     dists  = CROP_NORM.drop(target).apply(
#         lambda r: np.sqrt(((r - vec)**2).sum()), axis=1)
#     top3 = dists.nsmallest(3).reset_index()
#     top3.columns = ["Similar Crop","Distance (lower=closer)"]
#     top3["Distance (lower=closer)"] = top3["Distance (lower=closer)"].round(4)
#     st.write(f"**Top 3 crops most similar to {target}:**")
#     st.dataframe(top3, use_container_width=True)
#     sim_names   = top3["Similar Crop"].tolist()
#     sim_profile = CROP_MEANS.loc[[target]+sim_names].round(2)
#     st.dataframe(sim_profile.style.background_gradient(cmap="Greens", axis=0),
#                  use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔍 Crop Filter")
#     sel_crop  = st.selectbox("Select Crop", CROPS_LIST, key="filter")
#     crop_data = df[df["label"]==sel_crop]
#     m1,m2,m3,m4 = st.columns(4)
#     m1.metric("Avg Temp",     f"{crop_data['temperature'].mean():.1f} °C")
#     m2.metric("Avg Humidity", f"{crop_data['humidity'].mean():.1f} %")
#     m3.metric("Avg Rainfall", f"{crop_data['rainfall'].mean():.1f} mm")
#     m4.metric("Avg pH",       f"{crop_data['ph'].mean():.2f}")
#     n1,n2,n3 = st.columns(3)
#     n1.metric("Avg Nitrogen",   round(crop_data["N"].mean(),2))
#     n2.metric("Avg Phosphorus", round(crop_data["P"].mean(),2))
#     n3.metric("Avg Potassium",  round(crop_data["K"].mean(),2))
#     st.dataframe(crop_data, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔗 Feature Correlation Matrix")
#     corr = df[NUMERIC_FEATURES].corr().round(3)
#     fig  = px.imshow(corr, text_auto=True, color_continuous_scale="RdYlGn",
#                      zmin=-1, zmax=1, title="Feature Correlation Heatmap")
#     fig.update_layout(height=480)
#     fig.update_coloraxes(colorbar=colorbar_cfg())
#     st.plotly_chart(fig, use_container_width=True)
#     st.caption("🟢 Green = positive | 🔴 Red = negative | ⚪ White = no correlation")

#     pairs = corr.unstack().reset_index()
#     pairs.columns = ["Feature A","Feature B","Correlation"]
#     pairs = pairs[pairs["Feature A"] < pairs["Feature B"]]
#     pairs["Abs"] = pairs["Correlation"].abs()
#     pairs = pairs.sort_values("Abs", ascending=False).drop(columns="Abs")
#     pc1, pc2 = st.columns(2)
#     with pc1:
#         st.write("**Top 3 Positive**")
#         st.dataframe(pairs[pairs["Correlation"]>0].head(3).reset_index(drop=True),
#                      use_container_width=True)
#     with pc2:
#         st.write("**Top 3 Negative**")
#         st.dataframe(pairs[pairs["Correlation"]<0].head(3).reset_index(drop=True),
#                      use_container_width=True)
#     st.markdown("---")

#     st.subheader("📘 Feature Meaning")
#     feat_info = pd.DataFrame({
#         "Feature": ["N","P","K","temperature","humidity","ph","rainfall"],
#         "Meaning": [
#             "Nitrogen — leaf and stem growth",
#             "Phosphorus — root and flower growth",
#             "Potassium — plant strength and disease resistance",
#             "Temperature — optimal growing temperature",
#             "Humidity — moisture level in the air",
#             "Soil pH — acidity or alkalinity",
#             "Rainfall — water requirement"
#         ],
#         "Unit": ["mg/kg","mg/kg","mg/kg","°C","%","0–14","mm"]
#     })
#     st.dataframe(feat_info, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🌱 Farmer Understanding Guide")
#     g1, g2 = st.columns(2)
#     with g1:
#         st.success("🟢 **Low Nitrogen (≤50)** → Light fertilizer needed")
#         st.info("🔵 **Medium Nitrogen (51–120)** → Balanced fertilizer")
#         st.warning("🟡 **High Nitrogen (>120)** → Heavy fertilizer needed")
#         st.success("🟢 **Cool (≤20°C)** → Wheat, lentil, chickpea")
#         st.info("🔵 **Moderate (21–30°C)** → Most common crops")
#         st.warning("🟡 **Hot (>30°C)** → Tropical/summer crops")
#     with g2:
#         st.success("🟢 **Acidic (pH<6)** → Tea, rice, blueberry")
#         st.info("🔵 **Neutral (pH 6–7.5)** → Best for most crops")
#         st.warning("🟡 **Alkaline (pH>7.5)** → Cotton, maize")
#         st.success("🟢 **Low Rainfall (≤100mm)** → Drought-tolerant crops")
#         st.info("🔵 **Medium Rainfall (101–200mm)** → General crops")
#         st.warning("🟡 **High Rainfall (>200mm)** → Water-intensive crops")
#     st.markdown("---")

#     st.subheader("📌 Key Insights")
#     st.success("✅ Dataset is balanced with nearly equal crop distribution.")
#     st.success("✅ No missing values or duplicate rows found.")
#     st.success("✅ Dataset is clean and ready for ML model training.")
#     st.info("📊 Rainfall, temperature, humidity and soil nutrients drive crop suitability.")
#     st.info("🌱 Rice and jute need high humidity & rainfall; chickpea and kidney beans prefer dry conditions.")
#     st.info("🧪 Use Scatter and Box Plots to identify natural clusters for ML feature selection.")
#     st.info("⚖️ Use Crop Comparison and Similar Crops to help farmers choose alternative crops.")

# # =========================================================
# # PAGE: ML PREDICTION
# # =========================================================

# elif page == "🤖 ML Prediction":

#     st.header("🤖 AI-Powered Crop Recommendation")
#     st.markdown("---")

#     if ml_error:
#         st.error(
#             f"❌ Could not load ML model files.\n\n"
#             f"**Error:** `{ml_error}`\n\n"
#             "Please make sure `crop_model.pkl`, `scaler.pkl`, and "
#             "`label_encoder.pkl` are in the same folder as `app.py`."
#         )
#         st.stop()

#     if hasattr(crop_model, "feature_importances_"):
#         st.subheader("📈 Model Feature Importance")
#         imp_df = pd.DataFrame({
#             "Feature":    FEATURE_LABELS,
#             "Importance": crop_model.feature_importances_
#         }).sort_values("Importance", ascending=False)

#         fig = px.bar(imp_df, x="Feature", y="Importance",
#                      color="Importance", color_continuous_scale="Teal",
#                      text=imp_df["Importance"].round(3),
#                      title="Feature Importance (Higher = More Influential)")
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(height=380)
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         st.plotly_chart(fig, use_container_width=True)
#         st.info(
#             f"🔑 Most influential: **{imp_df.iloc[0]['Feature']}**  |  "
#             f"📉 Least influential: **{imp_df.iloc[-1]['Feature']}**"
#         )
#         st.markdown("---")

#     st.subheader("🌱 Enter Your Soil and Weather Conditions")

#     sl1, sl2 = st.columns(2)

#     with sl1:
#         N = st.slider("Nitrogen (N) mg/kg",
#                       int(df["N"].min()), int(df["N"].max()), int(df["N"].mean()))
#         P = st.slider("Phosphorus (P) mg/kg",
#                       int(df["P"].min()), int(df["P"].max()), int(df["P"].mean()))
#         K = st.slider("Potassium (K) mg/kg",
#                       int(df["K"].min()), int(df["K"].max()), int(df["K"].mean()))
#         temperature = st.slider("Temperature (°C)",
#                                 float(df["temperature"].min()),
#                                 float(df["temperature"].max()),
#                                 round(float(df["temperature"].mean()),1))
#     with sl2:
#         humidity = st.slider("Humidity (%)",
#                              float(df["humidity"].min()),
#                              float(df["humidity"].max()),
#                              round(float(df["humidity"].mean()),1))
#         ph = st.slider("Soil pH",
#                        float(df["ph"].min()), float(df["ph"].max()),
#                        round(float(df["ph"].mean()),1))
#         rainfall = st.slider("Rainfall (mm)",
#                              float(df["rainfall"].min()),
#                              float(df["rainfall"].max()),
#                              round(float(df["rainfall"].mean()),1))

#     st.markdown("---")
#     st.subheader("📊 Real-Time Input Analysis")
#     ia1, ia2, ia3, ia4 = st.columns(4)
#     ia1.info(f"🌿 N: **{nitrogen_category(N)}**\n\n💧 Humidity: **{humidity_category(humidity)}**")
#     ia2.info(f"🌿 P: **{phosphorus_category(P)}**\n\n🧪 Soil pH: **{ph_category(ph)}**")
#     ia3.info(f"🌿 K: **{potassium_category(K)}**\n\n🌧 Rainfall: **{rainfall_category(rainfall)}**")
#     ia4.info(f"🌡 Temp: **{temperature_category(temperature)}**")

#     st.markdown("---")

#     if st.button("🌾 Predict Best Crop", use_container_width=True):
#         try:
#             inp        = [[N, P, K, temperature, humidity, ph, rainfall]]
#             scaled     = crop_scaler.transform(inp)
#             prediction = crop_model.predict(scaled)
#             pred_crop  = crop_encoder.inverse_transform(prediction)[0]

#             st.success(f"✅ Recommended Crop: **{pred_crop.upper()}**")
#             st.markdown("---")

#             if hasattr(crop_model, "predict_proba"):
#                 st.subheader("📊 Top 5 Crop Predictions")
#                 proba  = crop_model.predict_proba(scaled)[0]
#                 prob_df = pd.DataFrame({
#                     "Crop":        crop_encoder.classes_,
#                     "Probability": proba
#                 }).sort_values("Probability", ascending=False).head(5)
#                 prob_df["Pct"] = (prob_df["Probability"]*100).round(2)

#                 fig = px.bar(prob_df, x="Crop", y="Probability",
#                              color="Probability",
#                              text=prob_df["Pct"].astype(str)+"%",
#                              color_continuous_scale="Greens",
#                              title="Prediction Confidence (Top 5)")
#                 fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#                 fig.update_layout(height=420)
#                 fig.update_coloraxes(colorbar=colorbar_cfg())
#                 st.plotly_chart(fig, use_container_width=True)

#                 top_pct = prob_df.iloc[0]["Pct"]
#                 if top_pct >= 80:
#                     st.success(f"🎯 High confidence: {top_pct}%")
#                 elif top_pct >= 50:
#                     st.info(f"🔍 Moderate confidence: {top_pct}% — verify with local conditions.")
#                 else:
#                     st.warning(f"⚠️ Low confidence: {top_pct}% — consult an agronomist.")
#                 st.markdown("---")

#             st.subheader(f"📐 Your Conditions vs Ideal for {pred_crop.capitalize()}")
#             ideal = df[df["label"]==pred_crop][NUMERIC_FEATURES].mean().round(2)
#             user_vals = [N, P, K, temperature, humidity, ph, rainfall]

#             fig = go.Figure([
#                 go.Bar(name="Your Input", x=FEATURE_LABELS, y=user_vals,
#                        marker_color="#1f77b4",
#                        text=[round(v,2) for v in user_vals], textposition="outside"),
#                 go.Bar(name=f"Ideal for {pred_crop}", x=FEATURE_LABELS,
#                        y=ideal.values, marker_color="#2ca02c",
#                        text=ideal.values, textposition="outside"),
#             ])
#             fig.update_layout(barmode="group",
#                               title=f"Your Input vs Ideal: {pred_crop}",
#                               height=400)
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown("---")

#             st.subheader("📋 Input Summary")
#             summ = pd.DataFrame({
#                 "Feature": ["Nitrogen (mg/kg)","Phosphorus (mg/kg)","Potassium (mg/kg)",
#                             "Temperature (°C)","Humidity (%)","Soil pH","Rainfall (mm)"],
#                 "Value":    [N, P, K, temperature, humidity, ph, rainfall],
#                 "Category": [nitrogen_category(N), phosphorus_category(P),
#                              potassium_category(K), temperature_category(temperature),
#                              humidity_category(humidity), ph_category(ph),
#                              rainfall_category(rainfall)]
#             })
#             st.dataframe(summ, use_container_width=True)
#             st.markdown("---")

#             st.subheader("🌱 Crop Advice")
#             crop_advice = {
#                 "rice":        "Requires high rainfall (150–300mm), high humidity (80–90%), and slightly acidic soil (pH 5.5–6.5).",
#                 "maize":       "Needs moderate rainfall, moderate temperature (21–27°C), and fertile loamy soil (pH 5.5–7.0).",
#                 "jute":        "Thrives in high humidity and rainfall. Requires warm climate (25–35°C) and alluvial soil.",
#                 "cotton":      "Grows well in well-drained black soil (pH 6–8), warm climate (21–35°C), and moderate rainfall.",
#                 "coconut":     "Requires tropical climate, high humidity (70–80%), and sandy loam soil.",
#                 "papaya":      "Needs warm climate (25–30°C), well-drained soil, moderate rainfall, and high humidity.",
#                 "banana":      "Requires rich loamy soil, high humidity, warm temperature (26–30°C), and regular rainfall.",
#                 "mango":       "Prefers deep well-drained soil, dry season at flowering, and tropical/subtropical climate.",
#                 "grapes":      "Needs well-drained sandy loam, dry hot summers and cool winters.",
#                 "watermelon":  "Requires warm climate (25–35°C), sandy loam soil, and moderate to high rainfall.",
#                 "muskmelon":   "Grows best in warm climate, sandy soil with good drainage, and moderate humidity.",
#                 "apple":       "Requires cool climate (cold winters for dormancy), loamy soil, and moderate rainfall.",
#                 "orange":      "Needs subtropical climate, well-drained sandy loam, and moderate rainfall (750–1200mm).",
#                 "pomegranate": "Drought-tolerant, wide pH range (5.5–7.5), grows well in semi-arid regions.",
#                 "lentil":      "Cool season crop, well-drained loamy soil (pH 6–8), low rainfall.",
#                 "blackgram":   "Warm climate (25–35°C), well-drained loamy soil, moderate rainfall (600–800mm).",
#                 "mungbean":    "Warm season, sandy loam soil, short rainfall period, moderate temperature (28–30°C).",
#                 "mothbeans":   "Drought-tolerant, arid/semi-arid regions, sandy soil, very low rainfall.",
#                 "pigeonpeas":  "Drought-tolerant legume, well-drained soil (pH 5–7), moderate rainfall.",
#                 "kidneybeans": "Cool temperature, well-drained fertile loam (pH 6–7), moderate rainfall.",
#                 "chickpea":    "Cool season, drought-tolerant, loamy soil (pH 5.5–7), low rainfall.",
#                 "coffee":      "Tropical climate (15–28°C), high humidity, acidic well-drained soil (pH 6–6.5), high rainfall."
#             }
#             advice = crop_advice.get(
#                 pred_crop.lower(),
#                 f"{pred_crop.capitalize()} is suited to the conditions you entered. "
#                 "Consult local agricultural guidelines for detailed advice."
#             )
#             st.info(f"🌿 **{pred_crop.capitalize()} Advice:** {advice}")
#             st.markdown("---")

#             st.subheader("🧪 Soil & Climate Summary")
#             sc1, sc2 = st.columns(2)
#             with sc1:
#                 if ph < 6:
#                     st.warning("⚠️ **Acidic Soil** — add lime to raise pH.")
#                 elif ph > 7.5:
#                     st.warning("⚠️ **Alkaline Soil** — add sulfur to lower pH.")
#                 else:
#                     st.success("✅ **Neutral Soil pH** — ideal for most crops.")
#                 n_cat = nitrogen_category(N)
#                 if n_cat == "Low":
#                     st.warning("⚠️ Low Nitrogen — apply urea or nitrogen-rich fertilizer.")
#                 elif n_cat == "High":
#                     st.info("ℹ️ High Nitrogen — reduce fertilizer application.")
#                 else:
#                     st.success("✅ Nitrogen level is balanced.")
#             with sc2:
#                 if rainfall > 200:
#                     st.info("🌧 High rainfall — ensure good field drainage.")
#                 elif rainfall < 80:
#                     st.info("☀️ Low rainfall — consider drip irrigation.")
#                 else:
#                     st.success("✅ Moderate rainfall — suitable for most crops.")
#                 t_cat = temperature_category(temperature)
#                 if t_cat == "Cool":
#                     st.info("❄️ Cool climate — suitable for wheat, lentil, chickpea.")
#                 elif t_cat == "Hot":
#                     st.info("🔥 Hot climate — suitable for tropical/summer crops.")
#                 else:
#                     st.success("✅ Moderate temperature — good for most crops.")

#         except Exception as e:
#             st.error(f"❌ Prediction failed: `{str(e)}`")

# # =========================================================
# # PAGE: DISEASE DETECTION
# # =========================================================

# elif page == "🌿 Disease Detection":

#     st.header("🌿 Plant Disease Detection System")
#     st.markdown("---")

#     if disease_error:
#         st.error(
#             f"❌ Disease model not found.\n\n"
#             f"**Error:** `{disease_error}`\n\n"
#             "Run `train_disease_model.py` first to train and save the model, "
#             "then restart the app."
#         )
#         st.stop()

#     st.subheader("📤 Upload a Plant Leaf Image")
#     st.caption(
#         "Upload a clear photo of a plant leaf. "
#         "The AI will predict whether it is healthy or diseased."
#     )

#     uploaded = st.file_uploader(
#         "Drag & drop or click to browse",
#         type=["jpg","jpeg","png","webp"],
#         label_visibility="collapsed"
#     )

#     if uploaded is not None:

#         image = Image.open(uploaded).convert("RGB")

#         col_img, col_res = st.columns([1, 1])

#         with col_img:
#             st.image(image, caption="Uploaded Leaf Image", use_column_width=True)

#         img_resized = image.resize((128, 128))
#         img_array   = np.array(img_resized, dtype="float32") / 255.0
#         img_array   = np.expand_dims(img_array, axis=0)

#         try:
#             preds         = disease_model.predict(img_array, verbose=0)
#             pred_idx      = int(np.argmax(preds))
#             disease_name  = disease_encoder.inverse_transform([pred_idx])[0]
#             confidence    = float(np.max(preds)) * 100
#             all_probs     = preds[0]

#             with col_res:
#                 st.markdown('<div class="disease-card">', unsafe_allow_html=True)

#                 if confidence >= 75:
#                     st.success(f"✅ **Predicted:** {disease_name.replace('_', ' ')}")
#                 elif confidence >= 50:
#                     st.warning(f"⚠️ **Predicted (Moderate Confidence):** {disease_name.replace('_', ' ')}")
#                 else:
#                     st.error(f"❓ **Low Confidence Prediction:** {disease_name.replace('_', ' ')}")

#                 st.metric("Confidence", f"{confidence:.2f}%")
#                 st.progress(int(min(confidence, 100)))

#                 is_healthy = "healthy" in disease_name.lower()
#                 if is_healthy:
#                     st.success("🌿 Your plant appears **HEALTHY**!")
#                 else:
#                     st.error("🦠 Disease detected — see treatment advice below.")

#                 st.markdown('</div>', unsafe_allow_html=True)

#             st.markdown("---")

#             st.subheader("💊 Treatment & Care Advice")

#             disease_advice = {
#                 "Tomato_healthy":
#                     ("✅ Healthy Plant", "success",
#                      "Maintain regular watering (avoid overhead irrigation), "
#                      "balanced fertilization, and good air circulation."),
#                 "Tomato_Early_blight":
#                     ("⚠️ Early Blight (Alternaria solani)", "warning",
#                      "Remove infected lower leaves immediately. Apply **mancozeb** "
#                      "or **chlorothalonil** fungicide every 7–10 days. Avoid overhead "
#                      "watering and ensure good air flow around plants."),
#                 "Tomato_Late_blight":
#                     ("🚨 Late Blight (Phytophthora infestans)", "error",
#                      "Act fast — this spreads rapidly. Remove and destroy infected "
#                      "plants. Apply **copper-based fungicide** or **metalaxyl**. "
#                      "Avoid watering leaves; water at the base."),
#                 "Tomato_Leaf_Mold":
#                     ("⚠️ Leaf Mold (Passalora fulva)", "warning",
#                      "Improve greenhouse/field air circulation. Reduce humidity. "
#                      "Apply **copper** or **sulfur-based fungicide**. Remove affected leaves."),
#                 "Tomato_Septoria_leaf_spot":
#                     ("⚠️ Septoria Leaf Spot", "warning",
#                      "Remove infected leaves. Apply **mancozeb** fungicide. "
#                      "Rotate crops and avoid overhead irrigation."),
#                 "Tomato_Spider_mites":
#                     ("⚠️ Spider Mites", "warning",
#                      "Spray plants with water to dislodge mites. "
#                      "Apply **neem oil** or **insecticidal soap**. "
#                      "Introduce predatory mites as biological control."),
#                 "Tomato_Target_Spot":
#                     ("⚠️ Target Spot", "warning",
#                      "Remove infected leaves. Apply **azoxystrobin** or "
#                      "**chlorothalonil** fungicide. Ensure good air circulation."),
#                 "Tomato_Mosaic_Virus":
#                     ("🚨 Tomato Mosaic Virus", "error",
#                      "No cure available. Remove and destroy infected plants to prevent spread. "
#                      "Control aphids (virus vectors) with **neem oil**. Sanitize tools."),
#                 "Tomato_Yellow_Leaf_Curl_Virus":
#                     ("🚨 Yellow Leaf Curl Virus", "error",
#                      "Spread by whiteflies — apply **imidacloprid** to control them. "
#                      "Remove infected plants. Use virus-resistant tomato varieties."),
#                 "Tomato_Bacterial_spot":
#                     ("⚠️ Bacterial Spot (Xanthomonas)", "warning",
#                      "Apply **copper-based bactericide** (copper hydroxide). "
#                      "Avoid working with plants when wet. Practice crop rotation."),
#                 "Potato_healthy":
#                     ("✅ Healthy Potato Plant", "success",
#                      "Keep soil consistently moist but not waterlogged. "
#                      "Earth up around stems to prevent greening."),
#                 "Potato_Early_blight":
#                     ("⚠️ Potato Early Blight", "warning",
#                      "Apply **mancozeb** or **chlorothalonil** fungicide. "
#                      "Remove heavily infected leaves. Avoid nitrogen excess."),
#                 "Potato_Late_blight":
#                     ("🚨 Potato Late Blight (Phytophthora infestans)", "error",
#                      "Most destructive potato disease. Apply **metalaxyl** or "
#                      "**cymoxanil** fungicide immediately. Destroy infected tubers. "
#                      "Do not compost infected material."),
#                 "Pepper,_bell_healthy":
#                     ("✅ Healthy Bell Pepper", "success",
#                      "Maintain consistent moisture, full sun, and warm temperatures (20–30°C)."),
#                 "Pepper,_bell_Bacterial_spot":
#                     ("⚠️ Bacterial Spot (Xanthomonas)", "warning",
#                      "Apply **copper hydroxide** spray. Avoid overhead watering. "
#                      "Use certified disease-free seeds."),
#                 "Corn_(maize)_healthy":
#                     ("✅ Healthy Maize Plant", "success",
#                      "Ensure adequate nitrogen levels and consistent irrigation."),
#                 "Corn_(maize)_Common_rust":
#                     ("⚠️ Common Rust (Puccinia sorghi)", "warning",
#                      "Apply **propiconazole** fungicide early. "
#                      "Use rust-resistant hybrid varieties."),
#                 "Corn_(maize)_Northern_Leaf_Blight":
#                     ("⚠️ Northern Leaf Blight", "warning",
#                      "Apply **azoxystrobin** or **propiconazole** at early stages. "
#                      "Practice crop rotation; avoid corn-after-corn."),
#                 "Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot":
#                     ("⚠️ Gray Leaf Spot", "warning",
#                      "Apply **strobilurin** fungicide. Choose tolerant hybrids. "
#                      "Till crop residues to reduce inoculum."),
#                 "Apple_healthy":
#                     ("✅ Healthy Apple Tree", "success",
#                      "Prune for good air flow. Apply dormant oil spray in late winter."),
#                 "Apple_Apple_scab":
#                     ("⚠️ Apple Scab (Venturia inaequalis)", "warning",
#                      "Apply **myclobutanil** or **captan** fungicide at bud break. "
#                      "Remove fallen leaves to reduce infection source."),
#                 "Apple_Black_rot":
#                     ("⚠️ Black Rot (Botryosphaeria obtusa)", "warning",
#                      "Prune out dead/infected wood. Apply **captan** fungicide. "
#                      "Remove mummified fruits from the tree."),
#                 "Apple_Cedar_apple_rust":
#                     ("⚠️ Cedar Apple Rust", "warning",
#                      "Apply **myclobutanil** fungicide early in spring. "
#                      "Remove nearby cedar/juniper trees if possible."),
#             }

#             advice_key = disease_name
#             if advice_key in disease_advice:
#                 diag_label, diag_type, diag_text = disease_advice[advice_key]
#                 if diag_type == "success":
#                     st.success(f"**{diag_label}**\n\n{diag_text}")
#                 elif diag_type == "warning":
#                     st.warning(f"**{diag_label}**\n\n{diag_text}")
#                 else:
#                     st.error(f"**{diag_label}**\n\n{diag_text}")
#             else:
#                 if is_healthy:
#                     st.success(
#                         f"**{disease_name.replace('_',' ')}** — Plant appears healthy. "
#                         "Maintain good watering, fertilization, and pest monitoring practices."
#                     )
#                 else:
#                     st.warning(
#                         f"**Detected: {disease_name.replace('_',' ')}**\n\n"
#                         "🌿 General advice:\n"
#                         "• Remove visibly infected leaves immediately.\n"
#                         "• Apply an appropriate fungicide or bactericide.\n"
#                         "• Improve air circulation and avoid overhead irrigation.\n"
#                         "• Consult your local agricultural extension officer for a precise diagnosis."
#                     )

#             st.markdown("---")

#             st.subheader("📊 Prediction Confidence (All Classes)")

#             prob_df = pd.DataFrame({
#                 "Disease":    disease_encoder.classes_,
#                 "Confidence": all_probs
#             }).sort_values("Confidence", ascending=False)

#             fig = px.bar(
#                 prob_df, x="Disease", y="Confidence",
#                 color="Confidence",
#                 text=(prob_df["Confidence"]*100).round(2).astype(str)+"%",
#                 color_continuous_scale="Reds",
#                 title="Model Confidence per Disease Class"
#             )
#             fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#             fig.update_layout(xaxis_tickangle=-35, height=430, showlegend=False)
#             fig.update_coloraxes(colorbar=colorbar_cfg())
#             st.plotly_chart(fig, use_container_width=True)

#             st.markdown("---")

#             st.subheader("📝 General Plant Health Tips")
#             t1, t2, t3 = st.columns(3)
#             t1.info("💧 **Water at the Base**\nAvoid wetting leaves — wet leaves promote fungal disease.")
#             t2.info("🌬️ **Air Circulation**\nProper spacing between plants reduces humidity and disease spread.")
#             t3.info("🔄 **Crop Rotation**\nRotate crops every season to break disease and pest cycles.")

#         except Exception as e:
#             st.error(f"❌ Disease prediction failed: `{str(e)}`")

#     else:
#         st.info(
#             "👆 Upload a leaf image above to get started.\n\n"
#             "**Supported formats:** JPG, JPEG, PNG, WEBP\n\n"
#             "**Tips for best results:**\n"
#             "• Use a clear, well-lit photo of a single leaf\n"
#             "• Avoid blurry or dark images\n"
#             "• Capture the affected area clearly\n"
#             "• Image size: any — the model resizes automatically to 128×128"
#         )

#         st.markdown("---")
#         st.subheader("🌿 Diseases This Model Can Detect")
#         st.caption(
#             "The model is trained on the classes present in your Disease_Dataset folder. "
#             "Below are the common diseases supported when using the PlantVillage dataset."
#         )

#         sample_diseases = [
#             "Tomato — Healthy",        "Tomato — Early Blight",
#             "Tomato — Late Blight",    "Tomato — Leaf Mold",
#             "Tomato — Mosaic Virus",   "Tomato — Spider Mites",
#             "Potato — Healthy",        "Potato — Early Blight",
#             "Potato — Late Blight",    "Pepper — Bacterial Spot",
#             "Corn — Common Rust",      "Corn — Northern Leaf Blight",
#             "Apple — Apple Scab",      "Apple — Black Rot",
#         ]

#         cols = st.columns(3)
#         for i, d in enumerate(sample_diseases):
#             cols[i % 3].write(f"• {d}")




# import os
# import io
# import numpy as np
# import pandas as pd
# import joblib
# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.io as pio
# from PIL import Image

# # ── Multilingual Voice Assistant: optional deps, fail gracefully ──
# try:
#     import speech_recognition as sr
#     from gtts import gTTS
#     from audio_recorder_streamlit import audio_recorder
#     VOICE_DEPS_OK = True
#     voice_import_error = None
# except Exception as _e:
#     VOICE_DEPS_OK = False
#     voice_import_error = str(_e)

# try:
#     from groq import Groq
#     GROQ_SDK_OK = True
# except Exception:
#     GROQ_SDK_OK = False

# # Load variables from a .env file (e.g. GROQ_API_KEY=...) into os.environ.
# DOTENV_PATH_FOUND = None
# try:
#     from dotenv import load_dotenv, find_dotenv
#     _dotenv_path = find_dotenv(usecwd=True)
#     if not _dotenv_path:
#         # Fallback: look right next to this script, regardless of which
#         # folder `streamlit run` was launched from.
#         _candidate = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
#         if os.path.exists(_candidate):
#             _dotenv_path = _candidate
#     if _dotenv_path:
#         DOTENV_PATH_FOUND = _dotenv_path
#     load_dotenv(_dotenv_path if _dotenv_path else None)
#     DOTENV_OK = True
# except Exception:
#     DOTENV_OK = False

# # =========================================================
# # ===== GLOBAL PLOTLY THEME ================================
# # =========================================================

# pio.templates["krishi"] = go.layout.Template(
#     layout=go.Layout(
#         paper_bgcolor="#ffffff",
#         plot_bgcolor="#f9fdf9",
#         font=dict(
#             color="#1a1a1a",
#             family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
#         ),
#         title=dict(font=dict(color="#0d2e0d", size=16)),
#         xaxis=dict(
#             color="#1a1a1a",
#             gridcolor="#d4ecd4",
#             linecolor="#81c784",
#             tickfont=dict(color="#1a1a1a"),
#             title=dict(font=dict(color="#1a1a1a")),
#             zerolinecolor="#c8e6c9",
#         ),
#         yaxis=dict(
#             color="#1a1a1a",
#             gridcolor="#d4ecd4",
#             linecolor="#81c784",
#             tickfont=dict(color="#1a1a1a"),
#             title=dict(font=dict(color="#1a1a1a")),
#             zerolinecolor="#c8e6c9",
#         ),
#         legend=dict(
#             bgcolor="#ffffff",
#             bordercolor="#c8e6c9",
#             font=dict(color="#1a1a1a"),
#         ),
#         coloraxis=dict(
#             colorbar=dict(
#                 tickfont=dict(color="#1a1a1a", size=12),
#                 tickcolor="#1a1a1a",
#                 title=dict(font=dict(color="#1a1a1a", size=13), side="right"),
#                 bgcolor="#ffffff",
#                 outlinecolor="#c8e6c9",
#                 outlinewidth=1,
#                 bordercolor="#c8e6c9",
#                 borderwidth=1,
#                 len=0.85,
#             )
#         ),
#         polar=dict(
#             bgcolor="#f9fdf9",
#             radialaxis=dict(color="#1a1a1a", gridcolor="#d4ecd4"),
#             angularaxis=dict(color="#1a1a1a", gridcolor="#d4ecd4"),
#         ),
#         colorway=["#2e7d32","#1f77b4","#ff7f0e","#d62728","#9467bd",
#                   "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"],
#     )
# )
# pio.templates.default = "krishi"

# # =========================================================
# # ================= PAGE CONFIG ===========================
# # =========================================================

# st.set_page_config(
#     page_title="Krishi AI — Smart Farming Assistant",
#     page_icon="🌱",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # =========================================================
# # ================= CUSTOM CSS ============================
# # =========================================================

# st.markdown("""
# <style>
#     /* ── Reset & Base ── */
#     html, body, [class*="css"] {
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }

#     /* ── Main app background: light green-white ── */
#     .stApp {
#         background-color: #f0f7f0;
#     }

#     /* ── ALL main content text: DARK (visible on light bg) ── */
#     .stApp p,
#     .stApp span,
#     .stApp div,
#     .stApp label,
#     .stApp li,
#     .stApp td,
#     .stApp th,
#     .stApp caption,
#     .stApp small,
#     .stApp strong,
#     .stApp em {
#         color: #1a1a1a !important;
#     }

#     /* ── Headings: dark green ── */
#     .stApp h1, .stApp h2, .stApp h3,
#     .stApp h4, .stApp h5, .stApp h6 {
#         color: #0d2e0d !important;
#         font-weight: 700;
#     }

#     /* ── Markdown text ── */
#     .stMarkdown, .stMarkdown p,
#     .stMarkdown span, .stMarkdown div,
#     .stMarkdown li, .stMarkdown strong,
#     .stMarkdown em {
#         color: #1a1a1a !important;
#     }

#     /* ── Sidebar: dark green gradient — WHITE text ── */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #0d2e0d 0%, #1a5c2a 50%, #2e7d32 100%);
#     }
#     [data-testid="stSidebar"],
#     [data-testid="stSidebar"] *,
#     [data-testid="stSidebar"] p,
#     [data-testid="stSidebar"] span,
#     [data-testid="stSidebar"] div,
#     [data-testid="stSidebar"] label,
#     [data-testid="stSidebar"] h1,
#     [data-testid="stSidebar"] h2,
#     [data-testid="stSidebar"] h3,
#     [data-testid="stSidebar"] strong,
#     [data-testid="stSidebar"] em,
#     [data-testid="stSidebar"] li,
#     [data-testid="stSidebar"] .stMarkdown,
#     [data-testid="stSidebar"] .stMarkdown p,
#     [data-testid="stSidebar"] .stMarkdown span,
#     [data-testid="stSidebar"] .stMarkdown div,
#     [data-testid="stSidebar"] .stCaption,
#     [data-testid="stSidebar"] .stSelectbox label {
#         color: #ffffff !important;
#     }

#     /* ── Header banner: WHITE text on dark bg ── */
#     .krishi-header {
#         background: linear-gradient(135deg, #0d2e0d, #1b5e20, #2e7d32, #388e3c);
#         padding: 2.2rem 1.5rem 1.8rem 1.5rem;
#         border-radius: 18px;
#         text-align: center;
#         margin-bottom: 1.8rem;
#         box-shadow: 0 6px 28px rgba(13,46,13,0.35);
#     }
#     .krishi-header h1 {
#         color: #ffffff !important;
#         font-size: 2.6rem;
#         margin: 0;
#         letter-spacing: 2px;
#         text-shadow: 0 2px 8px rgba(0,0,0,0.4);
#     }
#     .krishi-header p {
#         color: #c8e6c9 !important;
#         margin: 0.4rem 0 0 0;
#         font-size: 1.05rem;
#     }

#     /* ── Metric cards: WHITE bg, DARK text ── */
#     [data-testid="stMetric"] {
#         background: #ffffff !important;
#         border-radius: 12px !important;
#         padding: 0.9rem 1.1rem !important;
#         border-left: 4px solid #2e7d32 !important;
#         box-shadow: 0 3px 10px rgba(0,0,0,0.09) !important;
#     }
#     [data-testid="stMetric"] *,
#     [data-testid="stMetric"] label,
#     [data-testid="stMetric"] div,
#     [data-testid="stMetricLabel"],
#     [data-testid="stMetricLabel"] p,
#     [data-testid="stMetricLabel"] div,
#     [data-testid="stMetricValue"],
#     [data-testid="stMetricValue"] div {
#         color: #0d2e0d !important;
#     }
#     [data-testid="stMetricLabel"] p {
#         color: #2e7d32 !important;
#         font-weight: 600;
#     }
#     [data-testid="stMetricValue"] {
#         font-size: 1.6rem !important;
#         font-weight: 700 !important;
#     }

#     /* ── Dataframe: DARK text on light bg ── */
#     .stDataFrame,
#     .stDataFrame *,
#     [data-testid="stDataFrameContainer"],
#     [data-testid="stDataFrameContainer"] * {
#         color: #1a1a1a !important;
#     }
#     [data-testid="stDataFrameContainer"] {
#         border: 1px solid #c8e6c9;
#         border-radius: 10px;
#     }

#     /* ── Chat bubbles ── */
#     .chat-user {
#         background: #1b5e20;
#         border-radius: 16px 16px 4px 16px;
#         padding: 0.75rem 1.2rem;
#         margin: 0.4rem 0;
#         max-width: 80%;
#         margin-left: auto;
#         color: #ffffff !important;
#         font-weight: 500;
#         box-shadow: 0 2px 8px rgba(27,94,32,0.25);
#     }
#     .chat-user * { color: #ffffff !important; }

#     .chat-ai {
#         background: #ffffff;
#         border-radius: 16px 16px 16px 4px;
#         padding: 0.75rem 1.2rem;
#         margin: 0.4rem 0;
#         max-width: 85%;
#         border-left: 3px solid #43a047;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#         color: #1a1a1a !important;
#     }
#     .chat-ai * { color: #1a1a1a !important; }

#     .chat-label-user {
#         text-align: right;
#         font-size: 0.75rem;
#         color: #2e7d32 !important;
#         margin-bottom: 3px;
#         font-weight: 600;
#     }
#     .chat-label-ai {
#         font-size: 0.75rem;
#         color: #2e7d32 !important;
#         margin-bottom: 3px;
#         font-weight: 600;
#     }

#     /* ── Disease result card: WHITE bg, DARK text ── */
#     .disease-card {
#         background: #ffffff;
#         border-radius: 16px;
#         padding: 1.6rem;
#         box-shadow: 0 4px 18px rgba(0,0,0,0.10);
#         margin: 1rem 0;
#         border-top: 4px solid #2e7d32;
#     }
#     .disease-card,
#     .disease-card * {
#         color: #1a1a1a !important;
#     }

#     /* ── Buttons: WHITE text on dark green bg ── */
#     .stButton > button {
#         background: linear-gradient(135deg, #1b5e20, #2e7d32, #43a047) !important;
#         color: #ffffff !important;
#         border: none !important;
#         border-radius: 10px !important;
#         font-weight: 700 !important;
#         font-size: 0.95rem !important;
#         padding: 0.55rem 1.2rem !important;
#         transition: all 0.2s ease !important;
#         letter-spacing: 0.3px;
#     }
#     .stButton > button:hover {
#         transform: translateY(-2px) !important;
#         box-shadow: 0 6px 16px rgba(46,125,50,0.4) !important;
#         background: linear-gradient(135deg, #155218, #256427, #36883a) !important;
#     }
#     .stButton > button *,
#     .stButton > button span,
#     .stButton > button p {
#         color: #ffffff !important;
#     }

#     /* ── Alert boxes: DARK text on coloured bg ── */
#     div[data-testid="stNotification"] {
#         border-radius: 12px !important;
#     }
#     /* SUCCESS box */
#     [data-testid="stNotification"][kind="success"],
#     div.stSuccess,
#     div.stSuccess > div {
#         background-color: #d4edda !important;
#         border-color: #28a745 !important;
#         border-radius: 12px !important;
#     }
#     div.stSuccess p,
#     div.stSuccess div,
#     div.stSuccess span,
#     div.stSuccess li,
#     div.stSuccess strong,
#     div.stSuccess em {
#         color: #155724 !important;
#     }
#     /* INFO box */
#     div.stInfo,
#     div.stInfo > div {
#         background-color: #d1ecf1 !important;
#         border-color: #17a2b8 !important;
#         border-radius: 12px !important;
#     }
#     div.stInfo p,
#     div.stInfo div,
#     div.stInfo span,
#     div.stInfo li,
#     div.stInfo strong,
#     div.stInfo em {
#         color: #0c5460 !important;
#     }
#     /* WARNING box */
#     div.stWarning,
#     div.stWarning > div {
#         background-color: #fff3cd !important;
#         border-color: #ffc107 !important;
#         border-radius: 12px !important;
#     }
#     div.stWarning p,
#     div.stWarning div,
#     div.stWarning span,
#     div.stWarning li,
#     div.stWarning strong,
#     div.stWarning em {
#         color: #856404 !important;
#     }
#     /* ERROR box */
#     div.stError,
#     div.stError > div {
#         background-color: #f8d7da !important;
#         border-color: #dc3545 !important;
#         border-radius: 12px !important;
#     }
#     div.stError p,
#     div.stError div,
#     div.stError span,
#     div.stError li,
#     div.stError strong,
#     div.stError em {
#         color: #721c24 !important;
#     }

#     /* ── Selectbox & input labels: DARK text ── */
#     .stSelectbox label,
#     .stSlider label,
#     .stTextInput label,
#     .stFileUploader label,
#     .stMultiSelect label {
#         color: #1a1a1a !important;
#         font-weight: 600 !important;
#     }

#     /* ── Text input box ── */
#     .stTextInput input {
#         background: #ffffff !important;
#         color: #1a1a1a !important;
#         border: 1.5px solid #81c784 !important;
#         border-radius: 8px !important;
#     }
#     .stTextInput input::placeholder {
#         color: #5a8c5a !important;
#     }
#     .stTextInput input:focus {
#         border-color: #2e7d32 !important;
#         box-shadow: 0 0 0 2px rgba(46,125,50,0.2) !important;
#     }

#     /* ── Slider: DARK labels ── */
#     .stSlider [data-testid="stTickBar"] div,
#     [data-testid="stSlider"] div[data-testid="stThumbValue"],
#     [data-testid="stSlider"] * {
#         color: #1a1a1a !important;
#     }

#     /* ── Plotly chart container background ── */
#     .js-plotly-plot, .plotly, .plot-container {
#         background: #ffffff !important;
#         border-radius: 12px;
#     }

#     /* ── Plotly SVG text: DARK on white chart bg ── */
#     .js-plotly-plot .plotly .xtick text,
#     .js-plotly-plot .plotly .ytick text,
#     .js-plotly-plot .plotly .xtitle,
#     .js-plotly-plot .plotly .ytitle,
#     .js-plotly-plot .plotly .g-xtitle text,
#     .js-plotly-plot .plotly .g-ytitle text,
#     .js-plotly-plot .plotly .gtitle,
#     .js-plotly-plot .plotly .cbaxis text,
#     .js-plotly-plot .plotly .cbtitle text,
#     .js-plotly-plot .plotly .legend text {
#         fill: #1a1a1a !important;
#     }

#     /* ── Plotly bar text labels ON bars: WHITE ── */
#     .js-plotly-plot .plotly .bartext text,
#     .js-plotly-plot .plotly g.points text,
#     .js-plotly-plot .plotly .textpoint text,
#     .js-plotly-plot .plotly .trace text {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly colorbar background ── */
#     .js-plotly-plot .plotly .cbfill,
#     .js-plotly-plot .plotly rect.cbbg {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly modebar ── */
#     .modebar-container {
#         background: rgba(0,0,0,0.6) !important;
#         border-radius: 6px !important;
#     }
#     .modebar-btn path { fill: #ffffff !important; }
#     .modebar-btn:hover path { fill: #cccccc !important; }

#     /* ── Dataframe toolbar ── */
#     [data-testid="stElementToolbar"] {
#         background: #2e7d32 !important;
#         border-radius: 8px !important;
#         padding: 2px 4px !important;
#     }
#     [data-testid="stElementToolbar"] button svg path,
#     [data-testid="stElementToolbar"] button svg rect,
#     [data-testid="stElementToolbar"] button svg circle {
#         fill: #ffffff !important;
#         stroke: #ffffff !important;
#     }
#     [data-testid="stElementToolbar"] button:hover {
#         background: #1b5e20 !important;
#         border-radius: 4px !important;
#     }

#     /* ── Divider ── */
#     hr {
#         border-color: #a5d6a7;
#         margin: 1.8rem 0;
#     }

#     /* ── Caption text ── */
#     .stCaption,
#     [data-testid="stCaptionContainer"],
#     [data-testid="stCaptionContainer"] p {
#         color: #4a7c4a !important;
#     }

#     /* ── Selectbox dropdown: DARK text ── */ 
            
#     [data-testid="stSelectbox"] div[data-baseweb="select"] {
#         background: #0b1220 !important;  /* dark background */
#     }

#     [data-testid="stSelectbox"] div[data-baseweb="select"] *,
#     [data-testid="stSelectbox"] span {
#         color: #ffffff !important;       /* white text */
#     }
                
    

#     /* ── File uploader ── */
#     [data-testid="stFileUploader"] {
#         background: #ffffff !important;
#         border: 2px dashed #81c784 !important;
#         border-radius: 10px !important;
#     }
#     [data-testid="stFileUploader"] *,
#     [data-testid="stFileUploader"] p,
#     [data-testid="stFileUploader"] span,
#     [data-testid="stFileUploader"] div {
#         color: #1a1a1a !important;
#     }

#     /* ── Progress bar ── */
#     [data-testid="stProgressBar"] > div {
#         background-color: #2e7d32 !important;
#     }

#     /* ── Tabs ── */
#     [data-testid="stTabs"] [data-baseweb="tab"] {
#         color: #1a1a1a !important;
#     }
#     [data-testid="stTabs"] [aria-selected="true"] {
#         color: #2e7d32 !important;
#         border-bottom-color: #2e7d32 !important;
#     }

#     /* ── Column containers ── */
#     [data-testid="column"] { padding: 0 0.4rem; }

#     /* ── Scrollbar ── */
#     ::-webkit-scrollbar { width: 7px; height: 7px; }
#     ::-webkit-scrollbar-track { background: #e8f5e9; }
#     ::-webkit-scrollbar-thumb { background: #81c784; border-radius: 4px; }
#     ::-webkit-scrollbar-thumb:hover { background: #2e7d32; }

#     /* ── ChatGPT-style unified input bar (text + mic + send) ── */
#     .krishi-input-bar {
#         background: #ffffff;
#         border: 1.5px solid #c8e6c9;
#         border-radius: 28px;
#         padding: 0.35rem 0.5rem 0.35rem 1.1rem;
#         box-shadow: 0 3px 14px rgba(0,0,0,0.08);
#         display: flex;
#         align-items: center;
#     }
#     .krishi-input-bar:focus-within {
#         border-color: #2e7d32;
#         box-shadow: 0 0 0 2px rgba(46,125,50,0.15);
#     }
#     /* Remove the default boxed look from the text input so it blends
#        into the unified pill-shaped bar */
#     .krishi-input-row [data-testid="stTextInput"] > div {
#         background: transparent !important;
#         border: none !important;
#     }
#     .krishi-input-row .stTextInput input {
#         border: none !important;
#         background: transparent !important;
#         box-shadow: none !important;
#         padding-left: 0.2rem !important;
#         font-size: 1rem !important;
#     }
#     .krishi-input-row .stTextInput input:focus {
#         box-shadow: none !important;
#     }
#     /* Mic recorder + send button: circular, sit flush inside the bar */
#     .krishi-input-row [data-testid="column"] {
#         padding: 0 0.15rem !important;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }
#     .krishi-input-row .stButton > button {
#         border-radius: 50% !important;
#         width: 2.6rem !important;
#         height: 2.6rem !important;
#         padding: 0 !important;
#         font-size: 1.2rem !important;
#         line-height: 1 !important;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }
# </style>
# """, unsafe_allow_html=True)

# # =========================================================
# # ================= MULTILINGUAL VOICE ASSISTANT ==========
# # =========================================================
# # Setup:
# #   pip install SpeechRecognition gTTS audio-recorder-streamlit groq python-dotenv
# #   Put your key in a .env file (same folder as app.py):
# #       GROQ_API_KEY=gsk_....
# #   — or in .streamlit/secrets.toml:
# #       GROQ_API_KEY = "gsk_...."
# #   (Get a free key at https://console.groq.com/keys)
# # (Swap the LLM call in get_ai_response() for another provider
# #  if you prefer — only that one function needs to change.)

# LANGUAGES = {
#     "English":            {"speech": "en-IN", "tts": "en"},
#     "हिंदी (Hindi)":       {"speech": "hi-IN", "tts": "hi"},
#     "मराठी (Marathi)":     {"speech": "mr-IN", "tts": "mr"},
#     "বাংলা (Bengali)":     {"speech": "bn-IN", "tts": "bn"},
#     "தமிழ் (Tamil)":       {"speech": "ta-IN", "tts": "ta"},
#     "తెలుగు (Telugu)":     {"speech": "te-IN", "tts": "te"},
#     "ਪੰਜਾਬੀ (Punjabi)":    {"speech": "pa-IN", "tts": "pa"},
#     "ગુજરાતી (Gujarati)":  {"speech": "gu-IN", "tts": "gu"},
#     "ಕನ್ನಡ (Kannada)":     {"speech": "kn-IN", "tts": "kn"},
#     "മലയാളം (Malayalam)":  {"speech": "ml-IN", "tts": "ml"},
# }


# @st.cache_resource(show_spinner=False)
# def get_groq_client():
#     if not GROQ_SDK_OK:
#         return None
#     # Check the environment variable first (works even with no secrets.toml).
#     api_key = os.environ.get("GROQ_API_KEY")
#     # st.secrets raises an error (not just empty) if no secrets.toml exists
#     # anywhere — so this lookup must be wrapped in try/except.
#     if not api_key:
#         try:
#             api_key = st.secrets.get("GROQ_API_KEY")
#         except Exception:
#             api_key = None
#     if not api_key:
#         return None
#     try:
#         return Groq(api_key=api_key)
#     except Exception as e:
#         # e.g. "got an unexpected keyword argument 'proxies'" — a version
#         # mismatch between the groq package and httpx. Don't crash the
#         # whole app; report it in the diagnostics panel instead.
#         global GROQ_INIT_ERROR
#         GROQ_INIT_ERROR = str(e)
#         return None


# GROQ_INIT_ERROR = None


# groq_client = get_groq_client()


# def speech_to_text(audio_bytes, lang_code):
#     """Convert recorded microphone audio (WAV bytes) into text, in the
#     farmer's chosen Indian language, using free Google speech recognition."""
#     recognizer = sr.Recognizer()
#     try:
#         with io.BytesIO(audio_bytes) as wav_io:
#             with sr.AudioFile(wav_io) as source:
#                 audio_data = recognizer.record(source)
#         text = recognizer.recognize_google(audio_data, language=lang_code)
#         return text, None
#     except sr.UnknownValueError:
#         return None, "🙇 Sorry, I couldn't understand the audio clearly. Please try again, speaking slowly and close to the mic."
#     except sr.RequestError as e:
#         return None, f"⚠️ Speech recognition service error: {e}"
#     except Exception as e:
#         return None, f"⚠️ Could not process the audio: {e}"


# def text_to_speech(text, tts_lang_code):
#     """Synthesize speech audio (MP3 bytes) from text in real time using
#     gTTS — generated fresh every call, never pre-recorded."""
#     try:
#         clean_text = text.replace("**", "").replace("*", "")
#         tts = gTTS(text=clean_text, lang=tts_lang_code)
#         buf = io.BytesIO()
#         tts.write_to_fp(buf)
#         buf.seek(0)
#         return buf.read()
#     except Exception:
#         return None


# def rule_based_fallback(user_text):
#     """Tiny keyword fallback (English) so the assistant still responds
#     even if no LLM API key has been configured yet."""
#     q = user_text.lower()
#     if any(k in q for k in ["fertilizer", "npk", "urea", "nitrogen"]):
#         return "Get a soil test, then choose N-P-K fertilizer based on the deficiency it shows."
#     if any(k in q for k in ["disease", "pest", "blight", "fungus"]):
#         return "Try the Disease Detection tab — upload a leaf photo for a diagnosis and treatment advice."
#     if any(k in q for k in ["water", "irrigation", "rain"]):
#         return "Drip irrigation and morning/evening watering save water and reduce disease risk."
#     if any(k in q for k in ["crop", "grow", "plant"]):
#         return "Use the ML Prediction tab — enter your soil and weather values for an AI crop recommendation."
#     return "Please ask about crops, soil, fertilizer, irrigation, or plant disease for tailored advice."


# def get_ai_response(user_text, lang_name):
#     """Ask an LLM to respond like a knowledgeable Indian agricultural
#     extension officer, replying ONLY in the farmer's chosen language."""

#     system_prompt = (
#         "You are Krishi AI, a friendly, knowledgeable agricultural assistant "
#         "for Indian farmers. Give clear, practical, locally-relevant advice on "
#         "crops, soil, fertilizers, irrigation, weather, government schemes, "
#         "market prices, and plant diseases. "
#         f"Always reply ONLY in {lang_name}, using simple everyday language a "
#         "farmer can easily understand. Keep answers concise (under 120 words) "
#         "unless asked for more detail. Use a warm, respectful tone."
#     )

#     if groq_client is None:
#         if not GROQ_SDK_OK:
#             reason = "the `groq` Python package isn't installed — run `pip install groq`"
#         elif GROQ_INIT_ERROR:
#             reason = (
#                 f"the Groq client failed to start (`{GROQ_INIT_ERROR}`) — likely an "
#                 "`httpx` version mismatch. Try `pip install \"httpx==0.27.2\"`, then restart"
#             )
#         else:
#             reason = (
#                 "no `GROQ_API_KEY` could be found — check your `.env` file, "
#                 "environment variable, or `.streamlit/secrets.toml`, then "
#                 "**fully restart** `streamlit run app.py`"
#             )
#         return (
#             f"⚠️ *AI assistant not fully configured* — {reason}. "
#             "See the **🔧 AI Chat Diagnostics** panel in the sidebar for exact "
#             "status. Showing a basic English fallback for now:\n\n"
#             + rule_based_fallback(user_text)
#         )

#     try:
#         completion = groq_client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_text},
#             ],
#             temperature=0.4,
#             max_tokens=400,
#         )
#         return completion.choices[0].message.content.strip()
#     except Exception as e:
#         return f"⚠️ AI service error: {e}"


# # =========================================================
# # ================= HEADER ================================
# # =========================================================

# st.markdown("""
# <div class="krishi-header">
#     <h1>🌱 Krishi AI</h1>
#     <p>AI-Powered Smart Farming Assistant — Crop Recommendation · Disease Detection · Analytics</p>
# </div>
# """, unsafe_allow_html=True)

# # =========================================================
# # ================= LOAD DATASET ==========================
# # =========================================================

# DATASET_PATH = "Krishi_ai_dataset/cleaned_crop_dataset.csv"

# @st.cache_data(show_spinner=False)
# def load_dataset(path):
#     if not os.path.exists(path):
#         return None
#     return pd.read_csv(path)

# df = load_dataset(DATASET_PATH)

# if df is None:
#     st.error(
#         f"❌ Dataset not found at `{DATASET_PATH}`. "
#         "Please add the CSV file and restart."
#     )
#     st.stop()

# # =========================================================
# # ================= FEATURE CATEGORIES ====================
# # =========================================================

# def nitrogen_category(n):
#     if n <= 50:         return "Low"
#     elif n <= 120:      return "Medium"
#     else:               return "High"

# def phosphorus_category(p):
#     if p <= 40:         return "Low"
#     elif p <= 80:       return "Medium"
#     else:               return "High"

# def potassium_category(k):
#     if k <= 40:         return "Low"
#     elif k <= 80:       return "Medium"
#     else:               return "High"

# def temperature_category(temp):
#     if temp <= 20:      return "Cool"
#     elif temp <= 30:    return "Moderate"
#     else:               return "Hot"

# def humidity_category(hum):
#     if hum <= 40:       return "Low"
#     elif hum <= 70:     return "Medium"
#     else:               return "High"

# def ph_category(ph):
#     if ph < 6:          return "Acidic"
#     elif ph <= 7.5:     return "Neutral"
#     else:               return "Alkaline"

# def rainfall_category(rain):
#     if rain <= 100:     return "Low"
#     elif rain <= 200:   return "Medium"
#     else:               return "High"

# # =========================================================
# # ================= ADD CATEGORY COLUMNS ==================
# # =========================================================

# @st.cache_data(show_spinner=False)
# def enrich_dataframe(dataframe):
#     df2 = dataframe.copy()
#     df2["Nitrogen_Category"]    = df2["N"].apply(nitrogen_category)
#     df2["Phosphorus_Category"]  = df2["P"].apply(phosphorus_category)
#     df2["Potassium_Category"]   = df2["K"].apply(potassium_category)
#     df2["Temperature_Category"] = df2["temperature"].apply(temperature_category)
#     df2["Humidity_Category"]    = df2["humidity"].apply(humidity_category)
#     df2["PH_Category"]          = df2["ph"].apply(ph_category)
#     df2["Rainfall_Category"]    = df2["rainfall"].apply(rainfall_category)
#     return df2

# df = enrich_dataframe(df)

# # =========================================================
# # ================= LOAD ML FILES =========================
# # =========================================================

# @st.cache_resource(show_spinner=False)
# def load_ml_files():
#     try:
#         ml_model      = joblib.load("crop_model.pkl")
#         ml_scaler     = joblib.load("scaler.pkl")
#         ml_encoder    = joblib.load("label_encoder.pkl")
#         return ml_model, ml_scaler, ml_encoder, None
#     except FileNotFoundError as e:
#         return None, None, None, str(e)
#     except Exception as e:
#         return None, None, None, str(e)

# crop_model, crop_scaler, crop_encoder, ml_error = load_ml_files()

# # =========================================================
# # ================= LOAD DISEASE MODEL ====================
# # =========================================================

# @st.cache_resource(show_spinner=False)
# def load_disease_model():
#     try:
#         from tensorflow.keras.models import load_model
#         d_model   = load_model("plant_disease_model.h5")
#         d_encoder = joblib.load("disease_label_encoder.pkl")
#         return d_model, d_encoder, None
#     except FileNotFoundError as e:
#         return None, None, str(e)
#     except Exception as e:
#         return None, None, str(e)

# disease_model, disease_encoder, disease_error = load_disease_model()

# # =========================================================
# # ================= SIDEBAR ===============================
# # =========================================================

# with st.sidebar:
#     st.markdown("### 🌾 Navigation")
#     page = st.selectbox(
#         "Go To",
#         ["🏠 Home", "📊 Analytics", "🤖 ML Prediction", "🌿 Disease Detection"],
#         label_visibility="collapsed"
#     )

#     st.markdown("---")
#     st.markdown("### 📌 Quick Info")

#     total_crops  = df["label"].nunique()
#     total_rows   = df.shape[0]
#     ml_status    = "✅ Loaded" if crop_model  else "❌ Not Found"
#     dis_status   = "✅ Loaded" if disease_model else "❌ Not Found"

#     if not GROQ_SDK_OK:
#         ai_status = "❌ Package Missing"
#     elif groq_client is None:
#         ai_status = f"❌ Init Error: {GROQ_INIT_ERROR}" if GROQ_INIT_ERROR else "❌ No API Key Found"
#     else:
#         ai_status = "✅ Ready"

#     st.markdown(f"**Dataset Crops :** {total_crops}")
#     st.markdown(f"**Dataset Rows  :** {total_rows:,}")
#     st.markdown(f"**Crop Model    :** {ml_status}")
#     st.markdown(f"**Disease Model :** {dis_status}")
#     st.markdown(f"**AI Chat (Groq):** {ai_status}")

#     with st.expander("🔧 AI Chat Diagnostics"):
#         st.write("Groq package installed:", "✅ Yes" if GROQ_SDK_OK else "❌ No — run `pip install groq`")
#         st.write("python-dotenv installed:", "✅ Yes" if DOTENV_OK else "❌ No — run `pip install python-dotenv`")
#         st.write(".env file found at:", DOTENV_PATH_FOUND if DOTENV_PATH_FOUND else "❌ Not found")
#         if not DOTENV_PATH_FOUND:
#             try:
#                 _script_dir = os.path.dirname(os.path.abspath(__file__))
#                 _suspects = [
#                     f for f in os.listdir(_script_dir)
#                     if "env" in f.lower() and not f.lower().startswith("venv")
#                 ]
#                 st.write("Files with 'env' in the app folder:", _suspects if _suspects else "(none found)")
#                 st.caption(
#                     "If you see `.env.txt` above instead of `.env`, that's a common "
#                     "Windows Notepad issue — rename it so it has **no .txt at the end**."
#                 )
#             except Exception:
#                 pass
#         env_key_found = bool(os.environ.get("GROQ_API_KEY"))
#         try:
#             secrets_key_found = bool(st.secrets.get("GROQ_API_KEY"))
#         except Exception:
#             secrets_key_found = False
#         st.write("Key found (.env or environment variable):", "✅ Yes" if env_key_found else "❌ No")
#         st.write("Key found in .streamlit/secrets.toml:", "✅ Yes" if secrets_key_found else "❌ No")
#         if GROQ_INIT_ERROR:
#             st.error(
#                 f"Groq client failed to initialize: `{GROQ_INIT_ERROR}`\n\n"
#                 "This usually means `httpx` is too new for your `groq` package "
#                 "version (httpx ≥0.28 removed the `proxies` argument). Fix with:\n\n"
#                 "`pip install \"httpx==0.27.2\"`\n\nthen fully restart the app."
#             )
#         st.caption(
#             "If you just added/changed the key, you must **fully stop and restart** "
#             "`streamlit run app.py` — the key is only read once per server "
#             "start (cached), so a page refresh alone won't pick it up."
#         )

#     st.markdown("---")
#     st.caption("Krishi AI v2.0 — Built with ❤️ for Farmers")

# # =========================================================
# # Shared constants
# # =========================================================

# NUMERIC_FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
# FEATURE_LABELS   = ["Nitrogen", "Phosphorus", "Potassium",
#                     "Temperature", "Humidity", "pH", "Rainfall"]
# CROPS_LIST       = sorted(df["label"].unique())

# @st.cache_data(show_spinner=False)
# def get_crop_stats(dataframe):
#     means = dataframe.groupby("label")[NUMERIC_FEATURES].mean()
#     norm  = (means - means.min()) / (means.max() - means.min())
#     return means, norm

# CROP_MEANS, CROP_NORM = get_crop_stats(df)

# # =========================================================
# # Helper: colorbar config (dark tick text on white bg)
# # =========================================================

# def colorbar_cfg():
#     return dict(
#         bgcolor="#ffffff",
#         tickfont=dict(color="#1a1a1a", size=12),
#         tickcolor="#1a1a1a",
#         title=dict(font=dict(color="#1a1a1a", size=13)),
#         outlinecolor="#c8e6c9",
#         outlinewidth=1,
#     )

# # =========================================================
# # PAGE: HOME
# # =========================================================

# if page == "🏠 Home":

#     col_left, col_mid, col_right = st.columns([1, 2, 1])

#     with col_mid:

#         st.markdown("## 💬 Krishi AI Voice Assistant")
#         st.caption(
#             "Speak or type your farming question in your own language. "
#             "Krishi AI answers instantly — in text **and** voice."
#         )

#         if not VOICE_DEPS_OK:
#             st.warning(
#                 "🎤 Voice features need a few extra packages.\n\n"
#                 "Run: `pip install SpeechRecognition gTTS audio-recorder-streamlit`\n\n"
#                 f"(Details: `{voice_import_error}`)"
#             )

#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = []
#         if "selected_lang" not in st.session_state:
#             st.session_state.selected_lang = "हिंदी (Hindi)"

#         lang_col, clear_col = st.columns([3, 1])
#         with lang_col:
#             st.session_state.selected_lang = st.selectbox(
#                 "🌐 Choose your language",
#                 list(LANGUAGES.keys()),
#                 index=list(LANGUAGES.keys()).index(st.session_state.selected_lang),
#             )
#         with clear_col:
#             st.write("")
#             if st.button("🗑️ Clear Chat", use_container_width=True):
#                 st.session_state.chat_history = []
#                 st.rerun()

#         lang_codes = LANGUAGES[st.session_state.selected_lang]

#         # ── render chat history ──
#         for i, entry in enumerate(st.session_state.chat_history):
#             if entry["role"] == "user":
#                 st.markdown(
#                     f"<div class='chat-label-user'>You</div>"
#                     f"<div class='chat-user'>{entry['text']}</div>",
#                     unsafe_allow_html=True
#                 )
#             else:
#                 st.markdown(
#                     f"<div class='chat-label-ai'>🌱 Krishi AI</div>"
#                     f"<div class='chat-ai'>{entry['text']}</div>",
#                     unsafe_allow_html=True
#                 )
#                 if VOICE_DEPS_OK and st.button("🔊 Listen", key=f"listen_{i}"):
#                     audio_bytes = text_to_speech(entry["text"], lang_codes["tts"])
#                     if audio_bytes:
#                         st.audio(audio_bytes, format="audio/mp3", autoplay=True)
#                     else:
#                         st.warning("Could not generate voice for this reply.")

#         # ── Unified ChatGPT-style input bar: text box + mic + send, all in one row ──
#         st.markdown('<div class="krishi-input-bar krishi-input-row">', unsafe_allow_html=True)

#         if VOICE_DEPS_OK:
#             in_col, mic_col, send_col = st.columns([7, 1, 1.3])
#         else:
#             in_col, send_col = st.columns([8, 1.3])
#             mic_col = None

#         with in_col:
#             user_input = st.text_input(
#                 "Your question",
#                 placeholder="e.g.  लाल मिट्टी और कम बारिश में कौन सी फसल अच्छी होती है?",
#                 label_visibility="collapsed",
#                 key="home_input"
#             )

#         audio_bytes_in = None
#         if mic_col is not None:
#             with mic_col:
#                 audio_bytes_in = audio_recorder(
#                     text="",
#                     icon_size="1.4x",
#                     pause_threshold=2.0,
#                     recording_color="#dc3545",
#                     neutral_color="#2e7d32",
#                     key="mic_recorder",
#                 )

#         with send_col:
#             send_clicked = st.button("➤", use_container_width=True, key="send_btn")

#         st.markdown('</div>', unsafe_allow_html=True)

#         if VOICE_DEPS_OK:
#             st.caption(
#                 f"🎤 Tap the mic and speak, or type, in **{st.session_state.selected_lang}**. "
#                 "Recording stops automatically after a short pause."
#             )
#         else:
#             st.caption(f"⌨️ Type your question in **{st.session_state.selected_lang}**.")

#         # ── handle voice input ──
#         if audio_bytes_in:
#             with st.spinner("🎧 Listening & transcribing..."):
#                 transcribed, err = speech_to_text(audio_bytes_in, lang_codes["speech"])
#             if err:
#                 st.warning(err)
#             elif transcribed:
#                 st.session_state.chat_history.append({"role": "user", "text": transcribed})
#                 with st.spinner("🤖 Thinking..."):
#                     reply = get_ai_response(transcribed, st.session_state.selected_lang)
#                 st.session_state.chat_history.append({"role": "ai", "text": reply})
#                 audio_out = text_to_speech(reply, lang_codes["tts"])
#                 if audio_out:
#                     st.audio(audio_out, format="audio/mp3", autoplay=True)
#                 st.rerun()

#         # ── handle typed input (send button) ──
#         if send_clicked:
#             if not user_input.strip():
#                 st.warning("⚠️ Please type or speak a farming question first.")
#             else:
#                 st.session_state.chat_history.append({"role": "user", "text": user_input})
#                 with st.spinner("🤖 Thinking..."):
#                     reply = get_ai_response(user_input, st.session_state.selected_lang)
#                 st.session_state.chat_history.append({"role": "ai", "text": reply})
#                 if VOICE_DEPS_OK:
#                     audio_out = text_to_speech(reply, lang_codes["tts"])
#                     if audio_out:
#                         st.audio(audio_out, format="audio/mp3", autoplay=True)
#                 st.rerun()

#     st.markdown("---")

#     st.markdown("### 🚀 What Krishi AI Can Do For You")
#     c1, c2, c3 = st.columns(3)

#     with c1:
#         st.info(
#             "### 📊 Smart Analytics\n"
#             "Explore 24+ charts and insights about crops, soil nutrients, "
#             "rainfall, temperature, and more."
#         )
#     with c2:
#         st.success(
#             "### 🤖 Crop Prediction\n"
#             "Enter your soil and weather data to get an ML-powered crop "
#             "recommendation with confidence scores."
#         )
#     with c3:
#         st.warning(
#             "### 🌿 Disease Detection\n"
#             "Upload a leaf image and our CNN model will identify plant "
#             "diseases and suggest treatment in seconds."
#         )

# # =========================================================
# # PAGE: ANALYTICS
# # =========================================================

# elif page == "📊 Analytics":

#     st.header("📊 Krishi Data Analytics Dashboard")

#     st.subheader("📁 Dataset Overview")
#     c1, c2, c3, c4, c5 = st.columns(5)
#     c1.metric("Total Rows",      f"{df.shape[0]:,}")
#     c2.metric("Total Columns",   df.shape[1])
#     c3.metric("Unique Crops",    df["label"].nunique())
#     c4.metric("Duplicate Rows",  int(df.duplicated().sum()))
#     c5.metric("Missing Values",  int(df.isnull().sum().sum()))
#     st.markdown("---")

#     st.subheader("🔬 Data Quality Check")
#     q1, q2 = st.columns(2)
#     with q1:
#         st.write("#### Data Types")
#         dtype_df = df.dtypes.reset_index()
#         dtype_df.columns = ["Feature", "Type"]
#         dtype_df["Type"] = dtype_df["Type"].astype(str)
#         st.dataframe(dtype_df, use_container_width=True)
#     with q2:
#         st.write("#### Missing Values")
#         mv = df.isnull().sum().reset_index()
#         mv.columns = ["Feature", "Missing"]
#         st.dataframe(mv, use_container_width=True)
#         if mv["Missing"].sum() == 0:
#             st.success("✅ No missing values!")
#         if df.duplicated().sum() == 0:
#             st.success("✅ No duplicate rows!")
#     st.markdown("---")

#     st.subheader("🔍 Dataset Preview")
#     st.dataframe(df.head(50), use_container_width=True)
#     st.markdown("---")

#     st.subheader("📈 Statistical Summary")
#     st.dataframe(df.describe().round(2), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🌾 Crop Distribution")
#     crop_count = df["label"].value_counts().reset_index()
#     crop_count.columns = ["Crop", "Count"]

#     d1, d2 = st.columns(2)
#     with d1:
#         fig = px.bar(crop_count, x="Crop", y="Count",
#                      color="Count", color_continuous_scale="Greens",
#                      text="Count", title="Crop Count")
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(xaxis_tickangle=-45, showlegend=False, height=380)
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         st.plotly_chart(fig, use_container_width=True)
#     with d2:
#         fig2 = px.pie(crop_count, names="Crop", values="Count",
#                       title="Crop Share",
#                       color_discrete_sequence=px.colors.sequential.Greens_r)
#         fig2.update_traces(textposition="inside", textinfo="percent+label")
#         st.plotly_chart(fig2, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📊 Feature Category Analysis")
#     cat_cols = [
#         ("Nitrogen_Category", "Nitrogen"),
#         ("Phosphorus_Category", "Phosphorus"),
#         ("Potassium_Category", "Potassium"),
#         ("Temperature_Category", "Temperature"),
#         ("Humidity_Category", "Humidity"),
#         ("PH_Category", "Soil pH"),
#         ("Rainfall_Category", "Rainfall"),
#     ]
#     ca1, ca2 = st.columns(2)
#     for i, (col_name, title) in enumerate(cat_cols):
#         counts = df[col_name].value_counts().reset_index()
#         counts.columns = ["Category", "Count"]
#         fig = px.pie(counts, names="Category", values="Count",
#                      title=f"{title} Distribution", hole=0.4,
#                      color_discrete_sequence=px.colors.qualitative.Set2)
#         fig.update_traces(textinfo="percent+label")
#         (ca1 if i % 2 == 0 else ca2).plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     def climate_bar(feature, label, color_scale, unit=""):
#         grp = df.groupby("label")[feature].mean().round(2).reset_index()
#         grp.columns = ["Crop", label]
#         grp = grp.sort_values(label, ascending=True)
#         fig = px.bar(grp, x=label, y="Crop", orientation="h",
#                      title=f"Average {label} per Crop",
#                      color=label, color_continuous_scale=color_scale,
#                      text=label)
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(height=580, yaxis_title="")
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         return fig, grp

#     for feat, lbl, scale in [
#         ("temperature", "Avg Temperature (°C)", "RdYlGn_r"),
#         ("rainfall",    "Avg Rainfall (mm)",    "Blues"),
#         ("humidity",    "Avg Humidity (%)",      "Teal"),
#         ("ph",          "Avg pH",               "RdYlGn"),
#     ]:
#         icon = '🌡' if 'Temp' in lbl else '🌧' if 'Rain' in lbl else '💧' if 'Hum' in lbl else '🧪'
#         st.subheader(f"{icon} {lbl}")
#         fig, grp = climate_bar(feat, lbl, scale)
#         st.plotly_chart(fig, use_container_width=True)
#         t1, t2 = st.columns(2)
#         with t1:
#             st.write("**Top 5 (Highest)**")
#             st.dataframe(grp.tail(5)[::-1].reset_index(drop=True), use_container_width=True)
#         with t2:
#             st.write("**Bottom 5 (Lowest)**")
#             st.dataframe(grp.head(5).reset_index(drop=True), use_container_width=True)
#         st.markdown("---")

#     st.subheader("🪴 NPK Analysis")
#     avg_npk = df.groupby("label")[["N","P","K"]].mean().round(2).reset_index()
#     npk_m   = avg_npk.melt(id_vars="label", value_vars=["N","P","K"],
#                             var_name="Nutrient", value_name="Value")
#     cmap = {"N": "#2ca02c", "P": "#ff7f0e", "K": "#1f77b4"}

#     for mode, title in [("group","Grouped"), ("stack","Stacked — shows proportion")]:
#         fig = px.bar(npk_m, x="label", y="Value", color="Nutrient",
#                      barmode=mode, title=f"N, P, K per Crop ({title})",
#                      color_discrete_map=cmap,
#                      labels={"label":"Crop","Value":"mg/kg"})
#         fig.update_layout(xaxis_tickangle=-45, height=420)
#         st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(avg_npk.set_index("label"), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🧪 Soil Health Analysis")
#     c1,c2,c3 = st.columns(3)
#     c1.metric("Avg Nitrogen",   round(df["N"].mean(),2))
#     c2.metric("Avg Phosphorus", round(df["P"].mean(),2))
#     c3.metric("Avg Potassium",  round(df["K"].mean(),2))

#     soil = df.groupby("label")[["N","P","K"]].mean()
#     soil["Score"] = soil.mean(axis=1).round(2)
#     soil = soil.reset_index().sort_values("Score", ascending=False)
#     avg_s = soil["Score"].mean()

#     fig = px.bar(soil, x="label", y="Score", color="Score",
#                  color_continuous_scale="YlGn", text="Score",
#                  title="Soil Health Score (avg of N+P+K)")
#     fig.add_hline(y=avg_s, line_dash="dash", line_color="red",
#                   annotation_text=f"Avg: {avg_s:.1f}")
#     fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#     fig.update_layout(xaxis_tickangle=-45, height=420)
#     fig.update_coloraxes(colorbar=colorbar_cfg())
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("⚠️ Nutrient Deficiency Flag")
#     npk_flag = df.groupby("label")[["N","P","K"]].mean().round(2).reset_index()
#     npk_flag["N_Flag"] = npk_flag["N"].apply(lambda x: "⚠️ Low" if x<=50 else "✅ OK")
#     npk_flag["P_Flag"] = npk_flag["P"].apply(lambda x: "⚠️ Low" if x<=40 else "✅ OK")
#     npk_flag["K_Flag"] = npk_flag["K"].apply(lambda x: "⚠️ Low" if x<=40 else "✅ OK")
#     npk_flag["Status"] = npk_flag[["N_Flag","P_Flag","K_Flag"]].apply(
#         lambda r: "⚠️ Deficient" if "⚠️ Low" in r.values else "✅ Sufficient", axis=1)
#     deficient = npk_flag[npk_flag["Status"]=="⚠️ Deficient"]
#     if len(deficient):
#         st.warning(f"⚠️ {len(deficient)} crops have a nutrient in the Low range.")
#         st.dataframe(deficient[["label","N","N_Flag","P","P_Flag","K","K_Flag"]],
#                      use_container_width=True)
#     else:
#         st.success("✅ All crops have sufficient average NPK levels.")
#     st.markdown("---")

#     st.subheader("📏 Feature Range per Crop")
#     sel_feat = st.selectbox("Select Feature", NUMERIC_FEATURES, key="range_sel")
#     range_df = (df.groupby("label")[sel_feat]
#                 .agg(["min","max","mean","std"]).round(2).reset_index())
#     range_df.columns = ["Crop","Min","Max","Mean","Std Dev"]
#     range_df = range_df.sort_values("Mean", ascending=False)
#     fig = go.Figure(go.Bar(
#         x=range_df["Crop"], y=range_df["Mean"], name="Mean",
#         marker_color="#2ca02c",
#         error_y=dict(type="data", array=range_df["Std Dev"], visible=True),
#         text=range_df["Mean"], textposition="outside"
#     ))
#     fig.update_layout(title=f"{sel_feat} — Mean ± Std Dev",
#                       xaxis_tickangle=-45, height=440)
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(range_df.set_index("Crop"), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔵 Scatter Plot Analysis")
#     scatter_pairs = [
#         ("rainfall","humidity","Rainfall vs Humidity"),
#         ("temperature","ph","Temperature vs Soil pH"),
#         ("N","K","Nitrogen vs Potassium"),
#         ("temperature","rainfall","Temperature vs Rainfall"),
#     ]
#     s1, s2 = st.columns(2)
#     for i, (x, y, title) in enumerate(scatter_pairs):
#         fig = px.scatter(df, x=x, y=y, color="label",
#                          hover_name="label", title=title, opacity=0.6)
#         fig.update_layout(height=420, showlegend=False)
#         (s1 if i % 2 == 0 else s2).plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📦 Feature Distribution (Box Plot)")
#     box_sel = st.selectbox("Select Feature", NUMERIC_FEATURES, key="box_sel")
#     fig = px.box(df, x="label", y=box_sel, color="label",
#                  title=f"{box_sel} Distribution by Crop",
#                  color_discrete_sequence=px.colors.qualitative.Pastel)
#     fig.update_layout(xaxis_tickangle=-45, height=500, showlegend=False)
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📋 Complete Crop Profile")
#     full_prof = df.groupby("label")[NUMERIC_FEATURES].mean().round(2)
#     full_prof.columns = ["N (mg/kg)","P (mg/kg)","K (mg/kg)",
#                          "Temp (°C)","Humidity (%)","pH","Rainfall (mm)"]
#     st.dataframe(full_prof.style.background_gradient(cmap="YlGn", axis=0),
#                  use_container_width=True)
#     st.markdown("---")

#     st.subheader("⚖️ Crop-to-Crop Comparison")
#     cc1, cc2 = st.columns(2)
#     crop_a = cc1.selectbox("Crop A", CROPS_LIST, index=0, key="ca")
#     crop_b = cc2.selectbox("Crop B", CROPS_LIST, index=1, key="cb")

#     a_v = df[df["label"]==crop_a][NUMERIC_FEATURES].mean().round(2)
#     b_v = df[df["label"]==crop_b][NUMERIC_FEATURES].mean().round(2)

#     fig = go.Figure([
#         go.Bar(name=crop_a, x=FEATURE_LABELS, y=a_v.values,
#                marker_color="#2ca02c", text=a_v.values, textposition="outside"),
#         go.Bar(name=crop_b, x=FEATURE_LABELS, y=b_v.values,
#                marker_color="#1f77b4", text=b_v.values, textposition="outside"),
#     ])
#     fig.update_layout(barmode="group",
#                       title=f"{crop_a} vs {crop_b}", height=400)
#     st.plotly_chart(fig, use_container_width=True)

#     a_n = CROP_NORM.loc[crop_a].values.tolist()
#     b_n = CROP_NORM.loc[crop_b].values.tolist()
#     fig2 = go.Figure([
#         go.Scatterpolar(r=a_n+[a_n[0]], theta=NUMERIC_FEATURES+[NUMERIC_FEATURES[0]],
#                         fill="toself", name=crop_a,
#                         line_color="#2ca02c", fillcolor="rgba(44,160,44,0.15)"),
#         go.Scatterpolar(r=b_n+[b_n[0]], theta=NUMERIC_FEATURES+[NUMERIC_FEATURES[0]],
#                         fill="toself", name=crop_b,
#                         line_color="#1f77b4", fillcolor="rgba(31,119,180,0.15)"),
#     ])
#     fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])),
#                        title=f"Radar: {crop_a} vs {crop_b} (Normalized 0–1)", height=460)
#     st.plotly_chart(fig2, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔍 Similar Crops Finder")
#     target = st.selectbox("Select a Crop", CROPS_LIST, key="sim")
#     vec    = CROP_NORM.loc[target]
#     dists  = CROP_NORM.drop(target).apply(
#         lambda r: np.sqrt(((r - vec)**2).sum()), axis=1)
#     top3 = dists.nsmallest(3).reset_index()
#     top3.columns = ["Similar Crop","Distance (lower=closer)"]
#     top3["Distance (lower=closer)"] = top3["Distance (lower=closer)"].round(4)
#     st.write(f"**Top 3 crops most similar to {target}:**")
#     st.dataframe(top3, use_container_width=True)
#     sim_names   = top3["Similar Crop"].tolist()
#     sim_profile = CROP_MEANS.loc[[target]+sim_names].round(2)
#     st.dataframe(sim_profile.style.background_gradient(cmap="Greens", axis=0),
#                  use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔍 Crop Filter")
#     sel_crop  = st.selectbox("Select Crop", CROPS_LIST, key="filter")
#     crop_data = df[df["label"]==sel_crop]
#     m1,m2,m3,m4 = st.columns(4)
#     m1.metric("Avg Temp",     f"{crop_data['temperature'].mean():.1f} °C")
#     m2.metric("Avg Humidity", f"{crop_data['humidity'].mean():.1f} %")
#     m3.metric("Avg Rainfall", f"{crop_data['rainfall'].mean():.1f} mm")
#     m4.metric("Avg pH",       f"{crop_data['ph'].mean():.2f}")
#     n1,n2,n3 = st.columns(3)
#     n1.metric("Avg Nitrogen",   round(crop_data["N"].mean(),2))
#     n2.metric("Avg Phosphorus", round(crop_data["P"].mean(),2))
#     n3.metric("Avg Potassium",  round(crop_data["K"].mean(),2))
#     st.dataframe(crop_data, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔗 Feature Correlation Matrix")
#     corr = df[NUMERIC_FEATURES].corr().round(3)
#     fig  = px.imshow(corr, text_auto=True, color_continuous_scale="RdYlGn",
#                      zmin=-1, zmax=1, title="Feature Correlation Heatmap")
#     fig.update_layout(height=480)
#     fig.update_coloraxes(colorbar=colorbar_cfg())
#     st.plotly_chart(fig, use_container_width=True)
#     st.caption("🟢 Green = positive | 🔴 Red = negative | ⚪ White = no correlation")

#     pairs = corr.unstack().reset_index()
#     pairs.columns = ["Feature A","Feature B","Correlation"]
#     pairs = pairs[pairs["Feature A"] < pairs["Feature B"]]
#     pairs["Abs"] = pairs["Correlation"].abs()
#     pairs = pairs.sort_values("Abs", ascending=False).drop(columns="Abs")
#     pc1, pc2 = st.columns(2)
#     with pc1:
#         st.write("**Top 3 Positive**")
#         st.dataframe(pairs[pairs["Correlation"]>0].head(3).reset_index(drop=True),
#                      use_container_width=True)
#     with pc2:
#         st.write("**Top 3 Negative**")
#         st.dataframe(pairs[pairs["Correlation"]<0].head(3).reset_index(drop=True),
#                      use_container_width=True)
#     st.markdown("---")

#     st.subheader("📘 Feature Meaning")
#     feat_info = pd.DataFrame({
#         "Feature": ["N","P","K","temperature","humidity","ph","rainfall"],
#         "Meaning": [
#             "Nitrogen — leaf and stem growth",
#             "Phosphorus — root and flower growth",
#             "Potassium — plant strength and disease resistance",
#             "Temperature — optimal growing temperature",
#             "Humidity — moisture level in the air",
#             "Soil pH — acidity or alkalinity",
#             "Rainfall — water requirement"
#         ],
#         "Unit": ["mg/kg","mg/kg","mg/kg","°C","%","0–14","mm"]
#     })
#     st.dataframe(feat_info, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🌱 Farmer Understanding Guide")
#     g1, g2 = st.columns(2)
#     with g1:
#         st.success("🟢 **Low Nitrogen (≤50)** → Light fertilizer needed")
#         st.info("🔵 **Medium Nitrogen (51–120)** → Balanced fertilizer")
#         st.warning("🟡 **High Nitrogen (>120)** → Heavy fertilizer needed")
#         st.success("🟢 **Cool (≤20°C)** → Wheat, lentil, chickpea")
#         st.info("🔵 **Moderate (21–30°C)** → Most common crops")
#         st.warning("🟡 **Hot (>30°C)** → Tropical/summer crops")
#     with g2:
#         st.success("🟢 **Acidic (pH<6)** → Tea, rice, blueberry")
#         st.info("🔵 **Neutral (pH 6–7.5)** → Best for most crops")
#         st.warning("🟡 **Alkaline (pH>7.5)** → Cotton, maize")
#         st.success("🟢 **Low Rainfall (≤100mm)** → Drought-tolerant crops")
#         st.info("🔵 **Medium Rainfall (101–200mm)** → General crops")
#         st.warning("🟡 **High Rainfall (>200mm)** → Water-intensive crops")
#     st.markdown("---")

#     st.subheader("📌 Key Insights")
#     st.success("✅ Dataset is balanced with nearly equal crop distribution.")
#     st.success("✅ No missing values or duplicate rows found.")
#     st.success("✅ Dataset is clean and ready for ML model training.")
#     st.info("📊 Rainfall, temperature, humidity and soil nutrients drive crop suitability.")
#     st.info("🌱 Rice and jute need high humidity & rainfall; chickpea and kidney beans prefer dry conditions.")
#     st.info("🧪 Use Scatter and Box Plots to identify natural clusters for ML feature selection.")
#     st.info("⚖️ Use Crop Comparison and Similar Crops to help farmers choose alternative crops.")

# # =========================================================
# # PAGE: ML PREDICTION
# # =========================================================

# elif page == "🤖 ML Prediction":

#     st.header("🤖 AI-Powered Crop Recommendation")
#     st.markdown("---")

#     if ml_error:
#         st.error(
#             f"❌ Could not load ML model files.\n\n"
#             f"**Error:** `{ml_error}`\n\n"
#             "Please make sure `crop_model.pkl`, `scaler.pkl`, and "
#             "`label_encoder.pkl` are in the same folder as `app.py`."
#         )
#         st.stop()

#     if hasattr(crop_model, "feature_importances_"):
#         st.subheader("📈 Model Feature Importance")
#         imp_df = pd.DataFrame({
#             "Feature":    FEATURE_LABELS,
#             "Importance": crop_model.feature_importances_
#         }).sort_values("Importance", ascending=False)

#         fig = px.bar(imp_df, x="Feature", y="Importance",
#                      color="Importance", color_continuous_scale="Teal",
#                      text=imp_df["Importance"].round(3),
#                      title="Feature Importance (Higher = More Influential)")
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(height=380)
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         st.plotly_chart(fig, use_container_width=True)
#         st.info(
#             f"🔑 Most influential: **{imp_df.iloc[0]['Feature']}**  |  "
#             f"📉 Least influential: **{imp_df.iloc[-1]['Feature']}**"
#         )
#         st.markdown("---")

#     st.subheader("🌱 Enter Your Soil and Weather Conditions")

#     sl1, sl2 = st.columns(2)

#     with sl1:
#         N = st.slider("Nitrogen (N) mg/kg",
#                       int(df["N"].min()), int(df["N"].max()), int(df["N"].mean()))
#         P = st.slider("Phosphorus (P) mg/kg",
#                       int(df["P"].min()), int(df["P"].max()), int(df["P"].mean()))
#         K = st.slider("Potassium (K) mg/kg",
#                       int(df["K"].min()), int(df["K"].max()), int(df["K"].mean()))
#         temperature = st.slider("Temperature (°C)",
#                                 float(df["temperature"].min()),
#                                 float(df["temperature"].max()),
#                                 round(float(df["temperature"].mean()),1))
#     with sl2:
#         humidity = st.slider("Humidity (%)",
#                              float(df["humidity"].min()),
#                              float(df["humidity"].max()),
#                              round(float(df["humidity"].mean()),1))
#         ph = st.slider("Soil pH",
#                        float(df["ph"].min()), float(df["ph"].max()),
#                        round(float(df["ph"].mean()),1))
#         rainfall = st.slider("Rainfall (mm)",
#                              float(df["rainfall"].min()),
#                              float(df["rainfall"].max()),
#                              round(float(df["rainfall"].mean()),1))

#     st.markdown("---")
#     st.subheader("📊 Real-Time Input Analysis")
#     ia1, ia2, ia3, ia4 = st.columns(4)
#     ia1.info(f"🌿 N: **{nitrogen_category(N)}**\n\n💧 Humidity: **{humidity_category(humidity)}**")
#     ia2.info(f"🌿 P: **{phosphorus_category(P)}**\n\n🧪 Soil pH: **{ph_category(ph)}**")
#     ia3.info(f"🌿 K: **{potassium_category(K)}**\n\n🌧 Rainfall: **{rainfall_category(rainfall)}**")
#     ia4.info(f"🌡 Temp: **{temperature_category(temperature)}**")

#     st.markdown("---")

#     if st.button("🌾 Predict Best Crop", use_container_width=True):
#         try:
#             inp        = [[N, P, K, temperature, humidity, ph, rainfall]]
#             scaled     = crop_scaler.transform(inp)
#             prediction = crop_model.predict(scaled)
#             pred_crop  = crop_encoder.inverse_transform(prediction)[0]

#             st.success(f"✅ Recommended Crop: **{pred_crop.upper()}**")
#             st.markdown("---")

#             if hasattr(crop_model, "predict_proba"):
#                 st.subheader("📊 Top 5 Crop Predictions")
#                 proba  = crop_model.predict_proba(scaled)[0]
#                 prob_df = pd.DataFrame({
#                     "Crop":        crop_encoder.classes_,
#                     "Probability": proba
#                 }).sort_values("Probability", ascending=False).head(5)
#                 prob_df["Pct"] = (prob_df["Probability"]*100).round(2)

#                 fig = px.bar(prob_df, x="Crop", y="Probability",
#                              color="Probability",
#                              text=prob_df["Pct"].astype(str)+"%",
#                              color_continuous_scale="Greens",
#                              title="Prediction Confidence (Top 5)")
#                 fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#                 fig.update_layout(height=420)
#                 fig.update_coloraxes(colorbar=colorbar_cfg())
#                 st.plotly_chart(fig, use_container_width=True)

#                 top_pct = prob_df.iloc[0]["Pct"]
#                 if top_pct >= 80:
#                     st.success(f"🎯 High confidence: {top_pct}%")
#                 elif top_pct >= 50:
#                     st.info(f"🔍 Moderate confidence: {top_pct}% — verify with local conditions.")
#                 else:
#                     st.warning(f"⚠️ Low confidence: {top_pct}% — consult an agronomist.")
#                 st.markdown("---")

#             st.subheader(f"📐 Your Conditions vs Ideal for {pred_crop.capitalize()}")
#             ideal = df[df["label"]==pred_crop][NUMERIC_FEATURES].mean().round(2)
#             user_vals = [N, P, K, temperature, humidity, ph, rainfall]

#             fig = go.Figure([
#                 go.Bar(name="Your Input", x=FEATURE_LABELS, y=user_vals,
#                        marker_color="#1f77b4",
#                        text=[round(v,2) for v in user_vals], textposition="outside"),
#                 go.Bar(name=f"Ideal for {pred_crop}", x=FEATURE_LABELS,
#                        y=ideal.values, marker_color="#2ca02c",
#                        text=ideal.values, textposition="outside"),
#             ])
#             fig.update_layout(barmode="group",
#                               title=f"Your Input vs Ideal: {pred_crop}",
#                               height=400)
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown("---")

#             st.subheader("📋 Input Summary")
#             summ = pd.DataFrame({
#                 "Feature": ["Nitrogen (mg/kg)","Phosphorus (mg/kg)","Potassium (mg/kg)",
#                             "Temperature (°C)","Humidity (%)","Soil pH","Rainfall (mm)"],
#                 "Value":    [N, P, K, temperature, humidity, ph, rainfall],
#                 "Category": [nitrogen_category(N), phosphorus_category(P),
#                              potassium_category(K), temperature_category(temperature),
#                              humidity_category(humidity), ph_category(ph),
#                              rainfall_category(rainfall)]
#             })
#             st.dataframe(summ, use_container_width=True)
#             st.markdown("---")

#             st.subheader("🌱 Crop Advice")
#             crop_advice = {
#                 "rice":        "Requires high rainfall (150–300mm), high humidity (80–90%), and slightly acidic soil (pH 5.5–6.5).",
#                 "maize":       "Needs moderate rainfall, moderate temperature (21–27°C), and fertile loamy soil (pH 5.5–7.0).",
#                 "jute":        "Thrives in high humidity and rainfall. Requires warm climate (25–35°C) and alluvial soil.",
#                 "cotton":      "Grows well in well-drained black soil (pH 6–8), warm climate (21–35°C), and moderate rainfall.",
#                 "coconut":     "Requires tropical climate, high humidity (70–80%), and sandy loam soil.",
#                 "papaya":      "Needs warm climate (25–30°C), well-drained soil, moderate rainfall, and high humidity.",
#                 "banana":      "Requires rich loamy soil, high humidity, warm temperature (26–30°C), and regular rainfall.",
#                 "mango":       "Prefers deep well-drained soil, dry season at flowering, and tropical/subtropical climate.",
#                 "grapes":      "Needs well-drained sandy loam, dry hot summers and cool winters.",
#                 "watermelon":  "Requires warm climate (25–35°C), sandy loam soil, and moderate to high rainfall.",
#                 "muskmelon":   "Grows best in warm climate, sandy soil with good drainage, and moderate humidity.",
#                 "apple":       "Requires cool climate (cold winters for dormancy), loamy soil, and moderate rainfall.",
#                 "orange":      "Needs subtropical climate, well-drained sandy loam, and moderate rainfall (750–1200mm).",
#                 "pomegranate": "Drought-tolerant, wide pH range (5.5–7.5), grows well in semi-arid regions.",
#                 "lentil":      "Cool season crop, well-drained loamy soil (pH 6–8), low rainfall.",
#                 "blackgram":   "Warm climate (25–35°C), well-drained loamy soil, moderate rainfall (600–800mm).",
#                 "mungbean":    "Warm season, sandy loam soil, short rainfall period, moderate temperature (28–30°C).",
#                 "mothbeans":   "Drought-tolerant, arid/semi-arid regions, sandy soil, very low rainfall.",
#                 "pigeonpeas":  "Drought-tolerant legume, well-drained soil (pH 5–7), moderate rainfall.",
#                 "kidneybeans": "Cool temperature, well-drained fertile loam (pH 6–7), moderate rainfall.",
#                 "chickpea":    "Cool season, drought-tolerant, loamy soil (pH 5.5–7), low rainfall.",
#                 "coffee":      "Tropical climate (15–28°C), high humidity, acidic well-drained soil (pH 6–6.5), high rainfall."
#             }
#             advice = crop_advice.get(
#                 pred_crop.lower(),
#                 f"{pred_crop.capitalize()} is suited to the conditions you entered. "
#                 "Consult local agricultural guidelines for detailed advice."
#             )
#             st.info(f"🌿 **{pred_crop.capitalize()} Advice:** {advice}")
#             st.markdown("---")

#             st.subheader("🧪 Soil & Climate Summary")
#             sc1, sc2 = st.columns(2)
#             with sc1:
#                 if ph < 6:
#                     st.warning("⚠️ **Acidic Soil** — add lime to raise pH.")
#                 elif ph > 7.5:
#                     st.warning("⚠️ **Alkaline Soil** — add sulfur to lower pH.")
#                 else:
#                     st.success("✅ **Neutral Soil pH** — ideal for most crops.")
#                 n_cat = nitrogen_category(N)
#                 if n_cat == "Low":
#                     st.warning("⚠️ Low Nitrogen — apply urea or nitrogen-rich fertilizer.")
#                 elif n_cat == "High":
#                     st.info("ℹ️ High Nitrogen — reduce fertilizer application.")
#                 else:
#                     st.success("✅ Nitrogen level is balanced.")
#             with sc2:
#                 if rainfall > 200:
#                     st.info("🌧 High rainfall — ensure good field drainage.")
#                 elif rainfall < 80:
#                     st.info("☀️ Low rainfall — consider drip irrigation.")
#                 else:
#                     st.success("✅ Moderate rainfall — suitable for most crops.")
#                 t_cat = temperature_category(temperature)
#                 if t_cat == "Cool":
#                     st.info("❄️ Cool climate — suitable for wheat, lentil, chickpea.")
#                 elif t_cat == "Hot":
#                     st.info("🔥 Hot climate — suitable for tropical/summer crops.")
#                 else:
#                     st.success("✅ Moderate temperature — good for most crops.")

#         except Exception as e:
#             st.error(f"❌ Prediction failed: `{str(e)}`")

# # =========================================================
# # PAGE: DISEASE DETECTION
# # =========================================================

# elif page == "🌿 Disease Detection":

#     st.header("🌿 Plant Disease Detection System")
#     st.markdown("---")

#     if disease_error:
#         st.error(
#             f"❌ Disease model not found.\n\n"
#             f"**Error:** `{disease_error}`\n\n"
#             "Run `train_disease_model.py` first to train and save the model, "
#             "then restart the app."
#         )
#         st.stop()

#     st.subheader("📤 Upload a Plant Leaf Image")
#     st.caption(
#         "Upload a clear photo of a plant leaf. "
#         "The AI will predict whether it is healthy or diseased."
#     )

#     uploaded = st.file_uploader(
#         "Drag & drop or click to browse",
#         type=["jpg","jpeg","png","webp"],
#         label_visibility="collapsed"
#     )

#     if uploaded is not None:

#         image = Image.open(uploaded).convert("RGB")

#         col_img, col_res = st.columns([1, 1])

#         with col_img:
#             st.image(image, caption="Uploaded Leaf Image", use_column_width=True)

#         img_resized = image.resize((128, 128))
#         img_array   = np.array(img_resized, dtype="float32") / 255.0
#         img_array   = np.expand_dims(img_array, axis=0)

#         try:
#             preds         = disease_model.predict(img_array, verbose=0)
#             pred_idx      = int(np.argmax(preds))
#             disease_name  = disease_encoder.inverse_transform([pred_idx])[0]
#             confidence    = float(np.max(preds)) * 100
#             all_probs     = preds[0]

#             with col_res:
#                 st.markdown('<div class="disease-card">', unsafe_allow_html=True)

#                 if confidence >= 75:
#                     st.success(f"✅ **Predicted:** {disease_name.replace('_', ' ')}")
#                 elif confidence >= 50:
#                     st.warning(f"⚠️ **Predicted (Moderate Confidence):** {disease_name.replace('_', ' ')}")
#                 else:
#                     st.error(f"❓ **Low Confidence Prediction:** {disease_name.replace('_', ' ')}")

#                 st.metric("Confidence", f"{confidence:.2f}%")
#                 st.progress(int(min(confidence, 100)))

#                 is_healthy = "healthy" in disease_name.lower()
#                 if is_healthy:
#                     st.success("🌿 Your plant appears **HEALTHY**!")
#                 else:
#                     st.error("🦠 Disease detected — see treatment advice below.")

#                 st.markdown('</div>', unsafe_allow_html=True)

#             st.markdown("---")

#             st.subheader("💊 Treatment & Care Advice")

#             disease_advice = {
#                 "Tomato_healthy":
#                     ("✅ Healthy Plant", "success",
#                      "Maintain regular watering (avoid overhead irrigation), "
#                      "balanced fertilization, and good air circulation."),
#                 "Tomato_Early_blight":
#                     ("⚠️ Early Blight (Alternaria solani)", "warning",
#                      "Remove infected lower leaves immediately. Apply **mancozeb** "
#                      "or **chlorothalonil** fungicide every 7–10 days. Avoid overhead "
#                      "watering and ensure good air flow around plants."),
#                 "Tomato_Late_blight":
#                     ("🚨 Late Blight (Phytophthora infestans)", "error",
#                      "Act fast — this spreads rapidly. Remove and destroy infected "
#                      "plants. Apply **copper-based fungicide** or **metalaxyl**. "
#                      "Avoid watering leaves; water at the base."),
#                 "Tomato_Leaf_Mold":
#                     ("⚠️ Leaf Mold (Passalora fulva)", "warning",
#                      "Improve greenhouse/field air circulation. Reduce humidity. "
#                      "Apply **copper** or **sulfur-based fungicide**. Remove affected leaves."),
#                 "Tomato_Septoria_leaf_spot":
#                     ("⚠️ Septoria Leaf Spot", "warning",
#                      "Remove infected leaves. Apply **mancozeb** fungicide. "
#                      "Rotate crops and avoid overhead irrigation."),
#                 "Tomato_Spider_mites":
#                     ("⚠️ Spider Mites", "warning",
#                      "Spray plants with water to dislodge mites. "
#                      "Apply **neem oil** or **insecticidal soap**. "
#                      "Introduce predatory mites as biological control."),
#                 "Tomato_Target_Spot":
#                     ("⚠️ Target Spot", "warning",
#                      "Remove infected leaves. Apply **azoxystrobin** or "
#                      "**chlorothalonil** fungicide. Ensure good air circulation."),
#                 "Tomato_Mosaic_Virus":
#                     ("🚨 Tomato Mosaic Virus", "error",
#                      "No cure available. Remove and destroy infected plants to prevent spread. "
#                      "Control aphids (virus vectors) with **neem oil**. Sanitize tools."),
#                 "Tomato_Yellow_Leaf_Curl_Virus":
#                     ("🚨 Yellow Leaf Curl Virus", "error",
#                      "Spread by whiteflies — apply **imidacloprid** to control them. "
#                      "Remove infected plants. Use virus-resistant tomato varieties."),
#                 "Tomato_Bacterial_spot":
#                     ("⚠️ Bacterial Spot (Xanthomonas)", "warning",
#                      "Apply **copper-based bactericide** (copper hydroxide). "
#                      "Avoid working with plants when wet. Practice crop rotation."),
#                 "Potato_healthy":
#                     ("✅ Healthy Potato Plant", "success",
#                      "Keep soil consistently moist but not waterlogged. "
#                      "Earth up around stems to prevent greening."),
#                 "Potato_Early_blight":
#                     ("⚠️ Potato Early Blight", "warning",
#                      "Apply **mancozeb** or **chlorothalonil** fungicide. "
#                      "Remove heavily infected leaves. Avoid nitrogen excess."),
#                 "Potato_Late_blight":
#                     ("🚨 Potato Late Blight (Phytophthora infestans)", "error",
#                      "Most destructive potato disease. Apply **metalaxyl** or "
#                      "**cymoxanil** fungicide immediately. Destroy infected tubers. "
#                      "Do not compost infected material."),
#                 "Pepper,_bell_healthy":
#                     ("✅ Healthy Bell Pepper", "success",
#                      "Maintain consistent moisture, full sun, and warm temperatures (20–30°C)."),
#                 "Pepper,_bell_Bacterial_spot":
#                     ("⚠️ Bacterial Spot (Xanthomonas)", "warning",
#                      "Apply **copper hydroxide** spray. Avoid overhead watering. "
#                      "Use certified disease-free seeds."),
#                 "Corn_(maize)_healthy":
#                     ("✅ Healthy Maize Plant", "success",
#                      "Ensure adequate nitrogen levels and consistent irrigation."),
#                 "Corn_(maize)_Common_rust":
#                     ("⚠️ Common Rust (Puccinia sorghi)", "warning",
#                      "Apply **propiconazole** fungicide early. "
#                      "Use rust-resistant hybrid varieties."),
#                 "Corn_(maize)_Northern_Leaf_Blight":
#                     ("⚠️ Northern Leaf Blight", "warning",
#                      "Apply **azoxystrobin** or **propiconazole** at early stages. "
#                      "Practice crop rotation; avoid corn-after-corn."),
#                 "Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot":
#                     ("⚠️ Gray Leaf Spot", "warning",
#                      "Apply **strobilurin** fungicide. Choose tolerant hybrids. "
#                      "Till crop residues to reduce inoculum."),
#                 "Apple_healthy":
#                     ("✅ Healthy Apple Tree", "success",
#                      "Prune for good air flow. Apply dormant oil spray in late winter."),
#                 "Apple_Apple_scab":
#                     ("⚠️ Apple Scab (Venturia inaequalis)", "warning",
#                      "Apply **myclobutanil** or **captan** fungicide at bud break. "
#                      "Remove fallen leaves to reduce infection source."),
#                 "Apple_Black_rot":
#                     ("⚠️ Black Rot (Botryosphaeria obtusa)", "warning",
#                      "Prune out dead/infected wood. Apply **captan** fungicide. "
#                      "Remove mummified fruits from the tree."),
#                 "Apple_Cedar_apple_rust":
#                     ("⚠️ Cedar Apple Rust", "warning",
#                      "Apply **myclobutanil** fungicide early in spring. "
#                      "Remove nearby cedar/juniper trees if possible."),
#             }

#             advice_key = disease_name
#             if advice_key in disease_advice:
#                 diag_label, diag_type, diag_text = disease_advice[advice_key]
#                 if diag_type == "success":
#                     st.success(f"**{diag_label}**\n\n{diag_text}")
#                 elif diag_type == "warning":
#                     st.warning(f"**{diag_label}**\n\n{diag_text}")
#                 else:
#                     st.error(f"**{diag_label}**\n\n{diag_text}")
#             else:
#                 if is_healthy:
#                     st.success(
#                         f"**{disease_name.replace('_',' ')}** — Plant appears healthy. "
#                         "Maintain good watering, fertilization, and pest monitoring practices."
#                     )
#                 else:
#                     st.warning(
#                         f"**Detected: {disease_name.replace('_',' ')}**\n\n"
#                         "🌿 General advice:\n"
#                         "• Remove visibly infected leaves immediately.\n"
#                         "• Apply an appropriate fungicide or bactericide.\n"
#                         "• Improve air circulation and avoid overhead irrigation.\n"
#                         "• Consult your local agricultural extension officer for a precise diagnosis."
#                     )

#             st.markdown("---")

#             st.subheader("📊 Prediction Confidence (All Classes)")

#             prob_df = pd.DataFrame({
#                 "Disease":    disease_encoder.classes_,
#                 "Confidence": all_probs
#             }).sort_values("Confidence", ascending=False)

#             fig = px.bar(
#                 prob_df, x="Disease", y="Confidence",
#                 color="Confidence",
#                 text=(prob_df["Confidence"]*100).round(2).astype(str)+"%",
#                 color_continuous_scale="Reds",
#                 title="Model Confidence per Disease Class"
#             )
#             fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#             fig.update_layout(xaxis_tickangle=-35, height=430, showlegend=False)
#             fig.update_coloraxes(colorbar=colorbar_cfg())
#             st.plotly_chart(fig, use_container_width=True)

#             st.markdown("---")

#             st.subheader("📝 General Plant Health Tips")
#             t1, t2, t3 = st.columns(3)
#             t1.info("💧 **Water at the Base**\nAvoid wetting leaves — wet leaves promote fungal disease.")
#             t2.info("🌬️ **Air Circulation**\nProper spacing between plants reduces humidity and disease spread.")
#             t3.info("🔄 **Crop Rotation**\nRotate crops every season to break disease and pest cycles.")

#         except Exception as e:
#             st.error(f"❌ Disease prediction failed: `{str(e)}`")

#     else:
#         st.info(
#             "👆 Upload a leaf image above to get started.\n\n"
#             "**Supported formats:** JPG, JPEG, PNG, WEBP\n\n"
#             "**Tips for best results:**\n"
#             "• Use a clear, well-lit photo of a single leaf\n"
#             "• Avoid blurry or dark images\n"
#             "• Capture the affected area clearly\n"
#             "• Image size: any — the model resizes automatically to 128×128"
#         )

#         st.markdown("---")
#         st.subheader("🌿 Diseases This Model Can Detect")
#         st.caption(
#             "The model is trained on the classes present in your Disease_Dataset folder. "
#             "Below are the common diseases supported when using the PlantVillage dataset."
#         )

#         sample_diseases = [
#             "Tomato — Healthy",        "Tomato — Early Blight",
#             "Tomato — Late Blight",    "Tomato — Leaf Mold",
#             "Tomato — Mosaic Virus",   "Tomato — Spider Mites",
#             "Potato — Healthy",        "Potato — Early Blight",
#             "Potato — Late Blight",    "Pepper — Bacterial Spot",
#             "Corn — Common Rust",      "Corn — Northern Leaf Blight",
#             "Apple — Apple Scab",      "Apple — Black Rot",
#         ]

#         cols = st.columns(3)
#         for i, d in enumerate(sample_diseases):
#             cols[i % 3].write(f"• {d}")



# import os
# import io
# import numpy as np
# import pandas as pd
# import joblib
# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.io as pio
# from PIL import Image

# # ── Multilingual Voice Assistant: optional deps, fail gracefully ──
# try:
#     import speech_recognition as sr
#     from gtts import gTTS
#     from audio_recorder_streamlit import audio_recorder
#     VOICE_DEPS_OK = True
#     voice_import_error = None
# except Exception as _e:
#     VOICE_DEPS_OK = False
#     voice_import_error = str(_e)

# try:
#     from groq import Groq
#     GROQ_SDK_OK = True
# except Exception:
#     GROQ_SDK_OK = False

# # Load variables from a .env file (e.g. GROQ_API_KEY=...) into os.environ.
# DOTENV_PATH_FOUND = None
# try:
#     from dotenv import load_dotenv, find_dotenv
#     _dotenv_path = find_dotenv(usecwd=True)
#     if not _dotenv_path:
#         # Fallback: look right next to this script, regardless of which
#         # folder `streamlit run` was launched from.
#         _candidate = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
#         if os.path.exists(_candidate):
#             _dotenv_path = _candidate
#     if _dotenv_path:
#         DOTENV_PATH_FOUND = _dotenv_path
#     load_dotenv(_dotenv_path if _dotenv_path else None)
#     DOTENV_OK = True
# except Exception:
#     DOTENV_OK = False

# # =========================================================
# # ===== GLOBAL PLOTLY THEME ================================
# # =========================================================

# pio.templates["krishi"] = go.layout.Template(
#     layout=go.Layout(
#         paper_bgcolor="#ffffff",
#         plot_bgcolor="#f9fdf9",
#         font=dict(
#             color="#1a1a1a",
#             family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif"
#         ),
#         title=dict(font=dict(color="#0d2e0d", size=16)),
#         xaxis=dict(
#             color="#1a1a1a",
#             gridcolor="#d4ecd4",
#             linecolor="#81c784",
#             tickfont=dict(color="#1a1a1a"),
#             title=dict(font=dict(color="#1a1a1a")),
#             zerolinecolor="#c8e6c9",
#         ),
#         yaxis=dict(
#             color="#1a1a1a",
#             gridcolor="#d4ecd4",
#             linecolor="#81c784",
#             tickfont=dict(color="#1a1a1a"),
#             title=dict(font=dict(color="#1a1a1a")),
#             zerolinecolor="#c8e6c9",
#         ),
#         legend=dict(
#             bgcolor="#ffffff",
#             bordercolor="#c8e6c9",
#             font=dict(color="#1a1a1a"),
#         ),
#         coloraxis=dict(
#             colorbar=dict(
#                 tickfont=dict(color="#1a1a1a", size=12),
#                 tickcolor="#1a1a1a",
#                 title=dict(font=dict(color="#1a1a1a", size=13), side="right"),
#                 bgcolor="#ffffff",
#                 outlinecolor="#c8e6c9",
#                 outlinewidth=1,
#                 bordercolor="#c8e6c9",
#                 borderwidth=1,
#                 len=0.85,
#             )
#         ),
#         polar=dict(
#             bgcolor="#f9fdf9",
#             radialaxis=dict(color="#1a1a1a", gridcolor="#d4ecd4"),
#             angularaxis=dict(color="#1a1a1a", gridcolor="#d4ecd4"),
#         ),
#         colorway=["#2e7d32","#1f77b4","#ff7f0e","#d62728","#9467bd",
#                   "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"],
#     )
# )
# pio.templates.default = "krishi"

# # =========================================================
# # ================= PAGE CONFIG ===========================
# # =========================================================

# st.set_page_config(
#     page_title="Krishi AI — Smart Farming Assistant",
#     page_icon="🌱",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # =========================================================
# # ================= CUSTOM CSS ============================
# # =========================================================

# st.markdown("""
# <style>
#     /* ── Reset & Base ── */
#     html, body, [class*="css"] {
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }

#     /* ── Main app background: light green-white ── */
#     .stApp {
#         background-color: #f0f7f0;
#     }

#     /* ── ALL main content text: DARK (visible on light bg) ── */
#     .stApp p,
#     .stApp span,
#     .stApp div,
#     .stApp label,
#     .stApp li,
#     .stApp td,
#     .stApp th,
#     .stApp caption,
#     .stApp small,
#     .stApp strong,
#     .stApp em {
#         color: #1a1a1a !important;
#     }

#     /* ── Headings: dark green ── */
#     .stApp h1, .stApp h2, .stApp h3,
#     .stApp h4, .stApp h5, .stApp h6 {
#         color: #0d2e0d !important;
#         font-weight: 700;
#     }

#     /* ── Markdown text ── */
#     .stMarkdown, .stMarkdown p,
#     .stMarkdown span, .stMarkdown div,
#     .stMarkdown li, .stMarkdown strong,
#     .stMarkdown em {
#         color: #1a1a1a !important;
#     }

#     /* ── Sidebar: dark green gradient — WHITE text ── */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #0d2e0d 0%, #1a5c2a 50%, #2e7d32 100%);
#     }
#     [data-testid="stSidebar"],
#     [data-testid="stSidebar"] *,
#     [data-testid="stSidebar"] p,
#     [data-testid="stSidebar"] span,
#     [data-testid="stSidebar"] div,
#     [data-testid="stSidebar"] label,
#     [data-testid="stSidebar"] h1,
#     [data-testid="stSidebar"] h2,
#     [data-testid="stSidebar"] h3,
#     [data-testid="stSidebar"] strong,
#     [data-testid="stSidebar"] em,
#     [data-testid="stSidebar"] li,
#     [data-testid="stSidebar"] .stMarkdown,
#     [data-testid="stSidebar"] .stMarkdown p,
#     [data-testid="stSidebar"] .stMarkdown span,
#     [data-testid="stSidebar"] .stMarkdown div,
#     [data-testid="stSidebar"] .stCaption,
#     [data-testid="stSidebar"] .stSelectbox label {
#         color: #ffffff !important;
#     }

#     /* ── Header banner: WHITE text on dark bg ── */
#     .krishi-header {
#         background: linear-gradient(135deg, #0d2e0d, #1b5e20, #2e7d32, #388e3c);
#         padding: 2.2rem 1.5rem 1.8rem 1.5rem;
#         border-radius: 18px;
#         text-align: center;
#         margin-bottom: 1.8rem;
#         box-shadow: 0 6px 28px rgba(13,46,13,0.35);
#     }
#     .krishi-header h1 {
#         color: #ffffff !important;
#         font-size: 2.6rem;
#         margin: 0;
#         letter-spacing: 2px;
#         text-shadow: 0 2px 8px rgba(0,0,0,0.4);
#     }
#     .krishi-header p {
#         color: #c8e6c9 !important;
#         margin: 0.4rem 0 0 0;
#         font-size: 1.05rem;
#     }

#     /* ── Metric cards: WHITE bg, DARK text ── */
#     [data-testid="stMetric"] {
#         background: #ffffff !important;
#         border-radius: 12px !important;
#         padding: 0.9rem 1.1rem !important;
#         border-left: 4px solid #2e7d32 !important;
#         box-shadow: 0 3px 10px rgba(0,0,0,0.09) !important;
#     }
#     [data-testid="stMetric"] *,
#     [data-testid="stMetric"] label,
#     [data-testid="stMetric"] div,
#     [data-testid="stMetricLabel"],
#     [data-testid="stMetricLabel"] p,
#     [data-testid="stMetricLabel"] div,
#     [data-testid="stMetricValue"],
#     [data-testid="stMetricValue"] div {
#         color: #0d2e0d !important;
#     }
#     [data-testid="stMetricLabel"] p {
#         color: #2e7d32 !important;
#         font-weight: 600;
#     }
#     [data-testid="stMetricValue"] {
#         font-size: 1.6rem !important;
#         font-weight: 700 !important;
#     }

#     /* ── Dataframe: DARK text on light bg ── */
#     .stDataFrame,
#     .stDataFrame *,
#     [data-testid="stDataFrameContainer"],
#     [data-testid="stDataFrameContainer"] * {
#         color: #1a1a1a !important;
#     }
#     [data-testid="stDataFrameContainer"] {
#         border: 1px solid #c8e6c9;
#         border-radius: 10px;
#     }

#     /* ── Chat bubbles ── */
#     .chat-user {
#         background: #1b5e20;
#         border-radius: 16px 16px 4px 16px;
#         padding: 0.75rem 1.2rem;
#         margin: 0.4rem 0;
#         max-width: 80%;
#         margin-left: auto;
#         color: #ffffff !important;
#         font-weight: 500;
#         box-shadow: 0 2px 8px rgba(27,94,32,0.25);
#     }
#     .chat-user * { color: #ffffff !important; }

#     .chat-ai {
#         background: #ffffff;
#         border-radius: 16px 16px 16px 4px;
#         padding: 0.75rem 1.2rem;
#         margin: 0.4rem 0;
#         max-width: 85%;
#         border-left: 3px solid #43a047;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.08);
#         color: #1a1a1a !important;
#     }
#     .chat-ai * { color: #1a1a1a !important; }

#     .chat-label-user {
#         text-align: right;
#         font-size: 0.75rem;
#         color: #2e7d32 !important;
#         margin-bottom: 3px;
#         font-weight: 600;
#     }
#     .chat-label-ai {
#         font-size: 0.75rem;
#         color: #2e7d32 !important;
#         margin-bottom: 3px;
#         font-weight: 600;
#     }

#     /* ── Disease result card: WHITE bg, DARK text ── */
#     .disease-card {
#         background: #ffffff;
#         border-radius: 16px;
#         padding: 1.6rem;
#         box-shadow: 0 4px 18px rgba(0,0,0,0.10);
#         margin: 1rem 0;
#         border-top: 4px solid #2e7d32;
#     }
#     .disease-card,
#     .disease-card * {
#         color: #1a1a1a !important;
#     }

#     /* ── Buttons: WHITE text on dark green bg ── */
#     .stButton > button {
#         background: linear-gradient(135deg, #1b5e20, #2e7d32, #43a047) !important;
#         color: #ffffff !important;
#         border: none !important;
#         border-radius: 10px !important;
#         font-weight: 700 !important;
#         font-size: 0.95rem !important;
#         padding: 0.55rem 1.2rem !important;
#         transition: all 0.2s ease !important;
#         letter-spacing: 0.3px;
#     }
#     .stButton > button:hover {
#         transform: translateY(-2px) !important;
#         box-shadow: 0 6px 16px rgba(46,125,50,0.4) !important;
#         background: linear-gradient(135deg, #155218, #256427, #36883a) !important;
#     }
#     .stButton > button *,
#     .stButton > button span,
#     .stButton > button p {
#         color: #ffffff !important;
#     }

#     /* ── Alert boxes: DARK text on coloured bg ── */
#     div[data-testid="stNotification"] {
#         border-radius: 12px !important;
#     }
#     /* SUCCESS box */
#     [data-testid="stNotification"][kind="success"],
#     div.stSuccess,
#     div.stSuccess > div {
#         background-color: #d4edda !important;
#         border-color: #28a745 !important;
#         border-radius: 12px !important;
#     }
#     div.stSuccess p,
#     div.stSuccess div,
#     div.stSuccess span,
#     div.stSuccess li,
#     div.stSuccess strong,
#     div.stSuccess em {
#         color: #155724 !important;
#     }
#     /* INFO box */
#     div.stInfo,
#     div.stInfo > div {
#         background-color: #d1ecf1 !important;
#         border-color: #17a2b8 !important;
#         border-radius: 12px !important;
#     }
#     div.stInfo p,
#     div.stInfo div,
#     div.stInfo span,
#     div.stInfo li,
#     div.stInfo strong,
#     div.stInfo em {
#         color: #0c5460 !important;
#     }
#     /* WARNING box */
#     div.stWarning,
#     div.stWarning > div {
#         background-color: #fff3cd !important;
#         border-color: #ffc107 !important;
#         border-radius: 12px !important;
#     }
#     div.stWarning p,
#     div.stWarning div,
#     div.stWarning span,
#     div.stWarning li,
#     div.stWarning strong,
#     div.stWarning em {
#         color: #856404 !important;
#     }
#     /* ERROR box */
#     div.stError,
#     div.stError > div {
#         background-color: #f8d7da !important;
#         border-color: #dc3545 !important;
#         border-radius: 12px !important;
#     }
#     div.stError p,
#     div.stError div,
#     div.stError span,
#     div.stError li,
#     div.stError strong,
#     div.stError em {
#         color: #721c24 !important;
#     }

#     /* ── Selectbox & input labels: DARK text ── */
#     .stSelectbox label,
#     .stSlider label,
#     .stTextInput label,
#     .stFileUploader label,
#     .stMultiSelect label {
#         color: #1a1a1a !important;
#         font-weight: 600 !important;
#     }

#     /* ── Text input box ── */
#     .stTextInput input {
#         background: #ffffff !important;
#         color: #1a1a1a !important;
#         border: 1.5px solid #81c784 !important;
#         border-radius: 8px !important;
#     }
#     .stTextInput input::placeholder {
#         color: #5a8c5a !important;
#     }
#     .stTextInput input:focus {
#         border-color: #2e7d32 !important;
#         box-shadow: 0 0 0 2px rgba(46,125,50,0.2) !important;
#     }

#     /* ── Slider: DARK labels ── */
#     .stSlider [data-testid="stTickBar"] div,
#     [data-testid="stSlider"] div[data-testid="stThumbValue"],
#     [data-testid="stSlider"] * {
#         color: #1a1a1a !important;
#     }

#     /* ── Plotly chart container background ── */
#     .js-plotly-plot, .plotly, .plot-container {
#         background: #ffffff !important;
#         border-radius: 12px;
#     }

#     /* ── Plotly SVG text: DARK on white chart bg ── */
#     .js-plotly-plot .plotly .xtick text,
#     .js-plotly-plot .plotly .ytick text,
#     .js-plotly-plot .plotly .xtitle,
#     .js-plotly-plot .plotly .ytitle,
#     .js-plotly-plot .plotly .g-xtitle text,
#     .js-plotly-plot .plotly .g-ytitle text,
#     .js-plotly-plot .plotly .gtitle,
#     .js-plotly-plot .plotly .cbaxis text,
#     .js-plotly-plot .plotly .cbtitle text,
#     .js-plotly-plot .plotly .legend text {
#         fill: #1a1a1a !important;
#     }

#     /* ── Plotly bar text labels ON bars: WHITE ── */
#     .js-plotly-plot .plotly .bartext text,
#     .js-plotly-plot .plotly g.points text,
#     .js-plotly-plot .plotly .textpoint text,
#     .js-plotly-plot .plotly .trace text {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly colorbar background ── */
#     .js-plotly-plot .plotly .cbfill,
#     .js-plotly-plot .plotly rect.cbbg {
#         fill: #ffffff !important;
#     }

#     /* ── Plotly modebar ── */
#     .modebar-container {
#         background: rgba(0,0,0,0.6) !important;
#         border-radius: 6px !important;
#     }
#     .modebar-btn path { fill: #ffffff !important; }
#     .modebar-btn:hover path { fill: #cccccc !important; }

#     /* ── Dataframe toolbar ── */
#     [data-testid="stElementToolbar"] {
#         background: #2e7d32 !important;
#         border-radius: 8px !important;
#         padding: 2px 4px !important;
#     }
#     [data-testid="stElementToolbar"] button svg path,
#     [data-testid="stElementToolbar"] button svg rect,
#     [data-testid="stElementToolbar"] button svg circle {
#         fill: #ffffff !important;
#         stroke: #ffffff !important;
#     }
#     [data-testid="stElementToolbar"] button:hover {
#         background: #1b5e20 !important;
#         border-radius: 4px !important;
#     }

#     /* ── Divider ── */
#     hr {
#         border-color: #a5d6a7;
#         margin: 1.8rem 0;
#     }

#     /* ── Caption text ── */
#     .stCaption,
#     [data-testid="stCaptionContainer"],
#     [data-testid="stCaptionContainer"] p {
#         color: #4a7c4a !important;
#     }

#     /* ── Selectbox dropdown: DARK text ── */ 
            
#     [data-testid="stSelectbox"] div[data-baseweb="select"] {
#         background: #0b1220 !important;  /* dark background */
#     }

#     [data-testid="stSelectbox"] div[data-baseweb="select"] *,
#     [data-testid="stSelectbox"] span {
#         color: #ffffff !important;       /* white text */
#     }
                
    

#     /* ── File uploader ── */
#     [data-testid="stFileUploader"] {
#         background: #ffffff !important;
#         border: 2px dashed #81c784 !important;
#         border-radius: 10px !important;
#     }
#     [data-testid="stFileUploader"] *,
#     [data-testid="stFileUploader"] p,
#     [data-testid="stFileUploader"] span,
#     [data-testid="stFileUploader"] div {
#         color: #1a1a1a !important;
#     }

#     /* ── Progress bar ── */
#     [data-testid="stProgressBar"] > div {
#         background-color: #2e7d32 !important;
#     }

#     /* ── Tabs ── */
#     [data-testid="stTabs"] [data-baseweb="tab"] {
#         color: #1a1a1a !important;
#     }
#     [data-testid="stTabs"] [aria-selected="true"] {
#         color: #2e7d32 !important;
#         border-bottom-color: #2e7d32 !important;
#     }

#     /* ── Column containers ── */
#     [data-testid="column"] { padding: 0 0.4rem; }

#     /* ── Scrollbar ── */
#     ::-webkit-scrollbar { width: 7px; height: 7px; }
#     ::-webkit-scrollbar-track { background: #e8f5e9; }
#     ::-webkit-scrollbar-thumb { background: #81c784; border-radius: 4px; }
#     ::-webkit-scrollbar-thumb:hover { background: #2e7d32; }

#     /* ── Sticky chat title/language header: stays put at the top of the
#        Voice Assistant card, like the navigation bar in a normal chat app —
#        never gets pushed away as the conversation grows ── */
#     .krishi-chat-header {
#         position: sticky;
#         top: 0;
#         z-index: 30;
#         background: #f0f7f0;
#         padding-top: 0.3rem;
#         padding-bottom: 0.4rem;
#     }

#     /* ── Chat history scrolls inside its own box instead of the whole
#        page, so the header above and the input bar below never move ── */
#     .krishi-chat-scroll {
#         max-height: 48vh;
#         overflow-y: auto;
#         padding: 0.2rem 0.5rem 0.2rem 0.1rem;
#         margin-bottom: 0.6rem;
#     }
#     .krishi-chat-scroll::-webkit-scrollbar { width: 6px; }
#     .krishi-chat-scroll::-webkit-scrollbar-thumb {
#         background: #81c784;
#         border-radius: 4px;
#     }

#     /* ── ChatGPT-style unified input bar (text + mic + send) ── */
#     .krishi-input-bar {
#         background: #ffffff;
#         border: 1.5px solid #c8e6c9;
#         border-radius: 28px;
#         padding: 0.35rem 0.5rem 0.35rem 1.1rem;
#         box-shadow: 0 3px 14px rgba(0,0,0,0.08);
#         display: flex;
#         align-items: center;
#         /* keep the input bar visible without scrolling, like a normal
#            chat app's message box at the bottom of the screen */
#         position: sticky;
#         bottom: 0.6rem;
#         z-index: 30;
#     }
#     .krishi-input-bar:focus-within {
#         border-color: #2e7d32;
#         box-shadow: 0 0 0 2px rgba(46,125,50,0.15);
#     }
#     /* Remove the default boxed look from the text input so it blends
#        into the unified pill-shaped bar */
#     .krishi-input-row [data-testid="stTextInput"] > div {
#         background: transparent !important;
#         border: none !important;
#     }
#     .krishi-input-row .stTextInput input {
#         border: none !important;
#         background: transparent !important;
#         box-shadow: none !important;
#         padding-left: 0.2rem !important;
#         font-size: 1rem !important;
#     }
#     .krishi-input-row .stTextInput input:focus {
#         box-shadow: none !important;
#     }
#     /* Mic recorder + send button: circular, sit flush inside the bar */
#     .krishi-input-row [data-testid="column"] {
#         padding: 0 0.15rem !important;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }
#     .krishi-input-row .stButton > button {
#         border-radius: 50% !important;
#         width: 2.6rem !important;
#         height: 2.6rem !important;
#         padding: 0 !important;
#         font-size: 1.2rem !important;
#         line-height: 1 !important;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }
# </style>
# """, unsafe_allow_html=True)

# # =========================================================
# # ================= MULTILINGUAL VOICE ASSISTANT ==========
# # =========================================================
# # Setup:
# #   pip install SpeechRecognition gTTS audio-recorder-streamlit groq python-dotenv
# #   Put your key in a .env file (same folder as app.py):
# #       GROQ_API_KEY=gsk_....
# #   — or in .streamlit/secrets.toml:
# #       GROQ_API_KEY = "gsk_...."
# #   (Get a free key at https://console.groq.com/keys)
# # (Swap the LLM call in get_ai_response() for another provider
# #  if you prefer — only that one function needs to change.)

# LANGUAGES = {
#     "English":            {"speech": "en-IN", "tts": "en"},
#     "हिंदी (Hindi)":       {"speech": "hi-IN", "tts": "hi"},
#     "मराठी (Marathi)":     {"speech": "mr-IN", "tts": "mr"},
#     "বাংলা (Bengali)":     {"speech": "bn-IN", "tts": "bn"},
#     "தமிழ் (Tamil)":       {"speech": "ta-IN", "tts": "ta"},
#     "తెలుగు (Telugu)":     {"speech": "te-IN", "tts": "te"},
#     "ਪੰਜਾਬੀ (Punjabi)":    {"speech": "pa-IN", "tts": "pa"},
#     "ગુજરાતી (Gujarati)":  {"speech": "gu-IN", "tts": "gu"},
#     "ಕನ್ನಡ (Kannada)":     {"speech": "kn-IN", "tts": "kn"},
#     "മലയാളം (Malayalam)":  {"speech": "ml-IN", "tts": "ml"},
# }


# @st.cache_resource(show_spinner=False)
# def get_groq_client():
#     if not GROQ_SDK_OK:
#         return None
#     # Check the environment variable first (works even with no secrets.toml).
#     api_key = os.environ.get("GROQ_API_KEY")
#     # st.secrets raises an error (not just empty) if no secrets.toml exists
#     # anywhere — so this lookup must be wrapped in try/except.
#     if not api_key:
#         try:
#             api_key = st.secrets.get("GROQ_API_KEY")
#         except Exception:
#             api_key = None
#     if not api_key:
#         return None
#     try:
#         return Groq(api_key=api_key)
#     except Exception as e:
#         # e.g. "got an unexpected keyword argument 'proxies'" — a version
#         # mismatch between the groq package and httpx. Don't crash the
#         # whole app; report it in the diagnostics panel instead.
#         global GROQ_INIT_ERROR
#         GROQ_INIT_ERROR = str(e)
#         return None


# GROQ_INIT_ERROR = None


# groq_client = get_groq_client()


# def speech_to_text(audio_bytes, lang_code):
#     """Convert recorded microphone audio (WAV bytes) into text, in the
#     farmer's chosen Indian language, using free Google speech recognition."""
#     recognizer = sr.Recognizer()
#     try:
#         with io.BytesIO(audio_bytes) as wav_io:
#             with sr.AudioFile(wav_io) as source:
#                 audio_data = recognizer.record(source)
#         text = recognizer.recognize_google(audio_data, language=lang_code)
#         return text, None
#     except sr.UnknownValueError:
#         return None, "🙇 Sorry, I couldn't understand the audio clearly. Please try again, speaking slowly and close to the mic."
#     except sr.RequestError as e:
#         return None, f"⚠️ Speech recognition service error: {e}"
#     except Exception as e:
#         return None, f"⚠️ Could not process the audio: {e}"


# def text_to_speech(text, tts_lang_code):
#     """Synthesize speech audio (MP3 bytes) from text in real time using
#     gTTS — generated fresh every call, never pre-recorded."""
#     try:
#         clean_text = text.replace("**", "").replace("*", "")
#         tts = gTTS(text=clean_text, lang=tts_lang_code)
#         buf = io.BytesIO()
#         tts.write_to_fp(buf)
#         buf.seek(0)
#         return buf.read()
#     except Exception:
#         return None


# def rule_based_fallback(user_text):
#     """Tiny keyword fallback (English) so the assistant still responds
#     even if no LLM API key has been configured yet."""
#     q = user_text.lower()
#     if any(k in q for k in ["fertilizer", "npk", "urea", "nitrogen"]):
#         return "Get a soil test, then choose N-P-K fertilizer based on the deficiency it shows."
#     if any(k in q for k in ["disease", "pest", "blight", "fungus"]):
#         return "Try the Disease Detection tab — upload a leaf photo for a diagnosis and treatment advice."
#     if any(k in q for k in ["water", "irrigation", "rain"]):
#         return "Drip irrigation and morning/evening watering save water and reduce disease risk."
#     if any(k in q for k in ["crop", "grow", "plant"]):
#         return "Use the ML Prediction tab — enter your soil and weather values for an AI crop recommendation."
#     return "Please ask about crops, soil, fertilizer, irrigation, or plant disease for tailored advice."


# def get_ai_response(user_text, lang_name):
#     """Ask an LLM to respond like a knowledgeable Indian agricultural
#     extension officer, replying ONLY in the farmer's chosen language."""

#     system_prompt = (
#         "You are Krishi AI, a friendly, knowledgeable agricultural assistant "
#         "for Indian farmers. Give clear, practical, locally-relevant advice on "
#         "crops, soil, fertilizers, irrigation, weather, government schemes, "
#         "market prices, and plant diseases. "
#         f"Always reply ONLY in {lang_name}, using simple everyday language a "
#         "farmer can easily understand. Keep answers concise (under 120 words) "
#         "unless asked for more detail. Use a warm, respectful tone."
#     )

#     if groq_client is None:
#         if not GROQ_SDK_OK:
#             reason = "the `groq` Python package isn't installed — run `pip install groq`"
#         elif GROQ_INIT_ERROR:
#             reason = (
#                 f"the Groq client failed to start (`{GROQ_INIT_ERROR}`) — likely an "
#                 "`httpx` version mismatch. Try `pip install \"httpx==0.27.2\"`, then restart"
#             )
#         else:
#             reason = (
#                 "no `GROQ_API_KEY` could be found — check your `.env` file, "
#                 "environment variable, or `.streamlit/secrets.toml`, then "
#                 "**fully restart** `streamlit run app.py`"
#             )
#         return (
#             f"⚠️ *AI assistant not fully configured* — {reason}. "
#             "See the **🔧 AI Chat Diagnostics** panel in the sidebar for exact "
#             "status. Showing a basic English fallback for now:\n\n"
#             + rule_based_fallback(user_text)
#         )

#     try:
#         completion = groq_client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_text},
#             ],
#             temperature=0.4,
#             max_tokens=400,
#         )
#         return completion.choices[0].message.content.strip()
#     except Exception as e:
#         return f"⚠️ AI service error: {e}"


# # =========================================================
# # ================= HEADER ================================
# # =========================================================

# st.markdown("""
# <div class="krishi-header">
#     <h1>🌱 Krishi AI</h1>
#     <p>AI-Powered Smart Farming Assistant — Crop Recommendation · Disease Detection · Analytics</p>
# </div>
# """, unsafe_allow_html=True)

# # =========================================================
# # ================= LOAD DATASET ==========================
# # =========================================================

# DATASET_PATH = "Krishi_ai_dataset/cleaned_crop_dataset.csv"

# @st.cache_data(show_spinner=False)
# def load_dataset(path):
#     if not os.path.exists(path):
#         return None
#     return pd.read_csv(path)

# df = load_dataset(DATASET_PATH)

# if df is None:
#     st.error(
#         f"❌ Dataset not found at `{DATASET_PATH}`. "
#         "Please add the CSV file and restart."
#     )
#     st.stop()

# # =========================================================
# # ================= FEATURE CATEGORIES ====================
# # =========================================================

# def nitrogen_category(n):
#     if n <= 50:         return "Low"
#     elif n <= 120:      return "Medium"
#     else:               return "High"

# def phosphorus_category(p):
#     if p <= 40:         return "Low"
#     elif p <= 80:       return "Medium"
#     else:               return "High"

# def potassium_category(k):
#     if k <= 40:         return "Low"
#     elif k <= 80:       return "Medium"
#     else:               return "High"

# def temperature_category(temp):
#     if temp <= 20:      return "Cool"
#     elif temp <= 30:    return "Moderate"
#     else:               return "Hot"

# def humidity_category(hum):
#     if hum <= 40:       return "Low"
#     elif hum <= 70:     return "Medium"
#     else:               return "High"

# def ph_category(ph):
#     if ph < 6:          return "Acidic"
#     elif ph <= 7.5:     return "Neutral"
#     else:               return "Alkaline"

# def rainfall_category(rain):
#     if rain <= 100:     return "Low"
#     elif rain <= 200:   return "Medium"
#     else:               return "High"

# # =========================================================
# # ================= ADD CATEGORY COLUMNS ==================
# # =========================================================

# @st.cache_data(show_spinner=False)
# def enrich_dataframe(dataframe):
#     df2 = dataframe.copy()
#     df2["Nitrogen_Category"]    = df2["N"].apply(nitrogen_category)
#     df2["Phosphorus_Category"]  = df2["P"].apply(phosphorus_category)
#     df2["Potassium_Category"]   = df2["K"].apply(potassium_category)
#     df2["Temperature_Category"] = df2["temperature"].apply(temperature_category)
#     df2["Humidity_Category"]    = df2["humidity"].apply(humidity_category)
#     df2["PH_Category"]          = df2["ph"].apply(ph_category)
#     df2["Rainfall_Category"]    = df2["rainfall"].apply(rainfall_category)
#     return df2

# df = enrich_dataframe(df)

# # =========================================================
# # ================= LOAD ML FILES =========================
# # =========================================================

# @st.cache_resource(show_spinner=False)
# def load_ml_files():
#     try:
#         ml_model      = joblib.load("crop_model.pkl")
#         ml_scaler     = joblib.load("scaler.pkl")
#         ml_encoder    = joblib.load("label_encoder.pkl")
#         return ml_model, ml_scaler, ml_encoder, None
#     except FileNotFoundError as e:
#         return None, None, None, str(e)
#     except Exception as e:
#         return None, None, None, str(e)

# crop_model, crop_scaler, crop_encoder, ml_error = load_ml_files()

# # =========================================================
# # ================= LOAD DISEASE MODEL ====================
# # =========================================================

# @st.cache_resource(show_spinner=False)
# def load_disease_model():
#     try:
#         from tensorflow.keras.models import load_model
#         d_model   = load_model("plant_disease_model.h5")
#         d_encoder = joblib.load("disease_label_encoder.pkl")
#         return d_model, d_encoder, None
#     except FileNotFoundError as e:
#         return None, None, str(e)
#     except Exception as e:
#         return None, None, str(e)

# disease_model, disease_encoder, disease_error = load_disease_model()

# # =========================================================
# # ================= SIDEBAR ===============================
# # =========================================================

# with st.sidebar:
#     st.markdown("### 🌾 Navigation")
#     page = st.selectbox(
#         "Go To",
#         ["🏠 Home", "📊 Analytics", "🤖 ML Prediction", "🌿 Disease Detection"],
#         label_visibility="collapsed"
#     )

#     st.markdown("---")
#     st.markdown("### 📌 Quick Info")

#     total_crops  = df["label"].nunique()
#     total_rows   = df.shape[0]
#     ml_status    = "✅ Loaded" if crop_model  else "❌ Not Found"
#     dis_status   = "✅ Loaded" if disease_model else "❌ Not Found"

#     if not GROQ_SDK_OK:
#         ai_status = "❌ Package Missing"
#     elif groq_client is None:
#         ai_status = f"❌ Init Error: {GROQ_INIT_ERROR}" if GROQ_INIT_ERROR else "❌ No API Key Found"
#     else:
#         ai_status = "✅ Ready"

#     st.markdown(f"**Dataset Crops :** {total_crops}")
#     st.markdown(f"**Dataset Rows  :** {total_rows:,}")
#     st.markdown(f"**Crop Model    :** {ml_status}")
#     st.markdown(f"**Disease Model :** {dis_status}")
#     st.markdown(f"**AI Chat (Groq):** {ai_status}")

#     with st.expander("🔧 AI Chat Diagnostics"):
#         st.write("Groq package installed:", "✅ Yes" if GROQ_SDK_OK else "❌ No — run `pip install groq`")
#         st.write("python-dotenv installed:", "✅ Yes" if DOTENV_OK else "❌ No — run `pip install python-dotenv`")
#         st.write(".env file found at:", DOTENV_PATH_FOUND if DOTENV_PATH_FOUND else "❌ Not found")
#         if not DOTENV_PATH_FOUND:
#             try:
#                 _script_dir = os.path.dirname(os.path.abspath(__file__))
#                 _suspects = [
#                     f for f in os.listdir(_script_dir)
#                     if "env" in f.lower() and not f.lower().startswith("venv")
#                 ]
#                 st.write("Files with 'env' in the app folder:", _suspects if _suspects else "(none found)")
#                 st.caption(
#                     "If you see `.env.txt` above instead of `.env`, that's a common "
#                     "Windows Notepad issue — rename it so it has **no .txt at the end**."
#                 )
#             except Exception:
#                 pass
#         env_key_found = bool(os.environ.get("GROQ_API_KEY"))
#         try:
#             secrets_key_found = bool(st.secrets.get("GROQ_API_KEY"))
#         except Exception:
#             secrets_key_found = False
#         st.write("Key found (.env or environment variable):", "✅ Yes" if env_key_found else "❌ No")
#         st.write("Key found in .streamlit/secrets.toml:", "✅ Yes" if secrets_key_found else "❌ No")
#         if GROQ_INIT_ERROR:
#             st.error(
#                 f"Groq client failed to initialize: `{GROQ_INIT_ERROR}`\n\n"
#                 "This usually means `httpx` is too new for your `groq` package "
#                 "version (httpx ≥0.28 removed the `proxies` argument). Fix with:\n\n"
#                 "`pip install \"httpx==0.27.2\"`\n\nthen fully restart the app."
#             )
#         st.caption(
#             "If you just added/changed the key, you must **fully stop and restart** "
#             "`streamlit run app.py` — the key is only read once per server "
#             "start (cached), so a page refresh alone won't pick it up."
#         )

#     st.markdown("---")
#     st.caption("Krishi AI v2.0 — Built with ❤️ for Farmers")

# # =========================================================
# # Shared constants
# # =========================================================

# NUMERIC_FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
# FEATURE_LABELS   = ["Nitrogen", "Phosphorus", "Potassium",
#                     "Temperature", "Humidity", "pH", "Rainfall"]
# CROPS_LIST       = sorted(df["label"].unique())

# @st.cache_data(show_spinner=False)
# def get_crop_stats(dataframe):
#     means = dataframe.groupby("label")[NUMERIC_FEATURES].mean()
#     norm  = (means - means.min()) / (means.max() - means.min())
#     return means, norm

# CROP_MEANS, CROP_NORM = get_crop_stats(df)

# # =========================================================
# # Helper: colorbar config (dark tick text on white bg)
# # =========================================================

# def colorbar_cfg():
#     return dict(
#         bgcolor="#ffffff",
#         tickfont=dict(color="#1a1a1a", size=12),
#         tickcolor="#1a1a1a",
#         title=dict(font=dict(color="#1a1a1a", size=13)),
#         outlinecolor="#c8e6c9",
#         outlinewidth=1,
#     )

# # =========================================================
# # PAGE: HOME
# # =========================================================

# if page == "🏠 Home":

#     col_left, col_mid, col_right = st.columns([1, 2, 1])

#     with col_mid:

#         # ── Sticky header: title + language/clear-chat row never scroll away ──
#         st.markdown('<div class="krishi-chat-header">', unsafe_allow_html=True)

#         st.markdown("## 💬 Krishi AI Voice Assistant")
#         st.caption(
#             "Speak or type your farming question in your own language. "
#             "Krishi AI answers instantly — in text **and** voice."
#         )

#         if "chat_history" not in st.session_state:
#             st.session_state.chat_history = []
#         if "selected_lang" not in st.session_state:
#             st.session_state.selected_lang = "हिंदी (Hindi)"

#         lang_col, clear_col = st.columns([3, 1])
#         with lang_col:
#             st.session_state.selected_lang = st.selectbox(
#                 "🌐 Choose your language",
#                 list(LANGUAGES.keys()),
#                 index=list(LANGUAGES.keys()).index(st.session_state.selected_lang),
#             )
#         with clear_col:
#             st.write("")
#             if st.button("🗑️ Clear Chat", use_container_width=True):
#                 st.session_state.chat_history = []
#                 st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)
#         # ── end sticky header ──

#         lang_codes = LANGUAGES[st.session_state.selected_lang]

#         if not VOICE_DEPS_OK:
#             st.warning(
#                 "🎤 Voice features need a few extra packages.\n\n"
#                 "Run: `pip install SpeechRecognition gTTS audio-recorder-streamlit`\n\n"
#                 f"(Details: `{voice_import_error}`)"
#             )

#         # ── render chat history inside its own scroll box, so new messages
#         #    never push the header above or the input bar below out of view ──
#         st.markdown('<div class="krishi-chat-scroll">', unsafe_allow_html=True)
#         for i, entry in enumerate(st.session_state.chat_history):
#             if entry["role"] == "user":
#                 st.markdown(
#                     f"<div class='chat-label-user'>You</div>"
#                     f"<div class='chat-user'>{entry['text']}</div>",
#                     unsafe_allow_html=True
#                 )
#             else:
#                 st.markdown(
#                     f"<div class='chat-label-ai'>🌱 Krishi AI</div>"
#                     f"<div class='chat-ai'>{entry['text']}</div>",
#                     unsafe_allow_html=True
#                 )
#                 if VOICE_DEPS_OK and st.button("🔊 Listen", key=f"listen_{i}"):
#                     audio_bytes = text_to_speech(entry["text"], lang_codes["tts"])
#                     if audio_bytes:
#                         st.audio(audio_bytes, format="audio/mp3", autoplay=True)
#                     else:
#                         st.warning("Could not generate voice for this reply.")
#         if not st.session_state.chat_history:
#             st.caption("Your conversation will appear here once you ask something.")
#         st.markdown('</div>', unsafe_allow_html=True)
#         # ── end chat scroll box ──

#         # ── Unified ChatGPT-style input bar: text box + mic + send, all in one row ──
#         st.markdown('<div class="krishi-input-bar krishi-input-row">', unsafe_allow_html=True)

#         if VOICE_DEPS_OK:
#             in_col, mic_col, send_col = st.columns([7, 1, 1.3])
#         else:
#             in_col, send_col = st.columns([8, 1.3])
#             mic_col = None

#         with in_col:
#             user_input = st.text_input(
#                 "Your question",
#                 placeholder="e.g.  लाल मिट्टी और कम बारिश में कौन सी फसल अच्छी होती है?",
#                 label_visibility="collapsed",
#                 key="home_input"
#             )

#         audio_bytes_in = None
#         if mic_col is not None:
#             with mic_col:
#                 audio_bytes_in = audio_recorder(
#                     text="",
#                     icon_size="1.4x",
#                     pause_threshold=2.0,
#                     recording_color="#dc3545",
#                     neutral_color="#2e7d32",
#                     key="mic_recorder",
#                 )

#         with send_col:
#             send_clicked = st.button("➤", use_container_width=True, key="send_btn")

#         st.markdown('</div>', unsafe_allow_html=True)

#         if VOICE_DEPS_OK:
#             st.caption(
#                 f"🎤 Tap the mic and speak, or type, in **{st.session_state.selected_lang}**. "
#                 "Recording stops automatically after a short pause."
#             )
#         else:
#             st.caption(f"⌨️ Type your question in **{st.session_state.selected_lang}**.")

#         # ── handle voice input ──
#         if audio_bytes_in:
#             with st.spinner("🎧 Listening & transcribing..."):
#                 transcribed, err = speech_to_text(audio_bytes_in, lang_codes["speech"])
#             if err:
#                 st.warning(err)
#             elif transcribed:
#                 st.session_state.chat_history.append({"role": "user", "text": transcribed})
#                 with st.spinner("🤖 Thinking..."):
#                     reply = get_ai_response(transcribed, st.session_state.selected_lang)
#                 st.session_state.chat_history.append({"role": "ai", "text": reply})
#                 audio_out = text_to_speech(reply, lang_codes["tts"])
#                 if audio_out:
#                     st.audio(audio_out, format="audio/mp3", autoplay=True)
#                 st.rerun()

#         # ── handle typed input (send button) ──
#         if send_clicked:
#             if not user_input.strip():
#                 st.warning("⚠️ Please type or speak a farming question first.")
#             else:
#                 st.session_state.chat_history.append({"role": "user", "text": user_input})
#                 with st.spinner("🤖 Thinking..."):
#                     reply = get_ai_response(user_input, st.session_state.selected_lang)
#                 st.session_state.chat_history.append({"role": "ai", "text": reply})
#                 if VOICE_DEPS_OK:
#                     audio_out = text_to_speech(reply, lang_codes["tts"])
#                     if audio_out:
#                         st.audio(audio_out, format="audio/mp3", autoplay=True)
#                 st.rerun()

#     st.markdown("---")

#     st.markdown("### 🚀 What Krishi AI Can Do For You")
#     c1, c2, c3 = st.columns(3)

#     with c1:
#         st.info(
#             "### 📊 Smart Analytics\n"
#             "Explore 24+ charts and insights about crops, soil nutrients, "
#             "rainfall, temperature, and more."
#         )
#     with c2:
#         st.success(
#             "### 🤖 Crop Prediction\n"
#             "Enter your soil and weather data to get an ML-powered crop "
#             "recommendation with confidence scores."
#         )
#     with c3:
#         st.warning(
#             "### 🌿 Disease Detection\n"
#             "Upload a leaf image and our CNN model will identify plant "
#             "diseases and suggest treatment in seconds."
#         )

# # =========================================================
# # PAGE: ANALYTICS
# # =========================================================

# elif page == "📊 Analytics":

#     st.header("📊 Krishi Data Analytics Dashboard")

#     st.subheader("📁 Dataset Overview")
#     c1, c2, c3, c4, c5 = st.columns(5)
#     c1.metric("Total Rows",      f"{df.shape[0]:,}")
#     c2.metric("Total Columns",   df.shape[1])
#     c3.metric("Unique Crops",    df["label"].nunique())
#     c4.metric("Duplicate Rows",  int(df.duplicated().sum()))
#     c5.metric("Missing Values",  int(df.isnull().sum().sum()))
#     st.markdown("---")

#     st.subheader("🔬 Data Quality Check")
#     q1, q2 = st.columns(2)
#     with q1:
#         st.write("#### Data Types")
#         dtype_df = df.dtypes.reset_index()
#         dtype_df.columns = ["Feature", "Type"]
#         dtype_df["Type"] = dtype_df["Type"].astype(str)
#         st.dataframe(dtype_df, use_container_width=True)
#     with q2:
#         st.write("#### Missing Values")
#         mv = df.isnull().sum().reset_index()
#         mv.columns = ["Feature", "Missing"]
#         st.dataframe(mv, use_container_width=True)
#         if mv["Missing"].sum() == 0:
#             st.success("✅ No missing values!")
#         if df.duplicated().sum() == 0:
#             st.success("✅ No duplicate rows!")
#     st.markdown("---")

#     st.subheader("🔍 Dataset Preview")
#     st.dataframe(df.head(50), use_container_width=True)
#     st.markdown("---")

#     st.subheader("📈 Statistical Summary")
#     st.dataframe(df.describe().round(2), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🌾 Crop Distribution")
#     crop_count = df["label"].value_counts().reset_index()
#     crop_count.columns = ["Crop", "Count"]

#     d1, d2 = st.columns(2)
#     with d1:
#         fig = px.bar(crop_count, x="Crop", y="Count",
#                      color="Count", color_continuous_scale="Greens",
#                      text="Count", title="Crop Count")
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(xaxis_tickangle=-45, showlegend=False, height=380)
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         st.plotly_chart(fig, use_container_width=True)
#     with d2:
#         fig2 = px.pie(crop_count, names="Crop", values="Count",
#                       title="Crop Share",
#                       color_discrete_sequence=px.colors.sequential.Greens_r)
#         fig2.update_traces(textposition="inside", textinfo="percent+label")
#         st.plotly_chart(fig2, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📊 Feature Category Analysis")
#     cat_cols = [
#         ("Nitrogen_Category", "Nitrogen"),
#         ("Phosphorus_Category", "Phosphorus"),
#         ("Potassium_Category", "Potassium"),
#         ("Temperature_Category", "Temperature"),
#         ("Humidity_Category", "Humidity"),
#         ("PH_Category", "Soil pH"),
#         ("Rainfall_Category", "Rainfall"),
#     ]
#     ca1, ca2 = st.columns(2)
#     for i, (col_name, title) in enumerate(cat_cols):
#         counts = df[col_name].value_counts().reset_index()
#         counts.columns = ["Category", "Count"]
#         fig = px.pie(counts, names="Category", values="Count",
#                      title=f"{title} Distribution", hole=0.4,
#                      color_discrete_sequence=px.colors.qualitative.Set2)
#         fig.update_traces(textinfo="percent+label")
#         (ca1 if i % 2 == 0 else ca2).plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     def climate_bar(feature, label, color_scale, unit=""):
#         grp = df.groupby("label")[feature].mean().round(2).reset_index()
#         grp.columns = ["Crop", label]
#         grp = grp.sort_values(label, ascending=True)
#         fig = px.bar(grp, x=label, y="Crop", orientation="h",
#                      title=f"Average {label} per Crop",
#                      color=label, color_continuous_scale=color_scale,
#                      text=label)
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(height=580, yaxis_title="")
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         return fig, grp

#     for feat, lbl, scale in [
#         ("temperature", "Avg Temperature (°C)", "RdYlGn_r"),
#         ("rainfall",    "Avg Rainfall (mm)",    "Blues"),
#         ("humidity",    "Avg Humidity (%)",      "Teal"),
#         ("ph",          "Avg pH",               "RdYlGn"),
#     ]:
#         icon = '🌡' if 'Temp' in lbl else '🌧' if 'Rain' in lbl else '💧' if 'Hum' in lbl else '🧪'
#         st.subheader(f"{icon} {lbl}")
#         fig, grp = climate_bar(feat, lbl, scale)
#         st.plotly_chart(fig, use_container_width=True)
#         t1, t2 = st.columns(2)
#         with t1:
#             st.write("**Top 5 (Highest)**")
#             st.dataframe(grp.tail(5)[::-1].reset_index(drop=True), use_container_width=True)
#         with t2:
#             st.write("**Bottom 5 (Lowest)**")
#             st.dataframe(grp.head(5).reset_index(drop=True), use_container_width=True)
#         st.markdown("---")

#     st.subheader("🪴 NPK Analysis")
#     avg_npk = df.groupby("label")[["N","P","K"]].mean().round(2).reset_index()
#     npk_m   = avg_npk.melt(id_vars="label", value_vars=["N","P","K"],
#                             var_name="Nutrient", value_name="Value")
#     cmap = {"N": "#2ca02c", "P": "#ff7f0e", "K": "#1f77b4"}

#     for mode, title in [("group","Grouped"), ("stack","Stacked — shows proportion")]:
#         fig = px.bar(npk_m, x="label", y="Value", color="Nutrient",
#                      barmode=mode, title=f"N, P, K per Crop ({title})",
#                      color_discrete_map=cmap,
#                      labels={"label":"Crop","Value":"mg/kg"})
#         fig.update_layout(xaxis_tickangle=-45, height=420)
#         st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(avg_npk.set_index("label"), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🧪 Soil Health Analysis")
#     c1,c2,c3 = st.columns(3)
#     c1.metric("Avg Nitrogen",   round(df["N"].mean(),2))
#     c2.metric("Avg Phosphorus", round(df["P"].mean(),2))
#     c3.metric("Avg Potassium",  round(df["K"].mean(),2))

#     soil = df.groupby("label")[["N","P","K"]].mean()
#     soil["Score"] = soil.mean(axis=1).round(2)
#     soil = soil.reset_index().sort_values("Score", ascending=False)
#     avg_s = soil["Score"].mean()

#     fig = px.bar(soil, x="label", y="Score", color="Score",
#                  color_continuous_scale="YlGn", text="Score",
#                  title="Soil Health Score (avg of N+P+K)")
#     fig.add_hline(y=avg_s, line_dash="dash", line_color="red",
#                   annotation_text=f"Avg: {avg_s:.1f}")
#     fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#     fig.update_layout(xaxis_tickangle=-45, height=420)
#     fig.update_coloraxes(colorbar=colorbar_cfg())
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("⚠️ Nutrient Deficiency Flag")
#     npk_flag = df.groupby("label")[["N","P","K"]].mean().round(2).reset_index()
#     npk_flag["N_Flag"] = npk_flag["N"].apply(lambda x: "⚠️ Low" if x<=50 else "✅ OK")
#     npk_flag["P_Flag"] = npk_flag["P"].apply(lambda x: "⚠️ Low" if x<=40 else "✅ OK")
#     npk_flag["K_Flag"] = npk_flag["K"].apply(lambda x: "⚠️ Low" if x<=40 else "✅ OK")
#     npk_flag["Status"] = npk_flag[["N_Flag","P_Flag","K_Flag"]].apply(
#         lambda r: "⚠️ Deficient" if "⚠️ Low" in r.values else "✅ Sufficient", axis=1)
#     deficient = npk_flag[npk_flag["Status"]=="⚠️ Deficient"]
#     if len(deficient):
#         st.warning(f"⚠️ {len(deficient)} crops have a nutrient in the Low range.")
#         st.dataframe(deficient[["label","N","N_Flag","P","P_Flag","K","K_Flag"]],
#                      use_container_width=True)
#     else:
#         st.success("✅ All crops have sufficient average NPK levels.")
#     st.markdown("---")

#     st.subheader("📏 Feature Range per Crop")
#     sel_feat = st.selectbox("Select Feature", NUMERIC_FEATURES, key="range_sel")
#     range_df = (df.groupby("label")[sel_feat]
#                 .agg(["min","max","mean","std"]).round(2).reset_index())
#     range_df.columns = ["Crop","Min","Max","Mean","Std Dev"]
#     range_df = range_df.sort_values("Mean", ascending=False)
#     fig = go.Figure(go.Bar(
#         x=range_df["Crop"], y=range_df["Mean"], name="Mean",
#         marker_color="#2ca02c",
#         error_y=dict(type="data", array=range_df["Std Dev"], visible=True),
#         text=range_df["Mean"], textposition="outside"
#     ))
#     fig.update_layout(title=f"{sel_feat} — Mean ± Std Dev",
#                       xaxis_tickangle=-45, height=440)
#     st.plotly_chart(fig, use_container_width=True)
#     st.dataframe(range_df.set_index("Crop"), use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔵 Scatter Plot Analysis")
#     scatter_pairs = [
#         ("rainfall","humidity","Rainfall vs Humidity"),
#         ("temperature","ph","Temperature vs Soil pH"),
#         ("N","K","Nitrogen vs Potassium"),
#         ("temperature","rainfall","Temperature vs Rainfall"),
#     ]
#     s1, s2 = st.columns(2)
#     for i, (x, y, title) in enumerate(scatter_pairs):
#         fig = px.scatter(df, x=x, y=y, color="label",
#                          hover_name="label", title=title, opacity=0.6)
#         fig.update_layout(height=420, showlegend=False)
#         (s1 if i % 2 == 0 else s2).plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📦 Feature Distribution (Box Plot)")
#     box_sel = st.selectbox("Select Feature", NUMERIC_FEATURES, key="box_sel")
#     fig = px.box(df, x="label", y=box_sel, color="label",
#                  title=f"{box_sel} Distribution by Crop",
#                  color_discrete_sequence=px.colors.qualitative.Pastel)
#     fig.update_layout(xaxis_tickangle=-45, height=500, showlegend=False)
#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("---")

#     st.subheader("📋 Complete Crop Profile")
#     full_prof = df.groupby("label")[NUMERIC_FEATURES].mean().round(2)
#     full_prof.columns = ["N (mg/kg)","P (mg/kg)","K (mg/kg)",
#                          "Temp (°C)","Humidity (%)","pH","Rainfall (mm)"]
#     st.dataframe(full_prof.style.background_gradient(cmap="YlGn", axis=0),
#                  use_container_width=True)
#     st.markdown("---")

#     st.subheader("⚖️ Crop-to-Crop Comparison")
#     cc1, cc2 = st.columns(2)
#     crop_a = cc1.selectbox("Crop A", CROPS_LIST, index=0, key="ca")
#     crop_b = cc2.selectbox("Crop B", CROPS_LIST, index=1, key="cb")

#     a_v = df[df["label"]==crop_a][NUMERIC_FEATURES].mean().round(2)
#     b_v = df[df["label"]==crop_b][NUMERIC_FEATURES].mean().round(2)

#     fig = go.Figure([
#         go.Bar(name=crop_a, x=FEATURE_LABELS, y=a_v.values,
#                marker_color="#2ca02c", text=a_v.values, textposition="outside"),
#         go.Bar(name=crop_b, x=FEATURE_LABELS, y=b_v.values,
#                marker_color="#1f77b4", text=b_v.values, textposition="outside"),
#     ])
#     fig.update_layout(barmode="group",
#                       title=f"{crop_a} vs {crop_b}", height=400)
#     st.plotly_chart(fig, use_container_width=True)

#     a_n = CROP_NORM.loc[crop_a].values.tolist()
#     b_n = CROP_NORM.loc[crop_b].values.tolist()
#     fig2 = go.Figure([
#         go.Scatterpolar(r=a_n+[a_n[0]], theta=NUMERIC_FEATURES+[NUMERIC_FEATURES[0]],
#                         fill="toself", name=crop_a,
#                         line_color="#2ca02c", fillcolor="rgba(44,160,44,0.15)"),
#         go.Scatterpolar(r=b_n+[b_n[0]], theta=NUMERIC_FEATURES+[NUMERIC_FEATURES[0]],
#                         fill="toself", name=crop_b,
#                         line_color="#1f77b4", fillcolor="rgba(31,119,180,0.15)"),
#     ])
#     fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,1])),
#                        title=f"Radar: {crop_a} vs {crop_b} (Normalized 0–1)", height=460)
#     st.plotly_chart(fig2, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔍 Similar Crops Finder")
#     target = st.selectbox("Select a Crop", CROPS_LIST, key="sim")
#     vec    = CROP_NORM.loc[target]
#     dists  = CROP_NORM.drop(target).apply(
#         lambda r: np.sqrt(((r - vec)**2).sum()), axis=1)
#     top3 = dists.nsmallest(3).reset_index()
#     top3.columns = ["Similar Crop","Distance (lower=closer)"]
#     top3["Distance (lower=closer)"] = top3["Distance (lower=closer)"].round(4)
#     st.write(f"**Top 3 crops most similar to {target}:**")
#     st.dataframe(top3, use_container_width=True)
#     sim_names   = top3["Similar Crop"].tolist()
#     sim_profile = CROP_MEANS.loc[[target]+sim_names].round(2)
#     st.dataframe(sim_profile.style.background_gradient(cmap="Greens", axis=0),
#                  use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔍 Crop Filter")
#     sel_crop  = st.selectbox("Select Crop", CROPS_LIST, key="filter")
#     crop_data = df[df["label"]==sel_crop]
#     m1,m2,m3,m4 = st.columns(4)
#     m1.metric("Avg Temp",     f"{crop_data['temperature'].mean():.1f} °C")
#     m2.metric("Avg Humidity", f"{crop_data['humidity'].mean():.1f} %")
#     m3.metric("Avg Rainfall", f"{crop_data['rainfall'].mean():.1f} mm")
#     m4.metric("Avg pH",       f"{crop_data['ph'].mean():.2f}")
#     n1,n2,n3 = st.columns(3)
#     n1.metric("Avg Nitrogen",   round(crop_data["N"].mean(),2))
#     n2.metric("Avg Phosphorus", round(crop_data["P"].mean(),2))
#     n3.metric("Avg Potassium",  round(crop_data["K"].mean(),2))
#     st.dataframe(crop_data, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🔗 Feature Correlation Matrix")
#     corr = df[NUMERIC_FEATURES].corr().round(3)
#     fig  = px.imshow(corr, text_auto=True, color_continuous_scale="RdYlGn",
#                      zmin=-1, zmax=1, title="Feature Correlation Heatmap")
#     fig.update_layout(height=480)
#     fig.update_coloraxes(colorbar=colorbar_cfg())
#     st.plotly_chart(fig, use_container_width=True)
#     st.caption("🟢 Green = positive | 🔴 Red = negative | ⚪ White = no correlation")

#     pairs = corr.unstack().reset_index()
#     pairs.columns = ["Feature A","Feature B","Correlation"]
#     pairs = pairs[pairs["Feature A"] < pairs["Feature B"]]
#     pairs["Abs"] = pairs["Correlation"].abs()
#     pairs = pairs.sort_values("Abs", ascending=False).drop(columns="Abs")
#     pc1, pc2 = st.columns(2)
#     with pc1:
#         st.write("**Top 3 Positive**")
#         st.dataframe(pairs[pairs["Correlation"]>0].head(3).reset_index(drop=True),
#                      use_container_width=True)
#     with pc2:
#         st.write("**Top 3 Negative**")
#         st.dataframe(pairs[pairs["Correlation"]<0].head(3).reset_index(drop=True),
#                      use_container_width=True)
#     st.markdown("---")

#     st.subheader("📘 Feature Meaning")
#     feat_info = pd.DataFrame({
#         "Feature": ["N","P","K","temperature","humidity","ph","rainfall"],
#         "Meaning": [
#             "Nitrogen — leaf and stem growth",
#             "Phosphorus — root and flower growth",
#             "Potassium — plant strength and disease resistance",
#             "Temperature — optimal growing temperature",
#             "Humidity — moisture level in the air",
#             "Soil pH — acidity or alkalinity",
#             "Rainfall — water requirement"
#         ],
#         "Unit": ["mg/kg","mg/kg","mg/kg","°C","%","0–14","mm"]
#     })
#     st.dataframe(feat_info, use_container_width=True)
#     st.markdown("---")

#     st.subheader("🌱 Farmer Understanding Guide")
#     g1, g2 = st.columns(2)
#     with g1:
#         st.success("🟢 **Low Nitrogen (≤50)** → Light fertilizer needed")
#         st.info("🔵 **Medium Nitrogen (51–120)** → Balanced fertilizer")
#         st.warning("🟡 **High Nitrogen (>120)** → Heavy fertilizer needed")
#         st.success("🟢 **Cool (≤20°C)** → Wheat, lentil, chickpea")
#         st.info("🔵 **Moderate (21–30°C)** → Most common crops")
#         st.warning("🟡 **Hot (>30°C)** → Tropical/summer crops")
#     with g2:
#         st.success("🟢 **Acidic (pH<6)** → Tea, rice, blueberry")
#         st.info("🔵 **Neutral (pH 6–7.5)** → Best for most crops")
#         st.warning("🟡 **Alkaline (pH>7.5)** → Cotton, maize")
#         st.success("🟢 **Low Rainfall (≤100mm)** → Drought-tolerant crops")
#         st.info("🔵 **Medium Rainfall (101–200mm)** → General crops")
#         st.warning("🟡 **High Rainfall (>200mm)** → Water-intensive crops")
#     st.markdown("---")

#     st.subheader("📌 Key Insights")
#     st.success("✅ Dataset is balanced with nearly equal crop distribution.")
#     st.success("✅ No missing values or duplicate rows found.")
#     st.success("✅ Dataset is clean and ready for ML model training.")
#     st.info("📊 Rainfall, temperature, humidity and soil nutrients drive crop suitability.")
#     st.info("🌱 Rice and jute need high humidity & rainfall; chickpea and kidney beans prefer dry conditions.")
#     st.info("🧪 Use Scatter and Box Plots to identify natural clusters for ML feature selection.")
#     st.info("⚖️ Use Crop Comparison and Similar Crops to help farmers choose alternative crops.")

# # =========================================================
# # PAGE: ML PREDICTION
# # =========================================================

# elif page == "🤖 ML Prediction":

#     st.header("🤖 AI-Powered Crop Recommendation")
#     st.markdown("---")

#     if ml_error:
#         st.error(
#             f"❌ Could not load ML model files.\n\n"
#             f"**Error:** `{ml_error}`\n\n"
#             "Please make sure `crop_model.pkl`, `scaler.pkl`, and "
#             "`label_encoder.pkl` are in the same folder as `app.py`."
#         )
#         st.stop()

#     if hasattr(crop_model, "feature_importances_"):
#         st.subheader("📈 Model Feature Importance")
#         imp_df = pd.DataFrame({
#             "Feature":    FEATURE_LABELS,
#             "Importance": crop_model.feature_importances_
#         }).sort_values("Importance", ascending=False)

#         fig = px.bar(imp_df, x="Feature", y="Importance",
#                      color="Importance", color_continuous_scale="Teal",
#                      text=imp_df["Importance"].round(3),
#                      title="Feature Importance (Higher = More Influential)")
#         fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#         fig.update_layout(height=380)
#         fig.update_coloraxes(colorbar=colorbar_cfg())
#         st.plotly_chart(fig, use_container_width=True)
#         st.info(
#             f"🔑 Most influential: **{imp_df.iloc[0]['Feature']}**  |  "
#             f"📉 Least influential: **{imp_df.iloc[-1]['Feature']}**"
#         )
#         st.markdown("---")

#     st.subheader("🌱 Enter Your Soil and Weather Conditions")

#     sl1, sl2 = st.columns(2)

#     with sl1:
#         N = st.slider("Nitrogen (N) mg/kg",
#                       int(df["N"].min()), int(df["N"].max()), int(df["N"].mean()))
#         P = st.slider("Phosphorus (P) mg/kg",
#                       int(df["P"].min()), int(df["P"].max()), int(df["P"].mean()))
#         K = st.slider("Potassium (K) mg/kg",
#                       int(df["K"].min()), int(df["K"].max()), int(df["K"].mean()))
#         temperature = st.slider("Temperature (°C)",
#                                 float(df["temperature"].min()),
#                                 float(df["temperature"].max()),
#                                 round(float(df["temperature"].mean()),1))
#     with sl2:
#         humidity = st.slider("Humidity (%)",
#                              float(df["humidity"].min()),
#                              float(df["humidity"].max()),
#                              round(float(df["humidity"].mean()),1))
#         ph = st.slider("Soil pH",
#                        float(df["ph"].min()), float(df["ph"].max()),
#                        round(float(df["ph"].mean()),1))
#         rainfall = st.slider("Rainfall (mm)",
#                              float(df["rainfall"].min()),
#                              float(df["rainfall"].max()),
#                              round(float(df["rainfall"].mean()),1))

#     st.markdown("---")
#     st.subheader("📊 Real-Time Input Analysis")
#     ia1, ia2, ia3, ia4 = st.columns(4)
#     ia1.info(f"🌿 N: **{nitrogen_category(N)}**\n\n💧 Humidity: **{humidity_category(humidity)}**")
#     ia2.info(f"🌿 P: **{phosphorus_category(P)}**\n\n🧪 Soil pH: **{ph_category(ph)}**")
#     ia3.info(f"🌿 K: **{potassium_category(K)}**\n\n🌧 Rainfall: **{rainfall_category(rainfall)}**")
#     ia4.info(f"🌡 Temp: **{temperature_category(temperature)}**")

#     st.markdown("---")

#     if st.button("🌾 Predict Best Crop", use_container_width=True):
#         try:
#             inp        = [[N, P, K, temperature, humidity, ph, rainfall]]
#             scaled     = crop_scaler.transform(inp)
#             prediction = crop_model.predict(scaled)
#             pred_crop  = crop_encoder.inverse_transform(prediction)[0]

#             st.success(f"✅ Recommended Crop: **{pred_crop.upper()}**")
#             st.markdown("---")

#             if hasattr(crop_model, "predict_proba"):
#                 st.subheader("📊 Top 5 Crop Predictions")
#                 proba  = crop_model.predict_proba(scaled)[0]
#                 prob_df = pd.DataFrame({
#                     "Crop":        crop_encoder.classes_,
#                     "Probability": proba
#                 }).sort_values("Probability", ascending=False).head(5)
#                 prob_df["Pct"] = (prob_df["Probability"]*100).round(2)

#                 fig = px.bar(prob_df, x="Crop", y="Probability",
#                              color="Probability",
#                              text=prob_df["Pct"].astype(str)+"%",
#                              color_continuous_scale="Greens",
#                              title="Prediction Confidence (Top 5)")
#                 fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#                 fig.update_layout(height=420)
#                 fig.update_coloraxes(colorbar=colorbar_cfg())
#                 st.plotly_chart(fig, use_container_width=True)

#                 top_pct = prob_df.iloc[0]["Pct"]
#                 if top_pct >= 80:
#                     st.success(f"🎯 High confidence: {top_pct}%")
#                 elif top_pct >= 50:
#                     st.info(f"🔍 Moderate confidence: {top_pct}% — verify with local conditions.")
#                 else:
#                     st.warning(f"⚠️ Low confidence: {top_pct}% — consult an agronomist.")
#                 st.markdown("---")

#             st.subheader(f"📐 Your Conditions vs Ideal for {pred_crop.capitalize()}")
#             ideal = df[df["label"]==pred_crop][NUMERIC_FEATURES].mean().round(2)
#             user_vals = [N, P, K, temperature, humidity, ph, rainfall]

#             fig = go.Figure([
#                 go.Bar(name="Your Input", x=FEATURE_LABELS, y=user_vals,
#                        marker_color="#1f77b4",
#                        text=[round(v,2) for v in user_vals], textposition="outside"),
#                 go.Bar(name=f"Ideal for {pred_crop}", x=FEATURE_LABELS,
#                        y=ideal.values, marker_color="#2ca02c",
#                        text=ideal.values, textposition="outside"),
#             ])
#             fig.update_layout(barmode="group",
#                               title=f"Your Input vs Ideal: {pred_crop}",
#                               height=400)
#             st.plotly_chart(fig, use_container_width=True)
#             st.markdown("---")

#             st.subheader("📋 Input Summary")
#             summ = pd.DataFrame({
#                 "Feature": ["Nitrogen (mg/kg)","Phosphorus (mg/kg)","Potassium (mg/kg)",
#                             "Temperature (°C)","Humidity (%)","Soil pH","Rainfall (mm)"],
#                 "Value":    [N, P, K, temperature, humidity, ph, rainfall],
#                 "Category": [nitrogen_category(N), phosphorus_category(P),
#                              potassium_category(K), temperature_category(temperature),
#                              humidity_category(humidity), ph_category(ph),
#                              rainfall_category(rainfall)]
#             })
#             st.dataframe(summ, use_container_width=True)
#             st.markdown("---")

#             st.subheader("🌱 Crop Advice")
#             crop_advice = {
#                 "rice":        "Requires high rainfall (150–300mm), high humidity (80–90%), and slightly acidic soil (pH 5.5–6.5).",
#                 "maize":       "Needs moderate rainfall, moderate temperature (21–27°C), and fertile loamy soil (pH 5.5–7.0).",
#                 "jute":        "Thrives in high humidity and rainfall. Requires warm climate (25–35°C) and alluvial soil.",
#                 "cotton":      "Grows well in well-drained black soil (pH 6–8), warm climate (21–35°C), and moderate rainfall.",
#                 "coconut":     "Requires tropical climate, high humidity (70–80%), and sandy loam soil.",
#                 "papaya":      "Needs warm climate (25–30°C), well-drained soil, moderate rainfall, and high humidity.",
#                 "banana":      "Requires rich loamy soil, high humidity, warm temperature (26–30°C), and regular rainfall.",
#                 "mango":       "Prefers deep well-drained soil, dry season at flowering, and tropical/subtropical climate.",
#                 "grapes":      "Needs well-drained sandy loam, dry hot summers and cool winters.",
#                 "watermelon":  "Requires warm climate (25–35°C), sandy loam soil, and moderate to high rainfall.",
#                 "muskmelon":   "Grows best in warm climate, sandy soil with good drainage, and moderate humidity.",
#                 "apple":       "Requires cool climate (cold winters for dormancy), loamy soil, and moderate rainfall.",
#                 "orange":      "Needs subtropical climate, well-drained sandy loam, and moderate rainfall (750–1200mm).",
#                 "pomegranate": "Drought-tolerant, wide pH range (5.5–7.5), grows well in semi-arid regions.",
#                 "lentil":      "Cool season crop, well-drained loamy soil (pH 6–8), low rainfall.",
#                 "blackgram":   "Warm climate (25–35°C), well-drained loamy soil, moderate rainfall (600–800mm).",
#                 "mungbean":    "Warm season, sandy loam soil, short rainfall period, moderate temperature (28–30°C).",
#                 "mothbeans":   "Drought-tolerant, arid/semi-arid regions, sandy soil, very low rainfall.",
#                 "pigeonpeas":  "Drought-tolerant legume, well-drained soil (pH 5–7), moderate rainfall.",
#                 "kidneybeans": "Cool temperature, well-drained fertile loam (pH 6–7), moderate rainfall.",
#                 "chickpea":    "Cool season, drought-tolerant, loamy soil (pH 5.5–7), low rainfall.",
#                 "coffee":      "Tropical climate (15–28°C), high humidity, acidic well-drained soil (pH 6–6.5), high rainfall."
#             }
#             advice = crop_advice.get(
#                 pred_crop.lower(),
#                 f"{pred_crop.capitalize()} is suited to the conditions you entered. "
#                 "Consult local agricultural guidelines for detailed advice."
#             )
#             st.info(f"🌿 **{pred_crop.capitalize()} Advice:** {advice}")
#             st.markdown("---")

#             st.subheader("🧪 Soil & Climate Summary")
#             sc1, sc2 = st.columns(2)
#             with sc1:
#                 if ph < 6:
#                     st.warning("⚠️ **Acidic Soil** — add lime to raise pH.")
#                 elif ph > 7.5:
#                     st.warning("⚠️ **Alkaline Soil** — add sulfur to lower pH.")
#                 else:
#                     st.success("✅ **Neutral Soil pH** — ideal for most crops.")
#                 n_cat = nitrogen_category(N)
#                 if n_cat == "Low":
#                     st.warning("⚠️ Low Nitrogen — apply urea or nitrogen-rich fertilizer.")
#                 elif n_cat == "High":
#                     st.info("ℹ️ High Nitrogen — reduce fertilizer application.")
#                 else:
#                     st.success("✅ Nitrogen level is balanced.")
#             with sc2:
#                 if rainfall > 200:
#                     st.info("🌧 High rainfall — ensure good field drainage.")
#                 elif rainfall < 80:
#                     st.info("☀️ Low rainfall — consider drip irrigation.")
#                 else:
#                     st.success("✅ Moderate rainfall — suitable for most crops.")
#                 t_cat = temperature_category(temperature)
#                 if t_cat == "Cool":
#                     st.info("❄️ Cool climate — suitable for wheat, lentil, chickpea.")
#                 elif t_cat == "Hot":
#                     st.info("🔥 Hot climate — suitable for tropical/summer crops.")
#                 else:
#                     st.success("✅ Moderate temperature — good for most crops.")

#         except Exception as e:
#             st.error(f"❌ Prediction failed: `{str(e)}`")

# # =========================================================
# # PAGE: DISEASE DETECTION
# # =========================================================

# elif page == "🌿 Disease Detection":

#     st.header("🌿 Plant Disease Detection System")
#     st.markdown("---")

#     if disease_error:
#         st.error(
#             f"❌ Disease model not found.\n\n"
#             f"**Error:** `{disease_error}`\n\n"
#             "Run `train_disease_model.py` first to train and save the model, "
#             "then restart the app."
#         )
#         st.stop()

#     st.subheader("📤 Upload a Plant Leaf Image")
#     st.caption(
#         "Upload a clear photo of a plant leaf. "
#         "The AI will predict whether it is healthy or diseased."
#     )

#     uploaded = st.file_uploader(
#         "Drag & drop or click to browse",
#         type=["jpg","jpeg","png","webp"],
#         label_visibility="collapsed"
#     )

#     if uploaded is not None:

#         image = Image.open(uploaded).convert("RGB")

#         col_img, col_res = st.columns([1, 1])

#         with col_img:
#             st.image(image, caption="Uploaded Leaf Image", use_column_width=True)

#         img_resized = image.resize((128, 128))
#         img_array   = np.array(img_resized, dtype="float32") / 255.0
#         img_array   = np.expand_dims(img_array, axis=0)

#         try:
#             preds         = disease_model.predict(img_array, verbose=0)
#             pred_idx      = int(np.argmax(preds))
#             disease_name  = disease_encoder.inverse_transform([pred_idx])[0]
#             confidence    = float(np.max(preds)) * 100
#             all_probs     = preds[0]

#             with col_res:
#                 st.markdown('<div class="disease-card">', unsafe_allow_html=True)

#                 if confidence >= 75:
#                     st.success(f"✅ **Predicted:** {disease_name.replace('_', ' ')}")
#                 elif confidence >= 50:
#                     st.warning(f"⚠️ **Predicted (Moderate Confidence):** {disease_name.replace('_', ' ')}")
#                 else:
#                     st.error(f"❓ **Low Confidence Prediction:** {disease_name.replace('_', ' ')}")

#                 st.metric("Confidence", f"{confidence:.2f}%")
#                 st.progress(int(min(confidence, 100)))

#                 is_healthy = "healthy" in disease_name.lower()
#                 if is_healthy:
#                     st.success("🌿 Your plant appears **HEALTHY**!")
#                 else:
#                     st.error("🦠 Disease detected — see treatment advice below.")

#                 st.markdown('</div>', unsafe_allow_html=True)

#             st.markdown("---")

#             st.subheader("💊 Treatment & Care Advice")

#             disease_advice = {
#                 "Tomato_healthy":
#                     ("✅ Healthy Plant", "success",
#                      "Maintain regular watering (avoid overhead irrigation), "
#                      "balanced fertilization, and good air circulation."),
#                 "Tomato_Early_blight":
#                     ("⚠️ Early Blight (Alternaria solani)", "warning",
#                      "Remove infected lower leaves immediately. Apply **mancozeb** "
#                      "or **chlorothalonil** fungicide every 7–10 days. Avoid overhead "
#                      "watering and ensure good air flow around plants."),
#                 "Tomato_Late_blight":
#                     ("🚨 Late Blight (Phytophthora infestans)", "error",
#                      "Act fast — this spreads rapidly. Remove and destroy infected "
#                      "plants. Apply **copper-based fungicide** or **metalaxyl**. "
#                      "Avoid watering leaves; water at the base."),
#                 "Tomato_Leaf_Mold":
#                     ("⚠️ Leaf Mold (Passalora fulva)", "warning",
#                      "Improve greenhouse/field air circulation. Reduce humidity. "
#                      "Apply **copper** or **sulfur-based fungicide**. Remove affected leaves."),
#                 "Tomato_Septoria_leaf_spot":
#                     ("⚠️ Septoria Leaf Spot", "warning",
#                      "Remove infected leaves. Apply **mancozeb** fungicide. "
#                      "Rotate crops and avoid overhead irrigation."),
#                 "Tomato_Spider_mites":
#                     ("⚠️ Spider Mites", "warning",
#                      "Spray plants with water to dislodge mites. "
#                      "Apply **neem oil** or **insecticidal soap**. "
#                      "Introduce predatory mites as biological control."),
#                 "Tomato_Target_Spot":
#                     ("⚠️ Target Spot", "warning",
#                      "Remove infected leaves. Apply **azoxystrobin** or "
#                      "**chlorothalonil** fungicide. Ensure good air circulation."),
#                 "Tomato_Mosaic_Virus":
#                     ("🚨 Tomato Mosaic Virus", "error",
#                      "No cure available. Remove and destroy infected plants to prevent spread. "
#                      "Control aphids (virus vectors) with **neem oil**. Sanitize tools."),
#                 "Tomato_Yellow_Leaf_Curl_Virus":
#                     ("🚨 Yellow Leaf Curl Virus", "error",
#                      "Spread by whiteflies — apply **imidacloprid** to control them. "
#                      "Remove infected plants. Use virus-resistant tomato varieties."),
#                 "Tomato_Bacterial_spot":
#                     ("⚠️ Bacterial Spot (Xanthomonas)", "warning",
#                      "Apply **copper-based bactericide** (copper hydroxide). "
#                      "Avoid working with plants when wet. Practice crop rotation."),
#                 "Potato_healthy":
#                     ("✅ Healthy Potato Plant", "success",
#                      "Keep soil consistently moist but not waterlogged. "
#                      "Earth up around stems to prevent greening."),
#                 "Potato_Early_blight":
#                     ("⚠️ Potato Early Blight", "warning",
#                      "Apply **mancozeb** or **chlorothalonil** fungicide. "
#                      "Remove heavily infected leaves. Avoid nitrogen excess."),
#                 "Potato_Late_blight":
#                     ("🚨 Potato Late Blight (Phytophthora infestans)", "error",
#                      "Most destructive potato disease. Apply **metalaxyl** or "
#                      "**cymoxanil** fungicide immediately. Destroy infected tubers. "
#                      "Do not compost infected material."),
#                 "Pepper,_bell_healthy":
#                     ("✅ Healthy Bell Pepper", "success",
#                      "Maintain consistent moisture, full sun, and warm temperatures (20–30°C)."),
#                 "Pepper,_bell_Bacterial_spot":
#                     ("⚠️ Bacterial Spot (Xanthomonas)", "warning",
#                      "Apply **copper hydroxide** spray. Avoid overhead watering. "
#                      "Use certified disease-free seeds."),
#                 "Corn_(maize)_healthy":
#                     ("✅ Healthy Maize Plant", "success",
#                      "Ensure adequate nitrogen levels and consistent irrigation."),
#                 "Corn_(maize)_Common_rust":
#                     ("⚠️ Common Rust (Puccinia sorghi)", "warning",
#                      "Apply **propiconazole** fungicide early. "
#                      "Use rust-resistant hybrid varieties."),
#                 "Corn_(maize)_Northern_Leaf_Blight":
#                     ("⚠️ Northern Leaf Blight", "warning",
#                      "Apply **azoxystrobin** or **propiconazole** at early stages. "
#                      "Practice crop rotation; avoid corn-after-corn."),
#                 "Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot":
#                     ("⚠️ Gray Leaf Spot", "warning",
#                      "Apply **strobilurin** fungicide. Choose tolerant hybrids. "
#                      "Till crop residues to reduce inoculum."),
#                 "Apple_healthy":
#                     ("✅ Healthy Apple Tree", "success",
#                      "Prune for good air flow. Apply dormant oil spray in late winter."),
#                 "Apple_Apple_scab":
#                     ("⚠️ Apple Scab (Venturia inaequalis)", "warning",
#                      "Apply **myclobutanil** or **captan** fungicide at bud break. "
#                      "Remove fallen leaves to reduce infection source."),
#                 "Apple_Black_rot":
#                     ("⚠️ Black Rot (Botryosphaeria obtusa)", "warning",
#                      "Prune out dead/infected wood. Apply **captan** fungicide. "
#                      "Remove mummified fruits from the tree."),
#                 "Apple_Cedar_apple_rust":
#                     ("⚠️ Cedar Apple Rust", "warning",
#                      "Apply **myclobutanil** fungicide early in spring. "
#                      "Remove nearby cedar/juniper trees if possible."),
#             }

#             advice_key = disease_name
#             if advice_key in disease_advice:
#                 diag_label, diag_type, diag_text = disease_advice[advice_key]
#                 if diag_type == "success":
#                     st.success(f"**{diag_label}**\n\n{diag_text}")
#                 elif diag_type == "warning":
#                     st.warning(f"**{diag_label}**\n\n{diag_text}")
#                 else:
#                     st.error(f"**{diag_label}**\n\n{diag_text}")
#             else:
#                 if is_healthy:
#                     st.success(
#                         f"**{disease_name.replace('_',' ')}** — Plant appears healthy. "
#                         "Maintain good watering, fertilization, and pest monitoring practices."
#                     )
#                 else:
#                     st.warning(
#                         f"**Detected: {disease_name.replace('_',' ')}**\n\n"
#                         "🌿 General advice:\n"
#                         "• Remove visibly infected leaves immediately.\n"
#                         "• Apply an appropriate fungicide or bactericide.\n"
#                         "• Improve air circulation and avoid overhead irrigation.\n"
#                         "• Consult your local agricultural extension officer for a precise diagnosis."
#                     )

#             st.markdown("---")

#             st.subheader("📊 Prediction Confidence (All Classes)")

#             prob_df = pd.DataFrame({
#                 "Disease":    disease_encoder.classes_,
#                 "Confidence": all_probs
#             }).sort_values("Confidence", ascending=False)

#             fig = px.bar(
#                 prob_df, x="Disease", y="Confidence",
#                 color="Confidence",
#                 text=(prob_df["Confidence"]*100).round(2).astype(str)+"%",
#                 color_continuous_scale="Reds",
#                 title="Model Confidence per Disease Class"
#             )
#             fig.update_traces(textposition="outside", textfont_color="#1a1a1a")
#             fig.update_layout(xaxis_tickangle=-35, height=430, showlegend=False)
#             fig.update_coloraxes(colorbar=colorbar_cfg())
#             st.plotly_chart(fig, use_container_width=True)

#             st.markdown("---")

#             st.subheader("📝 General Plant Health Tips")
#             t1, t2, t3 = st.columns(3)
#             t1.info("💧 **Water at the Base**\nAvoid wetting leaves — wet leaves promote fungal disease.")
#             t2.info("🌬️ **Air Circulation**\nProper spacing between plants reduces humidity and disease spread.")
#             t3.info("🔄 **Crop Rotation**\nRotate crops every season to break disease and pest cycles.")

#         except Exception as e:
#             st.error(f"❌ Disease prediction failed: `{str(e)}`")

#     else:
#         st.info(
#             "👆 Upload a leaf image above to get started.\n\n"
#             "**Supported formats:** JPG, JPEG, PNG, WEBP\n\n"
#             "**Tips for best results:**\n"
#             "• Use a clear, well-lit photo of a single leaf\n"
#             "• Avoid blurry or dark images\n"
#             "• Capture the affected area clearly\n"
#             "• Image size: any — the model resizes automatically to 128×128"
#         )

#         st.markdown("---")
#         st.subheader("🌿 Diseases This Model Can Detect")
#         st.caption(
#             "The model is trained on the classes present in your Disease_Dataset folder. "
#             "Below are the common diseases supported when using the PlantVillage dataset."
#         )

#         sample_diseases = [
#             "Tomato — Healthy",        "Tomato — Early Blight",
#             "Tomato — Late Blight",    "Tomato — Leaf Mold",
#             "Tomato — Mosaic Virus",   "Tomato — Spider Mites",
#             "Potato — Healthy",        "Potato — Early Blight",
#             "Potato — Late Blight",    "Pepper — Bacterial Spot",
#             "Corn — Common Rust",      "Corn — Northern Leaf Blight",
#             "Apple — Apple Scab",      "Apple — Black Rot",
#         ]

#         cols = st.columns(3)
#         for i, d in enumerate(sample_diseases):
#             cols[i % 3].write(f"• {d}")

