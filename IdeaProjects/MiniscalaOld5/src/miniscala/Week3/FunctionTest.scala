package miniscala.Week3
import miniscala.parser.Parser.parse
import miniscala.Interpreter.*
import miniscala.Ast.*
import miniscala.TypeChecker.*

object TestFunction {
  def main(args: Array[String]): Unit = {
    // recursion
    val c = "{def fib(n: Int): Int = if (n <= 1) n else fib(n - 1) + fib(n - 2);fib(10)}"
    val d = "{def f(x: Int): Int = x; f(2,3,4)}"
    val initialVenv = Map[Id, Val]()
    // simple check
    val b = "{def f(x: Int): Int = x; f(2)}"
    // higher order
    val high = "{def f(x, g): = g(0) + x}"
    assert(eval(parse(b), initialVenv) == IntVal(2))
    println(eval(parse(c), initialVenv))
    //println(typeCheck(parse(d), initVarTypeEnv, initFunTypeEnv))
    //
  }
}