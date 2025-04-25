import os
import subprocess
import time

class InputWindow:
    def __init__(self,
                 temp_file="temp_input.txt",
                 window_title="InputWindow",
                 pre_open_func = None,
                 post_close_func = None):
        self.temp_file = temp_file
        self.user_input = None
        self.window_title = window_title
        self.pre_open_func = pre_open_func
        self.post_close_func = post_close_func


    def open_window(self):

        if self.pre_open_func is not None:
            self.pre_open_func()

        # Ensure the temp file exists
        open(self.temp_file, 'a').close()

        # Open Kitty with Neovim
        home = os.getenv("HOME")
        nvim_config_path = home + "/.config/qtile/Scripts/nvim_temp_config.vim"
        nvim_process = subprocess.Popen(["kitty",
                                         "--title", self.window_title,
                                         "nvim", "-u", nvim_config_path,
                                         "--noplugin",
                                         self.temp_file])

        while nvim_process.poll() is None:
            time.sleep(0.5)  # Polling interval

        name = self.read_input()
        self.cleanup()

        if self.post_close_func is not None:
            self.post_close_func(name)

    def read_input(self):
        with open(self.temp_file, 'r') as file:
            self.user_input = file.read().strip()
        return self.user_input

    def cleanup(self):
        try:
            os.remove(self.temp_file)
        except OSError:
            pass

    def get_input(self):
        return self.user_input


def take_screenshot(file_name):
    os.chdir(os.getenv("HOME"))
    prefix = "Pictures/"
    subprocess.run(["gnome-screenshot", "-a" , "-f", prefix + file_name + ".png"])

def main(qtile):
    input_window = InputWindow(post_close_func=take_screenshot)
    input_window.open_window()
    user_input = input_window.get_input()
    print(f"User entered: {user_input}")

if __name__ == "__main__":
    main()
