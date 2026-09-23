import os

def discover_files(path, extension):
    file_paths = []
    for path, subdirs, files in os.walk(path):
        for name in files:
            if name.endswith(extension):
                file_paths.append(os.path.join(path, name))
                print(os.path.join(path, name))
    return file_paths

def discover_files_in_directory(path, extension, exclude_git_files=True):
    file_information = {
            "paths": [],
            "names": []
        }
    for name in os.listdir(path):
        if name.endswith(extension):
            if exclude_git_files and (name.startswith('.') or name == 'README.md'or name == 'LICENSE.md' or name == 'template-anleitung.md'):
                continue
            file_information["paths"].append(os.path.join(path, name))
            file_information["names"].append(name)
            print(os.path.join(path, name))
    print(f"Discovered {len(file_information['paths'])} files with extension '{extension}' in directory '{path}'")
    return file_information

def discover_folders_in_directory(path):
    folder_paths = []
    folder_names = []
    folder_information = {
        "paths": [],
        "names": []
    }
    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path, name)) and not name.startswith('.'):
            folder_paths.append(os.path.join(path, name))
            folder_names.append(name)
            folder_information["paths"].append(os.path.join(path, name))
            folder_information["names"].append(name)
            print(os.path.join(path, name))
    print(f"Discovered {len(folder_paths)} folders in directory '{path}'")
    return folder_information