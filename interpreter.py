import struct
import yaml
import argparse

class Interpreter:
    def __init__(self, binary_file, result_file, memory_range):
        self.binary_file = binary_file
        self.result_file = result_file
        self.memory = [0] * 1024
        self.start, self.end = memory_range

    def execute(self):
        with open(self.binary_file, 'rb') as f:
            binary_data = f.read()

        pc = 0
        while pc < len(binary_data):
            instruction = struct.unpack_from("<Q", binary_data, pc)[0]
            pc += 8

            opcode = (instruction >> 60) & 0xF
            b = (instruction >> 32) & 0xFFFFFFF
            c = instruction & 0xFFFFFFFF

            if opcode == 1:
                self.memory[b] = c
            elif opcode == 12:
                self.memory[b] = self.memory[c]
            elif opcode == 15:
                d = instruction & 0x3F
                self.memory[self.memory[b] + d] = self.memory[c]
            elif opcode == 13:
                self.memory[b] = abs(self.memory[c])
            else:
                raise ValueError(f"Unknown opcode: {opcode}")

        self.save_result()

    def save_result(self):
        result = {}
        for i in range(self.start, self.end):
            result[f"memory[{i}]"] = self.memory[i]

        with open(self.result_file, 'w') as f:
            yaml.dump(result, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter for UVM")
    parser.add_argument("--binary_file", required=True, help="Path to the binary file")
    parser.add_argument("--result_file", required=True, help="Path to the result file")
    parser.add_argument("--memory_range", required=True, help="Memory range (start:end)")
    args = parser.parse_args()

    start, end = map(int, args.memory_range.split(":"))
    interpreter = Interpreter(args.binary_file, args.result_file, (start, end))
    interpreter.execute()
