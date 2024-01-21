from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Existing YouTube comments API endpoint
YOUTUBE_API_URL = "https://app.ylytic.com/ylytic/test"

def get_youtube_comments(params):
    response = requests.get(YOUTUBE_API_URL, params=params)
    return response.json()

def filter_comments(comments, filters):
    filtered_comments = comments

    # Filter by author name
    if 'search_author' in filters:
        filtered_comments = [c for c in filtered_comments if c['author'] == filters['search_author']]

    # Filter by date range
    if 'at_from' in filters and 'at_to' in filters:
        filtered_comments = [c for c in filtered_comments if filters['at_from'] <= c['at'] <= filters['at_to']]

    # Filter by like and reply count range
    if 'like_from' in filters and 'like_to' in filters:
        filtered_comments = [c for c in filtered_comments if filters['like_from'] <= c['like'] <= filters['like_to']]

    if 'reply_from' in filters and 'reply_to' in filters:
        filtered_comments = [c for c in filtered_comments if filters['reply_from'] <= c['reply'] <= filters['reply_to']]

    # Filter by search text
    if 'search_text' in filters:
        filtered_comments = [c for c in filtered_comments if filters['search_text'].lower() in c['text'].lower()]

    return filtered_comments

@app.route('/search_comments', methods=['GET'])
def search_comments():
    search_params = {
        'search_author': request.args.get('search_author'),
        'at_from': request.args.get('at_from'),
        'at_to': request.args.get('at_to'),
        'like_from': request.args.get('like_from'),
        'like_to': request.args.get('like_to'),
        'reply_from': request.args.get('reply_from'),
        'reply_to': request.args.get('reply_to'),
        'search_text': request.args.get('search_text'),
    }

    youtube_params = {
        'page': request.args.get('page', 1),
        'per_page': request.args.get('per_page', 10),
    }

    youtube_comments = get_youtube_comments(youtube_params)
    filtered_comments = filter_comments(youtube_comments, search_params)

    return jsonify(filtered_comments)

if __name__ == '__main__':
    app.run(debug=True)