from flask import Flask, request, jsonify
from models import Post, db
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)

#---------------configurations--------------------
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)


# Define api routes
#----------------------------home route----------------------------
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message' : "Welkam to Flask home!"}), 200

#-----------------------------create post--------------------------
@app.route('/posts', methods=['POST'])
def create_post():
    # Get the data being posted to create a post
    data = request.get_json()
    title = data.get('title')
    body = data.get('body')
    image_url = data.get('image_url')

    # Check for data availability
    if not data or not title or not body or not image_url:
        return jsonify({'message' : 'All fields required'})
    
    # Create new post
    new_post = Post(title=title, body=body, image_url=image_url)
    db.session.add(new_post)
    db.session.commit()

    response = {'message' : 'Post created successfully', 'post' : new_post.to_dict()}
    return jsonify(response), 200

#-----------------------------get all posts-------------------------
@app.route('/posts', methods=['GET'])
def get_posts():
    try:
        posts = Post.query.all()
        if not posts:
            return jsonify({'message' : 'No posts found'}), 404
        response = [post.to_dict() for post in posts]
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#-----------------------------get post by id-------------------------
@app.route('/posts/<int:id>', methods=['GET'])
def get_post_by_id(id):
    data = Post.query.filter_by(id=id).first()
    if not data:
        return jsonify({'message' : 'Post not found.'}), 404
    response = data.to_dict()
    return jsonify(response), 200
    
#-----------------------------update post----------------------------
@app.route('/posts/<int:id>', methods=['PUT', 'PATCH'])
def update_post(id):
    data = request.get_json()

    # Extract key values
    title = data.get('title')
    body = data.get('body')
    image_url = data.get('image_url')

    # Validate input
    if not title or not body or not image_url:
        return jsonify({'message': 'All fields are required'}), 400

    # Find the existing post we want to update
    post = Post.query.get_or_404(id)

    # Update the post's fields
    post.title = title
    post.body = body
    post.image_url = image_url

    # Commit the changes
    db.session.commit()

    # Return the response in json format
    return jsonify({'message': 'Post updated successfully', 'post': post.to_dict()}), 200

#--------------------------delete post--------------------------
@app.route('/posts/<int:id>', methods=['DELETE']) 
def delete_post(id):
    # Fetch the post by ID or return 404 if not found
    post = Post.query.get_or_404(id)

    # Delete the post from the session
    db.session.delete(post)

    # Commit the deletion
    db.session.commit()

    # Return a success message
    response = {'message': 'Post deleted successfully', 'post': post.to_dict()}
    return jsonify(response), 200
    
    
    



if __name__ == "__main__":
    app.run(debug=False)
