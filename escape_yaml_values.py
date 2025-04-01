import os
import re
import argparse
import sys


def process_yaml_file(input_file_path, output_file_path, indent_spaces=2, scalar_style='|'):
    """
    Process a YAML file to properly escape special characters in value fields
    using a text-based approach.
    
    Args:
        input_file_path: Path to the input YAML file
        output_file_path: Path to write the processed YAML file
        indent_spaces: Number of spaces to indent content (default: 2)
        scalar_style: YAML scalar style to use ('|' for literal, '>' for folded)
    """
    # Validate scalar style
    if scalar_style not in ['|', '>']:
        print(f"Error: Invalid scalar style '{scalar_style}'. Must be '|' or '>'.")
        sys.exit(1)
    
    # Read the original YAML file as text
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file {input_file_path}: {str(e)}")
        sys.exit(1)
    
    # Regular expression to find 'value:' fields
    pattern = r'(\s+value:)\s*(\'|\")?(.*?)(\2|$)(?=\s+\-\s+name:|\s*$)'
    
    def replace_value(match):
        indent = match.group(1)  # The indentation + "value:"
        quote_type = match.group(2) or ""  # Quote type (' or ") or empty
        value = match.group(3)  # The actual value content
        
        # Calculate the base indentation (spaces before "value:")
        base_indent = ' ' * (len(indent) - len('value:'))
        content_indent = base_indent + ' ' * indent_spaces  # Customizable indentation
        
        # Replace the quoted value with a block scalar
        result = f"{indent} {scalar_style}"
        
        # Process each line in the value, maintaining proper indentation
        for line in value.split('\\n'):
            # Add each line with proper indentation
            result += f"\n{content_indent}{line}"
        
        return result
    
    # Apply the substitution
    modified_content = re.sub(pattern, replace_value, content, flags=re.DOTALL)
    
    # Write the processed content to the output file
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        return True
    except Exception as e:
        print(f"Error writing to file {output_file_path}: {str(e)}")
        return False


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Process YAML files to properly escape special characters in value fields.'
    )
    
    # Add arguments
    parser.add_argument('input_file', help='Path to the input YAML file')
    parser.add_argument(
        '-o', '--output-file', 
        help='Path to write the processed YAML file (default: input_file_escaped.yaml)'
    )
    parser.add_argument(
        '-i', '--indent', type=int, default=2,
        help='Number of spaces to indent content (default: 2)'
    )
    parser.add_argument(
        '-s', '--style', choices=['|', '>'], default='|',
        help="YAML scalar style to use: '|' for literal (preserves newlines), '>' for folded (default: '|')"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set output file path if not provided
    if not args.output_file:
        base, ext = os.path.splitext(args.input_file)
        args.output_file = f"{base}_escaped{ext}"
    
    # Process the file
    if not os.path.exists(args.input_file):
        print(f"Error: {args.input_file} does not exist.")
        sys.exit(1)
    
    success = process_yaml_file(
        args.input_file, 
        args.output_file, 
        args.indent, 
        args.style
    )
    
    if success:
        print(f"Processed YAML file has been written to {args.output_file}")
    else:
        print("Failed to process YAML file. See error above.")
        sys.exit(1)


if __name__ == "__main__":
    main() 