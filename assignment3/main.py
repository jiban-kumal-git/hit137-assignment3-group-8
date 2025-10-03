'''
Entry point for the app.
This just launches the Tkinter GUI. Keep this file small and clean
'''

from assignment3.gui import App  # imports the App class from gui.py

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()