from vac_parser import request_to_hh, input_params, page_parser
from vacancy_db import create_csv_db, save_to_db, show_db


if __name__ == '__main__':
    docs = request_to_hh(input_params())
    page_parser(docs)
    show_db()