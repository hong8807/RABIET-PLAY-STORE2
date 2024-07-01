import os
import streamlit as st
import openai

# Load API key from environment variable
api_key = st.secrets["OPENAI_API_KEY"]
if api_key is None:
    st.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
else:
    openai.api_key = api_key
    st.write("API 키가 성공적으로 로드되었습니다.")

    st.title("라비에트 영업사원 교육")

    # Page 1: 상세 시나리오 생성기
    st.header("페이지 1: 상세 시나리오 생성기")

    # Scenario Introduction
    st.markdown("**시나리오 소개**: 이 시나리오는 의료진에게 라베프라졸 (Rabeprazole)을 설명하는 내용을 포함합니다. 의료진의 전문 분야는 소화기 내과이며, 병원이나 클리닉에서 근무합니다.")

    # Scenario Challenge
    st.markdown("**시나리오 챌린지**: 다음 주제들 중 하나를 선택하여 설명을 시작하세요.")
    topic_options = ["효과", "안전성", "복약 순응도", "보험 인정 기준"]
    selected_topic = st.selectbox("토론할 주제를 선택하세요:", topic_options)

    if selected_topic == "효과":
        sub_topics = [
            "10mg BID 효과",
            "20mg BID 효과",
            "원조 대비 효과"
        ]
    elif selected_topic == "안전성":
        sub_topics = [
            "5년 임상 데이터",
            "소아 임상 데이터",
            "약물 상호작용에서 비효소적으로 대사됨: 다른 PPI는 cyp2c19로 대사되고 p-cap 계열은 cyp3a4로 대사됩니다. PPI 라비에트의 장점은 다약제를 복용하는 노인 환자에서도 상대적으로 안전하게 사용할 수 있다는 것입니다."
        ]
    elif selected_topic == "복약 순응도":
        sub_topics = [
            "작은 정제 크기",
            "식전 또는 식후 복용 가능"
        ]
    elif selected_topic == "보험 인정 기준":
        sub_topics = [
            "기간 제한 없이 처방 가능",
            "FULL DOSE BID (20MG BID)"
        ]

    selected_sub_topic = st.selectbox("세부 주제를 선택하세요:", sub_topics)

    # Detailed Scenario Generation
    if st.button("상세 시나리오 생성"):
        prompt = f"라베프라졸 (Rabeprazole)의 PPI 약물에 대해 의료진에게 설명하는 상세 시나리오를 생성하세요. 키워드: '{selected_topic}', 세부 주제: '{selected_sub_topic}'. " \
                 "다음과 같은 대화를 포함해주세요:\n\n" \
                 "IMP: 안녕하세요, DR.XXX. 오늘 저를 만나주셔서 감사합니다. 저는 라베프라졸에 대해 논의하고 싶습니다. 특히 {selected_topic}에 대해 말씀드리고자 합니다.\n\n" \
                 "DR.XXX: 안녕하세요, IMP. 라베프라졸은 익숙한 약물이지만, 귀사에서 제공하는 최신 정보와 인사이트를 듣고 싶습니다.\n\n" \
                 "IMP: 물론입니다, {selected_sub_topic}에 대해 설명드리겠습니다.\n\n"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            generated_text = response.choices[0].message["content"]

            # Display the generated scenario in Korean with the correct format
            st.markdown("### 시나리오")
            st.markdown(generated_text)

        except openai.error.OpenAIError as e:
            st.error(f"OpenAI 오류 발생: {e}")
        except Exception as e:
            st.error(f"오류 발생: {e}")

    if st.button("다른 주제로 이동"):
        st.experimental_rerun()
