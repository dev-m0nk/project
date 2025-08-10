# Project (I have made this file from chatGpt)

This project is an AI-enabled Python tool that processes multi-slide PowerPoint presentations (`.pptx`) to find factual and logical inconsistencies. It analyzes text found directly on the slides, in speaker notes, and within images to identify conflicting data points and calculation errors.

---

## Features

* **Comprehensive Text Extraction**: Extracts text from all slide elements, including text boxes, shapes, and speaker notes.
* **Image-to-Text Analysis (OCR)**: Includes an option to perform Optical Character Recognition (OCR) on images within the slides to analyze text in diagrams, screenshots, and charts.
* **Data Normalization**: Intelligently identifies and standardizes various data types including:
    * Currencies (e.g., `$2M`, `1,000,000`, `50K`)
    * Percentages (`50%`)
    * Durations (`15 mins`, `2 hours`)
    * Multipliers (`2x`, `10X`)
* **Inconsistency Detection**:
    * **Value Mismatches**: Flags when the same metric (e.g., "currency") has different values across the presentation.
    * **Sum Mismatches**: Checks if a stated total on a slide matches the sum of its itemized components.
* **Structured Reporting**: Generates a clear and machine-readable `report.json` file detailing each inconsistency, the slide number it occurred on, and the context.

---

## How It Works

The tool operates in a three-stage pipeline:

1.  **Extraction (`extractor.py`)**: The script first opens the `.pptx` file and iterates through each slide. It extracts all textual content and, if enabled, saves images to disk to be processed by an OCR engine.
2.  **Normalization (`normalizer.py`)**: The raw text from each slide is then processed. Using regular expressions, the script finds and converts specific data points (like currencies and percentages) into a standardized format called "facts."
3.  **Comparison (`comparator.py`)**: Finally, the script analyzes the complete list of facts. It groups them by type to find value mismatches and iterates through slides to check for sum inconsistencies, compiling all findings into a final report.

---

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    The project requirements are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Tesseract-OCR (required for `--use-ocr` flag):**
    This tool relies on Google's Tesseract engine for OCR functionality. You must install it on your system.
    * **macOS**: `brew install tesseract`
    * **Ubuntu**: `sudo apt-get install tesseract-ocr`
    * **Windows**: Download and run the installer from the [official Tesseract repository](https://github.com/tesseract-ocr/tessdoc).

---

## Usage

The script is run from the command line.

**Basic command:**
```bash
python analyze_deck.py /path/to/your/presentation.pptx






Output Format
The script generates a report.json file containing the analysis.

summary: A high-level overview of the number of inconsistencies found.

inconsistencies: A list of all detected issues. Each issue is an object with:

type: The type of inconsistency (e.g., currency_mismatch, sum_mismatch).

items or slide: The data points involved in the inconsistency and their context.

explanation: A human-readable description of the issue.

Limitations and Thoughtfulness of Approach
Hardcoded Sum Check: The sum_mismatch check in comparator.py is currently hardcoded to look for the specific phrase "Hours Saved Per Consultant Monthly". This makes it effective for the sample deck but not generalizable to other presentations with different wording for totals and components. A more robust solution would involve semantic analysis to identify totals and their related parts dynamically.

Numerical Focus: The current version primarily detects numerical inconsistencies. It does not yet analyze or compare textual claims (e.g., "market is highly competitive" vs. "few competitors").

No Timeline Analysis: The tool does not currently extract or compare dates to check for timeline mismatches.

Future Improvements
LLM Integration: Implement the --llm functionality to use a model like Gemini to detect more nuanced logical and semantic inconsistencies, such as contradictory textual claims and timeline mismatches.

Dynamic Sum Checking: Replace the hardcoded sum-finding logic with a more intelligent system that can identify totals and components regardless of the phrasing used on the slide.

Enhanced Data Normalizers: Add new regular expressions to normalizer.py to identify and standardize more data types, such as dates, addresses, or specific product names.

Configuration File: Allow users to define custom check types or patterns in a config.yaml file to make the tool more adaptable to specific use cases.

Unit Tests: Develop a suite of unit tests with pytest to ensure the reliability and robustness of the extraction, normalization, and comparison logic, especially as new features are added.
