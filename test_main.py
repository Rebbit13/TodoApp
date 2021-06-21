import time
import unittest
from unittest import TestCase

import config
from models import db, Task
import main


class TaskTestCase(TestCase):

    def _set_up(self):
        self.db_fd = db
        self.app = main.app.test_client()
        self.db_fd.create_tables([Task])

    def _tear_down(self):
        self.db_fd.close()

    def _get_all(self):
        response = self.app.get("/api/task")
        return response

    def _post(self, title, content):
        response = self.app.post("/api/task",
                                 json={"title": title, "content": content})
        return response

    def _post_without_some_attrs(self, values: dict):
        response = self.app.post("/api/task",
                                 json=values)
        return response

    def _get(self, task_id):
        response = self.app.get(f"/api/task/{task_id}")
        return response

    def _put(self, task_id, title, content):
        response = self.app.put(f"/api/task/{task_id}",
                                json={"title": title, "content": content})
        return response

    def _delete(self, task_id):
        response = self.app.delete(f"/api/task/{task_id}")
        return response

    def _post_test(self):
        # should go right
        r = self._post(title="test_title", content="test_content")
        task = r.json['tasks']
        self.assertEqual({"id": task['id'],
                          "title": task['title'],
                          "content": task['content']},
                         {"id": 1,
                          "title": "test_title",
                          "content": "test_content"})
        # should go wrong and get message
        # ac 'Atrs can not be NULL'
        r = self._post(title="test_title", content=None)
        self.assertEqual(str(r), "<Response streamed [400 BAD REQUEST]>")
        self.assertEqual(r.json['message'], 'Atrs can not be NULL')
        # should not go right, must get 400 resp and msg
        # 'Title length can not be more than 150 chars'
        r = self._post(title="151_char_more_than_150_chars_"
                             "fhghfhfgfhfhgfghfghfhfhhfh"
                             "fhgfhgfhgfhfhfhhgfhgfhhfhfhfhhgfhfhh"
                             "fhgfhgfhfhghfhfgfh"
                             "fhgfghfghfhfhhfhfhgfhgfhgfhfhfhfsdsdsdsdfs",
                       content="test_content")
        self.assertEqual(str(r), "<Response streamed [400 BAD REQUEST]>")
        self.assertEqual(r.json['message'],
                         'Title length can not be more than 150 chars')
        # should go right mast get 200 resp
        r = self._post(title="150_char_more_than_150_chars_fhghfhfgf"
                             "hfhgfghfghfhfhhfh"
                             "fhgfhgfhgfhfhfhhgfhgfhhfhfhfhhgfhfhh"
                             "fhgfhgfhfhghfhfgfh"
                             "fhgfghfghfhfhhfhfhgfhgfhgfhfhfhfsdsdsdsdf",
                       content="test_content")
        self.assertEqual(str(r), "<Response streamed [200 OK]>")
        # should get 400 resp and "Missing required attrs"
        r = self._post_without_some_attrs({'title': "ret"})
        self.assertEqual(str(r), "<Response streamed [400 BAD REQUEST]>")
        self.assertEqual(r.json['message'], "Missing required attrs")
        r = self._post_without_some_attrs({'content': "ret"})
        self.assertEqual(str(r), "<Response streamed [400 BAD REQUEST]>")
        self.assertEqual(r.json['message'], "Missing required attrs")

    def _get_all_test(self):
        r = self._get_all()
        self.assertEqual(len(r.json["tasks"]), 2)

    def _get_test(self):
        r = self._get(2)
        self.assertEqual(r.json["tasks"]['id'], 2)
        r = self._get(54)
        self.assertEqual(str(r), "<Response streamed [404 NOT FOUND]>")

    def _put_test(self):
        r = self._put(2, title="151_char_more_than_150_chars_"
                               "fhghfhfgfhfhgfghfghfhfhhfh"
                               "fhgfhgfhgfhfhfhhgfhgfhhfhfhfhhgfhfhh"
                               "fhgfhgfhfhghfhfgfh"
                               "fhgfghfghfhfhhfhfhgfhgfhgfhfhfhfsdsdsdsdfs",
                      content="test_content")
        self.assertEqual(str(r), "<Response streamed [400 BAD REQUEST]>")
        self.assertEqual(r.json['message'],
                         'Title length can not be more than 150 chars')
        r = self._put(2, title="test_title", content="test_content")
        task = r.json['tasks']
        self.assertEqual({"id": task['id'],
                          "title": task['title'],
                          "content": task['content']},
                         {"id": 2,
                          "title": "test_title",
                          "content": "test_content"})
        r = self._put(2, title="150_char_more_than_150_chars_fhghfhfgf"
                               "hfhgfghfghfhfhhfh"
                               "fhgfhgfhgfhfhfhhgfhgfhhfhfhfhhgfhfhh"
                               "fhgfhgfhfhghfhfgfh"
                               "fhgfghfghfhfhhfhfhgfhgfhgfhfhfhfsdsdsdsdf",
                      content="test_content")
        self.assertEqual(str(r), "<Response streamed [200 OK]>")
        r = self._put(5, title="test_title", content="test_content")
        self.assertEqual(str(r), "<Response streamed [404 NOT FOUND]>")

    def _delete_test(self):
        r = self._delete(2)
        self.assertEqual(str(r), "<Response streamed [200 OK]>")
        r = self._delete(5)
        self.assertEqual(str(r), "<Response streamed [404 NOT FOUND]>")
        r = self._get_all()
        self.assertEqual(len(r.json["tasks"]), 1)

    def test_all(self):
        if config.TESTING is False:
            print('YOU SHOULD SET config.TESTING = True TO USE TEMP DATABASE')
            raise AssertionError
        self._set_up()
        self._post_test()
        self._get_all_test()
        self._get_test()
        self._put_test()
        self._delete_test()
        self._tear_down()


if __name__ == '__main__':
    unittest.main()
