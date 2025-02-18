import pandas as pd
import streamlit as st

def run_about():
    st.title("👩🏻‍💻 개발 프로세스")
    col1, col2 = st.columns([1, 1])
    st.header("📌 개발 툴")
    st.markdown("""
    ✔ 데이터 전처리 & 모델링: Jupyter Notebook  
    ✔ 개발 & 코드 통합: Visual Studio Code (코드 작성, 디버깅, API 연동)   
    ✔ 웹 애플리케이션 프레임워크: Streamlit  
    """)
    st.markdown("___")
    st.header("🔍 사용된 기술")
    st.markdown("""
    - **개발언어**: Python
    - **예측 모델**: Prophet, XGBoost Regressor
    - **자연어 처리 모델**: Google Gemma-2-9b-it LLM API : Hugging Face Inference API를 활용한 맞춤형 여행 일정 추천
    - **데이터 출처**: 법무부_외국인 국적 및 월별 입국자 현황 "[데이터 출처: 공공데이터포털](https://www.data.go.kr/data/3074937/fileData.do)"
    - **웹 프레임워크**: Streamlit  
    - **활용 API**:  
        - 한국관광공사 API  
        - 네이버 블로그 API  
        - 카카오 맵 API  
    """)
    st.markdown("___")
    st.header("데이터 전처리 과정과정👾")
    st.markdown("""
    #### 1. 22\~24년 데이터로 작업 시작:  
    **20년\~21년**까지는 **코로나 영향**으로 입국제한이 있어 입국자수가 크게 감소  
    코로나시즌을 데이터에 반영하기에는 포스트코로나 시대도 종료된지 오래인 이 시점에 부적절하다 판단  
                
    #### 2. **22년 6월** 까지도 코로나 영향으로 **입국자수가 회복되지 않음**:  
    한국 또한 2022년 6월 8일부터 모든 입국자에 대한 자가격리 의무가 해제, 출국자수가 서서히 회복되었기 때문에 **22년 6월까지의 데이터 또한 예측데이터에 사용할 수 없다 판단**  
    나라별로 차이가 있어 22년 하반기까지도 영향이 있는 나라가 많아 **22년 데이터를 제외**하기로 결정  
    23,24년간의 적은 데이터양으로는 계절성 반영이 어려울것으로 예상은 하였으나, **시험삼아 Prophet Regressor 모델을 적용**하여 예측 진행  
    => 문제점 : 23년 1,2월까지도 일부국가들은 입국인원이 적다가, 후반기에 코로나 이전 수준으로 회복된것을 모델은 입국자수가 폭발적으로 증가한거로 예측하여 **예측오차**가 커짐  
    - 해결을 위한 노력:
        - growth="logistic" : 일정 수치 이상으로 증가하지 못하도록 제한 (입국인원은 한정적이다.)
        - 상한값 = 최대 입국자 수의 **110%** 로 제한
        - 하한값 = 24년 최소 입국자 수에 1.5를 곱하여 조절
        - 과대 성장 방지를 위한 변곡점 민감도 조절 → changepoint_prior_scale=0.05
        - ⇒ 하지만 위 모델로도 23년 초 **30141명** 가량이였다가, 회복 후 **430303명** 로 폭발적으로 증가하는 중국 등의 국가를 예측하는데에 한계가 있었다.*
                
    #### 3. **18,19년** 데이터 추가:  
    연속성이 깨질것이 염려되었으나, 23년, 24년 2년간의 데이터로는 계절특성을 반영하기 어렵다 판단되어 18,19년 데이터를 추가하여 4년간의 데이터로 모델링 진행  
    18년, 19년 데이터는 월별 컬럼이 따로 들어가는 양식이라 **피벗테이블**로 변환하여 23,24년 데이터와 양식을 맞춤               
    """)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("image/sc1.png", use_container_width=True)
        st.write("18,19년 Dataframe")
    with col2:
        st.image("image/sc2.png", width=235)
        st.write("23,24년 Dataframe")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
    #### 4. 국적 지역명 통일 및 개수 선정:  
    총 219개 국적지역 Value값 중  
    한국계 중국인, 터키, 체코공화국, 타이완 등 국적이 예전 이름이나 표기가 다른 경우가 있어 통일작업  
    201개국으로 정리
    모든 나라 데이터를 쓰는것보단  
    해당앱의 예상 사용자인 여행사 입장에서 **유효한 관광수요**로 보여지는 **입국자 총계 상위 15개국**으로 선정
    """)
        st.image("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi6wU-_akiUF8dX0CIkUmAxyYdkN3HWxUFtYy6qbNeaxilKVqaJG6j6IUolj-zObVd_jk4he57Lm1RcMdPQ-8oaF8wRje8QvYLCJDJkxxGMP_qbIqoNY8MYzG60ng7r_LtnJmqEa1J9uYS1/s800/character_earth_chikyu.png", width=300)
    with col2:
        st.image("image/sc3.png", width=400)

                

    st.markdown("___")
    st.header("Regressor 모델 채택과정👾")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        ### 1. **Linear Regression** 모델로 접근(r2_score = 0.88):  
        r2스코어는 높았으나 **선형 회귀모델로는 계절성 반영의 한계**가 있었음
        """)
    with col2:
        st.image("image/linear.png", width=500)


    df=pd.read_csv("data/evaluation_df.csv")
    st.dataframe(df, use_container_width=True)
    st.image("image/prophet.png", use_container_width=True)
    st.markdown("""
    ### 2. **Prophet** 모델 적용 :  
    계절성 반영이 가능한 모델, **중국제외 MAPE(평균 절대 백분율 오차)도 4~15%** 대로 준수한 예측 수준을 보여 채택
    """)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("image/xgb1.png", use_container_width=True)
    with col2:
        st.image("image/xgb2.png", use_container_width=True)
    st.markdown("""
    ### 3. **XGBoost** 모델 적용(r2_score=0.98) :  
    계절성 규칙이 깨진 **중국에 대해서만 트리 기반 회귀 XGBoost 모델** 적용,  
    최대한의 계절성 반영을 위해 **'월_sin', '월_cos’** 로 처리하여 **1월과 12월간의 연속성을 반영** 할 수 있게 처리

    """)
    st.markdown("___")
    st.subheader("LLM 선정 기준👾")
    st.markdown("""
    **채택한 LLM** : google/gemma-2-9b-it  
    **API 형태** 로 제공: 별도의 학습 과정 없이 즉시 활용 가능  
    **사용자의 입력 정보** 를 종합적으로 분석하여 여행사 수준의 맞춤형 여행 계획을 자동 생성하는 데 최적화된것으로 판단하여 선정      
    """)
    
    