package miniscala.Week2

sealed abstract class IntList
case object Nil extends IntList
case class Cons(x: Int, xs: IntList) extends IntList

def square(xs: IntList): IntList = xs match {
  case Nil => Nil
  case Cons(x, ys) => Cons(x*x, square(ys))
}

def ordered(xs: IntList): Boolean = xs match {
  case Nil => true
  case Cons(x, Cons(y, zs)) =>
    val first = x
    val second = y
    val nextStep = Cons(y, zs)
    if (first < second)
      ordered(Cons(y, zs))
    else
      false
  // This case is last, as it would otherwise conflict with the second case.
  case Cons(x, ys) => true
}

def myToString(xs: IntList): String = xs match {
  case Nil => ""
  case Cons(x, Nil) => s"$x"
  case Cons(x, ys) => s"${x}, ".concat(myToString(ys))
}

def odd(xs: IntList): IntList = xs match {
  case Nil => Nil
  case Cons(x, Nil) => Cons(x, Nil)
  case Cons(x, Cons(y, zs)) => Cons(x, odd(zs))
}

object IntListTest2 {
  def main(args: Array[String]): Unit = {
    val b = Nil
    val a = Cons(2, Nil)
    val q = Cons(3, a)
    val c = Cons(4, q)
    val d = square(c)
    val e = ordered(c)
    val f = ordered(Cons(1, Cons(2, Cons(3, Nil))))
    val g = myToString(d)
    val h = Cons(1, Cons(2, Cons(3, Cons(4, Cons(5, Nil)))))
    val h1 = odd(c)
    val h2 = odd(h)
    println(c)
    println(d)
    println(e)
    println(f)
    println(g)
    println(h1)
    print(h2)
  }
}