
#!/usr/bin/env python3
import os
import glob
import json
import subprocess
from datetime import datetime
import fitz  # PyMuPDF

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "/usr/lib/x86_64-linux-gnu/qt5/plugins"
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QListWidget,
                            QListWidgetItem, QLabel, QHBoxLayout, QSplitter,
                            QGraphicsView, QGraphicsScene, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPalette, QFont, QFontDatabase, QPixmap, QImage

# class PDFPreviewWindow(QMainWindow):
#     """Separate window for PDF preview"""
#     def __init__(self, pywal_colors):
#         super().__init__()
#         self.setWindowTitle("PDF Preview")
#         self.setGeometry(100, 100, 800, 900)  # Larger separate window
#         app = QApplication.instance()
#         app.setApplicationName("pdf_preview")
#         # Apply pywal colors
#         self.apply_pywal_theme(pywal_colors)
        
#         # Create central widget
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
        
#         # Create layout
#         layout = QVBoxLayout(central_widget)
#         layout.setContentsMargins(20, 20, 20, 20)
        
#         # Add header
#         header_font = QFont("Hack Nerd Font", 12)
#         header_font.setBold(True)
#         self.title_label = QLabel("PDF Preview")
#         self.title_label.setFont(header_font)
#         self.title_label.setAlignment(Qt.AlignCenter)
#         # layout.addWidget(self.title_label)
        
#         # Add preview view
#         self.preview = QGraphicsView()
#         self.scene = QGraphicsScene(self.preview)
#         self.preview.setScene(self.scene)
#         self.preview.setAlignment(Qt.AlignCenter)
#         self.current_pixmap = None
#         layout.addWidget(self.preview)
        
#         # Add info label at bottom
#         self.info_label = QLabel("")
#         self.info_label.setFont(QFont("Hack Nerd Font", 10))
#         self.info_label.setAlignment(Qt.AlignCenter)
#         # layout.addWidget(self.info_label)
        
#         # Set zoom factor - higher value means more zoomed in
#         self.zoom_factor = 5  # Increased zoom
        
#         # Display initial message
#         # self.display_message("Select a PDF to preview")
        
#     def apply_pywal_theme(self, colors):
#         """Apply pywal colors to the application"""
#         palette = QPalette()
        
#         # Background (window, button, base)
#         bg_color = QColor(colors["colors"]["background"])
#         palette.setColor(QPalette.Window, bg_color)
#         palette.setColor(QPalette.Button, bg_color)
#         palette.setColor(QPalette.Base, QColor(colors["colors"]["color0"]))
        
#         # Foreground (text)
#         fg_color = QColor(colors["colors"]["foreground"])
#         palette.setColor(QPalette.WindowText, fg_color)
#         palette.setColor(QPalette.ButtonText, fg_color)
#         palette.setColor(QPalette.Text, fg_color)
        
#         # Highlights
#         palette.setColor(QPalette.Highlight, QColor(colors["colors"]["color4"]))
#         palette.setColor(QPalette.HighlightedText, QColor(colors["colors"]["color7"]))
        
#         # Apply palette
#         self.setPalette(palette)
        
#     def display_message(self, message):
#         """Show a text message in the preview area"""
#         self.scene.clear()
#         text = self.scene.addText(message, QFont("Hack Nerd Font", 14))
#         text.setDefaultTextColor(QColor(self.palette().color(QPalette.Text)))
#         self.info_label.setText("")
#         self.title_label.setText("PDF Preview")
        
#     def load_pdf_preview(self, pdf_path):
#         """Load the first page of a PDF as preview"""
#         self.scene.clear()
        
#         if not os.path.exists(pdf_path):
#             self.display_message("PDF file not found")
#             return
            
#         try:
#             # Update window title and labels with filename
#             filename = os.path.basename(pdf_path)
#             self.setWindowTitle(f"pdf_preview")
#             self.title_label.setText(f"  {filename}")
            
#             # Open the PDF
#             doc = fitz.open(pdf_path)
#             if doc.page_count > 0:
#                 # Get the first page
#                 page = doc.load_page(0)
                
