from app import create_app

app = create_app('dev')
app.app_context().push()


if __name__ == '__main__':
    app.run()
