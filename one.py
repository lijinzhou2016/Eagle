import os

print os.getpid()
os.environ.setdefault("test","hello")
os.system("bash two.sh")