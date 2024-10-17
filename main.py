import streamlit as st
from chroma_db import getSimilarUsers
from firebase import getDream

with st.sidebar:
    st.title('로그인')

    # st.write("<br><br>", unsafe_allow_html=True) #빈칸 여백

    input_user_id = st.text_input('닉네임으로 로그인') 
    st.caption('닉네임을 입력하고 커뮤니티 활동을 시작해요') 
    signup_btn = st.button("로그인") 
    if signup_btn:
        if getDream(input_user_id):
            #DB 연동
            st.success(f'로그인이 완료되었습니다. \'{input_user_id}\'님')
        else:
            st.warning('조각앱을 사용하시는 유저만 사용이 가능합니다. 스토어에서 조각앱을 다운받아주세요.')



try:
    st.title('조각 커뮤니티🍊')
    st.write('나와 비슷한 꿈을 갖고 있는 사람들의 첫 시작을 통해 동기부여를 받아요.')

    st.write("<br><br>", unsafe_allow_html=True) #빈칸 여백

    def recordContainer(username = '박한솔', dream = '꿈', title = '제목입니다', content = '회고 내용이 없어요'):
        with st.container(border=True):
            col1, col2 = st.columns([9,1])
            with col1:
                st.subheader('오랜지: ' + title)
                st.write('조각: ' + content)
                st.write(f"'{dream}'" + '의 꿈을 가진 ' + username + ' 조각가')
            with col2:
                st.container(height=10, border=False)
                st.write('✅')


    simliar_user_dict = getSimilarUsers(nickname=input_user_id)
    dreams = simliar_user_dict.get('documents')[0]
    titles = [dict.get('title', '') for dict in simliar_user_dict.get('metadatas')[0]]
    contents = [dict.get('content', '') for dict in simliar_user_dict.get('metadatas')[0]]
    nicknames = simliar_user_dict.get('ids')[0]

    # print(dreams)
    # print(titles)
    # print(contents)
    # print(nicknames)

    try:
        #로그인 하기 전은 이렇게 보여야 함
        for i in range(len(nicknames)):
            recordContainer(username = nicknames[i], dream = dreams[i], title = titles[i], content = contents[i])
    except:
        pass
except:
    pass








