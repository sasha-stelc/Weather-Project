from modules import app, window

def main():
    try:
        window.show()
        app.exec()
    except Exception as error:
        print("Помилка запуску:", error)


if __name__ == "__main__":
    main()