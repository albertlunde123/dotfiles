package miniscala.Week3
import miniscala.parser.Parser.parse
import miniscala.Interpreter.*
import miniscala.Ast.*
import miniscala.TypeChecker.*

object TestFunction {
  def main(args: Array[String]): Unit = {
    val c = "{def fib(n: Int): Int = if (n <= 1) n else fib(n - 1) + fib(n - 2);fib(10)}"
    val d = "{def f(x: Int): Int = x; f(2,3,4)}"
    val initialVenv = Map[Var, Val]()
    val initialFenv = Map[Fun, Closure]()
    val initVarTypeEnv = Map[Var, Type]()
    val initFunTypeEnv = Map[Fun, (List[Type], Type)]()
    val b = "{def f(x: Int): Int = x; f(2)}"
    assert(eval(parse(b), initialVenv, initialFenv) == IntVal(2))
    //println(typeCheck(parse(d), initVarTypeEnv, initFunTypeEnv))
    //
    println(eval(parse(d), initialVenv, initialFenv))
  }
}