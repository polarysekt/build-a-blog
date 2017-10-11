#! /usr/bin/python3

# app.py
# Build A Blog
# 2017, polarysekt

# imports
from flask import Flask, Markup, request, redirect, url_for, render_template

from flask_sqlalchemy import SQLAlchemy

from random import randint

from gh_slogan import *
from gh_poker import *

# init Flask w/ Debugging
g_app = Flask( __name__ )
g_app.config['DEBUG'] = True
g_app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:3306/build-a-blog'
g_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#g_app.config['SQLALCHEMY_ECHO' ] = True

g_db = SQLAlchemy(g_app)

#g_app.add_url_rule('/favicon.ico', redirect_to=url_for('static',filename='favicon.ico'))


g_ghSITE_NAME = "Build-A-Blog"
g_ghSITE_VERSION = "2017.10.09::[gsh]"

class BlogEntry(g_db.Model):
    id = g_db.Column(g_db.Integer, primary_key=True)
    title = g_db.Column(g_db.String(127))
    content = g_db.Column(g_db.String(1024))
    #date
    
    def __init__(self, title, content):
        self.title = title
        self.content = content


#@g_app.before_request
#def check_login():

# ROUTE "/" ==> REDIRECT to '/blog'
@g_app.route( "/" )
def index( ):
    return redirect( url_for('blog'), 302 )

# ROUTE "/flop" is EASTER EGG
@g_app.route( "/flop" )
def flop():
    return render_template('flop.html', ghSite_Name=g_ghSITE_NAME, ghSlogan=getSlogan(), ghPokerFlop=Markup(getHandHTML()),ghPage_Title="Community" )

# ROUTE "/blog" :: Landing Page / Posts Overview / View Individual
@g_app.route( "/blog" )
def blog():
    # TODO: check GET for entry view
    strEntryTitle = "BLog :: "
    
    postID = request.args.get('id')
    
    if( postID == None ):
        strEntryTitle += "All Entries"
        view_entries = BlogEntry.query.all()
    else:
        strEntryTitle += "Entry #" + postID
        view_entries = BlogEntry.query.filter_by(id=postID)
#    print( "DEBUG:::::::", view_entries )
#    if( view_entries == "" ):
#        print( "IS NOTHING" )
#    if( len(view_entries) == 0 ):
#        print( "IS NOTHING #2" )
    return render_template('blog.html',ghSite_Name=g_ghSITE_NAME, ghSlogan=getSlogan(),ghPage_Title=strEntryTitle,ghEntries=view_entries )

# ROUTE "/newpost" :: New Blog Post Form [ Get | Post ]
@g_app.route( "/newpost", methods=['POST', 'GET'] )
def newpost():
	# TODO: determine if GET or POST
	# GET ==> FORM
	# POST ==> FORM on FAIL
	#      ==> ADD POST on SUCCESS
    # TODO: validate form
    
    return render_template('newpost.html',ghSite_Name=g_ghSITE_NAME, ghSlogan=getSlogan(),ghPage_Title="BLog :: New Post" )


def main():
    g_app.run()

if __name__ == "__main__":
    main()
