from abc import ABC, abstractmethod
from typing import Iterable, Dict

from lib.segment_name_provider import SegmentNameProvider, UsersSegmentNameProvider


class SegmentNameProviderFactory(ABC):
    @abstractmethod
    def get_segment_name_provider(self, dimensions: Iterable) -> SegmentNameProvider:
        pass


class UsersSegmentNameProviderFactory(SegmentNameProviderFactory):
    def __init__(self, provider_map: Dict[str, SegmentNameProvider]):
        self.provider_map = provider_map

    def get_segment_name_provider(self, dimensions: Iterable):
        try:
            providers = [self.provider_map[dim] for dim in dimensions]
            return UsersSegmentNameProvider(providers)
        except KeyError as ex:
            raise NotImplementedError(f'There is no provider for dimension {ex.args[0]}')
