import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='qoE_I9wpwrwGV0-XtFR_KVoCGsMqqwlP6oXjlyHobDK1')

with open('./frenchfries.jpg', 'rb') as images_file:
    classes = visual_recognition.classify(
        images_file,
        threshold='0.6',
	classifier_ids='food').get_result()
print(json.dumps(classes, indent=2))
