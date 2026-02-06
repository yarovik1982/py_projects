

def main():
    name = input("Как тебя зовут? ")
    age = input("Сколько лет? ")
    if int(age) > 18:
        print(name + " Тебе уже можно")
        return
    else:
        print(name + " Тебе еще рано")
   #  print("Hello "+name)

if __name__ == "__main__":
    main()