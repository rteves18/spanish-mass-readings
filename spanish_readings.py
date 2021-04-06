from readings_utility import ReadingsParser
from latex_generator import LatexGenerator


def main():
    rp = ReadingsParser()
    #readings = rp.get_readings(language='en')
    readings = "foo"
    gl = LatexGenerator(readings)
    gl.generate_latex_file()
    print(readings)


if __name__ == "__main__":
    main()