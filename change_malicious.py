#load datasets/rmc_bench.json

import json

with open('datasets/rmc_bench.json', 'r') as f:
    rmc_bench = json.load(f)

print(rmc_bench)

#make a dictionary with the following structure:
# {
#     "Id": id,
#     "Prompt": prompt,
# }

rmc_bench_dict = {}

#now go entry by entry in rmc_bench and add to the dictionary only the entries with 'category' == 'text-to-code' and 'level' == 1 
for entry in rmc_bench:
    if entry['category'] == 'text-to-code' and entry['level'] == 1:
        rmc_bench_dict[entry['pid']] = entry['prompt']

print(rmc_bench_dict)

# Transform the dictionary into a list of dictionaries with the desired structure
# Replace "a code" with "python code" in each prompt
formatted_data = [
    {
        "Id": pid, 
        "Prompt": prompt.replace("a code", "python code")
    } 
    for pid, prompt in rmc_bench_dict.items()
]

# Save the formatted data to the JSON file
with open('datasets/malicious_goals.json', 'w') as f:
    json.dump(formatted_data, f)
    