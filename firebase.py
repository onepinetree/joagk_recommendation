import firebase_admin
from firebase_admin import credentials, firestore
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

if not firebase_admin._apps:
    cred = credentials.Certificate('/etc/secrets/orengecommunity.json')
    # cred = credentials.Certificate('orengeapp-43854-firebase-adminsdk-zq2mz-1a989fa573.json')
    app = firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection('userinfo')
docs = users_ref.stream()


def getEmbeddingInfo():
    users_ref = db.collection('userinfo')
    docs = users_ref.stream()

    documents = []  # user의 꿈이 들어감
    ids = []  # user의 닉네임이 들어감
    metadatas = []  # title(가장 마지막의 오랜지와 true인 가장 마지막의 조각을 title, content에 넣음)

    for doc in docs:
        # 문서의 필드 가져오기
        doc_dict = doc.to_dict()
        documents.append(doc_dict.get('꿈'))
        ids.append(doc_dict.get('닉네임'))

        # 하위 컬렉션에 접근하기 (doc.reference 사용)
        orenge_doc_ref = doc.reference.collection('오랜지').document('오랜지_1')

        # 문서를 가져오기 위해 get() 호출
        orenge_doc = orenge_doc_ref.get()
        if orenge_doc.exists:
            first_orenge = orenge_doc.to_dict().get('오랜지 이름')
            
            # 하위 컬렉션 안에 있는 "조각_1" 문서를 가져옴
            first_slice_doc = orenge_doc.to_dict().get('조각_1').get('이름')
            if first_slice_doc:
                first_slice = first_slice_doc
            else:
                first_slice = None  # 조각_1이 존재하지 않는 경우
        else:
            first_orenge = None  # 오랜지_1이 존재하지 않는 경우
            first_slice = None

        metadatas.append({'title': first_orenge, 'content': first_slice})

    return documents, ids, metadatas



# '''client와 꿈이 가장 비슷한 유저를 찾고 그 유저의 가장 마지막의 오랜지와 달성 현황이 true인 가장 마지막의 조각 이름을 보여줌, 없으면 가장 첫번째 조각 가장 동일한 목표를 vectordb에서 찾음, 
# 그 후 id에서 이름 = username, meta_data에서 = title, 여부 = acheive_bool, 그날의 일기 기록 = content로 적어온다.'''


#임베딩시 필요정보
# title, content, acheive_bool, username, usergoal, userID(collection 이름)

#title: metadata : 가장 최근에 이룬 조각
#content: metadata : 회고 내용
# -> 묶어서 dict으로 list

#username: ids : 닉네임 -> 리스트
#usergoal: documents : 현재 목표 -> 리스트

def getVectorDBCollectionName(nickname:str):
    '''닉네임을 입력하면 VectorDB의 collection이름으로 정할 userID를 return '''
    users_ref = db.collection('userinfo')
    docs = users_ref.stream()
    for doc in docs:
        if doc.to_dict().get('닉네임', '') == nickname:
            return doc.id.split('@')[0]

# print(getVectorDBCollectionName('ddd'))

def getDream(nickname):
    users_ref = db.collection('userinfo')
    docs = users_ref.stream()
    for doc in docs:
        if doc.to_dict().get('닉네임') == nickname:
            return doc.to_dict().get('꿈', '')
