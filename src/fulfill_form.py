from src.parse_user_data import data
from src.create_executors import executors
from get_access import services

import os


def fulfill_form():

    images = {}
    for filename in os.listdir(data['imagesFolder']):
        if any([filename.endswith("." + ext) for ext in data['imagesExtensions']]):
            author = filename.rsplit('.', 1)[0]
            path = os.path.join(data['imagesFolder'], filename)
            images[author] = executors['drive'].upload_image(path)

    with open("assets/active.txt", "a") as f:
        f.write(str(images.keys().__sizeof__()))

    requests = []
    for i, author in enumerate(images.keys()):
        requests.append({
            "createItem": {
                "item": {
                    "title": author,
                    "questionItem": {
                        "question": {
                            "required": False,
                            "scaleQuestion": {
                                "low": 1,
                                "high": data['questionScale'],
                            }
                        }
                    }
                },
                "location": {
                    "index": i * 2
                }
            }
        })

        if author in images:
            requests.append({
                "createItem": {
                    "item": {
                        "imageItem": {
                            "image": {
                                "sourceUri": images[author],
                                "altText": f"Image for question: {author}"
                            }
                        }
                    },
                    "location": {
                        "index": i * 2 + 1
                    }
                }
            })

    batch_update_request = {
        "requests": requests
    }

    services['forms'].forms().batchUpdate(
        formId=executors['form'].id,
        body=batch_update_request
    ).execute()
