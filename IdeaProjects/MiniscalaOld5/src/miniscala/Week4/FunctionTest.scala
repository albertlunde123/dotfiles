package miniscala.Week4

import miniscala.Ast._
import miniscala.Interpreter._
import miniscala.TypeChecker.{TypeEnv, TypeError, typeCheck}
import miniscala.parser.Parser.*

object Test49 {

  def main(args: Array[String]): Unit = {
    test("{def f(x: Int): Int = x; f(2)}", IntVal(2), IntType())
    testFail("{def f(x: Int): Int = x; f(2, 3)}")
    test(readFile("examples/sqrt4.s"), FloatVal(1.4142157), FloatType())
    test(readFile("examples/scope1.s"), IntVal(4), IntType())
   // test(readFile("examples/even.s"), BoolVal(true), BoolType())
    testFail("{def f(x: String): String = x; f(2)}")
    testFail("{def f(x: Int): String = x; f(2)}")
    // <-- add more test cases here

    println("All tests passed successfully!")
  }

  def test(prg: String, rval: Val, rtype: Type): Unit = {
    testVal(prg, rval)
    testType(prg, rtype)
  }

  def testFail(prg: String): Unit = {
    testValFail(prg)
    testTypeFail(prg)
  }

  def testVal(prg: String, value: Val, venv: Env = Map[Id, Val]()): Unit = {
    assert(eval(parse(prg), venv) == value)
  }

  def testType(prg: String, out: Type, venv: TypeEnv = Map[Id, Type]()): Unit = {
    assert(typeCheck(parse(prg), venv) == out)
  }

  def testValFail(prg: String): Unit = {
    try {
      eval(parse(prg), Map[Id, Val]())
      assert(false)
    } catch {
      case _: InterpreterError => assert(true)
    }
  }

  def testTypeFail(prg: String): Unit = {
    try {
      typeCheck(parse(prg), Map[Id, Type]())
      assert(false)
    } catch {
      case _: TypeError => assert(true)
    }
  }
}
