import sys
import re
from enum import Enum


class State(Enum):
    NONE = 0
    NAME = 1
    DESC = 2
    EXITS = 3


EXITSTRINGS = [
    "[38;5;231m The only obvious exits are",
    "[38;5;231m Obvious exits are",
]


def isexit(line):
    for ex in EXITSTRINGS:
        if line.startswith(ex):
            return True
    return False


def cleanline_before(line):
    res = re.sub(r"[\n ]+", " ", line).strip()
    return res


def cleanline_after(line):
    res = re.sub(r"\[\d+;\d+;\d+m", "", line).strip()
    res = re.sub(r"\[0m", "", res).strip()
    return res


data = sys.argv[1]

data = data.split("\x1b")

state = State.NONE

name = []
desc = []
exits = []

for line in data:
    line = cleanline_before(line)
    if line.startswith("[38;5") and state == State.NONE:
        state = State.NAME
        name = [cleanline_after(line)]
    elif line.startswith("[0m") and state == State.NAME:
        state = State.DESC
        desc = [cleanline_after(line)]
    elif isexit(line) and state == State.DESC:
        state = State.EXITS
        exits = [cleanline_after(line)]
    else:
        if state == State.NAME:
            name += [cleanline_after(line)]
        if state == State.DESC:
            desc += [cleanline_after(line)]
        if state == State.EXITS:
            exits += [cleanline_after(line)]

exits = "".join(exits)
for ex in EXITSTRINGS:
    exits = exits.replace(cleanline_after(ex), "")
exits = exits.replace(", and ", ", ").replace(" and ", ", ")
exits = exits.replace(", ", "=")
exits = exits.replace(".", "").strip()


print("".join(name))
print("".join(desc))
print(exits)

with open("out.txt", "w") as o:
    o.write("-".join(sys.argv))
