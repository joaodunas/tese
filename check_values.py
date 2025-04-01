#open /results/or_bench/llama3_3_70b_judge/OR_bench_codellama.json

import json

with open('results/or_bench/llama3_3_70b_judge/OR_bench_llama2.json', 'r') as f:
    data = json.load(f)

#falses= not refusal, trues= refusal

def get_refusal_acceptance_rate(data):
    num_entries=len(data)
    num_falses=0
    num_trues=0
    for i in data.keys():
        for j in data[i].keys():
            if data[i][j]['role'] == 'assistant':
                if data[i][j]['scores'][0]['score_value'] == "False":
                    num_falses += 1
                else:
                    num_trues += 1
    return num_falses/num_entries, num_trues/num_entries

print(f'Refusal rate_llama2: {get_refusal_acceptance_rate(data)[1]}')
print(f'Acceptance rate_llama2: {get_refusal_acceptance_rate(data)[0]}')

with open('results/or_bench/llama3_3_70b_judge/OR_bench_codellama.json', 'r') as f:
    data = json.load(f)

print(f'Refusal rate_codellama: {get_refusal_acceptance_rate(data)[1]}')
print(f'Acceptance rate_codellama: {get_refusal_acceptance_rate(data)[0]}')

