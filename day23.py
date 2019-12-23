import asyncio
import logging
from dataclasses import dataclass
from typing import List

from intcode import IntcodeComputer

logging.basicConfig(level=logging.INFO)


@dataclass(frozen=True)
class Packet:
    address: int
    x: int
    y: int


class NIC:
    def __init__(self, address: int, network_queue: asyncio.Queue):
        self.address = address
        self.partial_packet = []
        self.input = asyncio.Queue()
        self.network_queue = network_queue
        self.computer = IntcodeComputer(
            'day23.txt', self.get_input, self.put_output)

        self.input.put_nowait(address)

    async def run(self):
        logging.debug(f'NIC[%d] started', self.address)
        try:
            await self.computer.execute()
        except KeyboardInterrupt:
            logging.debug('NIC[%d] interrupted, halting.', self.address)

    async def get_input(self):
        if self.input.empty():
            await asyncio.sleep(.01)
            return -1
        else:
            value = await self.input.get()
            logging.debug('NIC[%d] input %s', self.address, value)
            return value

    async def put_output(self, value):
        self.partial_packet.append(value)
        if len(self.partial_packet) == 3:
            packet = Packet(
                self.partial_packet[0], self.partial_packet[1], self.partial_packet[2])
            self.partial_packet = []

            logging.debug('NIC[%d] output: %r', self.address, packet)
            await self.network_queue.put(packet)


class NetworkController:
    def __init__(self, number_of_nics: int):
        self.network_queue = asyncio.Queue()
        self.nics = {}
        for address in range(number_of_nics):
            self.nics[address] = NIC(address, self.network_queue)

    async def run(self):
        nic_tasks = [
            asyncio.create_task(nic.run())
            for nic in self.nics.values()
        ]

        await self.packet_handler()

        for task in nic_tasks:
            task.cancel()

    async def packet_handler(self):
        logging.debug('Packet Handler started')
        while True:
            packet = await self.network_queue.get()

            if packet.address == 255:
                logging.info(
                    'Part 1: y-value sent to address 255 = %d', packet.y)
                break

            elif packet.address in self.nics:
                logging.debug('Packet to known target: %r', packet)
                nic = self.nics[packet.address]
                await nic.input.put(packet.x)
                await nic.input.put(packet.y)

            else:
                logging.debug('Packet to unknown target: %r', packet)


async def part1():
    controller = NetworkController(50)
    await controller.run()

asyncio.run(part1())
