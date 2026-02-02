import time

# Sample Data: 20 records derived from the XML parsing
transactions_list = [
    {"id": i, "transaction_ref": f"REF{i}", "amount": 1000 + i} 
    for i in range(1, 21)
]

# Dictionary Lookup Preparation: Mapping ID to the transaction object
transactions_dict = {t['id']: t for t in transactions_list}

def linear_search(data_list, target_id):
    """Scan through the list one by one."""
    for item in data_list:
        if item["id"] == target_id:
            return item
    return None

def dictionary_lookup(data_dict, target_id):
    """Find by key using hash map."""
    return data_dict.get(target_id)

# --- Efficiency Measurement ---
target = 20

# Measure Linear Search
start_time = time.perf_counter()
linear_search(transactions_list, target)
end_linear = time.perf_counter() - start_time

# Measure Dictionary Lookup
start_time = time.perf_counter()
dictionary_lookup(transactions_dict, target)
end_dict = time.perf_counter() - start_time

print(f"Linear Search Time:     {end_linear:.10f} seconds")
print(f"Dictionary Lookup Time: {end_dict:.10f} seconds")
