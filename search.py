# CS 411 - Assignment 3 Starter Code
# Iteratie Deepening Search on 15 Puzzle
# Name: Duc Tran, UIN: 679876782
# Spring 2024

import random
import math
import time
import psutil
import os
from collections import deque
import sys


# This class defines the state of the problem in terms of board configuration
class Board:
    def __init__(self, tiles):
        self.size = int(math.sqrt(len(tiles)))  # defining length/width of the board
        self.tiles = tiles

    # This function returns the resulting state from taking particular action from current state
    def execute_action(self, action):
        new_tiles = self.tiles[:]
        empty_index = new_tiles.index('0')
        if action == 'L':
            if empty_index % self.size > 0:
                new_tiles[empty_index - 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index - 1]
        if action == 'R':
            if empty_index % self.size < (self.size - 1):
                new_tiles[empty_index + 1], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[empty_index + 1]
        if action == 'U':
            if empty_index - self.size >= 0:
                new_tiles[empty_index - self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index - self.size]
        if action == 'D':
            if empty_index + self.size < self.size * self.size:
                new_tiles[empty_index + self.size], new_tiles[empty_index] = new_tiles[empty_index], new_tiles[
                    empty_index + self.size]
        return Board(new_tiles)


# This class defines the node on the search tree, consisting of state, parent and previous action
class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    # Returns string representation of the state
    def __repr__(self):
        return str(self.state.tiles)

    # Comparing current node with other node. They are equal if states are equal
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

    def __hash__(self):
        return hash(tuple(self.state.tiles))

class Search:

    # Utility function to randomly generate 15-puzzle
    def generate_puzzle(self, size):
        numbers = list(range(size * size))
        random.shuffle(numbers)
        return Node(Board(numbers), None, None)

    # This function returns the list of children obtained after simulating the actions on current node
    def get_children(self, parent_node):
        children = []
        actions = ['L', 'R', 'U', 'D']  # left,right, up , down ; actions define direction of movement of empty tile
        for action in actions:
            child_state = parent_node.state.execute_action(action)
            child_node = Node(child_state, parent_node, action)
            children.append(child_node)
        return children

    # This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
    def find_path(self, node):
        path = []
        while (node.parent is not None):
            path.append(node.action)
            node = node.parent
        path.reverse()
        return path
    
    # This function get the depth of any nodes by backtracking and counting the number of parents
    def get_depth(self, node):
        depth = 0
        while (node.parent is not None):
            depth += 1
            node = node.parent
        return depth

    # This function checked for a cycle in a node
    def cycle_check(self, node):
        hashset = set()
        hashset.add(str(node.__hash__()))
        temp_hash_string = ""
        while (node.parent is not None):
            node = node.parent
            temp_hash_string = str(node.__hash__())
            if (temp_hash_string in hashset):
                return True
            hashset.add(temp_hash_string)
        return False
            
    # This function run depth_limited_search from 0 to inf in order to search the 16-puzzle
    def ids(self, root_node):
        depth_lim = 0
        result = "Failure"
        while result == "Failure" or result == "Cutoff": 
            result = self.run_depth_limited_search(root_node, depth_lim)
            depth_lim += 1
        return result

    # This function searching for goal states with depth_limit as a limit parameter for function to stop
    def run_depth_limited_search(self, root_node, depth_limit):
        start_time = time.time()
        frontier = deque([root_node])
        result = "Failure"
        max_memory = 0
        explored = set()
        while (len(frontier) > 0):
            max_memory = max(max_memory, sys.getsizeof(frontier) + sys.getsizeof(explored))
            cur_node = frontier.pop()
            explored.add(cur_node)
            if (self.goal_test(cur_node.state.tiles)):
                path = self.find_path(cur_node)
                end_time = time.time()
                result = "Solved"
                return path, len(explored), (end_time - start_time), max_memory
            if self.get_depth(cur_node) > depth_limit:
                result = "Cutoff"
            elif not self.cycle_check(cur_node):
                for child in self.get_children(cur_node):
                    frontier.append(child)
        return result
    

    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def solve(self, input):

        initial_list = input.split(" ")
        root = Node(Board(initial_list), None, None)
        

        path, expanded_nodes, time_taken, memory_consumed = self.ids(root)
        print("Moves: " + " ".join(path))
        print("Number of expanded Nodes: " + str(expanded_nodes))
        print("Time Taken: " + str(time_taken))
        print("Max Memory (Bytes): " + str(memory_consumed))
        return "".join(path)

if __name__ == '__main__':
    agent = Search()
    agent.solve("1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15")