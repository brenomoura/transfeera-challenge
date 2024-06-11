from shared.domain.repositories import SearchParams, PAGE, PAGE_SIZE


def test_valid_search_params():
    SearchParams(page=1, page_size=10)


def test_invalid_search_params():
    search_params = SearchParams(page=0, page_size=0)
    assert search_params.page == PAGE
    assert search_params.page_size == PAGE_SIZE
