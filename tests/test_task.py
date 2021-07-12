import unittest
from unittest import TestCase

from app import app
from models.task import Task
from peewee import SqliteDatabase

app.testing = True

test_db = SqliteDatabase(":memory:")


class TaskTest(TestCase):
    def setUp(self):
        self.app = app.test_client()
        test_db.bind([Task], bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables([Task])
        self.test_task = Task(title="title", content="content")
        self.test_task.save()

    def tearDown(self):
        self.app.delete()
        test_db.drop_tables([Task])
        test_db.close()

    def test_post_success(self):
        r = self.app.post("/api/task/",
                          json={"title": "some title", "content": "some content"})
        self.assertEqual(r.status_code, 201)

    def test_post_missing_argument_title(self):
        r = self.app.post("/api/task/",
                          json={"content": "some content"})
        self.assertEqual(r.status_code, 400)

    def test_post_missing_argument_content(self):
        r = self.app.post("/api/task/",
                          json={"title": "some title"})
        self.assertEqual(r.status_code, 400)

    def test_post_missing_arguments_all(self):
        r = self.app.post("/api/task/",
                          json={})
        self.assertEqual(r.status_code, 400)

    def test_post_title_less_chars(self):
        r = self.app.post("/api/task/",
                          json={"title": "", "content": "some content"})
        self.assertEqual(r.status_code, 400)

    def test_post_content_less_chars(self):
        r = self.app.post("/api/task/",
                          json={"title": "some title", "content": ""})
        self.assertEqual(r.status_code, 400)

    def test_post_title_more_chars(self):
        r = self.app.post("/api/task/",
                          json={"title": "s" * 151, "content": "some content"})
        self.assertEqual(r.status_code, 400)

    def test_post_typo_title(self):
        r = self.app.post("/api/task/",
                          json={"tutle": "some title", "content": "some content"})
        self.assertEqual(r.status_code, 400)

    def test_post_typo_content(self):
        r = self.app.post("/api/task/",
                          json={"title": "some title", "cuntent": "some content"})
        self.assertEqual(r.status_code, 400)

    def test_get_all(self):
        r = self.app.get("/api/task/")
        self.assertEqual(r.status_code, 200)

    def test_get_success(self):
        r = self.app.get("/api/task/1/")
        self.assertEqual(r.status_code, 200)

    def test_get_fail(self):
        r = self.app.get("/api/task/100/")
        self.assertEqual(r.status_code, 404)

    def test_delete_success(self):
        r = self.app.delete("/api/task/1/")
        self.assertEqual(r.status_code, 200)

    def test_delete_fail(self):
        r = self.app.delete("/api/task/100/")
        self.assertEqual(r.status_code, 404)

    def test_put_success(self):
        r = self.app.put("/api/task/1/",
                         json={"title": "some title", "content": "some content"})
        self.assertEqual(r.status_code, 201)

    def test_put_fail_not_found(self):
        r = self.app.put("/api/task/100/",
                         json={"title": "some title", "content": "some content"})
        self.assertEqual(r.status_code, 404)

    def test_put_missing_argument_title(self):
        r = self.app.put("/api/task/1/",
                         json={"content": "some content"})
        self.assertEqual(r.status_code, 400)

    def test_put_missing_argument_content(self):
        r = self.app.put("/api/task/1/",
                         json={"title": "some title"})
        self.assertEqual(r.status_code, 400)

    def test_put_missing_arguments_all(self):
        r = self.app.put("/api/task/1/",
                         json={})
        self.assertEqual(r.status_code, 400)

    def test_put_title_less_chars(self):
        r = self.app.put("/api/task/1/",
                         json={"title": "", "content": "some content"})
        self.assertEqual(r.status_code, 400)

    def test_put_content_less_chars(self):
        r = self.app.put("/api/task/1/",
                         json={"title": "some title", "content": ""})
        self.assertEqual(r.status_code, 400)

    def test_put_title_more_chars(self):
        r = self.app.put("/api/task/1/",
                         json={"title": "s" * 151, "content": "some content"})
        self.assertEqual(r.status_code, 400)

    def test_put_typo_title(self):
        r = self.app.put("/api/task/1/",
                         json={"tutle": "some title", "content": "some content"})
        self.assertEqual(r.status_code, 400)

    def test_put_typo_content(self):
        r = self.app.put("/api/task/1/",
                         json={"title": "some title", "cuntent": "some content"})
        self.assertEqual(r.status_code, 400)


if __name__ == '__main__':
    unittest.main()
