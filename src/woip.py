from kavalkade.app import Kavalkade

app = Kavalkade()
if __name__ == '__main__':
    import bjoern
    bjoern.run(app, "127.0.0.1", 8000)