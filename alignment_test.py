# coding: utf-8
import alignment
import unittest

class TestAlignmentFunctions(unittest.TestCase):

  #def setUp(self):
  #  self.raw_segment = u"をぉぉ（感動詞,非標準表記）おお（感動詞）おって"

  def test_get_original_informal_pair(self):
    aligned_rules = alignment.rules_with_window_size(u"ということ", u"ってこと", 1)
    rules = [(u"と", u"と"),
             (u"こ", u"こ"),
             (u"う", u"て"),
             (u"い", u"っ"),
             (u"と", u"")]
    self.assertEqual(aligned_rules, rules)

  def test_alignment_two(self):
    aligned_rules = alignment.rules_with_window_size(u"かなり", u"かなぁーり", 1)
    rules = [(u"り", u"り"),
             (u"", u"ー"),
             (u"", u"ぁ"),
             (u"な", u"な"),
             (u"か", u"か")]
    self.assertEqual(aligned_rules, rules)

if __name__ == '__main__':
    unittest.main()
