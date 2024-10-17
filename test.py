def gspread():
    # import gspread module
    import gspread

    # json 파일이 위치한 경로를 값으로 줘야 합니다.
    json_file_path = "wanna-go-place-list-automation-1635b10f855f.json"
    # select JSON file path to authorize
    gc = gspread.service_account(json_file_path)

    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1dhDXlOlGUdKXBTgZMcRVd8MoRnhHyppXcsRpyst0-F4/edit?gid=0#gid=0"
    doc = gc.open_by_url(spreadsheet_url)

    worksheet = doc.worksheet("시트2")

    # Update a single cell
    worksheet.update_acell('A1','자동화 끝!')

    # Update a range
    worksheet.update('A1:B2', [[1,2],[3,4]])

# sklearn 설치
# from sklearn.feature_extraction.text import CountVectorizer
import scipy as sp
# 형태소 분석기 import
from konlpy.tag import Okt
# scikit-learn의 TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# CountVectorizer: 텍스트의 feature 추출 모듈
# min_df: 단어장에 포함되기 위한 최소 빈도

# 벡터 사이의 거리를 구하는 함수
def dist_raw(v1, v2):
    # norm 이용
    delta = v1 - v2
    return sp.linalg.norm(delta.toarray())

# 한 번만 등장해도 단어장에 포함
vectorizer = TfidfVectorizer(min_df = 1, decode_error='ignore')

# 후보 문장 3가지
contents = ['가배도 코엑스점',
            '가배도프리미엄',
            '가배도 강남점',
            '가배도 신논현',
            '가배도 명동',
            '가배도 남대문시장점',
            ]

# 형태소 기준으로 토큰화
t = Okt()
contents_tokens = [t.morphs(row) for row in contents] # morphs(): 품사명을 제외하고 형태소 결과만 리턴

# 형태소 분석 후 띄어쓰기로 구분하여 하나의 문장으로 만들기
contents_4_vectorize = []

for content in contents_tokens:
    sentence = ""
    for word in content:
        sentence = sentence + ' '  + word
    
    contents_4_vectorize.append(sentence)

# tf-idf vectorize
X = vectorizer.fit_transform(contents_4_vectorize)
num_samples, num_features = X.shape
# X.toarray().transpose()
# vectorizer.get_feature_names_out()

# new 문장을 형태소 기준으로 토큰화
new_post = ['명동 가배도']
new_post_tokens = [t.morphs(row) for row in new_post]

# new 문장 벡터화 준비
new_post_4_vectorize = []

for content in new_post_tokens:
    sentence = ""
    for word in content:
        sentence = sentence + ' '  + word
    
    new_post_4_vectorize.append(sentence)

# transform
new_post_vec = vectorizer.transform(new_post_4_vectorize)
new_post_vec.toarray()

# best_doc = None
best_dist = 65535 # 임의의 큰 값 설정
best_i = None # 가장 비슷한 문장의 인덱스

# 모든 문장에 대해 거리 계산
for i in range(len(contents)):
    post_vec = X.getrow(i)

    # 거리 계산 함수 호출
    d = dist_raw(post_vec, new_post_vec)

    print(f"Post {i} with dist {d}: {contents[i]}")

    if d < best_dist:
        best_dist = d
        best_i = i

print(f"Best {best_i} with dist {best_dist}: {contents[best_i]}")