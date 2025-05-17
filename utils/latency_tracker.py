def average_latency(latencies):
    if not latencies:
        return 0

    return round(sum(latencies) / len(latencies), 6)