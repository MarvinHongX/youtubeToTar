# youtube_to_tar.py
#########################################################################################
# Author  : Hong
# Created : 3/5/2024
# Modified: 3/6/2024
# Notes   : 
#########################################################################################
import shutil
import os
import datetime
import tarfile


def bytes_to_gib(bytes):
    gib = bytes / (1024 ** 3)  # 1 GiB = 1024^3 bytes
    return gib


def get_next_file_number(file_prefix, target_dir):
    max_file_number = 0
    found_files = False

    for filename in os.listdir(target_dir):
        if filename.startswith(file_prefix):
            found_files = True
            file_parts = filename.split('-')
            if len(file_parts) == 2 and file_parts[1].endswith('.tar'):
                try:
                    file_number = int(file_parts[1].split('.')[0])
                    max_file_number = max(max_file_number, file_number)
                except ValueError:
                    pass  # Ignore if the file number is invalid.

    if found_files:
        return max_file_number + 1
    else:
        return 1


def youtube_to_tar():
    source_dir='/storage/STUDIO/youtube'
    target_dir='/storage/STUDIO/youtube/0_TAR'
    completed_dir='/storage/STUDIO/youtube/0_COMPLETED'
    max_size=18.0
    min_size=17.1
    timestamp = datetime.datetime.now().strftime("%Y%m%d") 
    target_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=6) # time ago from now
    
    youtube_files = [f for f in os.listdir(source_dir) if f.endswith('.mp4')]
    selected_files = []
    total_size = 0


    print("Source Directory:", source_dir)
    print("Target Directory:", target_dir)
    print("Completed Directory:", completed_dir)
    print("Maximum Size:", max_size)
    print("Minimum Size:", min_size)
    print("Timestamp:", timestamp)
    print("Target Hours Ago:", target_hours_ago)


    # Create directories if they don't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if not os.path.exists(completed_dir):
        os.makedirs(completed_dir)


    # Get YouTube file list
    for file_name in youtube_files:
        # Exit loop if total size meets the minimum size condition
        if total_size >= min_size * (1024 ** 3):
            break

        file_path = os.path.join(source_dir, file_name)
        file_size = os.path.getsize(file_path)  # File size in bytes
        file_m_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)) # File modification time
        is_target = file_m_time < target_hours_ago

        file = {
            'file_path': file_path,
            'file_name': file_name,
            'file_size': file_size,
            'file_m_time': file_m_time,
            'is_target': is_target
        }

        # Select files modified within the last 6 hours and whose size fits within 17.1 to 18.0 GiB
        if is_target and (total_size + file_size) <= max_size * (1024 ** 3):
            selected_files.append(file)
            total_size += file_size



    # Print a message and exit if no files are selected
    if not selected_files:
        print("No files selected.")
        return
    

    # Print a message and exit if total size does not meet the minimum size condition
    if total_size < min_size * (1024 ** 3):
        print("Not enough files collected:", total_size)
        return
    
    print("total_size:", total_size)


    # Create tar archive
    file_prefix = f"{timestamp}-"
    tar_file_number = get_next_file_number(file_prefix, target_dir)
    tar_file_name = f"{file_prefix}{tar_file_number:04}.tar"
    log_file_name = f"{file_prefix}{tar_file_number:04}.log"
    tar_file_path = os.path.join(target_dir, tar_file_name)
    log_file_path = os.path.join(target_dir, log_file_name)
    completed_file_dir = f"{completed_dir}/{file_prefix}{tar_file_number:04}"
    print("file_prefix:", file_prefix);
    print("tar_file_number:", tar_file_number);
    print("tar_file_name:", tar_file_name);
    print("tar_file_path:", tar_file_path);
    print("completed_file_dir:", completed_file_dir);


    with tarfile.open(tar_file_path, 'w') as tar:
        for selected_file in selected_files:
            file_path = selected_file['file_path']
            tar.add(file_path, arcname=selected_file['file_name'])

    print(f"Tar file {tar_file_path} created.")


    # Move selected files to the completed directory
    if not os.path.exists(completed_file_dir):
        os.makedirs(completed_file_dir)

    for selected_file in selected_files:
        file_path = selected_file['file_path']
        file_name = selected_file['file_name']
        target_file_path = os.path.join(completed_file_dir, file_name)

        if os.path.exists(target_file_path):
            os.remove(target_file_path)  # Remove existing file

        shutil.move(file_path, completed_file_dir)


    with open(log_file_path, 'w') as log:
        log.write(f"# {log_file_name}\n\n")

        log.write(f"Tar File Name: {tar_file_name}\n")
        log.write(f"Total Size: {total_size} bytes\n\n")

        log.write(f"Source Directory: {source_dir}\n")
        log.write(f"Target Directory: {target_dir}\n")
        log.write(f"Completed Directory: {completed_dir}\n")
        log.write(f"Maximum Size: {max_size}\n")
        log.write(f"Minimum Size: {min_size}\n")
        log.write(f"Timestamp: {timestamp}\n")
        log.write(f"Target Hours Ago: {target_hours_ago}\n")

        log.write(f"File Prefix: {file_prefix}\n")
        log.write(f"Tar File Number: {tar_file_number}\n")
        log.write(f"Tar File Name: {tar_file_name}\n")
        log.write(f"Tar File Path: {tar_file_path}\n")
        log.write(f"Completed File Dir: {completed_file_dir}\n")


        log.write("\nSelected Files:\n")
        for selected_file in selected_files:
            log.write(f"File Name: {selected_file['file_name']}\n")
            log.write(f"File Size: {selected_file['file_size']} bytes\n")
            log.write(f"File Modification Time: {selected_file['file_m_time']}\n")
            log.write(f"Is Target: {selected_file['is_target']}\n")
            log.write("\n")


if __name__ == '__main__':
    youtube_to_tar();
