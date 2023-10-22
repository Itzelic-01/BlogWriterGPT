import openai
import streamlit as st
from streamlit_chat import message
import time
 
openai.api_key = st.secrets["MY_APIKEY"]
 
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant who writes a safety technology blog.\nThe user is the person in charge of safety guidance on construction sites and specific facilities.\n\nWhen a user asks you to recommend a topic, please recommend a topic in a blog post to inform people about safety rules and safety-related laws as a safety guide.\n\nWhen a user asks you to write a blog post, the user writes a blog post in Korean to inform people about safety rules and safety-related laws.\n\nThe writing is written in honorific, not too serious, so that people can be interested.\nWrite sentences that can give people credibility using technical terms.\nIn the article, it should be composed of contents suitable for the purpose, such as type, purpose, cause, solution, and improvement, depending on the subject.\nDon't use strange sentences or words that aren't logical.\n\nIf the user provides the data in the following sentence, please answer based on the contents of the data and write it in the vicinity of 2500 characters in Korean based on all the information you can refer to:" + txt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=3008,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
 
    message = response["choices"][0]["message"]["content"].replace("", "")
    return message

# st.image()
st.header("안전기술 블로그 글 생성")

# Progress Bar
progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()

txt = st.text_area(
    "참고자료", placeholder="블로그 글 작성에 참고할 자료를 붙혀주세요 (선택사항)"
    )

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

with st.form('form', clear_on_submit=True):
    user_input = st.text_input('You: ', '', key='input')
    submitted = st.form_submit_button('Send')

if submitted and user_input:
    output = generate_response(user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

