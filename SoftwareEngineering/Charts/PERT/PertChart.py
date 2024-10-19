import json
import math
import queue
from abc import abstractmethod


class TimeEstimations:
    def __init__(self, optimistic, likely, pessimistic):
        self.optimistic = optimistic
        self.likely = likely
        self.pessimistic = pessimistic


class PertNode:
    def __init__(self, name: str, duration: int,
                 connections: list["PertNode"],
                 times: TimeEstimations):

        self.name = name
        self.duration = duration

        self.connections = connections

        """
        Add self as a reversed connection to all following nodes in the connection
        """
        for c in self.connections:
            c.add_reversed_connection(self)

        self.reversed_connections: list["PertNode"] = []

        self.times = times

    def add_reversed_connection(self, other):
        self.reversed_connections.append(other)

    def get_name(self) -> str:
        return self.name

    def get_duration(self) -> int:
        return self.duration

    def esd(self):
        """
        Calculate 'earliest start date' for this task

        :return:
        """
        highest = 0

        for c in self.reversed_connections:
            highest = max(highest, c.esd()+c.get_duration())

        return highest

    def led(self):
        """
        Calculate 'latest start date' for this task

        :return:
        """

        if len(self.connections) == 0:
            return self.esd()+self.duration

        lowest = math.inf
        for c in self.connections:
            lowest = min(lowest, c.led()-c.get_duration())

        return lowest


class PertChart:
    def __init__(self, start_node, end_node, nodes: list[PertNode]):
        self.start_node = start_node
        self.end_node = end_node
        self.nodes = nodes

    def all_esd(self) -> list[tuple[PertNode, int]]:
        """
        method to get the earliest start date for each note

        :return:
        """

        output = []

        for n in self.nodes:
            output.append((n, n.esd()))

        return output

    def all_led(self) -> list[tuple[PertNode, int]]:
        """
        method to get the earliest start date for each note

        :return:
        """

        output = []

        for n in self.nodes:
            output.append((n, n.led()))

        return output


class ChartCreator:
    """
    Factory to create charts for project management
    """
    def __init__(self, json_file):

        with open(json_file) as f:
            self.json_data = json.load(f)

        self.node_map = {}

    def _get_node(self, node_name: str) -> PertNode:
        if node_name in self.node_map:
            return self.node_map.get(node_name)

        node_data = self.json_data["nodes"][node_name]

        duration = node_data["duration"]
        connections = [self._get_node(n) for n in node_data["connections"]]

        times = node_data["times"]

        time_estimations = TimeEstimations(times["OT"], times["LT"], times["PT"])

        node = PertNode(node_name, duration, connections, time_estimations)
        self.node_map[node_name] = node

        return node

    def create_pert_chart(self) -> PertChart:

        nodes = []
        for n in self.json_data["nodes"]:
            node = self._get_node(n)
            nodes.append(node)

        return PertChart(self.json_data["startNode"], self.json_data["endNode"], nodes)


if __name__ == "__main__":
    pert_chart = ChartCreator("example.json").create_pert_chart()

    esd_list = pert_chart.all_esd()
    for node, esd in esd_list:
        print(f"ESD: {node.get_name()} {esd}")

    print("-"*10)

    led_list = pert_chart.all_led()
    for node, led in led_list:
        print(f"LED: {node.get_name()} {led}")
