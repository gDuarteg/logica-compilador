{
    z = readln();
    println(z);

    a = 2;
    b = 5;
    {
        x = 10;
    }
    c = a + b; /*comentario*/
    println(c);

    if (2 == 2) {
        y = 4;
    } else {
        y = 22;
    }
    println(y);

    while (a < c || a == 2) {
        println(a);
        a = a + 1;
    }

    while (a < c && !(a == 2)) {
        println(a);
        a = a + 1;
    }
}
