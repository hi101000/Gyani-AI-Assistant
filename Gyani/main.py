import sys
import ai
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QScrollArea, QLineEdit

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window properties (title and initial size)
        self.setWindowTitle("Gyani AI Assistant")
        self.setGeometry(100, 100, 500, 400)  # (x, y, width, height)

        # Create a central widget for the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout to arrange the widgets
        layout = QVBoxLayout()

        # Create a QLabel widget to display chat messages
        self.chat_label = QLabel()
        self.scrollArea = QScrollArea(self)
        self.chat_label.setWordWrap(True)  # Wrap long messages
        self.scrollArea.setWidget(self.chat_label)
        self.scrollArea.setWidgetResizable(True)
        layout.addWidget(self.scrollArea)

        # Create a QLineEdit for typing new messages
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...and press Enter key.")
        self.message_input.returnPressed.connect(self.send_message)
        layout.addWidget(self.message_input)

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        # Initialize chat history
        self.chat_history = []

    def send_message(self):
        # Get the message from the input field
        message = self.message_input.text()

        # Append the message to the chat history
        self.chat_history.append(f'User: {message}\n\n\n')

        # Update the chat display
        self.update_chat_display()

        # Clear the input field
        self.sys_message()
        self.message_input.clear()
    
    def sys_message(self):
        message = self.message_input.text()
        message = ai.ask(message)
        self.chat_history.append(f'System: {message}\n\n\n')
        self.update_chat_display()

    def update_chat_display(self):
        # Display the chat history in the QLabel
        chat_text = "\n".join(self.chat_history)
        self.chat_label.setText(chat_text)

def main() -> None:
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
