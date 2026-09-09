from unittest.mock import patch, Mock
from django.test import TestCase
from django.core.cache import cache
from Main_Api.views import encode_features, predict_group, recommend_breeds, breed_photo_url, GROUPS


class EncodeFeaturesTests(TestCase):
    def test_returns_correct_shape(self):
        features = encode_features(
            "Daily Brushing", "Frequent", "Energetic", "Easy Training", "Friendly"
        )
        self.assertEqual(features.shape, (1, 5))

    def test_unknown_category_defaults_to_zero(self):
        features = encode_features("nonsense", "Frequent", "Energetic", "Easy Training", "Friendly")
        self.assertEqual(features.iloc[0, 0], 0)


class PredictGroupTests(TestCase):
    def test_returns_one_of_the_known_groups(self):
        group = predict_group(
            encode_features("Daily Brushing", "Frequent", "Energetic", "Easy Training", "Friendly")
        )
        self.assertIn(group, GROUPS)


class RecommendBreedsTests(TestCase):
    @patch('Main_Api.views.breed_photo_url', return_value=None)
    def test_returns_breeds_from_requested_group(self, mock_photo):
        breeds = recommend_breeds("Toy Group", limit=3)
        self.assertLessEqual(len(breeds), 3)
        for breed in breeds:
            self.assertEqual(breed["group"], "Toy Group")
            self.assertIn("Breed", breed)
            self.assertIn("description", breed)

    @patch('Main_Api.views.breed_photo_url', return_value=None)
    def test_sorted_by_popularity_ascending(self, mock_photo):
        breeds = recommend_breeds("Sporting Group", limit=5)
        pops = [b["popularity"] for b in breeds]
        self.assertEqual(pops, sorted(pops))


class UformViewTests(TestCase):
    def test_get_renders_the_form(self):
        response = self.client.get('/form/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Myforms/DogForm.html')

    @patch('Main_Api.views.breed_photo_url', return_value=None)
    def test_post_renders_a_recommendation(self, mock_photo):
        response = self.client.post('/form/', {
            'name': 'Test User',
            'gfc': 'Daily Brushing',
            'sc': 'Frequent',
            'elc': 'Energetic',
            'tc': 'Easy Training',
            'dc': 'Friendly',
            'xtra': 'none',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Myforms/Result.html')
        self.assertIn('group', response.context)
        self.assertIn('breeds', response.context)
        self.assertGreater(len(response.context['breeds']), 0)


class BreedPhotoUrlTests(TestCase):
    def setUp(self):
        cache.clear()

    @patch('Main_Api.views.requests.get')
    def test_matching_breed_returns_a_photo_url(self, mock_get):
        def fake_get(url, timeout=2):
            response = Mock()
            response.raise_for_status = Mock()
            if url == 'https://dog.ceo/api/breeds/list/all':
                response.json.return_value = {'message': {'retriever': ['golden']}}
            else:
                response.json.return_value = {
                    'status': 'success',
                    'message': 'https://images.dog.ceo/breeds/retriever-golden/fake.jpg',
                }
            return response
        mock_get.side_effect = fake_get

        self.assertEqual(
            breed_photo_url('Golden Retriever'),
            'https://images.dog.ceo/breeds/retriever-golden/fake.jpg',
        )

    @patch('Main_Api.views.requests.get')
    def test_unmatched_breed_returns_none(self, mock_get):
        def fake_get(url, timeout=2):
            response = Mock()
            response.raise_for_status = Mock()
            response.json.return_value = {'message': {'retriever': ['golden']}}
            return response
        mock_get.side_effect = fake_get

        self.assertIsNone(breed_photo_url('Totally Fictional Breed'))

    @patch('Main_Api.views.requests.get')
    def test_api_failure_returns_none_not_an_exception(self, mock_get):
        mock_get.side_effect = Exception('network is down')

        self.assertIsNone(breed_photo_url('Golden Retriever'))
