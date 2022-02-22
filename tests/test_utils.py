from core.util import paginate


class TestDabaseFunctionality:
    """
    Test the API requests functions.
    """

    # create a list of 20 items
    sample_list = list(range(20))

    def test_paginate_std(self):
        """
        test pagination with standard slice param.
        """
        pages = list(paginate(self.sample_list))

        assert len(pages) == 4
        assert len(pages[0]) == 5

    def test_paginate_custom(self):
        """
        test pagination with ustom slice param.
        """
        pages = list(paginate(self.sample_list, 10))

        assert len(pages) == 2
        assert len(pages[0]) == 10
