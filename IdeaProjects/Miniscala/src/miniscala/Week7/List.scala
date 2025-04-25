package miniscala.Week7

sealed abstract class List[T]
case class Nil[T]() extends List[T]
case class Cons[T](x: T, xs: List[T]) extends List[T]

def forAll[T](list: List[T], p: (T) => Boolean): Boolean = list match {
  case Nil() => true
  case Cons(x, xs) => if (p(x)) forAll(xs, p) else false
}

def exists[T](list: List[T], p: (T) => Boolean): Boolean = list match {
  case Nil() => false
  case Cons(x, xs) => if (p(x)) true else exists(xs, p)
}

def count[T](list: List[T], p: (T) => Boolean): Int = {
  def helper(list: List[T], p: (T) => Boolean, acc: Int): Int = list match {
    case Nil() => acc
    case Cons(x, xs) =>
      if (p(x)) {
        helper(xs, p, acc + 1)
      } else helper(xs, p, acc)
  }
  helper(list, p, 0)
}

def find[T](list: List[T], p: (T) => Boolean): Option[T] = list match {
  case Nil() => None
  case Cons(x, xs) => if (p(x)) Some(x) else find(xs, p)
}

object ListTests {
  def main(args: Array[String]): Unit = {
    def predicate(p: Int): Boolean = {
      if (p < 10) true else false
    }
    val a: List[Int] = Cons(11, Cons(10, Cons(2, Nil())))
    println(forAll(a, predicate))
    println(exists(a, predicate))
    println(count(a, predicate))
    println(find(a, predicate))
  }
}

