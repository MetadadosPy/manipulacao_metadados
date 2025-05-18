def format_time(seconds):
    """Converte segundos para formato mm:ss"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
