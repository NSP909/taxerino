import json
import math
import numpy as np
from typing import Dict, List, Union, Any

def extract_number(value: str) -> Union[float, str]:
    """Convert string representations of numbers to float if possible."""
    if not isinstance(value, str):
        return value
    
    try:
        cleaned = value.replace('$', '').replace(',', '')
        return float(cleaned)
    except ValueError:
        return value

def process_json(obj: Any) -> Any:
    """Recursively process JSON and convert string numbers to float."""
    if not isinstance(obj, dict) and not isinstance(obj, list):
        return extract_number(obj)
    
    if isinstance(obj, list):
        return [process_json(item) for item in obj]
    
    return {key: process_json(value) for key, value in obj.items()}

def get_first_digits(numbers: List[float]) -> List[int]:
    """Extract first digits from list of numbers."""
    first_digits = []
    for num in numbers:
        if num == 0:
            continue
        str_num = str(abs(num))
        if str_num[0] == '.':
            str_num = str_num[1:]
        for digit in str_num:
            if digit.isdigit() and digit != '0':
                first_digits.append(int(digit))
                break
    return first_digits

def get_benfords_distribution() -> np.ndarray:
    """Calculate expected Benford's Law distribution."""
    return np.array([math.log10(1 + 1/d) for d in range(1, 10)])

def get_actual_distribution(first_digits: List[int]) -> np.ndarray:
    """Calculate actual distribution of first digits."""
    counts = np.zeros(9)
    for digit in first_digits:
        counts[digit - 1] += 1
    return counts / len(first_digits) if len(first_digits) > 0 else counts

def calculate_similarity(actual: np.ndarray, expected: np.ndarray) -> float:
    """Calculate cosine similarity between actual and expected distributions."""
    dot_product = np.dot(actual, expected)
    magnitude1 = np.sqrt(np.sum(actual ** 2))
    magnitude2 = np.sqrt(np.sum(expected ** 2))
    return dot_product / (magnitude1 * magnitude2) if magnitude1 * magnitude2 != 0 else 0

def extract_all_numbers(obj: Any) -> List[float]:
    """Recursively extract all numbers from processed JSON."""
    numbers = []
    
    if isinstance(obj, (int, float)):
        numbers.append(float(obj))
    elif isinstance(obj, dict):
        for value in obj.values():
            numbers.extend(extract_all_numbers(value))
    elif isinstance(obj, list):
        for item in obj:
            numbers.extend(extract_all_numbers(item))
            
    return numbers

def analyze_benfords_law(data: Dict) -> Dict:
    """Analyze JSON data and compare with Benford's Law."""
    processed_data = process_json(data)
    numbers = extract_all_numbers(processed_data)
    first_digits = get_first_digits(numbers)
    actual_dist = get_actual_distribution(first_digits)
    expected_dist = get_benfords_distribution()
    similarity = calculate_similarity(actual_dist, expected_dist)
    
    return {
        'processed_data': processed_data,
        'numbers_found': numbers,
        'first_digits': first_digits,
        'actual_distribution': actual_dist.tolist(),
        'expected_distribution': expected_dist.tolist(),
        'similarity_score': similarity
    }

if __name__ == "__main__":
    input_file = "info.json"  # Change this to your JSON file path
    
    with open(input_file, "r") as file:
        data = json.load(file)
    
    results = analyze_benfords_law(data)
    
    print("\nProcessed Data:")
    print(json.dumps(results['processed_data'], indent=2))
    
    print("\nNumbers found:", results['numbers_found'])
    print("First digits:", results['first_digits'])
    print("\nActual Distribution:", results['actual_distribution'])
    print("Expected Distribution:", results['expected_distribution'])
    print("Similarity Score:", results['similarity_score'])
