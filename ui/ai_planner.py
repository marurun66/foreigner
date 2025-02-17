from huggingface_hub import InferenceClient
import streamlit as st
import csv
import streamlit as st

from navigation import navigate_to



HUGGING_FACE_READ_KEY = st.secrets["HUGGING_FACE_READ_KEY"]

def generate_ai_travel_plan():

    """AI에게 여행 패키지 생성을 요청하고 결과를 반환"""
    client = InferenceClient(
        provider="hf-inference",
        api_key=HUGGING_FACE_READ_KEY
    )

    # ✅ 세션 상태에서 유저가 선택한 정보 가져오기
    print
    year = st.session_state.get("year", 2025)
    month = st.session_state.get("month", 4)
    selected_country = st.session_state.get("selected_country", "대만")
    info = st.session_state.get("info", {})
    selected_travel = st.session_state.get("selected_travel", "축제,테마 정보 없음")
    selected_location = st.session_state.get("selected_location", "위치 정보 없음")
    selected_places = st.session_state.get("selected_places", [])

    # ✅ 유저의 여행 성향 정보
    language = info.get("언어", "알 수 없음")
    travel_preference = info.get("여행 성향", "알 수 없음")

    # ✅ AI에게 보낼 프롬프트 생성
    prompt = f"""
    나는 한국 여행사의 직원입니다. 
    {year}년 {month}월 {selected_country} 손님을 위한 한국 여행 코스를 준비해야 합니다. 
    {selected_country} 손님을 위해 사전에 준비하면 좋을 게 무엇인지 알려주세요.
    {selected_travel}를 중심으로 {selected_location}을 방문하며, 
    다음 관광지를 여행 코스에 포함하려고 합니다(다음 관광지중에 "호텔", "숙소", "펜션", "리조트"에서는 숙박합니다.): {", ".join(selected_places)}.
    
    고객이 한국에 입국해서 관광지들을 둘러보고, 귀국할 수 있는 여행 일정을 작성해주세요.
    또한, **{travel_preference}** 성향의 {selected_country} 고객에게 이 여행에서 어떤 부분이 어필될지도 작성해주세요.
    
    한글로 작성해주세요.
    """

    # ✅ LLM에게 요청 보내기
    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        model="google/gemma-2-9b-it", 
        messages=messages, 
        max_tokens=1024,
    )

    # ✅ 응답 결과 반환
    return completion.choices[0].message["content"]



def run_ai_planner():
    if not st.session_state.get("selected_places"):  # 선택된 관광지 & 숙소가 없을 경우
        st.warning("""🚨 해당 메뉴에서는 외국인 관광객, 여행 날짜, 여행 지역 정보를 바탕으로 AI와 함께 여행 일정을 계획할 수 있습니다.  
                Country 메뉴부터 시작해주세요.😉""")
        if st.button("➡ Country"):
            navigate_to("Country")
        
        return
    ## 🔹 이전 페이지에서 가져온 정보들
    year = st.session_state.get("year")
    month = st.session_state.get("month")
    selected_country = st.session_state.get("selected_country")
    info = st.session_state.get("info", {})  # 기본값 빈 딕셔너리
    expected_visitors = st.session_state.get("expected_visitors", "미정")  # 기본값 설정
    selected_travel = st.session_state.get("selected_travel", "축제,테마 정보 없음")
    selected_location = st.session_state.get("selected_location", "위치 정보 없음")
    selected_places = st.session_state.get("selected_places", [])
        # ✅ 유저의 여행 성향 정보
    language = info.get("언어", "알 수 없음")
    travel_preference = info.get("여행 성향", "알 수 없음")

    st.title("🤖 AI 여행 플래너")
    st.write("""
    ✨ AI가 선택한 정보를 기반으로 맞춤형 여행 일정을 생성합니다.  
    아래 버튼을 클릭하면 AI가 여행 코스를 추천해줍니다! 🚀
    """)

    # ✅ AI 여행 일정 생성 버튼
    if st.button("🚀 AI 여행 패키지 생성하기"):
        with st.spinner("AI가 여행 일정을 생성 중입니다... ⏳"):
            travel_plan = generate_ai_travel_plan()
        
        # ✅ AI가 생성한 여행 패키지 표시
        st.subheader("📌 AI 추천 여행 일정")
        st.write(travel_plan)

