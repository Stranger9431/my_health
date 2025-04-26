import json
from api.models import Tip

with open('tips.json', 'r') as f:
    tips = json.load(f)

for tip_data in tips:
    Tip.objects.create(text=tip_data['text'])

print(f"{len(tips)} tips loaded successfully!")
