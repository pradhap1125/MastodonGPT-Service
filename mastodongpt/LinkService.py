from flask import jsonify

from mastodongpt.DbService import save_link

file_directory= "D:\\resume_test\\"

def process_pdf(file):

    file.save(file_directory + file.filename)
    save_link(file_directory + file.filename,'file_path')
    return jsonify(message="File uploaded!")

def process_url(url):
    save_link(url,'web_url')
    return jsonify(message="URL uploaded!")

