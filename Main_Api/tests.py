from django.test import TestCase
from Main_Api.views import encode_features, predict_group, recommend_breeds, GROUPS


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
    def test_returns_breeds_from_requested_group(self):
        breeds = recommend_breeds("Toy Group", limit=3)
        self.assertLessEqual(len(breeds), 3)
        for breed in breeds:
            self.assertEqual(breed["group"], "Toy Group")
            self.assertIn("Breed", breed)
            self.assertIn("description", breed)

    def test_sorted_by_popularity_ascending(self):
        breeds = recommend_breeds("Sporting Group", limit=5)
        pops = [b["popularity"] for b in breeds]
        self.assertEqual(pops, sorted(pops))


class UformViewTests(TestCase):
    def test_get_renders_the_form(self):
        response = self.client.get('/form/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Myforms/DogForm.html')

    def test_post_renders_a_recommendation(self):
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
