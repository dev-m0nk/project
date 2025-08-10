# Project 

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



---

## Developer Notes

* **Time-Constrained Implementation**: Given the one-day turnaround for this project, some functions were hardcoded to ensure functionality with the provided sample presentation. The immediate next step is to refactor this logic to be universally applicable.
* **Cross-Platform README**: The setup instructions in this `README.md` were generated with the assistance of an AI tool to ensure they are helpful for both Windows and macOS users. The Python code, however, is entirely original work.
* **Pending Features**: Timeline mismatch detection is a planned feature that has not yet been implemented. I am currently evaluating the most effective methods for extracting and comparing date-based information.


