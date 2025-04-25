package miniscala.Week7

object OrElse {
  def OrElse(iff: Boolean, elsee: => Boolean): Boolean = {
    if (iff) {
      if (elsee) true else false
    }
    else false
  }

  def elseTester(bool: Boolean): Boolean = {
    println("hello motherfucker")
    if (bool) true else false
  }

  def main(args: Array[String]): Unit = {
    val a = 2 > 3
    val b = 2 < 3
    println(elseTester(b))
    println(OrElse(a, elseTester(b)))
  }
}