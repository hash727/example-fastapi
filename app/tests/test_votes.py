import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, test_user, session):
    my_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(my_vote)
    session.commit()

def test_vote_authorized(authorized_client, test_posts):
    res = authorized_client.post(f"/vote/", json={"post_id":test_posts[3].id, "dir":1})
    assert res.status_code == 201

def test_vote_already_voted_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id":test_posts[3].id, "dir":1})
    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id":test_posts[3].id, "dir":0})
    assert res.status_code == 201

def test_delete_vote_non_exists(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id":test_posts[3].id, "dir":0})
    assert res.status_code == 404

def test_vote_posts_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id":8800, "dir":0})
    assert res.status_code == 404

def test_vote_posts_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id":test_posts[3].id, "dir":1})
    assert res.status_code == 401