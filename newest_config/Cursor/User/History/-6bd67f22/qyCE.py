import os
import re
import tempfile
import subprocess
import shlex  # Good practice for command construction, though less critical here
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPen, QColor, QPainter # Added QColor just in case it's needed directly
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QMessageBox # For error feedback
from pyqt_drawing_app.tools.base_tool import BaseTool
from pyqt_drawing_app.elements.latex_text_element import LatexTextElement # Import element class

# --- Determine Paths for Custom Neovim Config ---
# Get the directory where this Python script lives
_tool_script_dir = os.path.dirname(__file__)
# Go up one level to the 'tools' directory parent (project root)
_project_root = os.path.dirname(_tool_script_dir)
# Path to the minimal vimrc file
_custom_nvim_config_path = os.path.join(
    _project_root, "nvim_config", "minimal_latex.lua"
)
# Path to the snippets directory (needed for UltiSnips setting in vimrc)
_custom_snippets_dir = os.path.join(
    _project_root, "nvim_config", "custom_latex_snippets"
)

# Check if the custom config file exists
if not os.path.isfile(_custom_nvim_config_path):
    # Handle error - maybe raise an exception or show a critical message box
    # For now, print a warning. The launch will likely fail later.
    print(f"CRITICAL WARNING: Custom Neovim config not found at: {_custom_nvim_config_path}")
    # You might want to prevent the tool from working here.
    # raise FileNotFoundError(f"Custom Neovim config not found: {_custom_nvim_config_path}")


# --- Configuration for External Editor ---
TERMINAL_COMMAND = "alacritty"
TERMINAL_ARGS_BASE = [
    "--title", "LaTeX Editor (PyQtDraw)",
    "--class", "pyqtdraw_latex,PyQtDrawLatex",
    # Dimensions set in alacritty.toml
]
# Base command for Neovim with custom config
EDITOR_COMMAND_BASE = [
    "nvim",
    "-u", _custom_nvim_config_path, # Use our minimal config
    "-i", "NONE",                 # Don't use a shada file (history, etc.)
    "-n",                         # Don't use a swap file
]
# ---

