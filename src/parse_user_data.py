import json

"""
users.json is all you have to configure when setting up this project.
"""

with open('../user.json') as f:
    data = json.load(f)