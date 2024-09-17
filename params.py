import configparser


def conns(filename="../DataBaseWork/database.ini"):
    """ Считывание данных для подключения к БД """

    config = configparser.ConfigParser()
    config.read(filename)
    params = {"user": config["postgresql"]["user"],
              "password": config["postgresql"]["password"],
              "port": config["postgresql"]["port"]}

    return params
