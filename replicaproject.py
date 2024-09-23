import os
import time
import shutil
import hashlib
from datetime import datetime

#uction to log the messages
def log_message(message, log_file):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(log_file, 'a') as f:
        f.write(log_entry + '\n')

def get_md5(file_path):
    #Calculates the MD5 checksum of a file
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def sync_folders(source, replica, log_file):
    #a fuction that clones the data in the source file to the replica file
    # Creates a replica folder if a current one doesnt exist
    if not os.path.exists(replica):
        os.makedirs(replica)
        log_message(f"Created replica folder: {replica}", log_file)

    #Creates a source folder if a current one doesnt exist
    if not os.path.exists(source):
        os.makedirs(source)
        log_message(f"Created source folder: {source}", log_file)

    # Get the list of files and directories in the source folder
    for dirpath, dirnames, filenames in os.walk(source):
        rel_path = os.path.relpath(dirpath, source)
        replica_dir = os.path.join(replica, rel_path)

        # Create directories in the replica that exist in the source folder
        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)
            log_message(f"Created directory: {replica_dir}", log_file)

        # Clone files from source to replica
        for file in filenames:
            source_file = os.path.join(dirpath, file)
            replica_file = os.path.join(replica_dir, file)

            # Copy file/s if it doesn't exist in the replica folder or if it has changed
            if not os.path.exists(replica_file) or get_md5(source_file) != get_md5(replica_file):
                shutil.copy2(source_file, replica_file)
                log_message(f"Copied/Updated file: {source_file} to {replica_file}", log_file)

    # Remove files and directories from the replica folder that are not/no longer in the source folder
    for dirpath, dirnames, filenames in os.walk(replica):
        rel_path = os.path.relpath(dirpath, replica)
        source_dir = os.path.join(source, rel_path)

        # Remove files that are not in the source folder
        for file in filenames:
            replica_file = os.path.join(dirpath, file)
            source_file = os.path.join(source_dir, file)

            if not os.path.exists(source_file):
                os.remove(replica_file)
                log_message(f"Deleted file: {replica_file}", log_file)

        # Remove directories that are not in the source folder
        for dir in dirnames:
            replica_subdir = os.path.join(dirpath, dir)
            source_subdir = os.path.join(source_dir, dir)

            if not os.path.exists(source_subdir):
                shutil.rmtree(replica_subdir)
                log_message(f"Deleted directory: {replica_subdir}", log_file)

def main():
    source = "C:\\Users\\marco\\Desktop\\a\\s\\lab\\source1"  # Path to the source folder
    replica = "C:\\Users\\marco\\Desktop\\a\\s\\lab\\replica1"  # Path to the replica folder
    log_file = "C:\\Users\\marco\\Desktop\\a\\s\\lab\\log.txt"  # Path to the log file
    interval = 10  # Synchronization interval in seconds

    log_message(f"Starting synchronization from {source} to {replica} every {interval} seconds.", log_file)

    while True:
        sync_folders(source, replica, log_file)
        log_message(f"Synchronization complete. Next sync in {interval} seconds.", log_file)
        time.sleep(interval)

if __name__ == "__main__":
    main()


