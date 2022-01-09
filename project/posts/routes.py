from typing import List
from flask import request
from flask import flash
from flask import g
from flask import session
from flask import abort
from flask import redirect
from flask import url_for
from flask import render_template
from psycopg.rows import class_row

from .forms import CreatePostForm, UpdatePostForm

from .models import Post
from . import post as router
from .. import db


def get_post(id, check_author=True) -> Post:

    post: Post = db.connection.cursor(row_factory=class_row(Post)).execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = %s',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@router.get('/post')
@router.get('/post/')
def get_all_posts():
    
    posts: List[Post] = db.connection.cursor(row_factory=class_row(Post)).execute("SELECT * FROM posts").fetchall()
    return render_template('post/posts.html', posts=posts)


@router.get('/post/<int:post_id>')
def get_post_by_id(post_id: int):
    post = get_post(post_id, check_author=False)
    contexts: dict = dict(
        title='Post - ' + post.title,
        post=post
    )
    return render_template('post/post.html', **contexts)


@router.route('/post/create', methods=['POST', 'GET'])
def create(): 
    
    form: CreatePostForm = CreatePostForm()
    context: dict = dict(
        form=form,
        title='Create post'
    )
    if request.method == 'POST':
        if form.validate_on_submit():

            post = Post(
                title=form.title.data,
                body=form.body.data
            )
            with db.connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO posts (title, body, author_id) VALUES (%s, %s, %s)",
                        (post.title, post.body, g.user.id)
                    )
                except Exception:
                    db.connection.rollback()
                    abort(500)
                else:
                    flash("post has created successfully!", 'success')
                    return redirect(url_for('index'))
                finally:
                    db.connection.close()
    return render_template('post/create.html', **context)


@router.delete('/post/delete/<int:post_id>')
def delete(post_id: int): 
    get_post(post_id)
    with db.connection.cursor() as cursor:
        try:
            cursor.execute('DELETE FROM post WHERE id = ?', (id,))
        except Exception:
            db.connection.rollback()
        else:
            db.connection.commit()
        finally:
            db.connection.close()
    return redirect(url_for('index'))


@router.route('/post/update/<int:post_id>', methods=['GET', 'PUT'])
def update(post_id: int): 
    post = get_post(post_id)
    form = UpdatePostForm(data=post.__dict__)
    context: dict = dict(
        form=form,
        title='Update post ' + post.title
    )
    if request.method == 'PUT':
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data

            with db.connection.cursor() as cursor:
                try:
                    cursor.execute(
                        "UPDATE posts SET title = %s, body = %s"
                        "WHERE id = %s",
                        (post.title, post.body, post.id)
                    )
                except Exception:
                    db.connection.rollback()
                    abort(500)
                else:
                    flash('Post has been updated')
                    db.connection.commit()
                    return redirect(url_for('index'))
                finally:
                    db.connection.close()
    
    return render_template('post/update.html', **context)


