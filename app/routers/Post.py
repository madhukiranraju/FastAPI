from fastapi import FastAPI, Body, Response, HTTPException, status, Depends, APIRouter
from .. import schemas, Model, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# @router.get("/", response_model=list[schemas.Post])
@router.get("/", response_model=list[schemas.PostVoteOut])
async def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), 
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #SQL Alchemy
    # posts = db.query(Model.Post).filter(Model.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(Model.Post, func.count(Model.Vote.post_id).label("votes")).join(
        Model.Vote, Model.Vote.post_id == Model.Post.id, isouter=True
    ).group_by(Model.Post.id)
    
    return results.limit(limit).offset(skip).all()

    ### SQL
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    # return  posts

# @router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostVoteOut)
async def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    #sQL Alchemy
    # post = db.query(Model.Post).filter(Model.Post.id == id).first()
    post = db.query(Model.Post, func.count(Model.Vote.post_id).label("votes")).join(
        Model.Vote, Model.Vote.post_id == Model.Post.id, isouter=True
    ).group_by(Model.Post.id).filter(Model.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )
    return post


    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
    # fetchedPost = cursor.fetchone()
    # if not fetchedPost:
    #      raise HTTPException(
    #           status_code=status.HTTP_404_NOT_FOUND,
    #           detail=f"Post with id: {id} was not found"
    #      )
    # return {"post_detail": fetchedPost}


# async def get_post(id: int, response: Response):
#     post = find_post(id)
#     if not post: 
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"post_detail": f"Post with id: {id} was not found"}
#     return {"post_detail": post}


# async def get_post(id: int, response: Response):
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {id} was not found"
    #     )
    # return {"post_detail": post}
    # post = find_post(id)
    # if post:
    #     return {"post_detail": post}
    # else:
    #     return {"message": "post not found"}

# def find_post(id: int):
#     for post in my_posts:
#         if post['id'] == int(id):
#             return post


# def find_index_post(id: int):
#     for index, post in enumerate(my_posts):
#         if post['id'] == int(id):
#             return index


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    #SQL Alchemy
    # new_post = Model.Post(title=post.title, content=post.content, published=post.published)
    #if the there are many fields in the model then instead of writing each field we can unpack the object
    new_post = Model.Post(owner_id = current_user.id, **post.model_dump(exclude={"id"}))  # Unpacking the post object    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

    ### SQL
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data": new_post}

    # print(post)
    # #converting pydantic model to dictionary
    # print(post.model_dump)
    # dict = post.model_dump()
    # dict['id'] = randrange(0, 10000000)
    # my_posts.append(dict)
    # return dict
    # return {"post": f"title is {post.title} content is {post.content} and published is {post.published} and rated as {post.rating}"}


# always check the path operation order, specific to general

# my_posts = [
#     {"id": 1, " title": "title of post 1", "content": "content of post 1"},
#     {"id": 2, "title": "title of post 2", "content": "content of post 2"}
# ]

# @router.get("/latest")
# async def get_latest_post():
#     post = my_posts[-1]
#     return {"latest_post": post}



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    # SQL Alchemy
    post = db.query(Model.Post).filter(Model.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    ### SQL
    # cursor.execute("DELETE FROM POSTS WHERE id = %s RETURNING *", (str(id)))
    # deletedPost = cursor.fetchone()
    # conn.commit()
    # if deletedPost is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {id} does not exist"
    #     )
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


# async def delete_post(id: int):
#     index = find_index_post(id)
#     if index is not None:
#         my_posts.pop(index)
#         return Response(status_code=status.HTTP_204_NO_CONTENT) 
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id: {id} does not exist"
#         )
    
@router.put("/{id}")
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    # SQL Alchemy
    post_query = db.query(Model.Post).filter(Model.Post.id == id)
    existing_post = post_query.first()
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )
    update_data = post.model_dump(exclude_none=True)

    post_query.update(update_data, synchronize_session=False) # type: ignore
    
    db.commit()
    return {"data": post_query.first()}

    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Post with id: {id} does not exist"
    #     )
    # return {"data": updated_post}


# async def update_post(id: int, post: Post):
#     index = find_index_post(id)
#     if index is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id: {id} does not exist"
#         )
#     post_dict = post.model_dump()
#     post_dict['id'] = id
#     my_posts[index] = post_dict
#     return {"data": my_posts[index]}


# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

#     #SQL Alchemy
#     # new_post = Model.Post(title=post.title, content=post.content, published=post.published)
#     #if the there are many fields in the model then instead of writing each field we can unpack the object
#     new_post = Model.Post(**post.model_dump(exclude={"id"}))  # Unpacking the post object    
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post
