from flask import Flask, render_template, request, jsonify
import os
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PyPDF2 import PdfReader, PdfWriter
import psutil
import time
import hashlib
import struct
from concurrent.futures import ThreadPoolExecutor
import math
from datetime import datetime
import json

class ButterflyAES:
    def __init__(self):
        self.rounds = 12  # Increased rounds for better comparison
        
    def generate_butterfly_sbox(self, key, round_number):
        """Generate more complex S-box using butterfly effect"""
        sbox = bytearray(range(256))
        
        # Add round-specific complexity
        round_key = bytes([(b + round_number) % 256 for b in key])
        
        # Multiple transformation passes
        for pass_num in range(3):
            # Forward transformation
            for i in range(256):
                j = (i + round_key[i % 16] + pass_num) % 256
                sbox[i], sbox[j] = sbox[j], sbox[i]
                
                # Add butterfly effect
                k = (sbox[i] + sbox[j] + round_number) % 256
                sbox[k] = (sbox[k] * 7 + round_number) % 256
            
            # Reverse transformation
            for i in range(255, -1, -1):
                j = (sbox[i] + round_key[(i * round_number) % 16]) % 256
                sbox[i], sbox[j] = sbox[j], sbox[i]
        
        return bytes(sbox)

    def encrypt_block(self, block, key, round_number):
        """Encrypt a single block with round-specific S-box"""
        sbox = self.generate_butterfly_sbox(key, round_number)
        cipher = AES.new(key, AES.MODE_ECB)
        
        # Apply multiple rounds
        result = block
        for _ in range(self.rounds):
            result = bytes(sbox[b] for b in result)
            result = cipher.encrypt(result)
        
        return result

    def encrypt(self, plaintext, key):
        """Perform enhanced butterfly-based encryption"""
        try:
            padded_data = pad(plaintext, AES.block_size)
            blocks = [padded_data[i:i+AES.block_size] for i in range(0, len(padded_data), AES.block_size)]
            
            encrypted_blocks = []
            for i, block in enumerate(blocks):
                encrypted_block = self.encrypt_block(block, key, i + 1)
                encrypted_blocks.append(encrypted_block)
            
            return b''.join(encrypted_blocks)
        except Exception as e:
            print(f"Butterfly encryption error: {str(e)}")
            raise

class LEDECipher:
    def __init__(self):
        self.rounds = 12
        
    def generate_time_arrays(self, system_time, alpha, beta, gamma, round_number):
        """Generate time arrays with round-specific modifications"""
        time_bytes = struct.pack('>Q', system_time * round_number) * 16
        
        KA = bytearray(time_bytes)
        KB = bytearray(time_bytes)
        KC = bytearray(128)
        
        for pass_num in range(3):
            for i in range(64):
                KB[i] = (KB[i] + alpha + round_number * pass_num) % 256
                KB[127-i] = (KB[127-i] + beta + round_number * pass_num) % 256
                KB[i], KB[127-i] = KB[127-i], KB[i]
                
                mid = (KB[i] * KB[127-i] + gamma) % 256
                KB[i] = (KB[i] + mid) % 256
                KB[127-i] = (KB[127-i] ^ mid) % 256
            
            for i in range(128):
                KC[i] = (KA[i] * KB[i] + gamma * round_number + pass_num) % 256
                KA[i] = (KA[i] + KC[i]) % 256
        
        return KA, KB, KC

    def generate_sbox(self, KA, KB, KC, round_number):
        """Generate dynamic S-box"""
        sbox = []
        used_values = set()
        
        for pass_num in range(3):
            for arr in [KA, KB, KC]:
                for i, value in enumerate(arr):
                    modified_value = (value * round_number + pass_num) % 256
                    if modified_value not in used_values:
                        sbox.append(modified_value)
                        used_values.add(modified_value)
        
        remaining = set(range(256)) - used_values
        for value in sorted(remaining, reverse=bool(round_number % 2)):
            sbox.append(value)
            
        return bytes(sbox[:256])

    def encrypt_block(self, block, key, system_time, params, round_number):
        """Encrypt a single block"""
        alpha, beta, gamma = params
        KA, KB, KC = self.generate_time_arrays(system_time, alpha, beta, gamma, round_number)
        sbox = self.generate_sbox(KA, KB, KC, round_number)
        
        cipher = AES.new(key, AES.MODE_ECB)
        result = block
        
        for round_idx in range(self.rounds):
            round_sbox = self.generate_sbox(KA, KB, KC, round_idx + 1)
            result = bytes(round_sbox[b] for b in result)
            result = cipher.encrypt(result)
        
        return result

    def encrypt(self, plaintext, key):
        """Perform LEDE encryption"""
        try:
            alpha = secrets.randbelow(256)
            beta = secrets.randbelow(256)
            gamma = secrets.randbelow(256)
            system_time = int(time.time() * 1000)
            
            padded_data = pad(plaintext, AES.block_size)
            blocks = [padded_data[i:i+AES.block_size] for i in range(0, len(padded_data), AES.block_size)]
            
            encrypted_blocks = []
            for i, block in enumerate(blocks):
                encrypted_block = self.encrypt_block(block, key, system_time, (alpha, beta, gamma), i + 1)
                encrypted_blocks.append(encrypted_block)
            
            return {
                'ciphertext': b''.join(encrypted_blocks),
                'system_time': system_time,
                'params': (alpha, beta, gamma),
                've': hashlib.sha256(f"{system_time}{alpha}{beta}{gamma}".encode()).hexdigest()
            }
        except Exception as e:
            print(f"LEDE encryption error: {str(e)}")
            raise

