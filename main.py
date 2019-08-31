from vac_parser import request_to_hh, input_params, page_parser
from vacancy_db import show_db, clear_db, show_fresh


if __name__ == '__main__':
    docs = request_to_hh(input_params())
    page_parser(docs)
    show_db()
    show_fresh()
    #clear_db()