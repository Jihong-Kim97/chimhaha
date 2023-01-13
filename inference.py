import requests

API_URL = "https://api-inference.huggingface.co/models/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

output = query({
    "inputs": "장사잘되서 근심걱정 다 날리게 해주세요!",
    "parameters": {"candidate_labels": ["부자","건강","애정","행운","진로"]},
})
print(output)