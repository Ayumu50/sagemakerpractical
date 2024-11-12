import streamlit as st
import requests
import json
import boto3

import streamlit as st
import boto3
import json
import pandas as pd
import pandas as pd

# Streamlit アプリケーションのタイトルと説明
st.title("糖尿病予測アプリケーション")
st.write("以下の情報を入力して、糖尿病の予測を実行します。")

# 必要な入力パラメータをユーザーから取得
readmitted = st.selectbox("再入院", ["no", "yes"])
race = st.selectbox("人種", ["AfricanAmerican", "Caucasian", "Other"])
gender = st.selectbox("性別", ["Female", "Male"])
age = st.number_input("年齢", min_value=0, max_value=120, value=25)
time_in_hospital = st.number_input("入院時間 (日)", min_value=0, max_value=30, value=5)
num_lab_procedures = st.number_input("検査数", min_value=0, max_value=150, value=30)
num_procedures = st.number_input("手術回数", min_value=0, max_value=100, value=10)
num_medications = st.number_input("薬の種類数", min_value=0, max_value=100, value=10)
number_outpatient = st.number_input("外来診療回数", min_value=0, max_value=100, value=10)
number_emergency =st.number_input("緊急入院回数", min_value=0, max_value=100, value=10)
number_inpatient = st.number_input("入院回数", min_value=0, max_value=100, value=10)
number_diagnoses = st.number_input("診断数", min_value=0, max_value=1000, value=100)
max_glu_serum = st.number_input("血糖値の最大値", min_value=0, max_value=300, value=200)
a1c_result = st.number_input("A1C検査結果", min_value=0, max_value=10, value=5)
change = st.number_input("変化", min_value=0, max_value=2, value=1)

# boto3のクライアントを使用してエンドポイントを呼び出す準備
client = boto3.client('sagemaker-runtime', region_name='ap-northeast-1')

# エンドポイント名
endpoint_name = "canvas-new-deployment-11-12-2024-9-55-AM"

# 予測ボタン
if st.button("予測する"):
    # 入力データを辞書形式で準備
    body = pd.DataFrame({
        'readmitted': [readmitted],
        'race': [race],
        'gender': [gender],
        'age': [age],
        'time_in_hospital': [time_in_hospital],
        'num_lab_procedures': [num_lab_procedures],
        'num_procedures': [num_procedures],
        'num_medications': [num_medications],
        'number_outpatient': [number_outpatient],
        'number_emergency': [number_emergency],
        'number_inpatient': [number_inpatient],
        'number_diagnoses': [number_diagnoses],
        'max_glu_serum': [max_glu_serum],
        'A1Cresult': [a1c_result],
        'change': [change]
    }).to_csv(header=False, index=False).encode('utf-8')
        

    # JSON形式でデータを文字列に変換
    # data = json.dumps({"data": [input_data]})

    try:
        # SageMakerエンドポイントにPOSTリクエストを送信
        response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="text/csv",
        Body=body, 
        Accept="application/json"
    )

        # 予測結果を取得
        result = json.loads(response['Body'].read().decode())
        prediction = result.get("predictions")[0].get("predicted_label", "不明")

        # 予測結果を表示
        st.success(f"糖尿病予測結果: {prediction}")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