class PerformanceStorage:
    def __init__(self):
        self.data_file = "encryption_results.json"
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = []
    
    def save_run(self, butterfly_time, lede_time, cpu_usage, memory_usage, file_size):
        run_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'butterfly_time': butterfly_time,
            'lede_time': lede_time,
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'file_size': file_size,
            'efficiency_gain': ((butterfly_time - lede_time) / butterfly_time * 100) if butterfly_time > 0 else 0
        }
        self.data.append(run_data)
        
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_all_runs(self):
        return self.data

def process_page_chunk(chunk_data):
    """Process a chunk of pages in parallel"""
    pages, key, butterfly_aes, lede = chunk_data
    chunk_butterfly_time = 0
    chunk_time_based_time = 0
    
    for page in pages:
        content = page.extract_text()
        if content:
            content_bytes = content.encode('utf-8')
            
            butterfly_start = time.perf_counter()
            butterfly_aes.encrypt(content_bytes, key)
            butterfly_end = time.perf_counter()
            chunk_butterfly_time += (butterfly_end - butterfly_start)
            
            time_start = time.perf_counter()
            lede.encrypt(content_bytes, key)
            time_end = time.perf_counter()
            chunk_time_based_time += (time_end - time_start)
    
    return chunk_butterfly_time, chunk_time_based_time

app = Flask(__name__)
storage = PerformanceStorage()

def monitor_performance():
    """Monitor system performance metrics"""
    try:
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        battery = psutil.sensors_battery()
        
        return {
            'cpu': cpu_usage,
            'memory': memory.percent,
            'battery': battery.percent if battery else 'N/A'
        }
    except Exception as e:
        print(f"Performance monitoring error: {str(e)}")
        return {'cpu': 0, 'memory': 0, 'battery': 'N/A'}

