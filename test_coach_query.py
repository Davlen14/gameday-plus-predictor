import json
from urllib import request

GRAPHQL_URL = "https://graphql.collegefootballdata.com/v1/graphql"
API_KEY = "T0iV2bfp8UKCf8rTV12qsS26USzyDYiVNA7x6WbaV3NOvewuDQnJlv3NfPzr3f/p"

# Try different query approaches
queries = [
    # Approach 1: Search by last name
    '''{ coach(where: {lastName: {_eq: "Smart"}}) { firstName lastName seasons { year school games wins losses } } }''',
    
    # Approach 2: Try team-based query
    '''{ team(where: {school: {_eq: "Georgia"}}) { coaches { firstName lastName seasons { year games wins losses } } } }''',
]

for i, q in enumerate(queries, 1):
    print(f"\n{'='*60}")
    print(f"Query {i}:")
    print(f"{'='*60}")
    payload = {"query": q}
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        GRAPHQL_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as resp:
            body = resp.read()
            result = json.loads(body)
            print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
