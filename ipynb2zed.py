#!/usr/bin/env python3
"""
Jupyter Notebook to Python File Converter for Zed Editor REPL

This script converts a Jupyter Notebook (.ipynb) file to a Python (.py) file 
with a specific layout for use with Zed Editor's REPL functionality.

Features:
    - Each cell starts with '# %% Cell N' (where N is the cell number)
    - Markdown cells are preserved in triple-quoted docstrings containing ```md blocks
    - Code cells contain the original Python code from the notebook
    - Raw cells are preserved within docstrings
"""

import json
import sys
import argparse
from typing import TextIO


def process_code_cell(file_handle: TextIO, cell_content: str) -> None:
    """
    Process a code cell from the notebook.
    
    :param file_handle: File handle to write to
    :type file_handle: TextIO
    :param cell_content: Content of the code cell
    :type cell_content: str
    :return: None
    :rtype: None
    """
    # Write code directly
    file_handle.write(cell_content)
    if not cell_content.endswith('\n'):
        file_handle.write('\n')


def process_markdown_cell(file_handle: TextIO, cell_content: str) -> None:
    """
    Process a markdown cell from the notebook.
    
    :param file_handle: File handle to write to
    :type file_handle: TextIO
    :param cell_content: Content of the markdown cell
    :type cell_content: str
    :return: None
    :rtype: None
    """
    # Place markdown inside docstrings with ```md blocks
    file_handle.write('"""\n')
    file_handle.write("```md\n")
    file_handle.write(cell_content)
    if not cell_content.endswith('\n'):
        file_handle.write('\n')
    file_handle.write("```\n")
    file_handle.write('"""\n')


def process_raw_cell(file_handle: TextIO, cell_content: str) -> None:
    """
    Process a raw cell from the notebook.
    
    :param file_handle: File handle to write to
    :type file_handle: TextIO
    :param cell_content: Content of the raw cell
    :type cell_content: str
    :return: None
    :rtype: None
    """
    # Preserve raw cells within docstrings
    file_handle.write('"""\n')
    file_handle.write(cell_content)
    if not cell_content.endswith('\n'):
        file_handle.write('\n')
    file_handle.write('"""\n')


def write_cell(file_handle: TextIO, cell_number: int, cell_type: str, cell_content: str) -> None:
    """
    Write a cell to the output file based on its type.
    
    :param file_handle: File handle to write to
    :type file_handle: TextIO
    :param cell_number: Cell number for the marker
    :type cell_number: int
    :param cell_type: Type of the cell (code, markdown, or raw)
    :type cell_type: str
    :param cell_content: Content of the cell
    :type cell_content: str
    :return: None
    :rtype: None
    """
    # Write cell marker
    file_handle.write(f"# %% Cell {cell_number}\n")
    
    # Process cell based on type
    if cell_type == 'code':
        process_code_cell(file_handle, cell_content)
    elif cell_type == 'markdown':
        process_markdown_cell(file_handle, cell_content)
    elif cell_type == 'raw':
        process_raw_cell(file_handle, cell_content)
    
    # Add an empty line for readability
    file_handle.write('\n')


def convert_notebook_to_py(input_file: str, output_file: str) -> bool:
    """
    Convert a Jupyter Notebook file to a Python file with Zed REPL format.
    
    :param input_file: Path to input .ipynb file
    :type input_file: str
    :param output_file: Path to output .py file
    :type output_file: str
    :return: True if conversion is successful, False otherwise
    :rtype: bool
    """
    try:
        # Read the notebook file
        with open(input_file, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Extract cells
        cells = notebook.get('cells', [])
        
        # Open output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, cell in enumerate(cells):
                cell_type = cell.get('cell_type', 'code')
                cell_content = ''.join(cell.get('source', []))
                
                # Write the cell with appropriate formatting
                write_cell(f, i+1, cell_type, cell_content)
        
        print(f"Conversion completed: {input_file} → {output_file}")
        return True
    
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False


def main() -> None:
    """
    Main function to parse arguments and run the conversion.
    
    :return: None
    :rtype: None
    """
    parser = argparse.ArgumentParser(
        description='Convert Jupyter Notebook to Python file for Zed Editor REPL'
    )
    parser.add_argument('input', help='Input .ipynb file')
    parser.add_argument('output', help='Output .py file')
    
    args = parser.parse_args()
    
    success = convert_notebook_to_py(args.input, args.output)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