#                 # Render to an image at a higher resolution
#                 pix = page.get_pixmap(matrix=fitz.Matrix(self.zoom_factor, self.zoom_factor))
                
#                 # Convert to QImage and then QPixmap
#                 img = QImage(pix.samples, pix.width, pix.height, 
#                              pix.stride, QImage.Format_RGB888)
                
#                 pixmap = QPixmap.fromImage(img)
                
#                 # Add to scene and scale to fit view
#                 self.current_pixmap = self.scene.addPixmap(pixmap)
#                 self.preview.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
                
#                 # Update info label
#                 self.info_label.setText(f"Page 1 of {doc.page_count} • {self.get_file_size(pdf_path)}")
                
#             else:
#                 self.display_message("PDF has no pages")
                
#             doc.close()
#         except Exception as e:
#             self.display_message(f"Error loading PDF: {str(e)}")
    
#     def get_file_size(self, file_path):
#         """Format file size in human-readable format"""
#         size_bytes = os.path.getsize(file_path)
#         for unit in ['B', 'KB', 'MB', 'GB']:
#             if size_bytes < 1024.0:
#                 return f"{size_bytes:.1f} {unit}"
#             size_bytes /= 1024.0
#         return f"{size_bytes:.1f} TB"
    
#     def resizeEvent(self, event):
#         """Maintain proper scaling when the view is resized"""
#         if self.current_pixmap:
#             self.preview.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
#         super().resizeEvent(event)

class PDFLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.preview_window = None
        self.pywal_colors = self.load_pywal_colors()
        self.init_ui()
        
    def init_ui(self):
        # Set window properties
        self.setWindowTitle('PDF Launcher')
        self.setGeometry(300, 300, 650, 550)
        
        # Apply pywal colors to app
        self.apply_pywal_theme(self.pywal_colors)
        
        # Create layout with padding
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Set up Hack Nerd Font
        nerd_font = QFont("Hack Nerd Font", 16)
        header_font = QFont("Hack Nerd Font", 14)
        header_font.setBold(True)
        
        # Header with icon
        header = QLabel("  Select a PDF file to open with Zathura")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(header_font)
        layout.addWidget(header)
        
        # PDF list
        self.pdf_list = QListWidget()
        self.pdf_list.setFont(nerd_font)
        self.pdf_list.itemDoubleClicked.connect(self.open_pdf)
        self.pdf_list.currentItemChanged.connect(self.preview_pdf)
        self.pdf_list.setAlternatingRowColors(True)
        self.pdf_list.setFocusPolicy(Qt.StrongFocus)
        layout.addWidget(self.pdf_list)
        
        # Instructions footer
        footer = QLabel("Press Enter or double-click to open file • Select to preview")
        footer_font = QFont("Hack Nerd Font", 9)
        footer_font.setItalic(True)
        footer.setFont(footer_font)
        footer.setAlignment(Qt.AlignCenter)
        # layout.addWidget(footer)
        
        # Set layout
        self.setLayout(layout)
        
        # Populate list with PDF files
        self.populate_pdf_list()
        
        # Set focus to the list for immediate keyboard navigation
        self.pdf_list.setFocus()
        
        # Select first item if available
        if self.pdf_list.count() > 0:
            self.pdf_list.setCurrentRow(0)
            
    def keyPressEvent(self, event):
        """Handle key press events for the window"""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Get current selected item
            current_item = self.pdf_list.currentItem()
            if current_item:
                self.open_pdf(current_item)
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Close preview window when main window closes"""
        if self.preview_window:
            self.preview_window.close()
        super().closeEvent(event)
        
    def load_pywal_colors(self):
        """Load colors from pywal cache"""
        try:
            with open(os.path.expanduser('~/.cache/wal/colors1.json')) as f:
                return json.load(f)
        except Exception:
            # Fallback colors if pywal cache isn't available
            return {
                "colors": {
                    "color0": "#000000",
                    "color1": "#FF0000",
                    "color2": "#00FF00",
                    "color3": "#FFFF00",
                    "color4": "#0000FF",
                    "color5": "#FF00FF",
                    "color6": "#00FFFF",
                    "color7": "#FFFFFF",
                    "color8": "#808080",
                    "background": "#1a1a1a",
                    "foreground": "#d8d8d8"
                }
            }
            
    def apply_pywal_theme(self, colors):
        """Apply pywal colors to the application"""
        palette = QPalette()
        
        # Background (window, button, base)
        bg_color = QColor(colors["colors"]["background"])
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.Button, bg_color)
        palette.setColor(QPalette.Base, QColor(colors["colors"]["color0"]))
        
        # Foreground (text)
        fg_color = QColor(colors["colors"]["foreground"])
        palette.setColor(QPalette.WindowText, fg_color)
        palette.setColor(QPalette.ButtonText, fg_color)
        palette.setColor(QPalette.Text, fg_color)
        
        # Highlights
        palette.setColor(QPalette.Highlight, QColor(colors["colors"]["color4"]))
        palette.setColor(QPalette.HighlightedText, QColor(colors["colors"]["color7"]))
        
        # Alt row colors
        palette.setColor(QPalette.AlternateBase, QColor(colors["colors"]["color0"]).lighter(120))
        
        # Apply palette
        self.setPalette(palette)
        
    def populate_pdf_list(self):
        """Find all PDFs and add to list sorted by most recent"""
        # Find all PDFs in home directory and subdirectories
        home_dir = os.path.expanduser("~/Documents/Kandidat/")
        pdf_files = []
        
        # Get all PDF files with their modification times
        for root, _, files in os.walk(home_dir):
            for file in files:
                if file.lower().endswith('.pdf'):
                    full_path = os.path.join(root, file)
                    try:
                        mod_time = os.path.getmtime(full_path)
                        pdf_files.append((full_path, mod_time))
                    except:
                        pass
        
        # Sort by modification time (most recent first)
        pdf_files.sort(key=lambda x: x[1], reverse=True)
        
        # Add to list widget
        for file_path, mod_time in pdf_files:
            mod_date = datetime.fromtimestamp(mod_time)
            date_str = mod_date.strftime("%Y-%m-%d %H:%M")
            
            # Add PDF icon from Nerd Font
            display_name = f"  {os.path.basename(file_path)} " #- {date_str}"
            item = QListWidgetItem(display_name)
            item.setData(Qt.UserRole, file_path)
            self.pdf_list.addItem(item)
    
    def preview_pdf(self, current, previous):
        """Show preview of the selected PDF in separate window"""
        if current:
            file_path = current.data(Qt.UserRole)
            
            # Create preview window if it doesn't exist
            if not self.preview_window:
                self.preview_window = PDFPreviewWindow(self.pywal_colors)
                
                # Position it to the right of the main window
                preview_x = self.x() + self.width() + 300
                preview_y = self.y()
                self.preview_window.move(preview_x, preview_y)
                self.preview_window.show()
            
            # Update the preview
            self.preview_window.load_pdf_preview(file_path)
            
    def open_pdf(self, item):
        """Open selected PDF with Zathura and close launcher"""
        file_path = item.data(Qt.UserRole)
        
        # Launch Zathura with the PDF
        subprocess.Popen(['zathura', file_path])
        
        # Close the application and preview
        if self.preview_window:
            self.preview_window.close()
        self.close()

def main():
    app = QApplication([])
    
    # Set application name and class for window managers
    app.setApplicationName("PDF Launcher")
    app.setDesktopFileName("pdf_selector")
    
    # Ensure Hack Nerd Font is available
    QFontDatabase.addApplicationFont("/usr/share/fonts/truetype/hack/Hack-Regular.ttf")
    
    launcher = PDFLauncher()
    
    # Center the window on screen
    screen_geometry = app.desktop().screenGeometry()
    x = (screen_geometry.width() - launcher.width()) // 2
    y = (screen_geometry.height() - launcher.height()) // 2
    launcher.move(x, y)
    
    launcher.show()
    app.exec_()

if __name__ == '__main__':
    main()
