def main():
    print("The last leaf: A story about the persistence of art")

    for season in ['spring', 'summer', 'autumn', 'winter']:
        print("The leaves are on the tree")

    print("Two young artists named Sue and Johnsy are looking at the tree")
    johnsy_has_pneumonia = True

    while johnsy_has_pneumonia:
        print("A leaf falls off")
        if tree.number_of_leaves() == 1:
            johnsy_has_pneumonia = False

    print("Johnsy is dead")

    print("Sue has pneumonia now")
    sue_has_pneumonia = True

    while sue_has_pneumonia:
        print("A leaf falls off")
        if tree.number_of_leaves() == 0:
            sue_has_pneumonia = False

    print("Sue is dead")

    print("But wait, a leaf grows back!")
    print("Because Behrman is a drunk but he paints like Michelangelo")


if __name__ == "__main__":
    main()