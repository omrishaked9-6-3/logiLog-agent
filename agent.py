# Loglog Agent - Main Runner (agent.py)

from log_reader import read_log_file, split_to_blocks
#from gpt_interpreter import interpret_block
from interpreter import interpret_block
from report_writer import write_report
from config import LOG_PATH, BLOCK_SIZE, OUTPUT_DIR
from pathlib import Path
from datetime import datetime
import os

def run_loglog():
    print("[🔍] Reading log file...")
    log_lines = read_log_file(LOG_PATH)

    print(f"[🔀] Splitting log into blocks of {BLOCK_SIZE} lines...")
    blocks = split_to_blocks(log_lines, BLOCK_SIZE)

    all_alerts = []
    print(f"[🤖] Interpreting {len(blocks)} blocks with GPT...")
    for idx, block in enumerate(blocks):
        print(f"  → Interpreting block {idx+1}/{len(blocks)}")
        alerts = interpret_block(block)
        all_alerts.extend(alerts)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = os.path.join(OUTPUT_DIR, f"report_{timestamp}.json")

    print(f"[💾] Writing report to {out_file}")
    write_report(all_alerts, out_file)
    print("[✅] Loglog completed.")

if __name__ == "__main__":
    run_loglog()