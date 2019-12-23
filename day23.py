import asyncio
import logging
from dataclasses import dataclass, field, replace
from typing import List

from intcode import IntcodeComputer

logging.basicConfig(level=logging.INFO)
#logging.getLogger('NetworkController').setLevel(logging.DEBUG)
#logging.getLogger('NAT').setLevel(logging.DEBUG)

logging.getLogger('intcode').setLevel(logging.INFO)

@dataclass(frozen=True)
class Packet:
    address: int
    x: int
    y: int


@dataclass
class NicState:
    partial_packet: List[int] = field(default_factory=list)
    idle_count: int = 0


class NIC:
    def __init__(self, address: int, network_queue: asyncio.Queue):
        self.address = address
        self.state = NicState()
        self.input = asyncio.Queue()
        self.network_queue = network_queue
        self.computer = IntcodeComputer(
            'day23.txt', self.get_input, self.put_output)

        self.input.put_nowait(address)

    def is_idle(self):
        return self.state.idle_count >= 0

    async def run(self):
        logging.debug('NIC[%d] started', self.address)
        try:
            await self.computer.execute()
        except KeyboardInterrupt:
            logging.debug('NIC[%d] interrupted, halting.', self.address)
        except asyncio.CancelledError:
            pass
       
        logging.debug('NIC[%d] stopped', self.address)


    async def get_input(self):
        if self.input.empty():
            await asyncio.sleep(.01)
            self.state.idle_count += 1
            return -1
        else:
            value = await self.input.get()
            logging.debug('NIC[%d] input %s', self.address, value)
            return value

    async def put_output(self, value):
        self.state.idle_count = -2
        self.state.partial_packet.append(value)
        if len(self.state.partial_packet) == 3:
            packet = Packet(
                self.state.partial_packet[0],
                self.state.partial_packet[1],
                self.state.partial_packet[2])
            self.state.partial_packet = []

            logging.debug('NIC[%d] output: %r', self.address, packet)
            await self.network_queue.put(packet)


class NetworkController:
    LOG = logging.getLogger('NetworkController')

    def __init__(self, number_of_nics: int):
        self.network_queue = asyncio.Queue()
        self.nics = {}
        for address in range(number_of_nics):
            self.nics[address] = NIC(address, self.network_queue)

    def is_network_idle(self):
        result = all(
            nic.is_idle() for nic in self.nics.values()
        )
        self.LOG.debug('is_network_idle == %r', result)
        return result

    async def handle_packet(self, packet: Packet):
        if packet.address in self.nics:
            self.LOG.debug('Packet to NIC[%d]: %r', packet.address, packet)
            nic = self.nics[packet.address]
            await nic.input.put(packet.x)
            await nic.input.put(packet.y)

        else:
            self.LOG.debug('Packet to unknown target: %r', packet)

        return True

    async def run(self):
        nic_tasks = [
            asyncio.create_task(nic.run())
            for nic in self.nics.values()
        ]

        await self.packet_handler()

        for task in nic_tasks:
            task.cancel()

    async def packet_handler(self):
        self.LOG.debug('Packet Handler started')
        while True:
            packet = await self.network_queue.get()

            if not await self.handle_packet(packet):
                break


class NAT():
    LOG = logging.getLogger('NAT')

    def __init__(self, network_controller: NetworkController):
        self.last_received = None
        self.last_sent = None
        self.network_controller = network_controller

    def is_idle(self):
        return True

    async def run(self):
        self.LOG.debug('NAT started')
        try:
            while True:
                if self.network_controller.is_network_idle():
                    if self.last_received is not None:
                        packet = replace(self.last_received, address=0)
                        self.LOG.debug(
                            'Network is idle, sending value %d to address 0', packet.y)
                        self.last_received = None
                        
                        if packet.y == self.last_sent:
                            self.LOG.info('Part2: first Y value delivered twice in a row to address 0: %d', packet.y)
                            break
                        
                        self.last_sent = packet.y
                        await self.network_controller.network_queue.put(packet)
                    else:
                        await asyncio.sleep(0)
                else:
                    self.LOG.debug('Network is not idle')
                    await asyncio.sleep(0)
        except KeyboardInterrupt:
            self.LOG.debug('NAT interrupted, halting.')
        except asyncio.CancelledError:
            pass
        
        self.LOG.debug('NAT stopped')


class NetworkControllerPart1(NetworkController):
    def __init__(self, number_of_nics: int):
        super().__init__(number_of_nics)

    async def handle_packet(self, packet):
        if packet.address == 255:
            self.LOG.info('Part 1: y-value sent to address 255 = %d', packet.y)
            return False
        else:
            return await super().handle_packet(packet)


class NetworkControllerPart2(NetworkController):
    def __init__(self, number_of_nics: int):
        super().__init__(number_of_nics)
        self.nics[255] = NAT(self)

    async def handle_packet(self, packet):
        if packet.address == 255:
            self.LOG.debug('Packet to NAT: %r', packet)
            self.nics[255].last_received = packet
            await asyncio.sleep(0)
            return True
        else:
            return await super().handle_packet(packet)


async def part1():
    controller = NetworkControllerPart1(50)
    await controller.run()


async def part2():
    controller = NetworkControllerPart2(50)
    await controller.run()

#asyncio.run(part1())
asyncio.run(part2())
