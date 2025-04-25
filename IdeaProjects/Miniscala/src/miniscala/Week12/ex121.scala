package miniscala.Week12
import scala.util.Random

sealed abstract class List[+T]
case object Nil extends List[Nothing]
case class Cons[T](x: T, xs: List[T]) extends List[T]

abstract class Comparable[T] { // in real Scala code, this would be a “trait”, not an abstract class
  /** Returns <0 if this<that, ==0 if this==that, and >0 if this>that */
  def compareTo(that: T): Int
}

class Student(val id: Int) extends Comparable[Student] {
  override def toString: String = s"Student (${this.id})"
  def compareTo(that: Student) = this.id - that.id
}

def merge[T <: Comparable[T]](xs: List[T], ys: List[T]): List[T] = (xs, ys) match {
  case (Nil, Nil) => Nil // Both lists are empty, so the result is empty
  case (Nil, Cons(y, yi)) =>
    Cons(y, merge(Nil, yi)) // xs is empty, so prepend y and merge with the rest of ys
  case (Cons(x, xi), Nil) =>
    Cons(x, merge(xi, Nil)) // ys is empty, so prepend x and merge with the rest of xs
  case (Cons(x, xi), Cons(y, yi)) =>
    if (x.compareTo(y) <= 0) Cons(x, merge(xi, ys)) // x is smaller or equal, so prepend x and merge the rest of xs with ys
    else Cons(y, merge(xs, yi)) // y is smaller, so prepend y and merge xs with the rest of ys
}

def split[T](xs: List[T], n: Int): (List[T], List[T]) = (xs, n) match {
  case (Nil, _) => (Nil, Nil) // Empty list, return two empty lists
  case (list, 0) => (Nil, list) // n is 0, return empty first list and the original list
  case (Cons(head, tail), count) =>
    val (firstList, secondList) = split(tail, count - 1)
    (Cons(head, firstList), secondList) // Prepend head to the first list
}

def length[T](xs: List[T]): Int = xs match {
  case Nil => 0
  case Cons(y, ys) => 1 + length(ys)
}

def mergeSort[T <: Comparable[T]](xs: List[T]): List[T] = {
  val n = length(xs) / 2
  if (n == 0) xs
  else {
    val (left, right) = split(xs, n)
    merge(mergeSort(left), mergeSort(right))
  }
}

def randomStudentList(n: Int): List[Student] = n match {
  case 0 => Nil
  case n =>
    val r = Random
    val randint = r.nextInt(20)
    Cons(new Student(randint), randomStudentList(n-1))
}

object compareStudents {
  def main(args: Array[String]): Unit = {
    val list1: List[Student] = Cons(new Student(1), Cons(new Student(2), Nil))
    val list2: List[Student] = Cons(new Student(2), Cons(new Student(3), Nil))
    val mergedList = merge(list1, list2)
    val (first, last) = split(mergedList, 2)
    val randStud = randomStudentList(5)
    val sortedrandStud = mergeSort(randStud)
    println(randStud)
    println(sortedrandStud)
    //println(mergedList)
    //println(first)
    //println(last)
  }
}
  


