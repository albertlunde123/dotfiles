{
  class C(a: Int) {
      def f(p: Int): Int = {p + a}
  };
  {
    def g(c: C): Int = {
      2 * c.f(0)
    };
    {
      val b: C = new C(10);
      g(b)
    }
  }
}