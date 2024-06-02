from scrapStats import get_news, get_data, write_to_db, get_сurrent_data, get_all_data_db
from datetime import date
import locale

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(get_all_data_db(date(2024, 4,30)))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
