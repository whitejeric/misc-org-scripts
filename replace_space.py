import os
print (os.getcwd())
[os.rename(f, f.replace(' ', '_')) for f in os.listdir('.') if not f.startswith('.')]
for f in os.listdir('.'):
    if not f.startswith('.'):
        print(f)
