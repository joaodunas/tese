import pandas as pd
import yaml

def main():
    # Read the CSV file
    df = pd.read_csv("datasets/or-bench-hard-1k.csv")
    
    # Convert DataFrame to dictionary
    data_dict = df.to_dict(orient='records')

    # Create a new dictionary with the desired structure
    new_data_dict = []
    id_counter = 0

    for item in data_dict:
        
        new_item = {
            "name": f"or-bench-hard-1k_{id_counter}",
            "value": item["prompt"],
            "data_type": "text",
            "description": "OR-bench hard 1k prompts -" + item["category"] 
        }   
        new_data_dict.append(new_item)
        id_counter += 1
    
    # Write to YAML file
    with open("datasets/or-bench-hard-1k.yaml", 'w', encoding='utf-8') as file:
        yaml.dump(new_data_dict, file, allow_unicode=True)
    
    print(data_dict)

if __name__ == "__main__":
    main()
