class Place:
    place_name: str = "" # 장소 이름
    place_type: str = "" # 장소 유형
    place_location: str = "" # 장소 주소
    place_work_time: str = "" # 장소 영업시간
    place_break_day: str = "" # 장소 휴무일
    place_note: str = "" # 장소 비고
    place_link: str = "" # 장소 검색 url

    def __init__(self, place_name = "", place_type = "", place_location = "", place_work_time = "", place_break_day = "", place_note = "", place_link = "") -> None:
        self.place_name = place_name
        self.place_type = place_type
        self.place_location = place_location
        self.place_work_time = place_work_time
        self.place_break_day = place_break_day
        self.place_note = place_note
        self.place_link = place_link
    
    def get_data(self):
        return [self.place_name, self.place_type, self.place_location, self.place_work_time, self.place_break_day, self.place_note, self.place_link]