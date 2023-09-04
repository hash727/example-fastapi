from fastapi import status, HTTPException, Depends,  APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models,schemas, oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", response_model= List[schemas.Post])
@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    #print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #this is query of posts with number of votes << Left outer join table
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #post_dict = post.dict()
    #post_dict["id"] = randrange(0, 100000)
    #my_posts.append(post_dict)
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.publish))
    
    #new_post = cursor.fetchone()
    #conn.commit()
    #print(**post.model_dump())
    #print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #posts = find_posts(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # posts = cursor.fetchone()
    #posts = db.query(models.Post).filter_by(id=id).first()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(posts)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts with id = {id} not found.")
    return posts

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    #index = find_index_post(id)
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # del_post = cursor.fetchone()
    del_post = db.query(models.Post).filter_by(id=id)
    if del_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts with id = {id} not found. please try with different id")
    
    if del_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Current user is not authorized to modify or delete the post")
    #my_posts.pop(index)
    del_post.delete(synchronize_session = False)   
    db.commit()
    #conn.commit()
    #return {"message":f"The post with id = {id} was deleted"}
    #Response(status_code=status.HTTP_204_NO_CONTENT)
    return {"data" : del_post, "message" : f"The above post with id = {id} deleted successfully !"}

@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, post: schemas.PostCreate,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #index = find_index_post(id)
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.publish, str(id)))
    # update_post = cursor.fetchone()
    update_post = db.query(models.Post).filter_by(id=id)
    if update_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts with id = {id} not found. please try with different id")
    
    if update_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthorized access to the current post !")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    update_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    #conn.commit()
    return update_post.first()