import os


def run_server():
    os.system('python -m flask --app api/server run')