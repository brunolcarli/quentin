"""
System main runner
"""
from quentin.settings.common import TOKEN
from core.commands import client


if __name__ == "__main__":
    client.run(TOKEN)
