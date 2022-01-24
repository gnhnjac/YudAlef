def st():
    string = input("your string: ");
    oppy = "".join(reversed(string));
    print(oppy);
    again = input("again? (y/n) ");
    againl = again.lower();
    if againl == "y":
        st();
    else:
        return;
st();