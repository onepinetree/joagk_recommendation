import chromadb
from firebase import getEmbeddingInfo, getDream, getVectorDBCollectionName

chroma_client = chromadb.Client()

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time


def getSimilarUsers(nickname:str):
    userid = getVectorDBCollectionName(nickname=nickname)

    documents, ids, metadatas = getEmbeddingInfo()
    collection = chroma_client.get_or_create_collection(name=f"{userid}_my_collection")

    # switch `add` to `upsert` to avoid adding the same documents every time
    collection.upsert(
        documents=documents,
        ids=ids,
        metadatas=metadatas
        )

    user_query_text = getDream(nickname=nickname) 
    #여기다가 user에 관한 firebase호출함수

    results = collection.query(
        query_texts=[user_query_text], # Chroma will embed this for you
        n_results=5 # how many results to return
    )
    return results

# getSimilarUsers(nickname='ddd')

# simliar_user_dict = getSimilarUsers(nickname='ddd')
# dreams = simliar_user_dict.get('documents')[0]
# titles = [dict.get('title', '') for dict in simliar_user_dict.get('metadatas')[0]]
# contents = [dict.get('content', '') for dict in simliar_user_dict.get('metadatas')[0]]
# nicknames = simliar_user_dict.get('ids')[0]

# print(dreams)
# print(titles)
# print(contents)
# print(nicknames)