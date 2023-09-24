from unittest import TestCase
from app import app
from models import db, connect_db, User, Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views, for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_add_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-3">Create New User</h1>', html)

    def test_handle_add_form(self):
        with app.test_client() as client:
            d = {"first_name": "Test2", "last_name": "User2"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/2"></a>Test2 User2</li>', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get("/users/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-3">Test User Details</h1>', html)




class PostViewsTestCase(TestCase):
    """Tests for views, for Posts."""

    def setUp(self):
        """Add sample post."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name="Test", last_name="User")

        post = Post(title="Test Title", content="Test Content", user_id=user.id)

        db.session.add_all(post, user)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_post_form(self):
        with app.test_client() as client:
            resp = client.get("/users/1/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-3">Add a Post for Test User</h1>', html)

    def test_handle_post_form(self):
        with app.test_client() as client:
            d = {"title": "Test Title 2", "content": "Test Content 2", "user_id": 1}
            resp = client.post(f"/users/{1}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/posts/2">Test Title 2</a></li>', html)