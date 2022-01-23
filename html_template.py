import json
import os
def read_comments():
    if os.path.isfile('comment.txt'):
        with open("comment.txt", "r") as file:
            content = file.read()
            if content != "":
                return content
            else:
                return "no comment posted yet"
    else:
        return "problem loading the comments"


def create_html():
    with open('form.html', 'w') as file:
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="style.css">
            <title>Form</title>
        </head>
        <body>
            <h1>Custom web server</h1>
            <h3>This is Dynamically generated HTML page</h3>
            <ul>
                <a href="/">Home</a>
                <a href='form.html'>Form</a>

            </ul>
            <h4>Post a public comment</h4>
            <form method="post">
                <input required placeholder="Enter your name" name="name"/><br/>
                <textarea name='comment' rows="6" cols="35" placeholder="write a message here(short)" required></textarea></br>
                <i>After you post, the message cannot be deleted</i></br>
                <button type="submit">Post</button>
            </form>
            <h4>posted comments</h4>
            <p id="comment">"""+read_comments()+"""
             
        </body>
        </html>
        """ 
        file.write(html_template)
        file.close