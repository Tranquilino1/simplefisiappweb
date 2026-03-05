import os
import sys
import webbrowser
from threading import Timer

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DeLasGargolasChat.settings')
    
    # Add project directory to path
    if getattr(sys, 'frozen', False):
        # We are running via PyInstaller
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, BASE_DIR)

    import django
    django.setup()
    
    from django.core.management import call_command
    print("Iniciando DeLasGargolas Chat Server...")
    print("Aplicando base de datos a espacio de trabajo actual...")
    call_command("migrate", interactive=False)
    
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:8000/")
        
    # Open the browser automatically after brief delay
    Timer(1.5, open_browser).start()
    
    # Run ASGI using Daphne
    from daphne.cli import CommandLineInterface
    cli = CommandLineInterface()
    cli.run(["-p", "8000", "-b", "127.0.0.1", "DeLasGargolasChat.asgi:application"])
