{ val x = 1;
  val z = {
    val x = 21;
    def f(a: Int): (Int, Int) = {
      val x = a + x;
      (x, a)
    };
    (n: Int) => f(n + 1)
  };
  z(x)
}