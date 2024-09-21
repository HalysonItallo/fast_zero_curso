import freezegun
from fastapi import status

from fast_zero.todos.models import TodoState
from tests.conftest import TodoFactory


def test_create_todo(client, token):
    payload = {
        "title": "Test todo",
        "description": "Test todo description",
        "state": "draft",
    }

    response = client.post(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )

    payload["id"] = 1

    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["state"] == payload["state"]


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_pagination_should_return_2_todos(session, client, user, token):
    expected_todos = 2

    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        "/todos/?offset=1&limit=2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todo_filter_title_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, title="Test todo 1"))
    session.commit()

    response = client.get(
        "/todos/?title=Test todo 1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todo_filter_description_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, description="description"))
    session.commit()

    response = client.get(
        "/todos/?description=desc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todo_filter_state_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft))
    session.commit()

    response = client.get(
        "/todos/?state=draft",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_filter_combined_should_return_5_todos(session, client, user, token):
    expected_todo = 5

    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title="Test todo combined",
            description="test todo combined",
            state=TodoState.done,
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title="Other todo",
            description="other todo description",
            state=TodoState.todo,
        )
    )

    session.commit()

    response = client.get(
        "/todos/?title=Test todo combined&description=combined&state=done",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert len(response.json()["todos"]) == expected_todo


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(
        f"/todos/{todo.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_todo_should_be_raise_with_not_exist_todo(client, token):
    response = client.delete(
        "/todos/10",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f"/todos/{todo.id}",
        json={"title": "teste!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "teste!"


def test_patch_should_be_raise_with_not_exist_todo(client, token):
    response = client.patch(
        "/todos/10",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task not found"}
