import basil as application 

if __name__ == "__main__":
    httpd = make_server('', 8000, application)
    print("Serving on port 8000...")
    httpd.serve_forever()