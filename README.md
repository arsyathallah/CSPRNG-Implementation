### Key Files

- **`Concept/`**: Contains the core encryption logic scripts for both Butterfly-based AES and Time-based AES.

  - **`butterflybased_aes.py`**: Implements the Butterfly-based AES encryption.
  - **`compare.py`**: Compares the results of the Butterfly-based AES and Time-based AES algorithms.
  - **`timebased_aes.py`**: Implements the Time-based AES encryption.

- **`Project/`**: Contains the main project files, including the Flask app, templates, and file storage.

  - **`app.py`**: The main Flask application file that contains the logic for routing, user input handling, and encryption functionality.
  - **`templates/`**: Contains the HTML templates for user input and displaying results.
    - **`index.html`**: The input form where users can upload PDFs and enter keys for encryption.
    - **`result.html`**: The results page that displays encryption times, entropy values, and CPU usage.
  - **`uploads/`**: Stores the uploaded and encrypted PDF files.
    - Encrypted files are named with their respective encryption algorithm (e.g., `encrypted_butterfly_*` for Butterfly AES).

- **`README.md`**: Contains the documentation for the project, explaining how to run the project and the concepts behind the encryption algorithms.

---

This structure should now reflect your actual file structure and be more aligned with your project setup.

## Running the Project

1. Clone the repository or download the project files.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the Flask application by executing:

4. Open a browser and navigate to `http://127.0.0.1:5000/` to access the web interface.
5. Upload a plaintext file (or manually input data) and compare the encryption times and CPU usage for both AES algorithms.

## Key Features

- **Parallel Execution**: Both encryption algorithms are executed simultaneously to compare performance.
- **Real-time Metrics**: The app calculates and shows encryption time and CPU usage during the execution of both algorithms.
- **User-Friendly Interface**: Simple HTML form to upload files, input keys, and display results.

## Conclusion

This project helps in comparing the performance of two different AES encryption algorithms based on dynamic S-boxes generated using the butterfly effect and the system time.
