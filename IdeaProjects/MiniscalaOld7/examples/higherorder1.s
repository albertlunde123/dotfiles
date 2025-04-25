{ val x = 3;
 def use(f: (Int, Int) => Int, y: Int): Int = f(x, y);
 def add(a: Int, b: Int): Int = a + b;
 def mult(a: Int, b: Int): Int = a * b;
 use(add, 7) - use(mult, 13)
}