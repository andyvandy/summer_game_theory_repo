import os

def clear_directory(directory):
    for f in os.listdir(directory):
        f_path = os.path.join(directory, f)
        try:
            if os.path.isfile(f_path):
                os.unlink(f_path)
        except Exception, e:
            print e


def remove_file(f_path):
    if os.path.isfile(f_path):
        try:
            os.unlink(f_path)
        except Exception, e:
            print e