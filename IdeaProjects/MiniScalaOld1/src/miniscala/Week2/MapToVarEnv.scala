package miniscala.Week2

type Var = String
sealed abstract class VarEnv
private case class ConsVarEnv(x: Var, v: Int, next: VarEnv) extends VarEnv
private case object NilVarEnv extends VarEnv

def makeEmpty(): VarEnv = NilVarEnv

def extend(e: VarEnv, x: Var, v: Int): VarEnv = ConsVarEnv(x, v, e)

def lookup(e: VarEnv, x: Var): Int = e match {
  case ConsVarEnv(y, w, next) => if (x == y) w else lookup(next, x)
  case NilVarEnv => throw new RuntimeException("not found")
}

object TestMapToVarEnv {
  var a = makeEmpty()
  a = extend(a, "a", 1)
}