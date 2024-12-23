import struct
import yaml
import argparse

class Assembler:
    def __init__(self, source_file, binary_file, log_file):
        self.source_file = source_file
        self.binary_file = binary_file
        self.log_file = log_file

    def assemble(self):
        with open(self.source_file, 'r') as f:
            lines = f.readlines()

        binary_data = bytearray()
        log_entries = []

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 3:
                continue

            command, b, c = parts[0], int(parts[1]), int(parts[2])

            if command == "LOAD":
                opcode = 1
                instruction = struct.pack("<Q", (opcode << 60) | (b << 32) | c)
            elif command == "READ":
                opcode = 12
                instruction = struct.pack("<Q", (opcode << 60) | (b << 32) | c)
            elif command == "WRITE":
                opcode = 15
                d = int(parts[3]) if len(parts) > 3 else 0
                instruction = struct.pack("<Q", (opcode << 60) | (b << 32) | (c << 6) | d)
            elif command == "ABS":
                opcode = 13
                instruction = struct.pack("<Q", (opcode << 60) | (b << 32) | c)
            else:
                raise ValueError(f"Unknown command: {command}")

            binary_data.extend(instruction)

            log_entries.append({
                'command': command,
                'A': opcode,
                'B': b,
                'C': c,
                'D': parts[3] if len(parts) > 3 else None
            })

        with open(self.binary_file, 'wb') as f:
            f.write(binary_data)

        with open(self.log_file, 'w') as f:
            yaml.dump(log_entries, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler for UVM")
    parser.add_argument("--source_file", required=True, help="Path to the source file")
    parser.add_argument("--binary_file", required=True, help="Path to the binary file")
    parser.add_argument("--log_file", required=True, help="Path to the log file")
    args = parser.parse_args()

    assembler = Assembler(args.source_file, args.binary_file, args.log_file)
    assembler.assemble()

    with open(args.binary_file, 'rb') as f:
        binary_data = f.read()

    print("Contents of the binary file:")
    print(" ".join(f"{byte:02X}" for byte in binary_data))


# python assembler.py --source_file=main.asm --binary_file=out.bin --log_file=log.yaml
# python interpreter.py --binary_file=out.bin --result_file=res.yaml --memory_range=0:16
