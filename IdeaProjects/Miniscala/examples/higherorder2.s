{
  def f(g: Int => Int): Int => Int = (x: Int) => 2 * g(x);
  f((x: Int) => x/2)(2)
}
