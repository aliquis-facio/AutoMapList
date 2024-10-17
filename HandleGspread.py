import gspread

# authorize gspread service account
json_file_path = "wanna-go-place-list-automation-1635b10f855f.json"
gc = gspread.service_account(json_file_path)

# select handled gspread
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1dhDXlOlGUdKXBTgZMcRVd8MoRnhHyppXcsRpyst0-F4/edit?gid=0#gid=0"
doc = gc.open_by_url(spreadsheet_url)

