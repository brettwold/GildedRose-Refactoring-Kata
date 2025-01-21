# -*- coding: utf-8 -*-
from enum import Enum

class ItemTypes(Enum):
    AGED_BRIE = "Aged Brie"
    BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    CONJURED = "Conjured Mana Cake"

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class SalesItem:
    """ Generic class for items in the store.
        - Quality decreases by 1 when the sell_in value is not expired
        - Quality decreases by 2 when the sell_in value is expired
        - Quality is never negative
    """
    STANDARD_DEGRADATION_RATE = 1
    MAX_ITEM_QUALITY = 50
    MIN_ITEM_QUALITY = 0

    def __init__(self, item: Item, degradation_multiplier=1):
        self.item = item
        self.degradation_rate = degradation_multiplier * self.STANDARD_DEGRADATION_RATE
        if self.item.name != ItemTypes.SULFURAS and self.item.quality >= self.MAX_ITEM_QUALITY:
            self.item.quality = self.MAX_ITEM_QUALITY

    def _below_max_quality(self):
        return self.item.quality < self.MAX_ITEM_QUALITY

    def _above_min_quality(self):
        return self.item.quality > self.MIN_ITEM_QUALITY

    def _decrease_quality(self):
        self.item.quality -= self.degradation_rate

    def _increase_quality(self):
        self.item.quality += self.degradation_rate

    def _decrease_sell_in(self):
        self.item.sell_in -= 1

    def _is_expired(self):
        return self.item.sell_in < 0

    def update_quality(self):
        self._decrease_sell_in()
        if self._above_min_quality():
            self._decrease_quality()
        if self._is_expired() and self._above_min_quality():
            self._decrease_quality()

class AgedBrie(SalesItem):
    """ Aged Brie increases in quality as it gets older.
        - Quality increases by 1 when the sell_in value is not expired
        - Quality increases by 2 when the sell_in value is expired
        - Quality is never more than 50
    """

    def update_quality(self):
        self._decrease_sell_in()
        if self._below_max_quality():
            self._increase_quality()
        if self._is_expired() and self._below_max_quality():
            self._increase_quality()

class BackstagePasses(SalesItem):
    """ Backstage passes increase in quality as the sell_in value approaches.
        - Quality increases by 2 when there are 10 days or less
        - Quality increases by 3 when there are 5 days or less
        - Quality drops to 0 after the concert
        - Quality is never more than 50
    """
    TEN_DAYS = 10
    FIVE_DAYS = 5

    def update_quality(self):
        self._decrease_sell_in()
        if self._below_max_quality():
            self._increase_quality()
            if self.item.sell_in < self.TEN_DAYS and self._below_max_quality():
                self._increase_quality()
            if self.item.sell_in < self.FIVE_DAYS and self._below_max_quality():
                self._increase_quality()
        if self._is_expired():
            self.item.quality = 0

class Sulfuras(SalesItem):
    """ Sulfuras never changes quality and never expires. """
    SULFURAS_QUALITY = 80

    def __init__(self, item: Item):
        super().__init__(item)
        # force the sulfuras quality to be 80
        self.item.quality = self.SULFURAS_QUALITY

    def update_quality(self):
        pass

class Conjured(SalesItem):
    """ Conjured items degrade in quality twice as fast as normal items. """
    def __init__(self, item: Item):
        # "Twice as fast", could be interpreted as degrading by 2 each day or twice the standard rate
        # This implementation assumes the latter
        super().__init__(item, degradation_multiplier=2)


def _get_item_wrapper(item: Item):
    match item.name:
        case ItemTypes.AGED_BRIE.value:
            return AgedBrie(item)
        case ItemTypes.BACKSTAGE_PASSES.value:
            return BackstagePasses(item)
        case ItemTypes.SULFURAS.value:
            return Sulfuras(item)
        case ItemTypes.CONJURED.value:
            return Conjured(item)
        case _:
            return SalesItem(item)

class GildedRose(object):
    """ Gilded Rose class

        Maintains the items in the store and updates their quality.

        During the update, the quality of the items is updated according to their type.
    """

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            _get_item_wrapper(item).update_quality()