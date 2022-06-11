from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Iterable, Union


@dataclass
class SegmentNameProvider(ABC):
    @abstractmethod
    def get_segment_name(self, segment_key) -> str:
        pass


class UsersSegmentNameProvider(SegmentNameProvider):
    def __init__(self, providers: List[SegmentNameProvider]) -> None:
        super().__init__()
        self.providers = providers

    def get_segment_name(self, segment_key: Union[Iterable, str, bool]) -> str:
        if type(segment_key) in (str, bool):
            segment_key = [segment_key]
        segment_names = (provider.get_segment_name(key) for key, provider in zip(segment_key, self.providers))
        segment_names = ' and '.join(segment_names)
        return 'Users ' + segment_names


class CountrySegmentNameProvider(SegmentNameProvider):
    def get_segment_name(self, segment_key: str) -> str:
        return 'from ' + segment_key.capitalize()


class IsVipSegmentNameProvider(SegmentNameProvider):
    @staticmethod
    def is_vip(is_vip: bool):
        if is_vip:
            return 'VIP'
        return 'not VIP'

    def get_segment_name(self, segment_key: bool) -> str:
        return 'who are ' + self.is_vip(segment_key)
