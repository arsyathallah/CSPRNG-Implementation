# Encryption Comparison: Butterfly AES vs Time-based LEDE

A web-based application to compare the performance of two AES encryption variants: Butterfly-based AES and Time-based Low-Energy Data Encryption (LEDE).

## Glossary

### Core Concepts

1. **AES (Advanced Encryption Standard)**
   - A symmetric block cipher standard
   - Processes data blocks of 128 bits
   - Uses cryptographic keys of 128, 192, or 256 bits

2. **S-Box (Substitution Box)**
   - A basic component of symmetric key algorithms
   - Performs byte substitution in encryption process
   - Maps input bits to output bits based on predefined rules

3. **Dynamic S-Box**
   - An S-Box that changes based on certain parameters
   - Used to enhance encryption security
   - Generated using different methods in both algorithms

### Algorithm Details

1. **Butterfly-based AES**
   - Uses butterfly effect for S-box generation
   - Features:
     - Multiple transformation passes
     - Non-linear transformations
     - Round-specific modifications
   - Implementation:
     ```python
     sbox = generate_butterfly_sbox(key, round_number)
     for round in range(12):
         result = apply_sbox_transformation(data)
         result = aes_encrypt_round(result)
     ```

2. **Time-based LEDE**
   - Uses system time for S-box generation
   - Features:
     - Time parameter arrays (KA, KB, KC)
     - Dynamic S-box updates
     - Verification message generation
   - Implementation:
     ```python
     system_time = get_current_time()
     KA, KB, KC = generate_time_arrays(system_time)
     sbox = generate_dynamic_sbox(KA, KB, KC)
     ```

## Setup and Installation

### Prerequisites
```bash
# Required software
- Python 3.8 or higher
- pip (Python package manager)

# Required system libraries
- python3-venv
- python3-full
```

### Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Project Structure
```
project/
├── app.py                  # Main Flask application
├── encryption_results.json # Performance data storage
├── uploads/               # Directory for uploaded files
└── templates/
    ├── index.html        # Upload interface
    └── result.html       # Results and visualization
```

## Usage

1. Start the application:
```bash
./run.sh
# Or manually:
export FLASK_APP=app.py
flask run
```

2. Access the web interface:
   - Open browser and navigate to `http://127.0.0.1:5000`
   - Upload a PDF file for encryption
   - View comparison results and performance metrics

3. Understanding Results:
   - **Encryption Time**: Processing time in milliseconds
   - **CPU Usage**: Processor utilization percentage
   - **Memory Usage**: RAM utilization
   - **Efficiency Gain**: Performance comparison between methods

## Performance Metrics

The application measures:
1. Encryption time for both methods
2. System resource utilization
3. Efficiency comparison
4. File size impact on performance

Example results format:
```json
{
    "timestamp": "2024-12-08 00:26:10",
    "butterfly_time": 0.00128,
    "lede_time": 0.00528,
    "cpu_usage": 0,
    "memory_usage": 0,
    "file_size": 1145.96,
    "efficiency_gain": -311.89
}
```

## Limitations

1. File Size:
   - Optimal for files under 50MB
   - Large files may cause memory issues

2. Performance:
   - Results may vary based on system resources
   - Multiple runs recommended for accurate comparison

3. System Requirements:
   - Sufficient RAM for large files
   - Stable system time for LEDE algorithm

## Troubleshooting

Common issues and solutions:
1. Memory errors with large files:
   - Reduce file size
   - Close other applications

2. Performance inconsistencies:
   - Ensure consistent system state
   - Run multiple tests
   - Check system resource availability

## Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Submit pull request with detailed changes

## License

This project is licensed under MIT License - see LICENSE file for details.

---
For more information about the algorithms and implementation details, refer to the original paper: "Time Parameter Based Low-Energy Data Encryption Method for Mobile Applications"