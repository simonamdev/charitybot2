import os
import shutil

paths = []

print('Finding cache folders')
for path, dirs, files in os.walk(os.getcwd()):
    for folder in dirs:
        if folder == '__pycache__':
            paths.append(os.path.join(path, folder))
print('Deleting cache folders')
for path in paths:
    shutil.rmtree(path)
print('{} cache folders deleted'.format(len(paths)))
