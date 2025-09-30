# Entry point of the application.
# This file only imports the GUI class and starts the program.

from assignment3.gui import App  # import the App class from gui.py inside assignment3

def main():
    # Create the main window and start the Tkinter event loop.
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
