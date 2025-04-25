package miniscala.Week12

def zip[U, T](xs: List[U], ys: List[T]): List[(U, T)] = (xs, ys) match {
  case (Nil, Nil) => Nil
  case (Nil, _) => Nil
  case (_, Nil) => Nil
  case (Cons(x, xi), Cons(y, yi)) => Cons((x, y), zip(xi, yi))
}

def unzip[U, T](x: List[(U, T)]): (List[U], List[T]) = x match {
  case Nil => (Nil, Nil)
  case Cons((t, u), xs) =>
    val (f, l) = unzip(xs)
    (Cons(t, f), Cons(u, l))
}

object zipTest {
  def main(args: Array[String]): Unit = {
    val a: List[Int] = Cons(1, Cons(2, Nil))
    val a1: List[Int] = Cons(3, Cons(4, Nil))
    val b: List[Int] = Cons(1, Cons(2, Cons(3, Nil)))
    val zipped1 = zip(a, a1)
    val zipped2 = zip(b, a)
    val zipped3 = zip(a, b)
    val (uz1, uz2) = unzip(zipped1)
    println(uz1)
    println(uz2)
  }
}
