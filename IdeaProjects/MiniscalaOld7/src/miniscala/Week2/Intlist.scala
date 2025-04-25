package miniscala.Week2
import scala.util.Random

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
    if (first <= second)
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

def append(xs: IntList, x: Int): IntList = xs match {
 case Nil => Cons(x, Nil)
 case Cons(y, ys) => Cons(y, append(ys, x))
}

def merge(xs: IntList, ys: IntList): IntList = (xs, ys) match {
  case (Nil, Nil) => Nil // Both lists are empty, so the result is empty
  case (Nil, Cons(y, yi)) =>
    Cons(y, merge(Nil, yi)) // xs is empty, so prepend y and merge with the rest of ys
  case (Cons(x, xi), Nil) =>
    Cons(x, merge(xi, Nil)) // ys is empty, so prepend x and merge with the rest of xs
  case (Cons(x, xi), Cons(y, yi)) =>
    if (x <= y) Cons(x, merge(xi, ys)) // x is smaller or equal, so prepend x and merge the rest of xs with ys
    else Cons(y, merge(xs, yi)) // y is smaller, so prepend y and merge xs with the rest of ys
}
def split(xs: IntList, n: Int): (IntList, IntList) = (xs, n) match {
  case (Nil, _) => (Nil, Nil) // Empty list, return two empty lists
  case (list, 0) => (Nil, list) // n is 0, return empty first list and the original list
  case (Cons(head, tail), count) =>
    val (firstList, secondList) = split(tail, count - 1)
    (Cons(head, firstList), secondList) // Prepend head to the first list
}

def length(xs: IntList): Int = xs match {
  case Nil => 0
  case Cons(y, ys) => 1 + length(ys)
}

def mergeSort(xs: IntList): IntList = {
  val n = length(xs) / 2
  if (n == 0) xs
  else {
    val (left, right) = split(xs, n)
    merge(mergeSort(left), mergeSort(right))
  }
}

def randomIntList(): IntList = {
  val rand = Random.between(0, 10)
  def randHelper(xs: IntList, x: Int): IntList = (xs, x) match {
    case (ys, 0) => ys
    case (Nil, z) => 
      val c = Random.between(0, 100)
      randHelper(Cons(c, Nil), z-1)
    case (ys, z) =>
      val c = Random.between(0, 100)
      randHelper(Cons(c, ys), z-1)
  } 
  randHelper(Nil, rand)
}

def testMergeSort(): Boolean = {
  val b = Range.inclusive(0, 100)
  for (k <- b) {
    val randlist = randomIntList()
    val sorted = mergeSort(randlist)
    val isOrdered = !ordered(sorted)
    if (isOrdered) {false}
  }
  true
}
object IntListTest2 {
  def main(args: Array[String]): Unit = {
    val a = Cons(1, Cons(7, Nil))
    val b = Cons(2, Cons(4, Cons(5, Nil)))
    val c = merge(a, b)
    val d = randomIntList()
    println(testMergeSort())
    println(d)
  }
}
