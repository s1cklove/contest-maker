from src.fulfill_form import fulfill_form
from src.create_executors import executors

fulfill_form()
# connect_form_to_sheet()

with open("../assets/active.txt", "w") as f:
    f.write(executors['spreadsheet'].id)

print(f"Form URL: {executors['form'].url}")
print(f"Spreadsheet URL: {executors['spreadsheet'].url}")
