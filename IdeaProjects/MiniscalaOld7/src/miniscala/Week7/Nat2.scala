package miniscala.Week7

sealed abstract class Nat
case object Zero extends Nat
case class Succ(n: Nat) extends Nat

def decode(n: Nat): Int = n match {
  case Zero => 0
  case Succ(x) => 1 + decode(x)
}

def encode(n: Int): Nat = n match {
  case 0 => Zero
  case _ => Succ(encode(n - 1))
}

def fold[B](n: Nat, z: B, f: B => B): B = n match {
  case Zero => z
  case Succ(y) => f(fold(y, z, f))
}

def add(n: Nat, m: Nat): Nat = fold(n, m, x => Succ(x))
def mult(n: Nat, m: Nat): Nat = fold(n, (Zero: Nat), x => add(x, m))
def power(n: Nat, m: Nat): Nat = fold(m, (Succ(Zero): Nat), x => mult(x, n))

object NatTest {
  def main(args: Array[String]): Unit = {
    val a = encode(10)
    val b = encode(3)
    println(decode(add(a, b)))
    println(decode(mult(a, b)))
    println(decode(power(a, b)))
  }
}

