'''
Entry point for the app.
This just launches the Tkinter GUI. Keep this file small and clean
'''

from assignment3.gui import App  # imports the App class from gui.py

def main():
    app = App() # Initialize the GUI application
    app.mainloop() # Run the Tkinter main loop (blocks until window closed)

if __name__ == "__main__":
    main()
