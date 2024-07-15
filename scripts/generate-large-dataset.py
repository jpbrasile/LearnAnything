import json
import random
from datetime import datetime, timedelta

def generate_large_dataset(num_users=1000, num_posts=5000, num_comments=20000):
    users = []
    posts = []
    comments = []
    relationships = []

    # Generate users
    for i in range(num_users):
        users.append({
            "id": f"user_{i}",
            "name": f"User {i}",
            "joinDate": (datetime.now() - timedelta(days=random.randint(0, 1000))).isoformat()
        })

    # Generate posts
    for i in range(num_posts):
        author = random.choice(users)
        posts.append({
            "id": f"post_{i}",
            "authorId": author["id"],
            "content": f"This is post number {i}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
            "likes": random.randint(0, 1000)
        })

    # Generate comments
    for i in range(num_comments):
        author = random.choice(users)
        post = random.choice(posts)
        comments.append({
            "id": f"comment_{i}",
            "authorId": author["id"],
            "postId": post["id"],
            "content": f"This is comment number {i}",
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
            "likes": random.randint(0, 100)
        })

    # Generate relationships (friendships)
    for user in users:
        num_friends = random.randint(1, 50)
        friends = random.sample([u for u in users if u != user], num_friends)
        for friend in friends:
            relationships.append({
                "type": "friend",
                "from": user["id"],
                "to": friend["id"]
            })

    # Combine all data
    dataset = {
        "users": users,
        "posts": posts,
        "comments": comments,
        "relationships": relationships
    }

    return dataset

# Generate the dataset
large_dataset = generate_large_dataset()

# Save to file
with open('tests/data/large_real_dataset.json', 'w') as f:
    json.dump(large_dataset, f, indent=2)

print("Dataset generated and saved to tests/data/large_real_dataset.json")
