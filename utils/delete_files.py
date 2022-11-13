import os, shutil

def delete_all_files(file_dir):
# Delete all directories and files in files/ directory
    if not os.path.exists(file_dir):
        return
        
    for filename in os.listdir(file_dir):
        file_path = os.path.join(file_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))