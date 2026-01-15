from fastapi import status

# def test_create_user_class(client):
#     response = client.post(
#         "/user_class",
#         json={
#             "user_id": 1,
#             "class_id": 1,
#             "trainer_id": 1
#         }
#     )

#     assert response.status_code == status.HTTP_201_CREATED

#     data = response.json()
    #assert response.json() == []

    #assert data["user_id"] == 1
    #assert data["trainer_id"] == 1


def test_get_user_by_id(client):
    response = client.get("/user_class")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    #assert len(response.json()) >= 1