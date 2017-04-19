from mass_server import get_development_app


def main():
    app = get_development_app()
    app.run()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    main()
