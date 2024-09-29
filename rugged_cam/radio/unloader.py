# this file should look for any adidtional files in the loading dock directory and send them 
import os
import time
from meshtastic.serial_interface import SerialInterface
from serial import SerialException
import file_transfer.sender
from meshtastic.util import findPorts

from file_transfer.data_types import ResultSender




LOADING_DOCK_PATH = os.path.join(os.path.dirname(__file__), 'loading_dock/compressed')
def get_loading_dock_files():
    # look for files in the loading dock
    file_list = os.listdir(LOADING_DOCK_PATH)
    # remove any .md .gitignore .DS_STORE or subdirectories files
    file_list = [file for file in file_list if not file.endswith('.md') 
                 and not file.endswith('.gitignore') and not file.endswith('.DS_Store') 
                 and not os.path.isdir(os.path.join(LOADING_DOCK_PATH, file))]
    # create set 
    file_set = set(file_list)
    # return the set
    return file_set

class Unloader:
    def __init__(self):
        self.file_set = get_loading_dock_files()
        self.files_to_send_queue = []
        self.interface = None
        # get the interface
        ports = findPorts(True)
        interface = None
        if ports:
            for port in ports:
                try:
                    interface = SerialInterface(devPath=port)
                    print(f'connected to {interface.getShortName()}')
                    break
                except (BlockingIOError, SerialException) as e:
                    pass
        # add files to send queue
        self.files_to_send_queue.extend(self.file_set)
        pass

    def update_file_queue(self):
        most_recent_file_set = get_loading_dock_files()
        new_files = most_recent_file_set - self.file_set
        # add new files to queue
        self.files_to_send_queue.extend(new_files)
        # update the file set
        self.file_set = most_recent_file_set
        print(f'Files to send: {self.files_to_send_queue}')
        pass

    def send_file(self):
        # if no files to send, return
        if not self.files_to_send_queue:
            return ResultSender.NO_FILES
        file_path = self.files_to_send_queue.pop(0)
        if not os.path.exists(file_path):
            return ResultSender.FILE_NOT_FOUND
        # send the file
        print(f'Sending file: {file_path}')
        # send the file
        result_send = file_transfer.sender.run_sender(self.interface, path=file_path, shortname_destination_radio='palm')
        return result_send

    def has_files_to_send(self):
        # check if queue is empty
        return len(self.files_to_send_queue) > 0


if __name__ == '__main__':
    # queue for files to send
    files_to_send_queue = []
    current_file_set = get_loading_dock_files()
    unloader = Unloader()
    # now poll the directory every 45 seconds
    while True:
        unloader.update_file_queue()
        if unloader.has_files_to_send():
            result_send = unloader.send_file()
            if result_send == ResultSender.NO_FILES:
                print('No files to send')
            elif result_send == ResultSender.FILE_NOT_FOUND:
                print('File not found')
            elif result_send == ResultSender.SUCCESS:
                print('File sent successfully')
            elif result_send == ResultSender.FAIL:
                print('File failed to send')
        time.sleep(5)

