from libqtile import widget
import subprocess
import sys

class CustomGenPollText(widget.GenPollText):
    defaults = [
        ("update_interval", 1, "Update interval in seconds.")
    ]

    def __init__(self, click_script=None, update_script=None, colors=None, texts1=None, texts2=None, 
                 click_python_func=None, update_python_func=None, icon=None, **config):
        self.click_script = click_script
        self.update_script = update_script
        self.colors = colors or ["#ffffff", "#ffffff"]
        self.texts1 = texts1
        self.texts2 = texts2
        self.click_python_func = click_python_func
        self.update_python_func = update_python_func
        self.icon = icon

        config["mouse_callbacks"] = {'Button1': self.handle_click}

        super().__init__(**config)
        self.add_defaults(CustomGenPollText.defaults)

    def handle_click(self):
        if self.click_script:
            subprocess.run([self.click_script], capture_output=True, text=True, shell=True)
        elif self.click_python_func:
            self.click_python_func()

    def poll(self):
        if self.update_script:
            res = subprocess.run([self.update_script],
                             capture_output=True,
                             text=True,
                             shell=True)
            output = res.stdout.strip()

            if output == "True":
                self.foreground = self.colors[0]
                if type(self.texts1) == str:
                    return str(self.texts1)
                else:
                    return self.texts1()
            else:
                self.foreground = self.colors[1]
                return str(self.texts2)
        elif self.update_python_func:
            is_active = self.update_python_func()
            if is_active:
                self.foreground = self.colors[0]
                if type(self.texts1) == str:
                    return str(self.texts1)
                else:
                    return self.texts1()
            else:
                self.foreground = self.colors[1]
                return str(self.texts2)
        elif self.icon:
            return self.icon


# Usage example
# my_widget = CustomGenPollText(
#     click_script="/path/to/click_script.sh",
#     update_script="/path/to/update_script.sh",
#     colors=["#ff0000", "#0000ff"]
# )