def encrypt_pdf_with_comparison(input_pdf, key):
    """Encrypt PDF using both methods with parallel processing"""
    try:
        reader = PdfReader(input_pdf)
        writer_butterfly = PdfWriter()
        writer_time = PdfWriter()
        
        butterfly_aes = ButterflyAES()
        lede = LEDECipher()
        
        pages = list(reader.pages)
        total_pages = len(pages)
        
        num_chunks = min(os.cpu_count() or 1, max(1, total_pages // 2))
        chunk_size = max(1, total_pages // num_chunks)
        
        chunks = [
            (pages[i:i + chunk_size], key, butterfly_aes, lede)
            for i in range(0, total_pages, chunk_size)
        ]
        
        butterfly_total_time = 0
        time_based_total_time = 0
        
        with ThreadPoolExecutor(max_workers=num_chunks) as executor:
            results = list(executor.map(process_page_chunk, chunks))
            
            for butterfly_time, time_based_time in results:
                butterfly_total_time += butterfly_time
                time_based_total_time += time_based_time
        
        for page in pages:
            writer_butterfly.add_page(page)
            writer_time.add_page(page)
        
        butterfly_output = os.path.join("uploads", f"butterfly_encrypted_{os.path.basename(input_pdf)}")
        time_output = os.path.join("uploads", f"time_encrypted_{os.path.basename(input_pdf)}")
        
        with open(butterfly_output, "wb") as f:
            writer_butterfly.write(f)
        with open(time_output, "wb") as f:
            writer_time.write(f)
        
        avg_butterfly_time = butterfly_total_time / max(total_pages, 1)
        avg_time_based_time = time_based_total_time / max(total_pages, 1)
        
        print(f"Debug - Butterfly time: {avg_butterfly_time:.6f}s")
        print(f"Debug - Time-based time: {avg_time_based_time:.6f}s")
        
        return {
            'butterfly': {
                'output': butterfly_output,
                'avg_time': avg_butterfly_time,
                'total_time': butterfly_total_time,
                'pages': total_pages
            },
            'time_based': {
                'output': time_output,
                'avg_time': avg_time_based_time,
                'total_time': time_based_total_time,
                'pages': total_pages
            }
        }
    except Exception as e:
        print(f"PDF encryption error: {str(e)}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt_pdf', methods=['POST'])
def encrypt_pdf_route():
    try:
        if 'pdf_file' not in request.files:
            return "No file uploaded!", 400
        
        file = request.files['pdf_file']
        if file.filename == '':
            return "No file selected!", 400
            
        if not file.filename.lower().endswith('.pdf'):
            return "Please upload a PDF file!", 400
        
        key = secrets.token_bytes(16)
        
        os.makedirs("uploads", exist_ok=True)
        input_pdf = os.path.join("uploads", file.filename)
        file.save(input_pdf)
        
        start_metrics = monitor_performance()
        start_time = time.perf_counter()
        
        results = encrypt_pdf_with_comparison(input_pdf, key)
        
        end_time = time.perf_counter()
        end_metrics = monitor_performance()
        
        total_time = end_time - start_time
        cpu_usage = max(0, end_metrics['cpu'] - start_metrics['cpu'])
        memory_usage = max(0, end_metrics['memory'] - start_metrics['memory'])
        
        file_size = os.path.getsize(input_pdf) / 1024  # Convert to KB
        
        storage.save_run(
            butterfly_time=results['butterfly']['avg_time'],
            lede_time=results['time_based']['avg_time'],
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            file_size=file_size
        )
        
        butterfly_time = results['butterfly']['avg_time']
        timebased_time = results['time_based']['avg_time']
        
        if butterfly_time > 0:
            efficiency_gain = ((butterfly_time - timebased_time) / butterfly_time) * 100
        else:
            efficiency_gain = 0
            
        return render_template('result.html',
                             butterfly_time=results['butterfly']['avg_time'],
                             timebased_time=results['time_based']['avg_time'],
                             cpu_usage=cpu_usage,
                             memory_usage=memory_usage,
                             battery_percent=end_metrics['battery'],
                             efficiency_gain=efficiency_gain,
                             butterfly_pdf=results['butterfly']['output'],
                             timebased_pdf=results['time_based']['output'],
                             total_pages=results['butterfly']['pages'],
                             file_size=file_size,
                             all_runs=storage.get_all_runs())
                             
    except Exception as e:
        print(f"Route error: {str(e)}")
        return f"An error occurred: {str(e)}", 500

@app.route('/api/performance_history')
def get_performance_history():
    return jsonify