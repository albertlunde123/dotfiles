package week5

object Semantics {
  def main(args: Array[String]): Unit = {
    val x = 1
    val z = {
      val x = 21
      def f(a: Int): (Int, Int) = {
        val y = a + x // Bliver nødt til at type-annotere og anvende andet variable navn
        (y, a)
      }
      (n: Int) => f(n + 1)
    }
    val res = z(x)
    println(res)
  }
}
