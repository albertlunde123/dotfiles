package miniscala.Week2
import miniscala.Ast.*

sealed abstract class VarEnv {
  def extend(x: Var, v: Int): VarEnv
  def lookup(x: Var): Int
  def makeEmpty(): VarEnv
}

case object NilVarEnv extends VarEnv {
  def makeEmpty(): VarEnv = NilVarEnv
  def extend(x: Var, v: Int): VarEnv = ConsVarEnv(x, v, NilVarEnv)
  def lookup(x: Var): Int = throw new RuntimeException("not found")
}
case class ConsVarEnv(x: Var, v: Int, next: VarEnv) extends VarEnv {
  def makeEmpty(): VarEnv = NilVarEnv
  def extend(x2: Var, v2: Int): VarEnv = ConsVarEnv(x2, v2, ConsVarEnv(x, v, next))
  def lookup(a: Var): Int = {
    if (x == a)
      v
    else
      next.lookup(a)
  }
}

object MyVarEnvTest {
  def main(args: Array[String]): Unit = {
    val EmptyEnv = NilVarEnv
    try {
      EmptyEnv.lookup("x")
    } catch {
      case _ => println("lookup throws RuntimeException on the empty list")
    }
    // We test that extending works, makeEmpty works and lookup works
    val Env1 = EmptyEnv.extend("x", 1)
    assert(Env1.lookup("x") == 1)
    assert(Env1 == ConsVarEnv("x", 1, NilVarEnv))
    assert(Env1.makeEmpty() == EmptyEnv)
    // We test that it works for multiple elements
    val Env2 = Env1.extend("y", 2).extend("z", 3)
    assert(Env2.lookup("x") == 1)
    assert(Env2.lookup("y") == 2)
    assert(Env2.lookup("z") == 3)
    // Check that the shadowing happens as expected
    val Env3 = Env2.extend("x", 4)
    assert(Env3.lookup("x") == 4)
    }
  }
