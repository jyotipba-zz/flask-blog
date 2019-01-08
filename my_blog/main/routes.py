from flask import  Blueprint , render_template, request
from my_blog.models import Post

main = Blueprint('main' , __name__)

@main.route('/')
@main.route('/home')
def home():
     page = request.args.get('page', 1, type=int)
     posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=2)
     return render_template('home.html' , title = 'home', posts=posts)
