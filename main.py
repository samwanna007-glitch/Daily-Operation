import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.trackers import YouTubeTracker

if __name__ == "__main__":
    YouTubeTracker().run()