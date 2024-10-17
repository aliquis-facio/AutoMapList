장소를 입력하면 크롤러가 검색해서 그 장소에 대한 정보를 분류해서 구글 스프레드시트에 갱신하고 네이버 지도 혹은 구글 지도에 좌표 찍어주기
1. 장소 입력 받기
2. 장소 정보 추출하기
    1. 크롤링
    2. 어디서 크롤링을 할 것인지 -> 네이버 지도, 카카오맵, 구글맵
        1. 크롤링할 때 검색 장소가 나오지 않을 경우 -> 재검색하게 안내
        2. 크롤링할 때 검색 장소가 나왔는 데 다양하게 나올 경우 -> 유사도가 가장 높은 것 중에서 사용자가 직접 선택하게끔
    3. 추출 정보: 장소 이름, 유형, 지역, 영업시간, 휴무일, 비고, 링크 등
3. 구글 스프레드시트 갱신하기
    1. Wanna Do, 최근 방문일, 만족도는 직접 수정
    2. 그 외 나머지는 자동적으로 갱신
4. 봇으로 네이버, 구글 로그인하기
5. 네이버, 구글 지도에 장소 저장하기
    1. 저장할 때 유형별로 나눠서 저장하기
    2. 구글맵은 라벨 지정하면 될 듯

pip install gspread
pip install selenium
pip install webdriver_manager
pip install scikit-learn
pip install konlpy

tf-idf 이용 한글 문장 유사도 검사 완료하기
https://velog.io/@dy6578ekdbs/NLP-%EB%AC%B8%EC%9E%A5-%EC%9C%A0%EC%82%AC%EB%8F%84-%EC%B8%A1%EC%A0%95-%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4-%EA%B2%80%EC%B6%9C#1-%EC%A0%84%EC%B2%98%EB%A6%AC--%ED%86%A0%ED%81%B0%ED%99%94--%EC%9E%84%EB%B2%A0%EB%94%A9-%EA%B3%BC%EC%A0%95-%ED%9B%84%EB%B3%B4-%EB%AC%B8%EC%9E%A5

web driver에서 장소 검색 하나씩 클릭해서 정보 추출 준비까지