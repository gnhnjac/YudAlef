try:
    spl = list();
    def list():
        item = input("add/remove/reset item from shopping list: ");
        items = item.lower();
        if items == "add":
            add = input("item name: ");
            spl.append(add + '\n');
            global splfinal;
            splfinal = "".join(spl);
            print(splfinal)
            list();
        elif items == "reset":
            spl.clear();
            list();
        else:
            remove();

    def remove():
        rem = input("which item? ");
        remi = int(rem) -1;
        spl[remi] = ''
        del spl[remi];
        splfinal = "".join(spl);
        print(splfinal);
        list();
    list();

except ValueError:
    print("Please Type Numbers");
    remove();