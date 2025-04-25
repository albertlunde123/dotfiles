package miniscala.Week2

sealed abstract class Nat
case object Zero extends Nat
case class Succ(n: Nat) extends Nat

def decode(n: Nat): Int = n match {
  case Zero => 0
  case Succ(x) => 1 + decode(x)
}

def encode(n: Int): Nat = n match {
  case 0 => Zero
  case _ => Succ(encode(n-1))
}

def add(n: Nat, m: Nat): Nat = n match {
  case Zero => m
  case Succ(a) => add(a, Succ(m))
}

def multi(n: Nat, m: Nat): Nat = n match {
  case Zero => Zero
  case Succ(a) => add(m, multi(a, m))
}

def power(n: Nat, m: Nat): Nat = m match {
  case Zero => Succ(Zero)
  case Succ(a) => multi(n, power(n, a))
}

def decrement(n: Nat): Nat = n match {
  case Zero => Zero
  case Succ(Zero) => Zero
  case Succ(a) => a
}

object NatTest {
  def main(args: Array[String]): Unit = {
    // Tester at decoderen virker.
    assert(decode(Succ(Succ(Zero))) == 2)
    // Tester at encoderen virker.
    assert(decode(encode(2)) == 2)
    // Tester at add virker
    val a = encode(5)
    val b = encode(10)
    assert(decode(add(a, b)) == 15)
    // Tester at multi virker
    assert(decode(multi(a, b)) == 50)
    val c = encode(2)
    val d = encode(4)
    assert(decode(power(c, d)) == 16)
    println(c)
    println(decrement(c))
  }
}