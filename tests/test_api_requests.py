from core.api_call import get_trending


class TestDabaseFunctionality:
    """
    Test the API requests functions.
    """

    def test_get_api_results(self):
        """
        Verifica a resposta das requisições para a API.
        """
        data = get_trending('movie', 'week', 5)

        assert data['page'] == 5
        assert type(data['results']) == list
        assert len(data['results']) == 20

        result_keys = [
            'genre_ids',
            'original_language',
            'id',
            'poster_path',
            'video',
            'vote_average',
            'overview',
            'release_date',
            'vote_count',
            'title',
            'adult',
            'backdrop_path',
            'original_title',
            'popularity',
            'media_type'
        ]
        keys_are_valid = [key in result_keys for key in data['results'][0].keys()]

        assert all(keys_are_valid)

    def test_get_api_with_invalid_page_param(self):
        """
        Verifica a resposta das requisições para a API com parâmetros inválidos.
        """
        data = get_trending('foo', 'baz', 'bar')

        assert data['success'] == False
        assert data['status_code'] == 22

    def test_get_api_with_invalid_media_param(self):
        """
        Verifica a resposta das requisições para a API com parâmetros inválidos.
        """
        data = get_trending('foo', 'baz', 1)

        assert data['success'] == False
        assert data['status_code'] == 11
