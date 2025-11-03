import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def search_book_aladin(title):
    url = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord={title}"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    
    try:
        itemid = str(soup.find("div", {"class": "ss_book_box"})).split('>')[0].split(' ')[2][8:-1]
        
        url = f"https://www.aladin.co.kr/shop/wproduct.aspx?ItemId={itemid}"
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
    except Exception as e:
        return 0
    
    try:
        book_title = title
        # book_title = soup.find("span", {"class": "Ere_bo_title"})
        book_info = soup.find_all("a", {"class": "Ere_sub2_title"})
        book_author = book_info[0].text
        book_publisher = book_info[-1].text if not book_info[-1].text.startswith("원제") else book_info[-2].text

        book_categories = soup.find(id = "ulCategory").text.strip().split("접기")[:-1]
        cat_set = set()
        for cat in book_categories:
            cat_set.add(cat.split(">")[1].strip())
        cat_set.discard("추천도서")

        return {
            'source': '알라딘',
            'title': book_title,
            'author': book_author,
            'publisher': book_publisher,
            'category': cat_set
        }
    except Exception as e:
        return {
            'source': '알라딘',
            'title': None,
            'author': None,
            'publisher': None,
            'category': None,
            'error': f"알라딘에서 정보를 찾을 수 없습니다. 에러: {e}"
        }

def save_to_csv(data, filename="book_info.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"CSV 파일이 저장되었습니다: {filename}")

def main():
    searching_lst = []
    while(True):
        book_title = input("검색할 책 제목을 입력하세요: ").strip()

        if not book_title:
            break

        searching_lst.append(book_title)
    
    results = []
    for title in searching_lst:
        # 알라딘 검색
        print("\n[알라딘 검색 중...]")
        aladin_result = search_book_aladin(title)
        results.append(aladin_result)
        
    # 결과 출력
    for result in results:
        for k, v in result.items():
            print(f"{k}: {v}")
        print("--- --- ---")

if __name__ == "__main__":
    main()