"""
Temp file for testing when there's no node registry.
Remove from completed project.
"""

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--id", type=int, required=True)
parser.add_argument("--port", type=int, required=True)
parser.add_argument("--ip", type=str, required=True)

args = parser.parse_args()

port: int = args.port
ip: str = args.ip
id: int = args.id
