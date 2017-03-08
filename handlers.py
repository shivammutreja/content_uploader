#!/usr/bin/env python


import os, uuid, sys
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado import gen
import motor.motor_tornado
from tornado.web import asynchronous
import json
import pymongo

from amazon_s3 import AmazonS3
from s3_test import VideoUpload

file_path = os.path.dirname(os.path.abspath(__file__))
files_dir = file_path+'/files_to_upload/'

connection = pymongo.MongoClient()
coll = connection.content_db.uploader_coll


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print "setting headers!!!"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # self.links = list()

class Try(BaseHandler):
    def get(self):

        self.render("add_text.html", text="Question")

    @asynchronous
    @tornado.gen.coroutine
    def post(self):
        content = self.get_body_argument('editor1', default=None, strip=False)
        coll.update({'user_id': 1, 'question_id': 1}, {"$set": {'content': content}}, upsert=True)
        print content

        self.redirect("/file")

class HandleFile(BaseHandler):
    def get(self):
        self.render("add_choices.html")

    @asynchronous
    @tornado.gen.coroutine
    def post(self):
        choices_list = list()
        if self.request.files:
            for index, file in enumerate(self.request.files['get_image']):
                name = file['filename']
                body = file['body']

                if name.endswith("mp4"):
                    f = open(files_dir+name, 'ar+')
                    f.write(body)
                    file_path = f.name
                    f.close()

                    video = yield self.upload_vid(file_path)
                    print video, "####"
                    choices_list.append(video)
                    coll.update({'user_id': 1, 'question_id': 1}, {"$addToSet": {'choices': \
                        {'choice'+str(index+1): video} }}, upsert=True)
                else:
                    image = yield self.upload(body, name)
                    print image
                    choices_list.append(image.get("hdpi", ""))

                    coll.update({'user_id': 1, 'question_id': 1}, {"$addToSet": {'choices': \
                        {'choice'+str(index+1): image.get("hdpi", "")} }}, upsert=True)

            self.write({"choices": choices_list})

        else:
            text_choices = self.get_body_arguments("choice")

            for index, choice in enumerate(text_choices):
                coll.update({'user_id': 1, 'question_id': 1}, {"$addToSet": {'choices': \
                    {'choice'+str(index+1): choice} }}, upsert=True)

            self.write({"choices": text_choices})
        
            
        
    @tornado.gen.coroutine
    def upload(self, file_body, file_name):
        s3_obj = AmazonS3(image_link=file_body, news_id=file_name)
        raise tornado.gen.Return(s3_obj.run())


    @tornado.gen.coroutine
    def upload_vid(self, file_path):
        s3_obj = VideoUpload(file_path)
        raise tornado.gen.Return(s3_obj.upload_file())


##Ditched the idea of using a separate route to upload a video as of now.

# class HandleVideo(BaseHandler):
#     def get(self):
#         self.render("add_choices.html")

#     @asynchronous
#     @tornado.gen.coroutine
#     def post(self):
#         video_list = list()
        
#         for index, file in enumerate(self.request.files['get_image']):    
#             name = file['filename']
#             body = file['body']
            
#             f = open(files_dir+name, 'ar+')
#             f.write(body)
#             file_path = f.name
#             f.close()

#             image = yield self.upload(file_path)
#             print image

#             video_list.append(image.get("hdpi", ""))

#             print coll.update({'user_id': 1, 'question_id': 1}, {"$addToSet": {'choices': {'choice'+str(index+1): \
#                 image.get("hdpi", "")} }}, upsert=True)

#         self.write({"images": video_list})
            

#     @tornado.gen.coroutine
#     def upload(self, file_path):
#         s3_obj = VideoUpload(file_path)
#         raise tornado.gen.Return(s3_obj.upload_file())


class WriteSolution(BaseHandler):
    def get(self):
        self.render('add_text.html', text="Solution")

    @asynchronous
    @tornado.gen.coroutine
    def post(self):
        solution = self.get_body_argument('editor1', default=None, strip=False)
        coll.update({'user_id': 1, 'question_id': 1}, {"$set": {'solution': solution}}, upsert=True)
        print solution
        self.redirect("/preview")


class Preview(BaseHandler):
    def get(self):
        question_for_review = coll.find_one({'user_id': 1, 'question_id': 1}, {'id': False})
        question_id = question_for_review.get('question_id', '')
        question_content = question_for_review.get('content', '')
        choices = question_for_review.get('choices', '')
        solution = question_for_review.get('solution', '')

        if not choices:
            pass
            ##TODO: Add html to show just the question and ask user to add choices.
        else:
            self.render("preview.html", question_id=question_id, question_content=question_content, \
                choices=choices, solution=solution)

#TODO : Task Management System will post uploader id and ontology on this
#endpoint.

class GetUploaderData(BaseHandler):
    def post(self):
        uploader_id = self.get_argument('user_id')
        ontology = self.get_argument('permissions')
        print uploader_id, ontology
        self.write({"success": True})


class TestPreview(BaseHandler):
    def get(self):
        self.render("question_preview.html")

handlers = [
    (r'/test', Try),
    (r'/file', HandleFile),
    # (r'/upload_video', HandleVideo),
    (r'/solution', WriteSolution),
    (r'/preview', Preview),
    (r'/uploader_info', GetUploaderData),
    (r'/test_preview', TestPreview),

]

settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
)

app = tornado.web.Application(handlers, **settings)


def on_shutdown():
    print terminal.red(terminal.bold('Shutting down'))
    tornado.ioloop.IOLoop.instance().stop()
    ##gracefully closing mongo connection
    #MONGO_CONNECTION.close()
    # client.close()

def database_connection(app):
    conn = motor.motor_tornado.MotorClient()
    app.settings['uploader_coll'] = conn.content_db.uploader_coll


def main():
    # database_connection(app)
    sockets = tornado.netutil.bind_sockets(8000)
    tornado.process.fork_processes(10)
    http_server = tornado.httpserver.HTTPServer(app, max_body_size=200 * 1024 * 1024)
    http_server.add_sockets(sockets)
    # http_server = tornado.httpserver.HTTPServer(app)
    # http_server.bind("8000")
    # http_server.start(10)
    # app.listen('8000')
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()

if __name__ == '__main__':
    print 'Server Reloaded'
    main()
