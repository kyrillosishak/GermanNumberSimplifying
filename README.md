# Simplifying Numbers in Text with Python

This Python script, `simplify_numbers`, processes raw text to simplify numbers according to specific rules. It converts numeric representations into more human-readable formats, applying rounding, context-based adjustments, and formatting transformations. The script handles numbers with specific units (e.g., "Euro", "Prozent") and percentages, providing meaningful simplifications such as "jeder Vierte" (every fourth) for 25%.

## Table of Contents
1. [Function Overview](#function-overview)
2. [Core Features](#core-features)
3. [How It Works](#how-it-works)
4. [Code Highlights](#code-highlights)
5. [Test Cases](#test-cases)
6. [Running the Script](#running-the-script)
7. [Limitations](#limitations)

---

## Function Overview

### `simplify_numbers(raw_text)`
- **Input**: A string containing text with numbers and units.
- **Output**: The processed string with simplified numbers.

Key features:
- Rounds numbers to the nearest significant figure based on magnitude.
- Transforms specific percentages into descriptive phrases.
- Protects date strings from being altered.
- Applies contextual rules to determine whether to simplify numbers.

---

## Core Features

### 1. Rounding Numbers
- Numbers below `1,000`: Rounded to the nearest 100.
- Numbers between `1,000` and `100,000`: Rounded to the nearest 1,000.
- Numbers `100,000` or larger: Rounded to the nearest 1,000.

### 2. Simplifying Percentages
Percentages are replaced with meaningful phrases:
- `25%` → "jeder Vierte"
- `50%` → "die Hälfte"
- `90%` or more → "fast alle"

### 3. Context-Aware Simplifications
The script avoids altering:
- Year references in date contexts.
- Day and month combinations resembling calendar dates.

---

## How It Works

1. **Context Extraction**: Captures surrounding text to decide whether to simplify a number.
2. **Regular Expressions**:
   - Identify numeric patterns and their units.
   - Protect date strings to ensure they remain unaltered.
3. **Custom Rules**:
   - Simplifies percentages into descriptive phrases.
   - Applies different rounding rules based on magnitude.
4. **Post-Processing**: Restores protected text (e.g., dates) into the final output.

---

## Code Highlights

### Simplification Helpers
- **`round_to_nearest_magnitude`**: Rounds numbers based on their magnitude.
- **`simplify_percentage`**: Translates percentages into human-readable text.
- **`should_simplify_number`**: Ensures contextual relevance before simplifying a number.

### Regular Expressions
- Matches and processes numbers with optional units using:
  ```python
  pattern = r'(\d+(?:\.\d+)*(?:,\d+)?)\s*((?:Euro|Menschen|Teilnehmer|Grad\s+Celsius|Ereignisse|Prozent|Jahr|Jahr\s+\d{4})?)'
  ```
---

# Limitations of the Simplify Numbers Script

The `simplify_numbers` script is a **rule-based model**, meaning it relies on predefined rules and patterns to process text. While it performs well for the specific cases it is designed to handle, this approach has inherent limitations that affect its generalizability.

---

## Why Rule-Based Models Have Limitations

Rule-based models like this one depend on:
- **Explicitly Defined Rules**: The script uses specific patterns and logic (e.g., regular expressions, contextual checks) to process input.
- **Finite Context**: The context rules are hard-coded and may not account for all linguistic or domain-specific nuances.
- **Static Scope**: The model cannot learn or adapt to new cases unless manually updated.

---

## Situations Where the Script May Fail

### 1. **Unanticipated Formats**
The script relies on predefined patterns for numbers and units. If a number appears in a format not covered by these patterns, it will be ignored or processed incorrectly.

**Example**:
- Input: `1,234.56 USD were spent.`
- Expected: `etwa 1.200 USD were spent.`
- Output: Unchanged because "USD" is not defined as a unit in the script.

---

### 2. **Ambiguities in Context**
The script uses surrounding context to decide whether to simplify numbers, but this logic is limited and may fail for nuanced cases.

**Example**:
- Input: `Im Jahr 2024 wurden 2.018 Dinge registriert.`
- Expected: `Im Jahr 2024 wurden etwa 2.000 Dinge registriert.`
- Output: Unchanged because "2.018" resembles a year in context.

---

### 3. **Language-Specific Assumptions**
The script assumes specific German conventions (e.g., decimal commas, months). It will not work correctly for:
- Non-German texts.
- Texts with mixed formatting styles.

**Example**:
- Input: `12,345 items were recorded.`
- Expected: `etwa 12.000 items were recorded.`
- Output: Unchanged or incorrect because English number formatting differs from German.

---

### 4. **Complex Numerical Relationships**
The script cannot handle complex relationships between numbers or infer additional meaning beyond predefined logic.

**Example**:
- Input: `40% and 60% were distributed equally.`
- Expected: Simplified percentages with appropriate context.
- Output: Unchanged because the script processes percentages individually without considering their relationship.

---

## General Rule-Based Model Limitations

1. **Not Adaptive**: Rule-based systems do not improve with new data or examples.
2. **High Maintenance**: Adding new rules or handling edge cases requires manual intervention.
3. **Scalability Issues**: As the number of rules grows, maintaining and debugging the system becomes more challenging.
4. **Brittleness**: Small deviations in input can break the logic (e.g., typos, unexpected spacing).

