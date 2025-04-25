package miniscala

import miniscala.Ast._
import miniscala.Interpreter._
import miniscala.TypeChecker._
import miniscala.parser.Parser.*

object Test {
  def main(args: Array[String]): Unit = {
    testVal("{def f(x) = x; f(2)}", IntVal(2))
    testTypeFail("{def f(x) = x; f(2)}")
    testVal(readFile("examples/varenv1.s"), IntVal(42))
    testVal(readFile("examples/vars1_0.s"), IntVal(6))
    testVal(readFile("examples/varenv1_y.s"), IntVal(87))
    testVal(readFile("examples/varenv1_z.s"), IntVal(-1))

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

  def testVal(prg: String, value: Val, env: Env = Map[Id, Val]()): Unit = {
    assert(eval(parse(prg), env) == value)
  }

  def testType(prg: String, out: Type, tenv: TypeEnv = Map[Id, Type]()): Unit = {
    assert(typeCheck(parse(prg), tenv) == out)
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