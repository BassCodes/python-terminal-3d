# Alexander Bass
# Created 4/12/24
# Last Edited 4/13/24
def load_ppm(file):
    header = next(file).strip().upper()
    assert header == "P3"
    dimensions = next(file).strip()
    split_dimensions = dimensions.split()
    assert len(split_dimensions) == 2
    width = split_dimensions[0]
    height = split_dimensions[-1]
    width = int(width)
    height = int(height)

    # not really doing anything with this
    color_depth = next(file).strip()
    assert color_depth == "255"

    image = []
    for y, line in enumerate(file):
        assert y < height
        t = [int(value) for value in line.strip().split()]

        pixels = []

        assert len(t) % 3 == 0

        assert len(t) // 3 <= width

        highest = 0
        for x in range(0, len(t), 3):
            red = t[0 + x]
            green = t[1 + x]
            blue = t[2 + x]
            highest = x // 3
            pixels.append((red, green, blue))
        assert highest == width - 1
        image.append(pixels)

    assert len(image) == height
    file.close()
    return image


if __name__ == "__main__":
    print(load_ppm(open("dirt.ppm")))
