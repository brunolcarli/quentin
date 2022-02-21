"""
System main runner.
Execute the main service.
"""
from quentin.settings import TOKEN
from core.commands import client


def run():
    client.run(TOKEN)
