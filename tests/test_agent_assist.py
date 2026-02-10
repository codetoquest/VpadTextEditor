import unittest

from agent_assist import summarize_text, extract_action_items, improve_clarity, to_bullet_points


class TestAgentAssist(unittest.TestCase):
    def test_summarize_handles_empty(self):
        self.assertEqual(summarize_text('   '), 'No content to summarize.')

    def test_extract_action_items_splits_sentences(self):
        text = 'We need to ship this release. TODO: add tests. Also update docs.'
        items = extract_action_items(text)
        self.assertIn('- [ ] We need to ship this release', items)
        self.assertIn('- [ ] TODO: add tests', items)

    def test_improve_clarity_replaces_phrases(self):
        original = 'We utilize this in order to improve quality at this point in time.'
        refined = improve_clarity(original)
        self.assertEqual(refined, 'We use this to improve quality now.')

    def test_to_bullet_points(self):
        bullets = to_bullet_points('First sentence. Second sentence!')
        self.assertEqual(bullets, '• First sentence\n• Second sentence!')


if __name__ == '__main__':
    unittest.main()
