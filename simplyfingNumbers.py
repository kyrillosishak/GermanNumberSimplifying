import re
import math

def simplify_numbers(raw_text):
    """
    Simplifies numbers in text according to specified rules.

    Args:
        raw_text (str): Input text containing numbers to simplify

    Returns:
        str: Text with simplified numbers
    """

    def round_to_nearest_magnitude(number):
        """Helper function to round to nearest nice number"""
        if number < 1000:
            return round(number, -2)
        elif number < 100000:
            return round(number, -3)
        else:
            return round(number, -3)

    def format_number(number_str):
        """Convert number string to float, handling German number format"""
        # Remove thousand separators and convert decimal comma to point
        clean_num = number_str.replace('.', '').replace(',', '.')
        return float(clean_num)

    def simplify_percentage(percentage):
        """Convert percentage to descriptive text"""
        percentage = float(percentage)
        if percentage == 25:
            return "jeder Vierte"
        elif percentage == 50:
            return "die Hälfte"
        elif percentage == 75:
            return "drei von vier"
        elif percentage >= 90:
            return "fast alle"
        elif percentage >= 60:
            return "mehr als die Hälfte"
        elif percentage <= 15:
            return "wenige"
        return f"etwa {round(percentage)} Prozent"

    def should_simplify_number(number_str, context=""):
        """Determine if a number should be simplified based on context"""
        # Don't simplify years in dates or in year-specific contexts
        if re.match(r'20\d{2}$', number_str) and "Jahr" in context:
            return False

        # Don't simplify days in dates
        if re.match(r'\d{1,2}$', number_str) and any(month in context for month in
                                                     ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
                                                      "August", "September", "Oktober", "November", "Dezember"]):
            return False

        # Simplify "Ereignisse" only if not preceded by a year
        if "Ereignisse" in context and not re.search(r'20\d{2}', context):
            return True

        return True

    def process_match(match):
        """Process each number match and apply appropriate simplification"""
        full_match = match.group(0)
        number_part = match.group(1)
        unit_part = match.group(2) if match.group(2) else ""

        # Capture a larger context around the match (10 characters before and after)
        start_index = max(0, match.start() - 10)
        end_index = min(len(raw_text), match.end() + 10)
        context = raw_text[start_index:end_index]

        # Skip if number shouldn't be simplified
        if not should_simplify_number(number_part, context):
            return full_match

        # Handle percentages
        if 'Prozent' in full_match:
            number = format_number(number_part)
            return simplify_percentage(number)

        try:
            number = format_number(number_part)

            # Handle special cases for small numbers
            if number < 100:
                rounded = round(number)
                return f"etwa {rounded}{' ' + unit_part if unit_part else ''}"

            # Round larger numbers
            rounded = round_to_nearest_magnitude(number)
            formatted_number = f"{rounded:,.0f}".replace(',', '.')
            return f"etwa {formatted_number}{' ' + unit_part if unit_part else ''}"

        except ValueError:
            return full_match

    # Step 1: Protect full dates
    protected_dates = {}
    def protect_date(match):
        placeholder = f"[[FULLDATE_{len(protected_dates)}]]"
        protected_dates[placeholder] = match.group(0)
        return placeholder

    protected_text = re.sub(
        r'(\d{1,2}\.\s*(?:Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+\d{4})',
        protect_date,
        raw_text
    )

    # Step 2: Process numbers with units
    pattern = r'(\d+(?:\.\d+)*(?:,\d+)?)\s*((?:Euro|Menschen|Teilnehmer|Grad\s+Celsius|Ereignisse|Prozent|Jahr|Jahr\s+\d{4})?)'
    processed_text = re.sub(pattern, lambda match: process_match(match), protected_text)

    processed_text = re.sub(r'_etwa ', '_', processed_text)

    # Step 3: Restore protected dates
    for placeholder, original_date in protected_dates.items():
        processed_text = processed_text.replace(placeholder, original_date)

    return processed_text




# Test function
def run_tests():
    test_cases = [
        "324.620,22 Euro wurden gespendet.",
        "1.897 Menschen nahmen teil.",
        "25 Prozent der Bevölkerung sind betroffen.",
        "90 Prozent stimmten zu.",
        "14 Prozent lehnten ab.",
        "Bei 38,7 Grad Celsius ist es sehr heiß.",
        "denn die Rente steigt um 4,57 Prozent.",
        "Im Jahr 2024 gab es 1.234 Ereignisse.",
        "Am 1. Januar 2024 waren es 5.678 Teilnehmer.",
        "Im Jahr 2025 gab es 2018 Ereignisse."
    ]

    expected_outputs = [
        "etwa 325.000 Euro wurden gespendet.",
        "etwa 2.000 Menschen nahmen teil.",
        "jeder Vierte der Bevölkerung sind betroffen.",
        "fast alle stimmten zu.",
        "wenige lehnten ab.",
        "Bei etwa 39 Grad Celsius ist es sehr heiß.",
        "denn die Rente steigt um wenige.",
        "Im Jahr 2024 gab es etwa 1.000 Ereignisse.",
        "Am 1. Januar 2024 waren es etwa 6.000 Teilnehmer.",
        "Im Jahr 2025 gab es etwa 2.000 Ereignisse."
    ]

    for i, test_case in enumerate(test_cases):
        result = simplify_numbers(test_case)
        print(f"\nTest case {i + 1}:")
        print(f"Input:    {test_case}")
        print(f"Output:   {result}")
        print(f"Expected: {expected_outputs[i]}")
        print(f"Pass:     {result == expected_outputs[i]}")


if __name__ == "__main__":
    run_tests()