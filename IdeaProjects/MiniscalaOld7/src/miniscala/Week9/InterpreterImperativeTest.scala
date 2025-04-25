package miniscala.Week9

import miniscala.Ast._
import miniscala.Interpreter._
import miniscala.TypeChecker._
import miniscala.parser.Parser.parse

object Test95 {

  def main(args: Array[String]): Unit = {
    test("{ def f(x: Int): Int = x; f(2) }", IntVal(2), IntType())
    testFail("{ def f(x: Int): Int = x; f(2, 3) }")
    testVal("{ var z: Int = 0; { var t: Int = x; while (y <= t) { z = z + 1; t = t - y }; z } }", IntVal(3), Map("x" -> IntVal(17), "y" -> IntVal(5)))
    testType("{ var z: Int = 0; { var t: Int = x; while (y <= t) { z = z + 1; t = t - y }; z } }", IntType(), Map("x" -> IntType(), "y" -> IntType()))
    testVal("{ var x: Int = 0; def inc(): Int = { x = x + 1; x }; inc(); inc() }", IntVal(2))
    testType("{ var x: Int = 0; def inc(): Int = { x = x + 1; x }; inc(); inc() }", IntType())
    testVal("""{ def make(a: Int): Int => Int = {
              |    var c: Int = a;
              |    def add(b: Int): Int = { c = c + b; c };
              |    add
              |  };
              |  { val c1 = make(100);
              |    val c2 = make(1000);
              |    c1(1) + c1(2) + c2(3) } }""".stripMargin, IntVal(101 + 103 + 1003))

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

  def testVal(prg: String, value: Val, env: Env = Map(), cenv: ClassEnv = Map()): Unit = {
    val res = eval(parse(prg), env, cenv)
    assert(res == value)
  }

  def testType(prg: String, out: Type, tenv: TypeEnv = Map[Id, Type]()): Unit = {
    assert(typeCheck(parse(prg), tenv) == out)
  }

  def testValFail(prg: String,env: Env = Map[Id, Val](), cenv: ClassEnv = Map[Id, Constructor]()): Unit = {
    try {
      eval(parse(prg), env, cenv)
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