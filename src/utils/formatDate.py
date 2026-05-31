from datetime import datetime, timedelta

def days_ago_to_iso(days):
    return (datetime.utcnow() - timedelta(days=days)).isoformat() + 'Z'

def parse_gnews_date_to_iso(date_string):
    return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S GMT").isoformat() + "Z"