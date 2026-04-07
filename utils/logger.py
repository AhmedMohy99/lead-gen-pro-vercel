from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path('logs/app.log')



def log(message: str) -> None:
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    line = f'[{timestamp}] {message}'
    print(line)

    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open('a', encoding='utf-8') as file:
            file.write(line + '\n')
    except OSError:
        # Vercel file system is ephemeral; printing still preserves logs in deployment output.
        pass
