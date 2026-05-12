if __name__ == "__main__":
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\nBye.\n")