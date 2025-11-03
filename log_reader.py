def read_log_file(file_path):
    """
    Reads a log file and returns a list of non-empty lines.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def split_to_blocks(lines, block_size):
    """
    Splits a list of log lines into chunks (blocks) of given size.
    """
    return [lines[i:i + block_size] for i in range(0, len(lines), block_size)]
