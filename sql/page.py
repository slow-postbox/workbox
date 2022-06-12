from math import ceil

ITEM_PER_PAGE = 20


def get_max_page(session, model, filters) -> int:
    length = session.query(model).filter(filters).count()
    return ceil(length / ITEM_PER_PAGE)


def get_page(session, model, filters, page: int) -> list:
    return session.query(model).filter(filters) \
        .offset(ITEM_PER_PAGE * (page - 1)).limit(ITEM_PER_PAGE).all()
