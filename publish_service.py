#!/usr/bin/python3
import os
import subprocess

service_path = '/etc/avahi/services/roguecast.service'
project_dir = os.path.dirname(__file__)

def set_up_avahi_service() -> None:
    with open(os.path.join(project_dir, 'roguecast.service'), 'r') as f:
        contents = f.read()
    with open(service_path, 'w') as f:
        f.write(contents)
    subprocess.run(['avahi-daemon'])
    print('running')

def clean_up_avahi_service() -> None:
    os.remove(service_path)

def main() -> None:
    try:
        set_up_avahi_service()
    finally:
        clean_up_avahi_service()

if __name__ == '__main__':
    main()
