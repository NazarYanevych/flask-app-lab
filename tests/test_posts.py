import unittest

from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def make_post(self, title="Test post", content="Test content", **kwargs):
        """Допоміжний метод: створює пост у БД і повертає його id."""
        with self.app.app_context():
            post = Post(title=title, content=content, **kwargs)
            db.session.add(post)
            db.session.commit()
            return post.id


    def test_create_post(self):
        response = self.client.post("/post/create", data={
            "title": "My first post",
            "content": "This is TDD!",
            "category": "tech",
            "publish_date": "2026-11-16T12:00",
            "is_active": "y",
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post added successfully", response.data)

        with self.app.app_context():
            post = db.session.scalar(db.select(Post).where(Post.title == "My first post"))
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD!")
            self.assertEqual(post.author, "Anonymous")

    def test_create_post_invalid(self):
        response = self.client.post("/post/create", data={
            "title": "A",          # занадто короткий заголовок
            "content": "",
            "category": "tech",
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            self.assertEqual(len(db.session.scalars(db.select(Post)).all()), 0)

    def test_create_post_author_from_session(self):
        with self.client.session_transaction() as sess:
            sess["username"] = "admin"

        self.client.post("/post/create", data={
            "title": "Admin post",
            "content": "Written by admin",
            "category": "news",
            "publish_date": "2026-11-16T12:00",
        })

        with self.app.app_context():
            post = db.session.scalar(db.select(Post).where(Post.title == "Admin post"))
            self.assertEqual(post.author, "admin")


    def test_list_posts(self):
        self.make_post(title="Visible post")
        self.make_post(title="Hidden post", is_active=False)

        response = self.client.get("/post")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Visible post", response.data)
        self.assertNotIn(b"Hidden post", response.data)


    def test_view_post_detail(self):
        post_id = self.make_post(title="Detail post", content="Full content here")

        response = self.client.get(f"/post/{post_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detail post", response.data)
        self.assertIn(b"Full content here", response.data)


    def test_update_post(self):
        post_id = self.make_post(title="Old title", content="Old content")

        response = self.client.post(f"/post/{post_id}/update", data={
            "title": "New title",
            "content": "New content",
            "category": "news",
            "publish_date": "2026-11-16T12:00",
            "is_active": "y",
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post updated successfully", response.data)

        with self.app.app_context():
            post = db.session.get(Post, post_id)
            self.assertEqual(post.title, "New title")
            self.assertEqual(post.category, "news")

    def test_delete_confirm_page(self):
        post_id = self.make_post(title="To delete")

        response = self.client.get(f"/post/delete/{post_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"To delete", response.data)

    def test_delete_post(self):
        post_id = self.make_post(title="To delete")

        response = self.client.post(f"/post/delete/{post_id}", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Post deleted successfully", response.data)

        with self.app.app_context():
            self.assertIsNone(db.session.get(Post, post_id))

    def test_404_not_found(self):
        response = self.client.get("/post/9999")

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Page Not Found", response.data)


if __name__ == "__main__":
    unittest.main()