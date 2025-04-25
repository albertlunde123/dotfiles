package miniscala.Week4

object Exercise54 {

  // IntList definition and operations

  sealed abstract class IntList
  case object Nil extends IntList
  case class Cons(x: Int, xs: IntList) extends IntList

  def length(xs: IntList): Int = xs match {
    case Nil => 0
    case Cons(_, ys) => 1 + length(ys)
  }

  def ordered(l: IntList): Boolean = ??? // checks whether the list is ordered (from smallest to largest)

  def append(xs: IntList, x: Int): IntList = xs match {
    case Nil => Cons(x, Nil)
    case Cons(y, ys) => Cons(y, append(ys, x))
  }
  def concat(xs: IntList, ys: IntList): IntList = (xs, ys) match {
    case (xs, Nil) => xs

    case (xs, Cons(y, ys)) => concat(append(xs, y), ys)
  } // produce the list xs followed by ys


  // IntTree definition and operations

  sealed abstract class IntTree
  case object Leaf extends IntTree
  case class Branch(left: IntTree, x: Int, right: IntTree) extends IntTree

  def size(t: IntTree): Int = t match {
    case Leaf => 0
    case Branch(left, _, right) => size(left) + size(right) + 1
  }
  // number of branch nodes in t2

  def height(t: IntTree): Int = t match {
    case Leaf => 0
    case Branch(left, _, right) => (height(left) max height(right)) + 1
  }

  def flatten(t: IntTree): IntList = ??? // convert to IntList using left-to-right inorder

  def ordered(t: IntTree): Boolean = {
    def ord(t: IntTree, minval: Int, maxval: Int): Boolean = t match {
      case Branch(left, x, right) => ord(left, minval, x) & ord(right, x, maxval)
      case Leaf => minval <= maxval
    }
    ord(t, Int.MinValue, Int.MaxValue)
  }

  def insert(t: IntTree, x: Int): IntTree = t match {
    case Leaf => Branch(Leaf, x, Leaf)
    case Branch(left, y, right) =>
      if (x <= y) Branch(insert(left, x), y, right)
      else Branch(left, y, insert(right, x))
  }

  def contains(t: IntTree, x: Int): Boolean = ??? // returns true if the ordered tree t contains x

  def main(args: Array[String]): Unit = {
    val a = Cons(1, Cons(2, Nil))
    val b = Cons(3, Cons(4, Nil))
    val c = concat(a, b)
    println(c)
  }

}