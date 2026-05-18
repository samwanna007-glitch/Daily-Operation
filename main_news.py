import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.trackers import NewsTracker

if __name__ == "__main__":
    print("Building process")
    NewsTracker().run()