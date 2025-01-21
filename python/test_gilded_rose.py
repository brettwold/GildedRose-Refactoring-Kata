# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose
from python.gilded_rose import AGED_BRIE, BACKSTAGE_PASSES, CONJURED, SULFURAS


class GildedRoseTest(unittest.TestCase):
    # General tests
    def test_check_fields(self):
        items = [Item("Anything", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Anything", items[0].name)

    def test_quality_is_set(self):
        items = [Item("Anything", 10, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(49, items[0].quality)

    # This checks that items created with quality over 50 get set to 50, as in reqs it does state that the
    # "quality of an item can never be more than 50"
    def test_quality_reduced_to_max(self):
        items = [Item("Anything", 10, 60)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(49, items[0].quality)

    def test_quality_decreases(self):
        items = [Item("Anything", 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)

    def test_quality_decreases_twice_as_fast_after_sell_by(self):
        items = [Item("Anything", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(8, items[0].quality)

    def test_quality_never_negative(self):
        items = [Item("Anything", 10, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_sell_in_reduces_for_normal_items(self):
        items = [Item("Anything", 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)

    # Brie tests
    def test_quality_increases_for_brie(self):
        items = [Item(AGED_BRIE, 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(11, items[0].quality)

    def test_sell_in_reduces_for_brie(self):
        items = [Item(AGED_BRIE, 10, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)

    def test_quality_increases_twice_as_fast_for_aged_brie_past_sell_by(self):
        items = [Item(AGED_BRIE, 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(12, items[0].quality)

    def test_quality_never_more_than_50_for_brie(self):
        items = [Item(AGED_BRIE, 0, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)

    # Backstage passes tests
    def test_quality_increases_for_backstage_passes(self):
        items = [Item(BACKSTAGE_PASSES, 11, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(11, items[0].quality)

    def test_quality_increases_twice_as_fast_for_backstage_passes_at_10_days(self):
        items = [Item(BACKSTAGE_PASSES, 10, 25)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(27, items[0].quality)

    def test_quality_increases_by_three_for_backstage_passes_at_5_days(self):
        items = [Item(BACKSTAGE_PASSES, 5, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(13, items[0].quality)

    def test_quality_drops_to_zero_after_concert(self):
        items = [Item(BACKSTAGE_PASSES, 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_quality_never_more_than_50_for_backstage_passes(self):
        items = [Item(BACKSTAGE_PASSES, 10, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)

    def test_sell_in_reduces_for_backstage_passes(self):
        items = [Item(BACKSTAGE_PASSES, 10, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)

    # Conjured tests
    def test_sell_in_reduces_for_conjured_items(self):
        items = [Item(CONJURED, 10, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(9, items[0].sell_in)

    def test_conjured_items_degrade_twice_as_fast(self):
        items = [Item(CONJURED, 3, 6)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(4, items[0].quality)

    def test_quality_never_negative_for_conjured_items(self):
        items = [Item(CONJURED, 10, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_quality_reduces_twice_as_fast_after_sell_by_for_conjured_items(self):
        items = [Item(CONJURED, 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(6, items[0].quality)

    # Sulfuras tests
    def test_sulfuras_never_changes(self):
        items = [Item(SULFURAS, 10, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(80, items[0].quality)
        self.assertEqual(10, items[0].sell_in)

    def test_sulfuras_always_quality_80(self):
        items = [Item(SULFURAS, 10, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(80, items[0].quality)

    def test_sulfuras_sell_in_never_changes(self):
        items = [Item(SULFURAS, 10, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(10, items[0].sell_in)

if __name__ == '__main__':
    unittest.main()
