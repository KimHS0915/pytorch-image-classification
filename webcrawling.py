from google_images_download import google_images_download 

def imagedownloader(keywords, limit=100):

    response = google_images_download.googleimagesdownload()

    arguments = {"keywords":keywords,"limit":limit,"format":'jpg', "prefix":keywords, "type":'face'}

    paths = response.download(arguments)
    print(paths)

