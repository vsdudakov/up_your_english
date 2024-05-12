import asyncio
import typing as tp
from abc import abstractmethod


class BusAdapter:
    @abstractmethod
    async def up(self) -> None:
        ...

    @abstractmethod
    async def healthcheck(self) -> bool:
        ...

    @abstractmethod
    async def down(self) -> None:
        ...


class Bus:
    adapters: list[BusAdapter]

    def __init__(self) -> None:
        self.adapters = []

    def register_adapter(self, adapter: BusAdapter) -> None:
        self.adapters.append(adapter)

    def get_adapter(self, adapter_class: type[BusAdapter]) -> tp.Any:
        for adapter in self.adapters:
            if isinstance(adapter, adapter_class):
                return adapter
        raise ValueError(f"Adapter {adapter_class} not found")

    async def up(self) -> None:
        await asyncio.gather(*(adapter.up() for adapter in self.adapters))

    async def healthcheck(self) -> bool:
        return all(await asyncio.gather(*(adapter.healthcheck() for adapter in self.adapters)))

    async def down(self) -> None:
        await asyncio.gather(*(adapter.down() for adapter in self.adapters))


class Service:
    bus: Bus

    def __init__(self, bus: Bus) -> None:
        self.bus = bus
