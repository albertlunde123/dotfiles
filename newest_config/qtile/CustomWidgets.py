from libqtile import widget
import subprocess

class CustomGenPollText(widget.GenPollText):
    defaults = [
        ("update_interval", 1, "Update interval in seconds.")
    ]

    def __init__(self, click_script, update_script, colors, texts1, texts2, **config):
        self.click_script = click_script
        self.update_script = update_script
        self.colors = colors
        self.texts1 = texts1
        self.texts2 = texts2

        config["mouse_callbacks"] = {'Button1': self.run_click_script}

        super().__init__(**config)
        self.add_defaults(CustomGenPollText.defaults)

    def run_click_script(self):
        subprocess.run([self.click_script], capture_output=True, text=True, shell=True)

    def poll(self):
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
            return str(self.texts2)  # Replace with your desired text




# Usage example
# my_widget = CustomGenPollText(
#     click_script="/path/to/click_script.sh",
#     update_script="/path/to/update_script.sh",
#     colors=["#ff0000", "#0000ff"]
# )

