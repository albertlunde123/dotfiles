package miniscala.Week5

import miniscala.Ast._
import miniscala.Interpreter._
import miniscala.TypeChecker._
import miniscala.parser.Parser.*

object Test68 {

  def main(args: Array[String]): Unit = {
    testVal("{def f(x) = x; f(2)}", IntVal(2))
    testTypeFail("{def f(x) = x; f(2)}")
    test(readFile("examples/higherorder1.s"), IntVal(-29), IntType())
    test(readFile("examples/lambda1.s"), IntVal(2), IntType())
    test(readFile("examples/higherorder2.s"), IntVal(2), IntType())
    test(readFile("examples/higherorder3.s"), TupleVal(List(IntVal(23), IntVal(2))), TupleType(List(IntType(), IntType())))
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