import webhooks
import display
import threading
import multiprocessing

if __name__ == "__main__":
    THWebhooks = multiprocessing.Process(target=webhooks.setup)
    THWebhooks.start()
    
    THDisplay = multiprocessing.Process(target=display.setup)
    THDisplay.start()