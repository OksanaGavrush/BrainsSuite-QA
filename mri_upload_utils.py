import os

import hashlib
import gzip

import requests


def gzip_file(file_path, gz_path):
    """Create a gzip archive from a file."""
    with open(file_path, 'rb') as f_in, gzip.open(gz_path, 'wb') as f_out:
        f_out.writelines(f_in)


def send_files(url, headers, files):
    """Send a batch of files to the specified URL, and clean up after sending."""
    try:
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()
        print(f'Batch Upload Response for {len(files)} files: {response.text}')
    finally:
        for _, file_tuple in files:
            file_tuple[1].close()
            os.remove(file_tuple[1].name)
    return response


def send_files_in_batches(directory_path, url, headers, max_batch_size_mb=95):
    """Send files in batches to the API with a size limit."""
    max_batch_size = max_batch_size_mb * 1024 * 1024  # Convert MB to bytes
    responses = []
    batch_files = []
    current_batch_size = 0
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            gz_path = file_path + '.gz'
            gzip_file(file_path, gz_path)
            gz_size = os.path.getsize(gz_path)
            if current_batch_size + gz_size > max_batch_size:
                resp = send_files(url, headers, batch_files)
                responses.append(resp)
                batch_files, current_batch_size = [], 0
            batch_files.append(('files', (os.path.basename(gz_path), open(gz_path, 'rb'), 'application/gzip')))
            current_batch_size += gz_size
    if batch_files:
        resp = send_files(url, headers, batch_files)
        responses.append(resp)
    return responses


def get_md5_hash(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        return hashlib.md5(data).hexdigest()


def gather_hashes_from_directory(directory_path):
    return [get_md5_hash(os.path.join(directory_path, f)) for f in os.listdir(directory_path) if
            f.endswith(".dcm") and os.path.isfile(os.path.join(directory_path, f))]