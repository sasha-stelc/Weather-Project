from modules import app, window

def main():
    try:
        window.show()
        app.exec()
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()
