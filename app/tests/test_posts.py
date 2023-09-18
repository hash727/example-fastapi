import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    def validation(post):
        return schemas.PostOut(**post)
    post_map = map(validation, res.json())
    posts_list = list(post_map)
    assert len(res.json()) == len(test_posts)
    # print(res.json())
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorized_user_non_exist_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/898989")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published",[
    ("Awesome First title", "Awesome First content", True),
    ("Favourite Food", "I love biryani", False),
    ("Fav places visit", "I love to visit NZ", True)
])
def test_created_posts(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_posts = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_posts.title == title
    assert created_posts.content == content
    assert created_posts.published == published
    assert created_posts.owner_id == test_user['id']

def test_default_published_set_to_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title":"Some Title", "content":"Some Content"})
    created_posts = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_posts.title == "Some Title"
    assert created_posts.content == "Some Content"
    assert created_posts.published == True
    assert created_posts.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title":"Some Title", "content":"Some Content"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_non_existing_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/8000909")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    update_posts = schemas.Post(**res.json())
    assert res.status_code == 200
    assert update_posts.title == data['title']
    assert update_posts.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json = data)
    assert res.status_code == 403

def test_update_unauthorized_user_post(client, test_user, test_posts):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_update_posts_doesnot_exist(authorized_client, test_user, test_posts):
    data = {
        "title":"updated title",
        "content":"updated content",
        "id":test_posts[0].id
    }
    res = authorized_client.put(f"/posts/808880", json=data)
    assert res.status_code == 404