class LatexTextTool(BaseTool):
    def __init__(self, color):
        super().__init__()
        self.text_color = color
        # No need for click_position storage here anymore for the callback

    def activate(self, canvas):
        super().activate(canvas)
        # No specific activation needed for this version

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            clicked_element = None
            # Check if we clicked on an existing latex element
            for element in reversed(self.canvas.elements): # Check topmost first
                if (isinstance(element, LatexTextElement) and
                        element.contains_point(event.pos())):
                    clicked_element = element
                    break # Found the element under the cursor

            # Launch editor for new or existing element
            self._launch_external_editor(
                position=event.pos(), # Pass position for potential new elements
                existing_element=clicked_element
            )

    def _launch_external_editor(self, position=None, existing_element=None):
        """
        Handles creating/editing LaTeX via an external terminal editor
        using a custom Neovim configuration.
        """
        is_new = existing_element is None
        temp_file_path = None

        # Determine initial content
        if is_new:
            # Add some comments to guide the user in the temp file
            initial_content = (
            "\[ \]"
            )
            # Use the click position if creating a new element
            edit_position = position
        else:
            initial_content = f"\[ {existing_element.latex_code} \]"
            # Use the existing element's position
            edit_position = existing_element.position

        try:
            # 1. Create a temporary file
            with tempfile.NamedTemporaryFile(
                mode="w+", suffix=".tex", delete=False, encoding="utf-8"
            ) as f:
                temp_file_path = f.name
                print(f"Temporary LaTeX file created: {temp_file_path}")
                f.write(initial_content)
                f.flush() # Ensure content is written

            # 2. Construct the full command
            # Command to run inside the terminal: nvim [flags] <filepath>
            # EDITOR_COMMAND_BASE is defined outside this method
            nvim_command_parts = EDITOR_COMMAND_BASE + [temp_file_path]
            # command_string_for_e = " ".join(shlex.quote(part) for part in nvim_command_parts)

            full_command = [TERMINAL_COMMAND] + TERMINAL_ARGS_BASE + ["-e"] + nvim_command_parts
            print(f"Constructed command list: {full_command}")

            # 3. Launch the editor (blocking call)
            # This will freeze the PyQt app until Alacritty/Nvim is closed
            result = subprocess.run(full_command)
            print(f"Editor process finished with code: {result.returncode}")

            # 4. Process the result if the editor exited successfully
            if result.returncode == 0 and os.path.exists(temp_file_path):
                print(f"Reading content from: {temp_file_path}")
                with open(temp_file_path, "r", encoding="utf-8") as f:
                    edited_content = f.read()

                # Process the potentially edited LaTeX content
                # _process_edited_latex is another method in this class
                self._process_edited_latex(
                    edited_content, edit_position, existing_element
                )

            elif result.returncode != 0:
                 print(f"Editor process exited with error code: {result.returncode}")
                 QMessageBox.warning(
                     self.canvas, # Parent widget for the message box
                     "Editor Error",
                     f"The editor process exited with code {result.returncode}.\n"
                     "Check Neovim configuration and permissions.\n"
                     "No changes were applied."
                 )

        except FileNotFoundError as e:
             # This might catch alacritty or nvim if not in PATH
             error_msg = (
                 f"Error: Command not found during launch: {e}\n"
                 f"Ensure '{TERMINAL_COMMAND}' and '{EDITOR_COMMAND_BASE[0]}' are in your PATH."
             )
             print(error_msg)
             QMessageBox.critical(self.canvas, "Dependency Error", error_msg)

        except Exception as e:
            error_msg = f"An unexpected error occurred while launching the editor: {e}"
            print(error_msg)
            QMessageBox.critical(self.canvas, "Error", error_msg)

        finally:
            # 5. Clean up the temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                    print(f"Temporary file deleted: {temp_file_path}")
                except Exception as e:
                    print(f"Error deleting temp file {temp_file_path}: {e}")

    def _process_edited_latex(self, latex_content, position, existing_element):
        """
        Process the LaTeX content read from the temp file after editing.
        (This logic is moved from the old callback system)
        """
        try:
            # Extract the equation (handle potential comments)
            # Look for \[ ... \] potentially spanning multiple lines
            # latex_match = re.search(r'\\\[(.*?)\\\]', latex_content, re.DOTALL)
            latex_match = latex_content

            if latex_match:
                # latex_code = latex_match.group(1).strip()
                latex_code = latex_match

                # Avoid processing if the content is empty or just whitespace
                if not latex_code:
                    print("No LaTeX code found between \[ \]. Aborting.")
                    return

                print(f"Extracted LaTeX code: {latex_code}")

                # Render the LaTeX
                svg_renderer = self._render_latex(latex_code)

                if svg_renderer and svg_renderer.isValid():
                    if existing_element is None:
                        # Create and add LaTeX element to canvas
                        print(f"Creating new LaTeX element at {position}")
                        element = LatexTextElement(
                            position,
                            latex_code,
                            svg_renderer,
                            self.text_color
                        )
                        self.canvas.add_element(element)
                    else:
                        # Update the existing element
                        print(f"Updating existing LaTeX element")
                        existing_element.latex_code = latex_code
                        existing_element.svg_renderer = svg_renderer
                        # Update color potentially? If color tool was used maybe?
                        # existing_element.color = self.text_color
                        self.canvas.update() # Redraw canvas
                elif svg_renderer and not svg_renderer.isValid():
                     print("Rendered SVG is invalid.")
                     QMessageBox.warning(self.canvas, "Render Error", "Rendered SVG data is invalid. Check LaTeX syntax.")
                else:
                    # _render_latex already prints errors, but add a message box
                    QMessageBox.warning(self.canvas, "Render Error", "Failed to render the LaTeX code. Check console for details.")

            else:
                print("Could not find \[ ... \] block in the edited file.")
                # Optionally inform the user if the block is missing
                # QMessageBox.information(self.canvas, "Info", "No LaTeX block \[ ... \] found in the editor.")


        except Exception as e:
            print(f"Error processing LaTeX content: {e}")
            QMessageBox.critical(self.canvas, "Processing Error", f"Error processing LaTeX: {e}")


    def _render_latex(self, latex_code):
        """Render LaTeX to SVG format using direct LaTeX + dvisvgm"""
        # Check if latex and dvisvgm are available
        if not (self._check_command("latex") and self._check_command("dvisvgm")):
             QMessageBox.critical(
                 self.canvas,
                 "Dependency Error",
                 "Could not find 'latex' and/or 'dvisvgm'.\n"
                 "Please ensure a LaTeX distribution (like TeX Live) is installed and in your PATH."
             )
             return None

        try:
            # Create a temporary directory for build files
            with tempfile.TemporaryDirectory() as temp_dir:
                tex_file = os.path.join(temp_dir, "equation.tex")
                dvi_file = os.path.join(temp_dir, "equation.dvi")
                svg_file = os.path.join(temp_dir, "equation.svg")

                # Create LaTeX document
                latex_source = r"""
\documentclass[preview]{standalone}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{xcolor}
\begin{document}
\definecolor{textcolor}{RGB}{%s}
{\color{textcolor}%s}
\end{document}
""" % (self._color_to_rgb_values(), latex_code) # Use %s formatting for color

                # Note: Removed the outer '$...$' as we now expect \[...\] from the editor
                # If users enter inline math like $...$, standalone preview might handle it.

                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(latex_source)

                # Compile LaTeX to DVI
                latex_result = subprocess.run(
                    ["latex", "-interaction=nonstopmode", "-output-directory", temp_dir, tex_file],
                    capture_output=True, text=True # Capture output
                )
                if latex_result.returncode != 0:
                    print(f"LaTeX compilation failed:\n{latex_result.stdout}\n{latex_result.stderr}")
                    # Show error in GUI
                    QMessageBox.critical(
                        self.canvas, "LaTeX Error",
                        f"LaTeX compilation failed. Check your syntax.\n\nLog:\n{latex_result.stdout}\n{latex_result.stderr}"
                    )
                    return None

                # Check if DVI file was created
                if not os.path.exists(dvi_file):
                     print(f"DVI file not found after latex run: {dvi_file}")
                     QMessageBox.critical(self.canvas, "LaTeX Error", "DVI file was not generated by LaTeX.")
                     return None

                # Convert DVI to SVG
                dvisvgm_result = subprocess.run(
                    ["dvisvgm", "--no-fonts", "--exact", dvi_file, "-o", svg_file], # Added --exact for better bounding box
                     capture_output=True, text=True
                )
                if dvisvgm_result.returncode != 0:
                    print(f"dvisvgm conversion failed:\n{dvisvgm_result.stdout}\n{dvisvgm_result.stderr}")
                    QMessageBox.critical(self.canvas, "SVG Conversion Error", f"dvisvgm failed:\n{dvisvgm_result.stderr}")
                    return None

                # Check if SVG file exists
                if not os.path.exists(svg_file):
                     print(f"SVG file not found after dvisvgm run: {svg_file}")
                     QMessageBox.critical(self.canvas, "SVG Conversion Error", "SVG file was not generated by dvisvgm.")
                     return None

                # Read the SVG file
                with open(svg_file, 'rb') as f:
                    svg_data = f.read()

                # Create QSvgRenderer from the SVG data
                renderer = QSvgRenderer(svg_data)
                if not renderer.isValid():
                    print("QSvgRenderer could not load the generated SVG data.")
                    # Try decoding SVG data for logging if it fails
                    try:
                        print(f"Invalid SVG content:\n{svg_data.decode('utf-8', errors='ignore')[:500]}...")
                    except Exception:
                        pass
                    QMessageBox.warning(self.canvas, "SVG Load Error", "Generated SVG data could not be loaded by Qt.")
                    return None

                print("LaTeX rendering successful.")
                return renderer

        except FileNotFoundError as e:
             # This might catch latex/dvisvgm not found if _check_command failed somehow
             print(f"Error rendering LaTeX: Dependency not found - {e}")
             QMessageBox.critical(self.canvas, "Dependency Error", f"Command not found during rendering: {e}")
             return None
        except Exception as e:
            print(f"Error rendering LaTeX: {e}")
            QMessageBox.critical(self.canvas, "Rendering Error", f"An unexpected error occurred during LaTeX rendering: {e}")
            return None

    def _color_to_rgb_values(self):
        """Convert the QColor to RGB values for LaTeX color definition"""
        # Ensure text_color is a valid QColor object
        if isinstance(self.text_color, QColor):
            r = self.text_color.red()
            g = self.text_color.green()
            b = self.text_color.blue()
            return f"{r},{g},{b}"
        else:
            # Fallback to black if color is invalid
            print("Warning: Invalid text_color provided to LatexTextTool. Falling back to black.")
            return "0,0,0"

    def _check_command(self, cmd):
        """Check if a command exists in the system's PATH."""
        from shutil import which
        if which(cmd) is None:
            print(f"Command not found: {cmd}")
            return False
        return True

    def draw(self, painter):
        # No preview needed for this tool
        pass

    def mouseReleaseEvent(self, event):
        pass  # No action needed on release for this tool

    def keyPressEvent(self, event):
        """Handle keyboard events for the LaTeX text tool"""
        # Add any LaTeX text-specific keyboard shortcuts here
        event.ignore()  # Default behavior is to ignore the event

