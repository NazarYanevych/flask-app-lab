import unittest

from app import create_app, db
from app.posts import models as post_models  # noqa: F401
from app.users.models import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _create_user(self, username="testuser", email="test@example.com", password="secret123"):
        user = User(username=username, email=email, password="")
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    # 1. Перевірка коректного завантаження сторінок реєстрації та входу (Views Tests)
    def test_register_page_loads(self):
        response = self.client.get("/users/register")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Реєстрація", html)
        self.assertIn("Confirm Password", html)

    def test_login_page_loads(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Вхід у систему", html)
        self.assertIn("Remember Me", html)

    # 2. Тестування збереження користувача у БД при реєстрації
    def test_user_registration_saves_to_db(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "new_user",
                "email": "new_user@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Акаунт для new_user створено!", html)

        user = db.session.scalar(db.select(User).where(User.email == "new_user@example.com"))
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "new_user")
        self.assertNotEqual(user.password, "password123")
        self.assertTrue(user.check_password("password123"))

    # 3. Тестування входу, захисту сторінок і виходу користувача
    def test_login_and_logout_flow(self):
        self._create_user(username="nazarii", email="nazarii@example.com", password="secret123")

        # Неавторизований користувач перенаправляється на /users/login
        unauth_resp = self.client.get("/users/account", follow_redirects=True)
        self.assertIn("Please log in to access this page.", unauth_resp.get_data(as_text=True))

        # Успішний вхід
        login_resp = self.client.post(
            "/users/login",
            data={
                "email": "nazarii@example.com",
                "password": "secret123",
                "remember": False,
            },
            follow_redirects=True,
        )
        self.assertEqual(login_resp.status_code, 200)
        login_html = login_resp.get_data(as_text=True)
        self.assertIn("Welcome, nazarii!", login_html)

        # Доступ до закритого списку користувачів після входу
        users_resp = self.client.get("/users")
        self.assertEqual(users_resp.status_code, 200)
        self.assertIn("Users List (1)", users_resp.get_data(as_text=True))

        # Вихід із системи
        logout_resp = self.client.get("/users/logout", follow_redirects=True)
        self.assertEqual(logout_resp.status_code, 200)
        self.assertIn("Ви вийшли із системи", logout_resp.get_data(as_text=True))

        # Після виходу /users/account знову недоступний
        after_logout_resp = self.client.get("/users/account", follow_redirects=True)
        self.assertIn("Please log in to access this page.", after_logout_resp.get_data(as_text=True))

    def test_login_with_invalid_password(self):
        self._create_user(username="nazarii", email="nazarii@example.com", password="secret123")

        response = self.client.post(
            "/users/login",
            data={
                "email": "nazarii@example.com",
                "password": "wrong_password",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Неправильний email або пароль!", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()