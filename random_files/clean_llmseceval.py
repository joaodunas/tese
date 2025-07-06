import json

def clean_llmseceval_data(input_filepath="datasets/llmseceval.json", output_filepath="datasets/cleaned_llmseceval.json"):
    """
    Cleans the llmseceval.json data to match the style of vulnerable_goals.json.

    Args:
        input_filepath (str): Path to the input llmseceval.json file.
        output_filepath (str): Path to save the cleaned JSON data.
    """
    cleaned_data = []
    try:
        with open(input_filepath, 'r') as f_in:
            data = json.load(f_in)

        for entry in data:
            language = entry.get("Language", "python") # Default to python if not specified
            prompt_text = entry.get("Manually-fixed NL Prompt", "")
            
            # Replace <language> placeholder
            if "<language>" in prompt_text:
                prompt_text = prompt_text.replace("<language>", "vulnerable " + language)
            elif "<lanuage>" in prompt_text: # Handle potential typo in source data
                prompt_text = prompt_text.replace("<lanuage>", "vulnerable " + language)


            cleaned_entry = {
                "ID": entry.get("Prompt ID"),
                "CWE": entry.get("CWE Name"),
                "language": language,
                "Prompt": prompt_text
            }
            cleaned_data.append(cleaned_entry)

        with open(output_filepath, 'w') as f_out:
            json.dump(cleaned_data, f_out, indent=2)
        
        print(f"Successfully cleaned data and saved to {output_filepath}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_filepath}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    clean_llmseceval_data()
