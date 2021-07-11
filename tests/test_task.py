import unittest
from unittest import TestCase

from app import app
from models.task import Task
from peewee import SqliteDatabase

test_db = SqliteDatabase(":memory:")


class TaskTestCase(TestCase):
    task_path = "/api/task/"
    task_path_id_1 = "/api/task/1/"
    task_path_id_100 = "/api/task/100/"

    correct_json = {"title": "some title",
                    "content": "some content"}

    missing_argument_title = {"content": "some content"}
    missing_argument_content = {"title": "some title"}
    missing_arguments_all = {}

    title_less_chars = {"title": "",
                        "content": "some content"}
    content_less_chars = {"title": "some title",
                          "content": ""}

    title_more_chars = {"title": "s" * 151,
                        "content": "some content"}

    typo_title = {"tutle": "some title",
                  "content": "some content"}
    typo_content = {"title": "some title",
                    "cuntent": "some content"}

    def _set_up(self):
        self.app = app.test_client()
        test_db.bind([Task], bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables([Task])
        self.app.post("/api/task/",
                      json=self.correct_json)

    @staticmethod
    def _tear_down():
        test_db.drop_tables([Task])
        test_db.close()


class PostTaskTestCase(TaskTestCase):

    def test_post_success(self):
        self._set_up()
        r = self.app.post(self.task_path,
                          json=self.correct_json)
        self.assertEqual(r.status_code, 201)
        self._tear_down()

    def test_post_missing_argument_title(self):
        self._set_up()
        r = self.app.post(self.task_path,
                          json=self.missing_argument_title)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_post_missing_argument_content(self):
        self._set_up()
        r = self.app.post(self.task_path,
                          json=self.missing_argument_content)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_post_missing_arguments_all(self):
        self._set_up()
        r = self.app.post(self.task_path,
                          json=self.missing_arguments_all)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_post_title_less_chars(self):
        self._set_up()
        r = self.app.post(self.task_path,
                          json=self.title_less_chars)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_post_content_less_chars(self):
        self._set_up()
        r = self.app.post(self.task_path,
                          json=self.content_less_chars)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_post_title_more_chars(self):
        self._set_up()
        r = self.app.post(self.task_path,
                          json=self.title_more_chars)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_post_typo_title(self):
        self._set_up()
        r = self.app.post(self.task_path,
                          json=self.typo_title)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_post_typo_content(self):
        self._set_up()
        r = self.app.post(self.task_path,
                          json=self.typo_content)
        self.assertEqual(r.status_code, 400)
        self._tear_down()


class GetTaskTestCase(TaskTestCase):

    def test_get_all(self):
        self._set_up()
        r = self.app.get(self.task_path)
        self.assertEqual(r.status_code, 200)
        self._tear_down()

    def test_get_success(self):
        self._set_up()
        r = self.app.get(self.task_path_id_1)
        self.assertEqual(r.status_code, 200)
        self._tear_down()

    def test_get_fail(self):
        self._set_up()
        r = self.app.get(self.task_path_id_100)
        self.assertEqual(r.status_code, 404)
        self._tear_down()


class DeleteTaskTestCase(TaskTestCase):

    def test_delete_success(self):
        self._set_up()
        r = self.app.delete(self.task_path_id_1)
        self.assertEqual(r.status_code, 200)
        self._tear_down()

    def test_delete_fail(self):
        self._set_up()
        r = self.app.delete(self.task_path_id_100)
        self.assertEqual(r.status_code, 404)
        self._tear_down()


class PutTaskTestCase(TaskTestCase):

    def test_put_success(self):
        self._set_up()
        r = self.app.put(self.task_path_id_1,
                         json=self.correct_json)
        self.assertEqual(r.status_code, 201)
        self._tear_down()

    def test_put_fail_not_found(self):
        self._set_up()
        r = self.app.put(self.task_path_id_100,
                         json=self.correct_json)
        self.assertEqual(r.status_code, 404)
        self._tear_down()

    def test_put_missing_argument_title(self):
        self._set_up()
        r = self.app.put(self.task_path_id_1,
                         json=self.missing_argument_title)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_put_missing_argument_content(self):
        self._set_up()
        r = self.app.put(self.task_path_id_1,
                         json=self.missing_argument_content)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_put_missing_arguments_all(self):
        self._set_up()
        r = self.app.put(self.task_path_id_1,
                         json=self.missing_arguments_all)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_put_title_less_chars(self):
        self._set_up()
        r = self.app.put(self.task_path_id_1,
                         json=self.title_less_chars)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_put_content_less_chars(self):
        self._set_up()
        r = self.app.put(self.task_path_id_1,
                         json=self.content_less_chars)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_put_title_more_chars(self):
        self._set_up()
        r = self.app.put(self.task_path_id_1,
                         json=self.title_more_chars)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_put_typo_title(self):
        self._set_up()
        r = self.app.put(self.task_path_id_1,
                         json=self.typo_title)
        self.assertEqual(r.status_code, 400)
        self._tear_down()

    def test_put_typo_content(self):
        self._set_up()
        r = self.app.put(self.task_path_id_1,
                         json=self.typo_content)
        self.assertEqual(r.status_code, 400)
        self._tear_down()


if __name__ == '__main__':
    unittest.main()
