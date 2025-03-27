from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper

import os

def generate_script(subject, video_length, creativity, api_key):
    title_template= ChatPromptTemplate.from_messages(
       [ ("human", f"{subject} 의 주제를 기반으로 사람들의 이목을 끄는 영상 제목을 만들어줘")

        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human", """
        너는 숏츠를 주기적으로 업로드하는 유튜버야. 아래의 주제와 내용을 기반으로, 숏츠를 기반으로 제목과 스크립트를 작성해줘
        숏츠 제목: {title}, 숏츠 길이 {duration}분, 생성한 스크립트의 내용에 처음 단락이 사람이 보고 나가지 못하게끔 후킹을 해줘.
        중간에는 핵심 내용만 넣어주고, 결말에는 반전이 있거나 깜짝 놀랄 요소가 있으면 좋아. 스크립트 형식은 [도입부, 중간, 결말]로 나눠서 작성해줘.
        전반적인 표현은 가볍고 Z세대 등 젊은 층이 좋아할 스타일이면 좋아! 내용 작성 시 제공된 위키백과 정도는 참고용으로만 사용하고, 관련 있는 정보만 사용, 관련 없는 내용은 무시해줘.
        {wikipedia_search} """)
    ]
)

    model = ChatOpenAI(openai_api_key = api_key, temperature=creativity)

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject" : subject}).content

    search = WikipediaAPIWrapper(lang="ko")
    search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length,
                "wikipedia_search": search_result}).content

    return search_result,title,script

# print(generate_script("설날", 1, 0.9, os.getenv("OPENAI-API_KEY") ))