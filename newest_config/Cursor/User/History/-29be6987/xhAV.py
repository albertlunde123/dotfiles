import os
import tempfile
import subprocess
from PyQt5.QtSvg import QSvgRenderer

class LatexRenderer:
    """Class for rendering LaTeX code to SVG."""
    
    def __init__(self):
        self.cache = {}  # Cache for rendered SVGs
        
    def render(self, latex_code, color=None):
        """Render LaTeX code to SVG.
        
        Args:
            latex_code (str): The LaTeX code to render
            color (QColor, optional): The color to use for the text
            
        Returns:
            QSvgRenderer: A renderer for the SVG, or None if rendering failed
        """
        # Check cache first
        cache_key = f"{latex_code}_{color.name() if color else 'default'}"
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.tex', delete=False) as tex_file, \
             tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as svg_file:
            
            tex_path = tex_file.name
            svg_path = svg_file.name
            
            # Write LaTeX document
            tex_content = self._create_latex_document(latex_code, color)
            tex_file.write(tex_content.encode())
            tex_file.flush()
            
            try:
                # Run pdflatex to create PDF
                subprocess.run([
                    'pdflatex',
                    '-interaction=nonstopmode',
                    '-output-format=pdf',
                    tex_path
                ], check=True, capture_output=True)
                
                # Convert PDF to SVG using pdf2svg
                subprocess.run([
                    'pdf2svg',
                    tex_path.replace('.tex', '.pdf'),
                    svg_path
                ], check=True, capture_output=True)
                
                # Create renderer
                renderer = QSvgRenderer(svg_path)
                if renderer.isValid():
                    # Cache the renderer
                    self.cache[cache_key] = renderer
                    return renderer
                    
            except subprocess.CalledProcessError as e:
                print(f"Error rendering LaTeX: {e}")
                print(f"stdout: {e.stdout.decode()}")
                print(f"stderr: {e.stderr.decode()}")
                
            finally:
                # Clean up temporary files
                try:
                    os.remove(tex_path)
                    os.remove(tex_path.replace('.tex', '.pdf'))
                    os.remove(tex_path.replace('.tex', '.log'))
                    os.remove(tex_path.replace('.tex', '.aux'))
                    os.remove(svg_path)
                except OSError:
                    pass
                    
        return None
        
    def _create_latex_document(self, latex_code, color=None):
        """Create a complete LaTeX document with the given code.
        
        Args:
            latex_code (str): The LaTeX code to include
            color (QColor, optional): The color to use for the text
            
        Returns:
            str: The complete LaTeX document
        """
        color_def = ""
        if color:
            color_def = f"\\definecolor{{textcolor}}{{RGB}}{{{color.red()},{color.green()},{color.blue()}}}"
            
        return f"""\\documentclass[preview]{{standalone}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{color}}
{color_def}
\\begin{{document}}
{color_def and '\\color{textcolor}' or ''}
{latex_code}
\\end{{document}}
""" 