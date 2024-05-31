# A simple Django Website

A personal website used at [BlindPangolin.io](https://blindpangolin.io/) to be used as an image gallery.

I am not a Front-end developer and this site is mostly a fusion freely available resources (HTML templates, gallery javascript, etc...)

## How to run

If you do not know Django, please follow their tutorials to understand the base of initialising a project and creating the database.

### Deploying a server

I followed `Django in Production - From Zero to Hero` YouTube video series on how to set up the server (with minor modifications).

### Environment variables

for security in production, some parameters are set as environment variables:

```commandline
export SECRET_KEY='django-insecure-key-to-change'   # your unique key
export STATIC_ROOT='./static'                       # where to store static files
export MEDIA_ROOT='./media'                         # where to store media files (e.g. uploaded images)
export DEBUG='true'                                 # true for developpement, false in production
export ALLOWED_HOSTS='["{address}"]'                # from what {address} the site accept connection
export CSRF_TRUSTED_ORIGINS='["{address}"]'         # |
export CORS_ORIGIN_WHITELIST='["{address}"]'        # | https address to secure login in sessions (e.g. admin)
export CORS_ALLOWED_ORIGINS='["{address}"]'         # |
```

See Django documentation for more information and how to properly set them.

## Resources and Attributions

* [Django](https://www.djangoproject.com/) to build the website
* [HTML UP](https://html5up.net/) for responsive HTML templates  
  * [read-only](https://html5up.net/read-only) as global template
  * [multiverse](https://html5up.net/multiverse) as gallery template
* [lightGallery](https://www.lightgalleryjs.com/) for popup gallery

