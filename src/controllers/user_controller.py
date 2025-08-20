from flask import request, Response, json, Blueprint
import random
import json
import base64


users = Blueprint("users", __name__)

map_keyframes = "./src/dict/map_keyframes.json"

with open(map_keyframes, 'r') as f:
  KeyframesMapper = json.load(f)

random_video_ids = random.sample(list(KeyframesMapper), 2)
result = []
id = 0
for key in random_video_ids:
    random_frame_ids = random.sample(list(KeyframesMapper[key]),40)
    folder_key, video_key = key.split('_', 1)
    for frame_key in random_frame_ids:
        image_path = f'./src/data/Keyframes/{folder_key}/{video_key}/{frame_key.zfill(4) + ".webp"}'
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        result.append({
                'id': id,
                'folder_key': folder_key,
                'video_key': video_key,
                'frame_key': frame_key,
                'timestamp': KeyframesMapper[key][frame_key],
                'image': encoded_string
            })
        id += 1



@users.route('/', methods = ["GET"])
def handle_home():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 40, type=int)

    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = result[start:end]
    
    response_data = {
        "success": True,
        "data": paginated_data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_items": len(result),
            "total_pages": len(result)//per_page
        }
    }
    return Response(
        response=json.dumps(response_data, indent=2),
        status=200,
        mimetype="application/json"
    )
